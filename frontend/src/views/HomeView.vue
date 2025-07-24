<template>
  <div class="max-w-6xl mx-auto" style="background-color: lightblue;">
    <Menu />
    
    <!-- Hero Section -->
    <div class="text-center mb-16">
      <div class="mb-12">
        <div class="relative inline-block mb-6">
          <h1 class="text-6xl md:text-7xl font-bold mb-6 bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-600 bg-clip-text text-transparent animate-float">
            Smart Search Engine
          </h1>
          <div class="absolute -inset-4 bg-gradient-to-r from-blue-600/20 via-indigo-600/20 to-purple-600/20 rounded-full blur-3xl opacity-50 animate-pulse"></div>
        </div>
      </div>
      
      <!-- Search Box -->
      <div class="max-w-3xl mx-auto mb-8">
        <div class="mb-6 text-center">
          <p class="text-lg text-gray-500 mb-2 font-medium">Type your search query and press Enter or click Search</p>
        </div>
        <SearchBox @search="handleSearch" />
      </div>
    </div>

    <!-- Search Results -->
    <div v-if="loading" class="flex justify-center items-center py-16 custom-container">
      <div class="relative">
        <div class="w-16 h-16 border-4 border-blue-200 border-t-blue-600 rounded-full animate-spin"></div>
        <div class="absolute inset-0 w-16 h-16 border-4 border-transparent border-t-indigo-600 rounded-full animate-spin animation-delay-150"></div>
        <div class="absolute inset-0 w-16 h-16 border-4 border-transparent border-t-purple-600 rounded-full animate-spin animation-delay-300"></div>
      </div>
    </div>

    <div v-else-if="results.length" class="space-y-8 custom-container">
      <div class="flex items-center justify-between mb-8">
        <div class="flex items-center space-x-4">
          <h2 class="text-3xl font-bold text-gray-800">
            Search Results
          </h2>
          <span class="px-4 py-2 bg-gradient-to-r from-blue-500 to-indigo-500 text-white rounded-full text-sm font-semibold shadow-lg">
            {{ results.length }} results
          </span>
        </div>
        <div class="text-sm text-gray-500 bg-white/80 backdrop-blur-sm px-4 py-2 rounded-full border border-white/20">
          Found in {{ searchTime }}ms
        </div>
      </div>
      
      <div class="grid gap-8">
        <ResultCard 
          v-for="(doc, index) in results" 
          :key="doc.id" 
          :doc="doc" 
          :index="index"
        />
      </div>
    </div>

    <!-- No Results -->
    <div v-else-if="searched && !loading" class="text-center py-20 custom-container">
      <div class="max-w-md mx-auto">
        <div class="mb-8 relative">
          <div class="w-24 h-24 mx-auto bg-gradient-to-br from-gray-100 to-gray-200 rounded-full flex items-center justify-center shadow-lg">
            <svg class="w-12 h-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
          </div>
          <div class="absolute -inset-4 bg-gradient-to-r from-gray-200/50 to-gray-300/50 rounded-full blur-2xl opacity-50"></div>
        </div>
        <h3 class="text-2xl font-bold text-gray-700 mb-4">No results found</h3>
        <p class="text-gray-500 mb-8 leading-relaxed">
          Try adjusting your search terms or browse our tools to add more content to the index
        </p>
        <router-link 
          to="/tools" 
          class="inline-flex items-center px-8 py-4 bg-gradient-to-r from-blue-600 to-indigo-600 text-white rounded-2xl hover:from-blue-700 hover:to-indigo-700 transition-all duration-300 shadow-lg hover:shadow-xl hover:scale-105 font-semibold"
        >
          <svg class="w-5 h-5 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
          </svg>
          Add Content
        </router-link>
      </div>
    </div>

    <!-- Quick Stats -->
    <div v-if="!searched" class="mt-20 custom-container">
      <!-- Crawl Statistics -->
      <div class="mb-16">
        <div class="text-center mb-8">
          <h2 class="text-3xl font-bold text-gray-800 mb-4">Search Engine Statistics</h2>
          <p class="text-gray-600 max-w-2xl mx-auto">Real-time statistics about your indexed content</p>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8 mb-12">
          <div class="glass rounded-3xl p-8 text-center group hover:scale-105 transition-all duration-500 shadow-xl hover:shadow-2xl">
            
            <div class="text-4xl font-bold text-blue-600 mb-3">{{ crawlStats.total_documents || 0 }}</div>
            <p class="text-gray-600 font-medium">Indexed Documents</p>
          </div>
          
          <div class="glass rounded-3xl p-8 text-center group hover:scale-105 transition-all duration-500 shadow-xl hover:shadow-2xl">
            
            <div class="text-4xl font-bold text-indigo-600 mb-3">{{ crawlStats.unique_domains || 0 }}</div>
            <p class="text-gray-600 font-medium">Unique Domains</p>
          </div>
          
          <div class="glass rounded-3xl p-8 text-center group hover:scale-105 transition-all duration-500 shadow-xl hover:shadow-2xl">
           
            <div class="text-4xl font-bold text-purple-600 mb-3">{{ crawlStats.domains?.length || 0 }}</div>
            <p class="text-gray-600 font-medium">Recent Domains</p>
          </div>
        </div>
      </div>

      <div class="text-center mb-12 custom-container">
        <h2 class="text-3xl font-bold text-gray-800 mb-4">Why Choose Our Search Engine?</h2>
        <p class="text-gray-600 max-w-2xl mx-auto">Experience the next generation of search technology with our advanced features</p>
      </div>
      
      <div class="grid grid-cols-1 md:grid-cols-3 gap-8 custom-container">
        <div class="glass rounded-3xl p-8 text-center group hover:scale-105 transition-all duration-500 shadow-xl hover:shadow-2xl">
          <div class="relative mb-6">
            <div class="w-16 h-16 mx-auto bg-gradient-to-br from-blue-500 to-blue-600 rounded-2xl flex items-center justify-center shadow-lg group-hover:shadow-xl transition-all duration-300">
              <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            </div>
            <div class="absolute -inset-2 bg-gradient-to-r from-blue-500/20 to-blue-600/20 rounded-2xl blur opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
          </div>
          <h3 class="text-2xl font-bold text-gray-800 mb-3">Lightning Fast</h3>
          <p class="text-gray-600 leading-relaxed">Get instant search results with our optimized indexing and retrieval algorithms</p>
        </div>
        
        <div class="glass rounded-3xl p-8 text-center group hover:scale-105 transition-all duration-500 shadow-xl hover:shadow-2xl">
          <div class="relative mb-6">
            <div class="w-16 h-16 mx-auto bg-gradient-to-br from-indigo-500 to-indigo-600 rounded-2xl flex items-center justify-center shadow-lg group-hover:shadow-xl transition-all duration-300">
              <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
              </svg>
            </div>
            <div class="absolute -inset-2 bg-gradient-to-r from-indigo-500/20 to-indigo-600/20 rounded-2xl blur opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
          </div>
          <h3 class="text-2xl font-bold text-gray-800 mb-3">Intelligent Ranking</h3>
          <p class="text-gray-600 leading-relaxed">Advanced algorithms ensure the most relevant results appear first</p>
        </div>
        
        <div class="glass rounded-3xl p-8 text-center group hover:scale-105 transition-all duration-500 shadow-xl hover:shadow-2xl">
          <div class="relative mb-6">
            <div class="w-16 h-16 mx-auto bg-gradient-to-br from-purple-500 to-purple-600 rounded-2xl flex items-center justify-center shadow-lg group-hover:shadow-xl transition-all duration-300">
              <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div class="absolute -inset-2 bg-gradient-to-r from-purple-500/20 to-purple-600/20 rounded-2xl blur opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
          </div>
          <h3 class="text-2xl font-bold text-gray-800 mb-3">Accurate Results</h3>
          <p class="text-gray-600 leading-relaxed">High precision search with comprehensive content indexing and validation</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import SearchBox from '@/components/SearchBox.vue';
