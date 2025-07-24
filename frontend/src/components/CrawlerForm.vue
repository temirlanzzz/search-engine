<template>
  <div class="space-y-6">
    <!-- URL Input Section -->
    <div class="space-y-4">
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">
          Website URLs to Crawl
        </label>
        <textarea
          v-model="urls"
          placeholder="Enter URLs (one per line or comma-separated)&#10;&#10;Examples:&#10;https://example.com&#10;https://another-site.com&#10;https://third-site.com"
          class="w-full p-4 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent resize-none"
          rows="6"
        ></textarea>
        <p class="text-sm text-gray-500 mt-1">
          Enter one URL per line or separate with commas. The crawler will extract content from these websites.
        </p>
      </div>

      <button 
        @click="crawl" 
        :disabled="!urls.trim() || loading"
        class="custom-button"
      >
        <svg v-if="!loading" width="24" height="24" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9v-9m0-9v9" />
        </svg>
        <svg v-else width="24" height="24" class="w-5 h-5 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
        </svg>
        <span>{{ loading ? 'Crawling...' : 'Start Crawling' }}</span>
      </button>
    </div>

    <!-- Status Display -->
    <div v-if="status" class="bg-gray-50 rounded-lg p-4">
      <div class="flex items-center space-x-2">
        <svg v-if="status === 'success'" width="24" height="24" class="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
        </svg>
        <svg v-else width="24" height="24" class="w-5 h-5 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
        <span class="font-medium" :class="status === 'success' ? 'text-green-800' : 'text-red-800'">
          {{ status === 'success' ? 'Crawling completed successfully!' : 'Crawling failed' }}
        </span>
      </div>
    </div>

    <!-- Statistics Display -->
    <div v-if="top_ten_terms.length > 0 || top_ten_terms_inverted_index.length > 0" class="space-y-4">
      <h4 class="text-lg font-semibold text-gray-800">Crawling Statistics</h4>
      
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <!-- Top Terms -->
        <div v-if="top_ten_terms.length > 0" class="bg-white border border-gray-200 rounded-lg p-4">
          <h5 class="text-sm font-medium text-gray-700 mb-3">Top Terms Found</h5>
          <div class="space-y-1">
            <div 
              v-for="(term, index) in top_ten_terms.slice(0, 10)" 
              :key="index"
              class="flex items-center justify-between text-sm"
            >
              <span class="text-gray-600">{{ term }}</span>
              <span class="text-gray-400 text-xs">#{{ index + 1 }}</span>
            </div>
          </div>
        </div>

        <!-- Inverted Index Terms -->
        <div v-if="top_ten_terms_inverted_index.length > 0" class="bg-white border border-gray-200 rounded-lg p-4">
          <h5 class="text-sm font-medium text-gray-700 mb-3">Inverted Index Terms</h5>
          <div class="space-y-1">
            <div 
              v-for="(term, index) in top_ten_terms_inverted_index.slice(0, 10)" 
              :key="index"
              class="flex items-center justify-between text-sm"
            >
              <span class="text-gray-600">{{ term }}</span>
              <span class="text-gray-400 text-xs">#{{ index + 1 }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Info Card -->
    <div class="bg-purple-50 border border-purple-200 rounded-lg p-4">
      <div class="flex items-start space-x-3">
        <svg width="24" height="24" class="w-5 h-5 text-purple-600 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <div>
          <h4 class="text-sm font-medium text-purple-800">How crawling works</h4>
          <p class="text-sm text-purple-700 mt-1">
            The crawler visits each URL, extracts text content, and processes it for search indexing. 
            This may take a few minutes depending on the number and size of websites.
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue"
import axios from "axios"

const urls = ref("")
const status = ref("")
const loading = ref(false)
const top_ten_terms = ref<string[]>([])
const top_ten_terms_inverted_index = ref<string[]>([])

const crawl = async () => {
  if (!urls.value.trim()) return
  
  loading.value = true
  status.value = ""
  
  try {
    const urlList = urls.value
      .split(/[\n,]/)
      .map(u => u.trim())
      .filter(u => u.length > 0)
    
    const res = await axios.post("/api/task/crawl", urlList)
    status.value = "success"
    top_ten_terms.value = res.data.top_ten_terms || []
    top_ten_terms_inverted_index.value = res.data.top_ten_terms_inverted_index || []
  } catch (error) {
    console.error('Crawling failed:', error)
    status.value = "error"
  } finally {
    loading.value = false
  }
}
</script>
  