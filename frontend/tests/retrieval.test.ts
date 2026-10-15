import { test } from 'node:test'
import assert from 'node:assert/strict'
import { buildIndex, search, tokenize, parseImport } from '../src/lib/retrieval.ts'
const docs = [
  { id: 'a', title: 'Alpha', category: 'test', text: 'rare rare common' },
  { id: 'b', title: 'Beta', category: 'test', text: 'common' },
]
test('DF counts documents, not repeated occurrences', () => {
  const i = buildIndex(docs)
  assert.equal(i.df.get('rare'), 1)
  assert.equal(i.df.get('common'), 2)
})
test('AND cannot ignore absent query terms', () => {
  assert.equal(search(docs, 'rare absent', 'bm25', 'AND').length, 0)
  assert.equal(search(docs, 'rare absent', 'bm25', 'OR').length, 1)
})
test('scores are exact sums of inspectable contributions', () => {
  for (const model of ['bm25', 'tfidf'] as const) {
    const r = search(docs, 'rare common', model)[0]!
    assert.equal(
      r.score,
      r.terms.reduce((s, t) => s + t.score, 0),
    )
    assert.ok(r.score > 0)
  }
})
test('empty and stopword queries have no results', () => {
  assert.deepEqual(search([], 'rare'), [])
  assert.deepEqual(search(docs, 'the and'), [])
})
test('query repetition does not multiply scores', () =>
  assert.deepEqual(search(docs, 'rare rare'), search(docs, 'rare')))
test('tokenization handles whitespace, punctuation and unicode', () =>
  assert.deepEqual(tokenize('The café\nsearch-engine'), ['café', 'search', 'engine']))
test('import validation is atomic and rejects duplicate identifiers', () => {
  assert.throws(() => parseImport([{ title: 'x' }]))
  assert.throws(() => parseImport([docs[0], docs[0]]))
  assert.equal(parseImport([{ title: 'New', text: 'Document' }])[0]!.id, 'import-1')
})
test('BM25 single-term formula matches a hand calculation', () => {
  const r = search(docs, 'rare')[0]!
  const expected = (Math.log(2) * 4.4) / (2 + 1.2 * (0.25 + (0.75 * 4) / 3))
  assert.ok(Math.abs(r.score - expected) < 1e-12)
})
