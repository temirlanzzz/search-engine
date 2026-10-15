<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { corpus } from './lib/corpus'
import { buildIndex, parseImport, search, tokenize, type Model } from './lib/retrieval'
const documents = ref([...corpus])
const query = ref('document length')
const model = ref<Model>('bm25')
const mode = ref<'OR' | 'AND'>('OR')
const category = ref('All subjects')
const active = ref('10')
const tab = ref('Search collection')
const k1 = ref(1.2)
const b = ref(0.75)
const notice = ref('')
const imported = ref(false)
const fileInput = ref<HTMLInputElement>()
const index = computed(() => buildIndex(documents.value))
const ranked = computed(() =>
  search(documents.value, query.value, model.value, mode.value, k1.value, b.value),
)
const results = computed(() =>
  ranked.value.filter(
    (r) => category.value === 'All subjects' || r.document.category === category.value,
  ),
)
const alternative = computed(() =>
  search(
    documents.value,
    query.value,
    model.value === 'bm25' ? 'tfidf' : 'bm25',
    mode.value,
    k1.value,
    b.value,
  ).filter((r) => category.value === 'All subjects' || r.document.category === category.value),
)
const selected = computed(
  () => results.value.find((r) => r.document.id === active.value) ?? results.value[0],
)
const categories = computed(() => [
  'All subjects',
  ...new Set(documents.value.map((d) => d.category)),
])
const queryTerms = computed(() => [...new Set(tokenize(query.value))])
const missing = computed(() => queryTerms.value.filter((t) => !index.value.df.has(t)))
watch([query, model, mode, category], () => {
  active.value = results.value[0]?.document.id ?? ''
})
function parts(text: string) {
  return text
    .split(/([\p{L}\p{N}]+)/u)
    .map((text) => ({ text, match: queryTerms.value.includes(text.toLowerCase()) }))
}
function reset() {
  documents.value = [...corpus]
  imported.value = false
  category.value = 'All subjects'
  notice.value = 'The original collection is restored.'
}
async function importFile(event: Event) {
  const input = event.target as HTMLInputElement
  const file = input.files?.[0]
  if (!file) return
  try {
    if (file.size > 2_000_000) throw new Error('Please choose a JSON file smaller than 2 MB.')
    documents.value = parseImport(JSON.parse(await file.text()))
    imported.value = true
    category.value = 'All subjects'
    notice.value = `Imported ${documents.value.length} documents. They stay in this tab until refresh.`
  } catch (error) {
    notice.value = error instanceof Error ? error.message : 'Could not read that file.'
  }
  input.value = ''
}
function download() {
  const url = URL.createObjectURL(
    new Blob([JSON.stringify(corpus, null, 2)], { type: 'application/json' }),
  )
  const a = document.createElement('a')
  a.href = url
  a.download = 'marginalia-collection.json'
  a.click()
  URL.revokeObjectURL(url)
}
</script>

