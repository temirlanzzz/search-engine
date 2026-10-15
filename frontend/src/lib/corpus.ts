import type { Document } from './retrieval'
// Original, intentionally compact teaching corpus. No scraped or licensed articles.
export const corpus: Document[] = [
  {
    id: '01',
    category: 'Information retrieval',
    title: 'The art of finding what matters',
    text: 'Search is a conversation between a question and a collection. Information retrieval ranks documents using evidence from query terms. A useful search engine balances precision, the share of relevant results, with recall, the share of relevant documents found. Ranking is not understanding, but its decisions can be made visible.',
  },
  {
    id: '02',
    category: 'Information retrieval',
    title: 'BM25: a little less repetition',
    text: 'BM25 is a probabilistic ranking function for search. Term frequency saturation means repeating a query term yields diminishing returns. Document length normalization prevents long documents from winning simply because they contain more words. The k1 parameter controls saturation and b controls length normalization. BM25 scores combine evidence from each query term.',
  },
  {
    id: '03',
    category: 'Information retrieval',
    title: 'Why rare words carry more weight',
    text: 'TF-IDF weights terms by frequency and rarity. Inverse document frequency measures how many documents contain a term, not how often it appears overall. Rare words distinguish documents. This demo uses logarithmic term frequency with smoothed inverse document frequency. TF-IDF scores are additive and are not probabilities or cosine similarity.',
  },
  {
    id: '04',
    category: 'Data structures',
    title: 'Inside the inverted index',
    text: 'An inverted index maps each term to the documents that contain it. Posting lists store document identifiers and term frequencies. An AND query intersects posting lists; an OR query takes their union. If an AND query contains an absent term, the result must be empty. An index makes search efficient by avoiding repeated scans.',
  },
  {
    id: '05',
    category: 'Design',
    title: 'A library designed for wandering',
    text: 'A library invites discovery through structure and surprise. Clear categories, readable typography, and generous margins help readers browse a collection. Search supports a known question while browsing reveals questions we have not thought to ask. A digital library needs both paths.',
  },
  {
    id: '06',
    category: 'Machine learning',
    title: 'When vectors meet keywords',
    text: 'Semantic search embeds documents and queries as vectors. It can recover related ideas even when exact words differ. Keyword search is strong for exact identifiers and rare terms. Hybrid retrieval combines lexical and semantic rankings, often with reciprocal rank fusion. This collection uses lexical search only; no embedding model or external API is involved.',
  },
  {
    id: '07',
    category: 'Evaluation',
    title: 'Measuring a better search',
    text: 'Search evaluation starts with relevance judgments for a fixed set of queries. Precision at k measures how many top results are relevant. Reciprocal rank rewards the first relevant result. NDCG can evaluate graded relevance and ranking order. A small demonstration collection is useful for checking behavior but cannot establish production search quality.',
  },
  {
    id: '08',
    category: 'Engineering',
    title: 'Small systems, clear boundaries',
    text: 'A reliable system separates ingestion, indexing, and retrieval. Ingestion validates incoming documents. Indexing computes term frequencies and document statistics. Retrieval produces a deterministic ranking. A local first demo can keep all data in the browser, offering a fast start without credentials, servers, or network dependencies.',
  },
  {
    id: '09',
    category: 'Design',
    title: 'Trust begins with an explanation',
    text: 'Explainable search shows why a result appears. Highlight matched terms and reveal each term contribution to the final score. Let readers inspect document frequency, term frequency, and document length. An explanation should expose the actual calculation, not a plausible story invented after ranking.',
  },
  {
    id: '10',
    category: 'Information retrieval',
    title: 'The long and short of documents',
    text: 'Document length matters in ranking. A long document may repeat search terms many times without being more relevant. BM25 applies document length normalization relative to average collection length. At b equal to zero, length normalization is disabled. At b equal to one, the correction uses the full document length ratio.',
  },
  {
    id: '11',
    category: 'Engineering',
    title: 'Local first, private by default',
    text: 'Local first applications process data on the device. A browser can index a modest collection without sending documents to a server. Importing a JSON file keeps experimentation simple. Memory only storage means a refresh clears imported documents. Larger corpora need persistence, incremental indexing, and careful performance measurement.',
  },
  {
    id: '12',
    category: 'Evaluation',
    title: 'The trouble with a perfect score',
    text: 'A ranking score is not a confidence percentage. BM25 and TF-IDF produce different numerical scales, so their scores should not be compared directly. Compare document order and relevance instead. Deterministic tie breaking keeps repeated searches stable. Honest interfaces distinguish measured statistics from decorative metrics.',
  },
]
