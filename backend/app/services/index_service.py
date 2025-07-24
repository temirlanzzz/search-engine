from sqlalchemy.orm import Session
from sqlalchemy import func, text
from app.database import SearchIndex, Token, Document, get_db
from app.utilts.tokenizer import tokenize_text
import json
import math
from typing import List, Dict, Tuple
import logging

logger = logging.getLogger(__name__)


class IndexService:
    def __init__(self, db: Session):
        self.db = db
    
    def build_tfidf_index(self) -> Tuple[Dict[str, Dict[str, float]], Dict[str, int]]:
        """Build TF-IDF index from database"""
        try:
            logger.info("Building TF-IDF index...")
            
            # Get all documents and their tokens
            documents = self.db.query(Document).all()
            total_docs = len(documents)
            
            if total_docs == 0:
                logger.warning("No documents found for indexing")
                return {}, {}
            
            # Calculate document frequency for each term
            term_doc_freq = {}
            doc_term_freq = {}
            
            for doc in documents:
                tokens = self.db.query(Token).filter(Token.document_id == doc.id).all()
                doc_terms = {}
                
                for token in tokens:
                    term = token.token
                    # Count term frequency in this document
                    doc_terms[term] = doc_terms.get(term, 0) + 1
                    # Count how many documents contain this term
                    term_doc_freq[term] = term_doc_freq.get(term, 0) + 1
                
                doc_term_freq[doc.id] = doc_terms
            
            # Calculate TF-IDF scores
            tfidf_index = {}
            
            for term, doc_freq in term_doc_freq.items():
                # IDF = log(total_docs / doc_freq)
                idf = math.log(total_docs / doc_freq)
                tfidf_scores = {}
                
                for doc_id, term_freqs in doc_term_freq.items():
                    if term in term_freqs:
                        # TF = term frequency in document
                        tf = term_freqs[term]
                        # TF-IDF = TF * IDF
                        tfidf_score = tf * idf
                        tfidf_scores[doc_id] = tfidf_score
                
                tfidf_index[term] = tfidf_scores
            
            # Store in database
            self._store_search_index(tfidf_index, term_doc_freq)
            
            logger.info(f"TF-IDF index built with {len(tfidf_index)} terms")
            return tfidf_index, term_doc_freq
            
        except Exception as e:
            logger.error(f"Error building TF-IDF index: {e}")
            raise
    
    def _store_search_index(self, tfidf_index: Dict[str, Dict[str, float]], 
                           term_doc_freq: Dict[str, int]):
        """Store search index in database"""
        try:
            # Clear existing indices
            self.db.query(SearchIndex).delete()
            
            # Store each term's data
            for term, tfidf_scores in tfidf_index.items():
                doc_freq = term_doc_freq.get(term, 0)
                
                # Create inverted index (list of document IDs)
                doc_ids = list(tfidf_scores.keys())
                
                index_record = SearchIndex(
                    term=term,
                    document_frequency=doc_freq,
                    tfidf_data=json.dumps(tfidf_scores),
                    inverted_index_data=json.dumps(doc_ids)
                )
                
                self.db.add(index_record)
            
            self.db.commit()
            logger.info("Search index stored in database")
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error storing search index: {e}")
            raise
    
    def search(self, query: str, operation: str = "AND", limit: int = 10) -> List[Dict]:
        """Search documents using the index"""
        try:
            # Tokenize query
            query_tokens = tokenize_text(query)
            logger.info(f"Query tokens: {query_tokens}")
            if not query_tokens:
                logger.warning("No tokens found in query")
                return []
            
            # Get search results for each token
            token_results = {}
            for token in query_tokens:
                index_record = self.db.query(SearchIndex).filter(
                    SearchIndex.term == token
                ).first()
                
                if index_record:
                    tfidf_data = json.loads(index_record.tfidf_data)
                    token_results[token] = tfidf_data
                    logger.info(f"Found index record for token '{token}' with {len(tfidf_data)} documents")
                else:
                    logger.info(f"No index record found for token '{token}'")
            
            logger.info(f"Token results: {list(token_results.keys())}")
            if not token_results:
                logger.warning("No token results found")
                return []
            
            # Combine results based on operation
            if operation == "AND":
                # Find documents that contain ALL tokens
                doc_sets = [set(scores.keys()) for scores in token_results.values()]
                if not doc_sets:
                    return []
                matched_docs = set.intersection(*doc_sets)
            elif operation == "OR":
                # Find documents that contain ANY token
                matched_docs = set()
                for scores in token_results.values():
                    matched_docs.update(scores.keys())
            else:
                # Default to OR
                matched_docs = set()
                for scores in token_results.values():
                    matched_docs.update(scores.keys())
            
            # Calculate combined scores
            doc_scores = {}
            for doc_id in matched_docs:
                score = 0
                for token_scores in token_results.values():
                    score += token_scores.get(doc_id, 0)
                doc_scores[doc_id] = score
            
            # Sort by score and get top results
            sorted_docs = sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)
            
            # Get document details
            results = []
            for doc_id, score in sorted_docs[:limit]:
                document = self.db.query(Document).filter(Document.id == doc_id).first()
                if document:
                    # Get snippet
                    tokens = self.db.query(Token).filter(
                        Token.document_id == doc_id
                    ).order_by(Token.position).limit(20).all()
                    
                    snippet_tokens = [token.token for token in tokens]
                    snippet = " ".join(snippet_tokens)
                    if len(snippet) > 200:
                        snippet = snippet[:200] + "..."
                    
                    results.append({
                        "id": doc_id,
                        "title": document.title,
                        "url": document.url,
                        "snippet": snippet,
                        "score": score
                    })
            
            return results
            
        except Exception as e:
            logger.error(f"Error searching: {e}")
            return []
    
    def get_index_stats(self) -> Dict:
        """Get statistics about the search index"""
        try:
            total_terms = self.db.query(SearchIndex).count()
            total_documents = self.db.query(Document).count()
            
            # Get top terms by document frequency
            top_terms = self.db.query(SearchIndex).order_by(
                SearchIndex.document_frequency.desc()
            ).limit(10).all()
            
            stats = {
                "total_terms": total_terms,
                "total_documents": total_documents,
                "top_terms": [
                    {
                        "term": term.term,
                        "document_frequency": term.document_frequency
                    }
                    for term in top_terms
                ]
            }
            
            return stats
            
        except Exception as e:
            logger.error(f"Error getting index stats: {e}")
            return {}
    
    def rebuild_index(self) -> Dict:
        """Rebuild the entire search index"""
        try:
            logger.info("Starting index rebuild...")
            
            # Build TF-IDF index (this also stores it in database)
            tfidf_index, term_doc_freq = self.build_tfidf_index()
            
            # Get statistics
            stats = self.get_index_stats()
            
            logger.info("Index rebuild completed")
            return {
                "status": "success",
                "terms_indexed": len(tfidf_index),
                "stats": stats
            }
            
        except Exception as e:
            logger.error(f"Error rebuilding index: {e}")
            return {
                "status": "error",
                "error": str(e)
            }

    def get_search_suggestions(self, query: str, limit: int = 5) -> List[str]:
        """Get search suggestions based on indexed terms"""
        try:
            if not query.strip():
                return []
            
            # Get terms that start with the query
            suggestions = self.db.query(SearchIndex.term).filter(
                SearchIndex.term.ilike(f"{query}%")
            ).order_by(SearchIndex.document_frequency.desc()).limit(limit).all()
            
            return [suggestion.term for suggestion in suggestions]
            
        except Exception as e:
            logger.error(f"Error getting suggestions: {e}")
            return []

    def get_crawl_stats(self) -> Dict:
        """Get crawling statistics"""
        try:
            total_documents = self.db.query(Document).count()
            
            # Get unique domains
            domains = self.db.query(Document.url).distinct().all()
            unique_domains = set()
            for url in domains:
                try:
                    from urllib.parse import urlparse
                    parsed = urlparse(url[0])
                    domain = parsed.netloc
                    if domain:
                        unique_domains.add(domain)
                except:
                    continue
            
            return {
                "total_documents": total_documents,
                "unique_domains": len(unique_domains),
                "domains": list(unique_domains)[:10]  # Show first 10 domains
            }
            
        except Exception as e:
            logger.error(f"Error getting crawl stats: {e}")
            return {"total_documents": 0, "unique_domains": 0, "domains": []}


def get_index_service():
    """Dependency to get index service"""
    db = next(get_db())
    return IndexService(db) 