export interface Document {
  id: string
  title: string
  category: string
  text: string
}
export interface Contribution {
  term: string
  tf: number
  df: number
  idf: number
  score: number
}
export interface Result {
  document: Document
  score: number
  length: number
  terms: Contribution[]
}
export type Model = 'bm25' | 'tfidf'
const stopwords = new Set(
  'a an the and or of to in is it for on with as by are be that this from at'.split(' '),
)
export function tokenize(text: string): string[] {
  return (text.toLowerCase().match(/[\p{L}\p{N}]+/gu) ?? []).filter((t) => !stopwords.has(t))
}
export function buildIndex(documents: Document[]) {
  const records = documents.map((document) => {
    const tokens = tokenize(`${document.title} ${document.text}`)
    const counts = new Map<string, number>()
    tokens.forEach((t) => counts.set(t, (counts.get(t) ?? 0) + 1))
    return { document, counts, length: tokens.length }
  })
  const df = new Map<string, number>()
  records.forEach((r) => r.counts.forEach((_, t) => df.set(t, (df.get(t) ?? 0) + 1)))
  return {
    records,
    df,
    size: records.length,
    averageLength: records.reduce((s, r) => s + r.length, 0) / (records.length || 1),
  }
}
export function search(
  documents: Document[],
  query: string,
  model: Model = 'bm25',
  mode: 'OR' | 'AND' = 'OR',
  k1 = 1.2,
  b = 0.75,
): Result[] {
  const index = buildIndex(documents)
  const terms = [...new Set(tokenize(query))]
  if (!terms.length) return []
  return index.records
    .filter((r) =>
      mode === 'AND' ? terms.every((t) => r.counts.has(t)) : terms.some((t) => r.counts.has(t)),
    )
    .map((r) => {
      const contributions = terms.map((term) => {
        const tf = r.counts.get(term) ?? 0
        const df = index.df.get(term) ?? 0
        const idf =
          model === 'bm25'
            ? Math.log(1 + (index.size - df + 0.5) / (df + 0.5))
            : Math.log((index.size + 1) / (df + 1)) + 1
        const score =
          tf === 0
            ? 0
            : model === 'bm25'
              ? (idf * (tf * (k1 + 1))) /
                (tf + k1 * (1 - b + (b * r.length) / (index.averageLength || 1)))
              : (1 + Math.log(tf)) * idf
        return { term, tf, df, idf, score }
      })
      return {
        document: r.document,
        score: contributions.reduce((s, t) => s + t.score, 0),
        length: r.length,
        terms: contributions,
      }
    })
    .sort((a, b) => b.score - a.score || a.document.id.localeCompare(b.document.id))
}
export function parseImport(value: unknown): Document[] {
  if (!Array.isArray(value) || !value.length || value.length > 500)
    throw new Error('Use a JSON array containing 1–500 documents.')
  const ids = new Set<string>()
  return value.map((item, i) => {
    if (
      !item ||
      typeof item !== 'object' ||
      typeof item.title !== 'string' ||
      typeof item.text !== 'string' ||
      !item.title.trim() ||
      !item.text.trim()
    )
      throw new Error(`Document ${i + 1} needs a nonempty title and text.`)
    if (item.text.length > 100000 || item.title.length > 300)
      throw new Error(`Document ${i + 1} is too long (title: 300, text: 100,000 characters).`)
    const id = typeof item.id === 'string' ? item.id : `import-${i + 1}`
    if (ids.has(id)) throw new Error(`Duplicate document ID: ${id}`)
    ids.add(id)
    return {
      id,
      title: item.title,
      text: item.text,
      category: typeof item.category === 'string' ? item.category.slice(0, 100) : 'Your collection',
    }
  })
}
