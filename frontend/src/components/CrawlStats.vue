<template>
  <div class="glass rounded-3xl p-8 shadow-xl">
    <div class="flex items-center mb-6" style="justify-content: center;">
      <h3 class="text-2xl font-bold text-gray-800">Crawl Statistics</h3>
      <button 
        @click="refreshStats"
        :disabled="loading"
        class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:opacity-50 transition-colors duration-200"
      >
        <svg v-if="loading" class="w-4 h-4 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
        </svg>
        <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
        </svg>
      </button>
    </div>

    <div v-if="loading" class="flex py-8" style="justify-content: center;">
      <div class="w-8 h-8 border-4 border-blue-200 border-t-blue-600 rounded-full animate-spin"></div>
    </div>

    <div v-else-if="stats" class="space-y-6">
      <!-- Main Stats -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div class="bg-gradient-to-br from-blue-50 to-blue-100 rounded-2xl p-6 text-center">
          <div class="text-3xl font-bold text-blue-600 mb-2">{{ stats.total_documents }}</div>
          <div class="text-gray-600 font-medium">Indexed Documents</div>
        </div>
        
        <div class="bg-gradient-to-br from-indigo-50 to-indigo-100 rounded-2xl p-6 text-center">
          <div class="text-3xl font-bold text-indigo-600 mb-2">{{ stats.unique_domains }}</div>
          <div class="text-gray-600 font-medium">Unique Domains</div>
        </div>
      </div>

      <!-- Domains List -->
      <div v-if="stats.domains && stats.domains.length > 0">
        <h4 class="text-lg font-semibold text-gray-800 mb-4">Recently Crawled Domains</h4>
        <div class="space-y-2">
          <div 
            v-for="domain in stats.domains" 
            :key="domain"
            class="flex items-center space-x-3 p-3 bg-white/50 rounded-lg hover:bg-white/70 transition-colors duration-200"
          >
            <div class="w-2 h-2 bg-green-500 rounded-full"></div>
            <span class="text-gray-700 font-medium">{{ domain }}</span>
          </div>
        </div>
      </div>

      <!-- No Data Message -->
      <div v-else class="text-center py-8" style="display: flex; justify-content: center;">
          <svg class="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
        <p class="text-gray-500">No documents indexed yet. Start crawling to see statistics.</p>
      </div>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="text-center py-8">
      <div class="w-16 h-16 mx-auto bg-red-100 rounded-full flex items-center justify-center mb-4">
        <svg class="w-8 h-8 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      </div>
      <p class="text-red-600 mb-4">{{ error }}</p>
      <button 
        @click="refreshStats"
        class="px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 transition-colors duration-200"
      >
        Try Again
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import axios from 'axios';

interface CrawlStats {
  total_documents: number;
  unique_domains: number;
  domains: string[];
}

const stats = ref<CrawlStats | null>(null);
const loading = ref(false);
const error = ref<string | null>(null);

const fetchStats = async () => {
  loading.value = true;
  error.value = null;
  
  try {
    const response = await axios.get('/api/crawl-stats');
    stats.value = response.data;
  } catch (err) {
    console.error('Error fetching crawl stats:', err);
    error.value = 'Failed to load crawl statistics';
  } finally {
    loading.value = false;
  }
};

const refreshStats = () => {
  fetchStats();
};

onMounted(() => {
  fetchStats();
});

// Auto-refresh every 30 seconds
setInterval(() => {
  if (!loading.value) {
    fetchStats();
  }
}, 30000);
</script> 