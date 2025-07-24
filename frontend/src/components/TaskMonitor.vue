<template>
  <div class="space-y-6 custom-container">
    <!-- Crawl Task Input -->
    <div class="space-y-4">
      <div>
        <p class="text-sm text-blue-600 mb-4 font-medium">💡 Enter URLs below and click "Crawl & Index" to start</p>
      </div>
      
      <div class="space-y-3">
        <div class="relative">
          <textarea
            v-model="urls"
            placeholder="Enter URLs (one per line or comma-separated). Examples: https://example.com, https://another-site.com, https://third-site.com"
            class="w-full p-4 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent resize-none"
            rows="2"
          ></textarea>
        </div>
        
        <button 
          @click="startCrawlTask"
          :disabled="!urls.trim() || loading"
          class="custom-button"
        >
          <div class="flex items-center space-x-2">
            <svg height="24" width="24" v-if="!loading" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9v-9m0-9v9" />
            </svg>
            <svg height="24" width="24" v-else class="w-5 h-5 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            <span>{{ loading ? 'Crawling...' : 'Crawl' }}</span>
          </div>
        </button>
      </div>
    </div>

    <!-- Active Tasks List -->
    <div v-if="crawlTasks.length" class="space-y-4">
      <h3 class="text-lg font-semibold text-gray-800">Active Tasks</h3>
      
      <div class="space-y-3 max-h-64 overflow-y-auto">
        <div 
          v-for="(task, index) in crawlTasks" 
          :key="task.id" 
          class="bg-white border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow duration-200"
        >
          <div class="flex items-center justify-between mb-2">
            <div class="flex items-center space-x-2">
              <span class="text-sm font-medium text-gray-600">Task #{{ index + 1 }}</span>
              <span class="text-xs text-gray-400 font-mono">{{ task.id.slice(0, 8) }}...</span>
            </div>
            <StatusBadge :status="task.status" />
          </div>
          
          <div class="text-sm text-gray-600 mb-2">
            <span class="font-medium">URLs:</span> {{ task.urls.length }} site(s)
          </div>
          
          <div class="text-xs text-gray-500 space-y-1">
            <div v-for="url in task.urls.slice(0, 3)" :key="url" class="truncate">
              {{ url }}
            </div>
            <div v-if="task.urls.length > 3" class="text-blue-600">
              +{{ task.urls.length - 3 }} more...
            </div>
          </div>

          <!-- Progress Bar -->
          <div v-if="task.status !== 'SUCCESS' && task.status !== 'FAILURE'" class="mt-3">
            <div class="w-full bg-gray-200 rounded-full h-2">
              <div 
                class="h-2 rounded-full transition-all duration-500"
                :class="getProgressBarClass(task.status)"
                :style="{ width: getProgressWidth(task.status) }"
              ></div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-if="!crawlTasks.length" class="text-center py-8 text-gray-500">
      <div class="max-w-md mx-auto">
        <svg height="24" width="24" class="w-8 h-8 mx-auto mb-4 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9v-9m0-9v9" />
        </svg>
        <h3 class="text-lg font-semibold text-gray-700 mb-2">No crawling tasks</h3>
        <p class="text-gray-500">
          Enter URLs above to start crawling and indexing websites for search.
        </p>
      </div>
    </div>

    <!-- Info Card -->
    <div class="bg-blue-50 border border-blue-200 rounded-lg p-4">
      <div class="flex items-start space-x-3">
        <svg height="24" width="24" class="w-3 h-3 text-blue-600 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <div>
          <h4 class="text-sm font-medium text-blue-800">How it works</h4>
          <p class="text-sm text-blue-700 mt-1">
            The crawler visits each URL, extracts content, saves it to the database, and builds a search index. 
            Once complete, you can search for content from these websites.
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue"
import axios from "axios"
import StatusBadge from '@/components/StatusBadge.vue'

const urls = ref("")
const loading = ref(false)
const crawlTasks = ref<{ id: string; status: string; urls: string[] }[]>([])

const pollStatus = async (id: string, updateStatus: (s: string) => void) => {
  const interval = setInterval(async () => {
    try {
      const res = await axios.get(`/api/task/status/async/${id}`)
      updateStatus(res.data.status)
      if (["SUCCESS", "FAILURE"].includes(res.data.status)) {
        clearInterval(interval)
      }
    } catch (err) {
      updateStatus("ERROR")
      clearInterval(interval)
    }
  }, 2000)
}

const startCrawlTask = async () => {
  const urlList = urls.value
    .split(/[\n,]/)
    .map(u => u.trim())
    .filter(u => u.length > 0)
  
  if (!urlList.length) return alert("Please enter at least one URL.")

  loading.value = true
  
  try {
    const res = await axios.post("/api/task/crawl", urlList)
    const id = res.data.task_id

    const task = { id, status: "PENDING", urls: urlList }
    crawlTasks.value.push(task)

    pollStatus(id, (s) => {
      const t = crawlTasks.value.find((t) => t.id === id)
      if (t) t.status = s
    })

    urls.value = ""
  } catch (error) {
    console.error('Failed to start crawl task:', error)
    alert('Failed to start crawling task. Please try again.')
  } finally {
    loading.value = false
  }
}

const getProgressBarClass = (status: string) => {
  switch (status) {
    case 'PENDING': return 'bg-yellow-500'
    case 'STARTED': return 'bg-blue-500'
    case 'SUCCESS': return 'bg-green-500'
    case 'FAILURE': return 'bg-red-500'
    default: return 'bg-gray-500'
  }
}

const getProgressWidth = (status: string) => {
  switch (status) {
    case 'PENDING': return '25%'
    case 'STARTED': return '75%'
    case 'SUCCESS': return '100%'
    case 'FAILURE': return '100%'
    default: return '0%'
  }
}
</script>
