#!/usr/bin/env python3
"""
Test script to debug search functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal, Document, SearchIndex
from app.services.index_service import IndexService
from app.utilts.tokenizer import tokenize_text

def test_search():
    """Test the search functionality"""
    db = SessionLocal()
    try:
        index_service = IndexService(db)
        
        # Check if we have documents
        total_docs = db.query(Document).count()
        print(f"Total documents in database: {total_docs}")
        
        if total_docs == 0:
            print("No documents found. Please crawl some websites first.")
            return
        
        # Check if index is built
        total_terms = db.query(SearchIndex).count()
        print(f"Total indexed terms: {total_terms}")
        
        if total_terms == 0:
            print("No index found. Rebuilding index...")
            result = index_service.rebuild_index()
            print(f"Index rebuild result: {result}")
            
            # Check again
            total_terms = db.query(SearchIndex).count()
            print(f"Total indexed terms after rebuild: {total_terms}")
        
        # Get some sample terms
        sample_terms = db.query(SearchIndex).limit(5).all()
        print(f"Sample terms: {[term.term for term in sample_terms]}")
        
        # Test search
        test_queries = ["test", "document", "web", "search"]
        for query in test_queries:
            print(f"\nTesting search for: '{query}'")
            tokens = tokenize_text(query)
            print(f"Tokens: {tokens}")
            
            results = index_service.search(query)
            print(f"Found {len(results)} results")
            
            for i, result in enumerate(results[:3]):  # Show first 3 results
                print(f"  {i+1}. {result['title']} - {result['url']}")
    
    finally:
        db.close()

if __name__ == "__main__":
    test_search() 