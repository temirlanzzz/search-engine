<template>
  <div class="space-y-4">
    <div class="flex items-center justify-between">
      <div>
        <h3 class="text-lg font-semibold text-gray-800">Index Management</h3>
        <p class="text-sm text-gray-600">Rebuild the search index from existing documents</p>
      </div>
      <button 
        @click="rebuild" 
        :disabled="loading"
        class="custom-button"
      >
        <svg v-if="!loading" width="24" height="24" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
        </svg>
        <svg v-else width="24" height="24" class="w-4 h-4 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
        </svg>
        <span>{{ loading ? 'Rebuilding...' : 'Rebuild Index' }}</span>
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
          {{ status === 'success' ? 'Index rebuilt successfully!' : 'Failed to rebuild index' }}
        </span>
      </div>
      <p v-if="status === 'success'" class="text-sm text-green-600 mt-1">
        Your search index has been updated with the latest content.
      </p>
    </div>

    <!-- Info Card -->
    <div class="bg-blue-50 border border-blue-200 rounded-lg p-4">
      <div class="flex items-start space-x-3">
        <svg width="24" height="24" class="w-5 h-5 text-blue-600 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <div>
          <h4 class="text-sm font-medium text-blue-800">What does this do?</h4>
          <p class="text-sm text-blue-700 mt-1">
            Rebuilding the index processes all crawled documents and creates a new search index. 
            This improves search performance and ensures all content is properly indexed.
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue"
import axios from 'axios'

const status = ref("")
const loading = ref(false)

const rebuild = async () => {
  loading.value = true
  status.value = ""
  
  try {
    const res = await axios.post("/api/task/rebuild")
    status.value = "success"
  } catch (error) {
    console.error('Failed to rebuild index:', error)
    status.value = "error"
  } finally {
    loading.value = false
  }
}
</script>
  