<template>
  <div class="shell">
    <header class="masthead">
      <a class="brand" href="#" aria-label="Marginalia home"
        ><span class="brand-symbol">m.</span> marginalia<span class="edition"
          >A SEARCH FIELD GUIDE</span
        ></a
      ><span class="local"><i></i> Local, by design</span
      ><a
        class="source"
        href="https://github.com/temirlanzzz/search-engine"
        target="_blank"
        rel="noreferrer"
        >Source ↗</a
      >
    </header>
    <nav aria-label="Main navigation">
      <button
        v-for="item in ['Search collection', 'The reading room', 'How it works']"
        :key="item"
        :class="{ current: tab === item }"
        @click="tab = item"
      >
        {{ item }}</button
      ><span>VOL. 01 / EXPLAINABLE RETRIEVAL</span>
    </nav>
    <main>
      <section class="hero">
        <div>
          <div class="eyebrow">FOLLOW THE WORDS. SEE THE REASONING.</div>
          <h1>Good search leaves<br />a <em>paper trail.</em></h1>
          <p>
            A small collection. Two ranking models. Every score explained.<br />Explore how a search
            engine decides what matters.
          </p>
        </div>
        <div class="hero-art" aria-hidden="true">
          <div class="paper paper-back">INDEX<br /><span>01 — 12</span></div>
          <div class="paper paper-front">
            <span>FIELD NOTE Nº 01</span
            ><b>Relevance<br />is a sum of<br /><em>small clues.</em></b>
            <div>term × rarity × context</div>
          </div>
          <span class="stamp">OPEN<br />COLLECTION</span>
        </div>
      </section>
      <template v-if="tab === 'Search collection'">
        <section class="search-section" aria-label="Search controls">
          <label class="eyebrow" for="query">YOUR QUESTION, IN A FEW WORDS</label>
          <div class="search-line">
            <span aria-hidden="true">⌕</span
            ><input
              id="query"
              v-model="query"
              placeholder="Search the collection…"
              autocomplete="off"
            /><button v-if="query" class="clear" aria-label="Clear search" @click="query = ''">
              ×</button
            ><span class="search-label">LIVE SEARCH ↵</span>
          </div>
          <div class="suggestions">
            <span>Try a thread</span
            ><button
              v-for="example in [
                'document length',
                'rare terms',
                'explainable search',
                'local first',
              ]"
              :key="example"
              @click="query = example"
            >
              {{ example }} ↗
            </button>
          </div>
        </section>
        <div class="workspace">
          <aside class="controls">
            <div class="section-label">01 / THE LENS</div>
            <h2>Ways of seeing</h2>
            <label class="field-label" for="model">Ranking model</label
            ><select id="model" v-model="model">
              <option value="bm25">BM25</option>
              <option value="tfidf">TF-IDF</option>
            </select>
            <p class="muted">
              {{
                model === 'bm25'
                  ? 'Rewards rare terms, with a lighter touch on repetition and long documents.'
                  : 'Logarithmic term frequency, weighted by smoothed rarity. No length normalization.'
              }}
            </p>
            <label class="field-label" for="mode">Match terms</label
            ><select id="mode" v-model="mode">
              <option value="OR">Any term · OR</option>
              <option value="AND">Every term · AND</option></select
            ><label class="field-label" for="subject">Subject</label
            ><select id="subject" v-model="category">
              <option v-for="c in categories" :key="c">{{ c }}</option></select
            ><template v-if="model === 'bm25'"
              ><label class="slider-label" for="saturation"
                >Saturation <span>k₁ {{ k1.toFixed(1) }}</span></label
              ><input
                id="saturation"
                v-model.number="k1"
                type="range"
                min="0.2"
                max="3"
                step="0.1" /><label class="slider-label" for="normalization"
                >Length correction <span>b {{ b.toFixed(2) }}</span></label
              ><input
                id="normalization"
                v-model.number="b"
                type="range"
                min="0"
                max="1"
                step="0.05"
            /></template>
            <div class="collection-note">
              <span class="section-label">ON THE SHELVES</span
              ><strong>{{ documents.length }} documents</strong>
              <p>
                {{ index.df.size }} unique terms · {{ index.averageLength.toFixed(1) }} average
                tokens
              </p>
              <button class="text-button" @click="tab = 'The reading room'">
                Browse the collection ↗
              </button>
            </div>
          </aside>
          <section class="results" aria-label="Search results">
            <div class="results-header">
              <div>
                <span class="section-label">02 / THE FINDINGS</span>
                <h2>
                  {{ results.length }} {{ results.length === 1 ? 'result' : 'results'
                  }}<span class="query-caption"> for your curiosity</span>
                </h2>
              </div>
              <span class="model-tag">{{ model.toUpperCase() }}</span>
            </div>
            <p v-if="missing.length" class="missing">
              Not in the index: {{ missing.join(', ')
              }}<span v-if="mode === 'AND'">. Every term must match.</span>
            </p>
            <p v-if="!results.length" class="empty">
              {{
                queryTerms.length
                  ? 'No pages found. Try fewer words, another subject, or “Any term”.'
                  : 'Start with a word or two. The collection is ready to explore.'
              }}
            </p>
            <button
              v-for="(result, i) in results"
              :key="result.document.id"
              class="result-card"
              :class="{ selected: selected?.document.id === result.document.id }"
              @click="active = result.document.id"
              :aria-pressed="selected?.document.id === result.document.id"
            >
              <span class="rank">{{ String(i + 1).padStart(2, '0') }}</span>
              <div class="result-content">
                <span class="category">{{ result.document.category }}</span>
                <h3>
                  <template v-for="(part, j) in parts(result.document.title)" :key="j"
                    ><mark v-if="part.match">{{ part.text }}</mark
                    ><template v-else>{{ part.text }}</template></template
                  >
                </h3>
                <p>
                  <template v-for="(part, j) in parts(result.document.text.slice(0, 190))" :key="j"
                    ><mark v-if="part.match">{{ part.text }}</mark
                    ><template v-else>{{ part.text }}</template></template
                  >…
                </p>
                <div class="result-bottom">
                  <span
                    >{{ result.length }} tokens ·
                    {{ result.terms.filter((t) => t.tf > 0).length }}/{{ queryTerms.length }} terms
                    matched</span
                  ><span
                    >{{ result.score.toFixed(3) }} <span class="score-word">score</span> ↗</span
                  >
                </div>
              </div>
            </button>
          </section>
          <aside class="inspector" aria-label="Score explanation">
            <div class="section-label">03 / IN THE MARGINS</div>
            <h2>Why this page?</h2>
            <template v-if="selected"
              ><p class="inspector-title">{{ selected.document.title }}</p>
              <div class="score-total">
                <strong>{{ selected.score.toFixed(3) }}</strong
                ><span>{{ model.toUpperCase() }} SCORE<br />Sum of term contributions</span>
              </div>
              <div class="term" v-for="term in selected.terms" :key="term.term">
                <div>
                  <b>{{ term.term }}</b
                  ><span>{{ term.score.toFixed(3) }}</span>
                </div>
                <div class="bar">
                  <span
                    :style="{
                      width: `${selected.score ? (term.score / selected.score) * 100 : 0}%`,
                    }"
                  ></span>
                </div>
                <p>
                  {{ term.tf }} occurrences · in {{ term.df }} of
                  {{ documents.length }} docs<br />Inverse document frequency:
                  {{ term.idf.toFixed(3) }}
                </p>
              </div>
              <div class="comparison">
                <span class="section-label">A SECOND OPINION</span>
                <p>
                  With {{ model === 'bm25' ? 'TF-IDF' : 'BM25' }}, this page ranks
                  <b
                    >#{{
                      alternative.findIndex((r) => r.document.id === selected?.document.id) + 1
                    }}</b
                  >.
                </p>
                <small>Compare order, not scores: each model uses a different scale.</small>
              </div>
              <details>
                <summary>Read the full document</summary>
                <p>{{ selected.document.text }}</p>
              </details>
              <details>
                <summary>Show the calculation</summary>
                <p v-if="model === 'bm25'">
                  Σ IDF × tf(k₁ + 1) / (tf + k₁(1 − b + b × length / average length))<br /><br />IDF
                  = ln(1 + (N − df + 0.5) / (df + 0.5))
                </p>
                <p v-else>
                  Σ (1 + ln(tf)) × (ln((N + 1) / (df + 1)) + 1)<br /><br />Terms absent from the
                  document contribute zero.
                </p>
              </details></template
            >
            <p v-else class="muted">Choose a result to follow its paper trail.</p>
          </aside>
        </div>
      </template>
      <section v-else-if="tab === 'The reading room'" class="reading">
        <div class="room-header">
          <div>
            <span class="section-label">THE READING ROOM</span>
            <h2>A collection to think with.</h2>
            <p>Twelve original field notes on search, systems, and the act of discovery.</p>
          </div>
          <div>
            <button class="solid" @click="fileInput?.click()">Import JSON ↗</button
            ><button class="outline" @click="download">Download sample</button
            ><button v-if="imported" class="outline" @click="reset">Restore collection</button>
          </div>
        </div>
        <p class="muted">
          Bring 1–500 documents as a JSON array with title, text, and optional id and category.
          Maximum 2 MB. Imports replace this collection, stay in memory, and never leave this
          browser tab.
        </p>
        <div class="document-grid">
          <article v-for="doc in documents" :key="doc.id">
            <span class="category">{{ doc.category }}</span>
            <h3>{{ doc.title }}</h3>
            <p>{{ doc.text }}</p>
            <span class="section-label"
              >{{ tokenize(doc.title + ' ' + doc.text).length }} TOKENS / {{ doc.id }}</span
            >
          </article>
        </div>
      </section>
      <section v-else class="method">
        <span class="section-label">AN OPEN NOTEBOOK</span>
        <h2>No black box.<br />Just words and weights.</h2>
        <div class="method-grid">
          <article>
            <span>01</span>
            <h3>Read & normalize</h3>
            <p>
              Titles and body text receive equal weight. Unicode letters and numbers are lowercased,
              punctuation separates words, and a small fixed list of English stopwords is removed.
              There is no stemming, fuzzy matching, or semantic model.
            </p>
          </article>
          <article>
            <span>02</span>
            <h3>Count the evidence</h3>
            <p>
              The index counts occurrences within each document and the number of documents
              containing each term. Document frequency counts each document once, regardless of
              repetition. Queries use unique terms; AND requires all of them.
            </p>
          </article>
          <article>
            <span>03</span>
            <h3>Rank, then explain</h3>
            <p>
              BM25 adds frequency saturation and length normalization. TF-IDF uses log frequency and
              smoothed rarity. Each displayed score is the sum of the exact per-term contributions.
              Ties are broken by document ID.
            </p>
          </article>
        </div>
        <p class="honesty">
          A working retrieval laboratory, not a relevance benchmark. These are original teaching
          notes, not a web crawl. Statistics are computed from the current collection. Search
          happens entirely in your browser; the original Python crawler and database backend remain
          available separately.
        </p>
      </section>
      <input
        ref="fileInput"
        type="file"
        accept="application/json,.json"
        hidden
        @change="importFile"
      />
      <p v-if="notice" class="notice" role="status">
        {{ notice }} <button aria-label="Dismiss notice" @click="notice = ''">×</button>
      </p>
    </main>
    <footer>
      <span class="footer-brand">marginalia</span
      ><span>Made for curious minds. Built to be inspected.</span
      ><span>NO KEYS. NO CLOUD. JUST CLUES.</span>
    </footer>
  </div>
</template>