import ResultCard from '@/components/ResultCard.vue';
import Menu from '@/components/Menu.vue';
import axios from 'axios';

type SearchResult = {
  id: string;
  title: string;
  url: string;
  snippet: string;
};

const results = ref<SearchResult[]>([]);
const searched = ref(false);
const loading = ref(false);
const searchTime = ref(0);
const crawlStats = ref({
  total_documents: 0,
  unique_domains: 0,
  domains: []
});

const fetchCrawlStats = async () => {
  try {
    const response = await axios.get('/api/crawl-stats');
    crawlStats.value = response.data;
  } catch (error) {
    console.error('Error fetching crawl stats:', error);
  }
};

const handleSearch = async (query: string) => {
  if (!query.trim()) return;
  
  loading.value = true;
  const startTime = Date.now();
  
  try {
    const res = await axios.get(`/api/search?q=${encodeURIComponent(query)}`);
    results.value = res.data.results;
    searched.value = true;
    searchTime.value = Date.now() - startTime;
  } catch (error) {
    console.error('Search error:', error);
    results.value = [];
    searched.value = true;
  } finally {
    loading.value = false;
  }
};

// Fetch crawl stats on mount
onMounted(() => {
  fetchCrawlStats();
});
</script>

<style scoped>
.animation-delay-150 {
  animation-delay: 150ms;
}

.animation-delay-300 {
  animation-delay: 300ms;
}
</style>
