<template>
  <div class="max-w-6xl mx-auto" style="background-color: lightblue;">
    <Menu />
    
    <!-- Hero Section -->
    <div class="text-center mb-20">
      <div class="relative inline-block mb-6">
        <h1 class="text-6xl md:text-7xl font-bold mb-6 bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-600 bg-clip-text text-transparent">
          About Our Search Engine
        </h1>
        <div class="absolute -inset-4 bg-gradient-to-r from-blue-600/20 via-indigo-600/20 to-purple-600/20 rounded-full blur-3xl opacity-50"></div>
      </div>
      <p class="text-xl md:text-2xl text-gray-600 max-w-4xl mx-auto leading-relaxed font-light">
        A modern, intelligent search engine built with cutting-edge technology to provide fast, accurate, and relevant search results.
      </p>
    </div>

    <!-- Features Grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 mb-20">
      <div class="glass rounded-3xl p-8 shadow-xl text-center group hover:scale-105 transition-all duration-500">
        <div class="relative mb-6">
          <div class="w-16 h-16 mx-auto bg-gradient-to-br from-blue-500 to-blue-600 rounded-2xl flex items-center justify-center shadow-lg group-hover:shadow-xl transition-all duration-300">
            <svg width="24" height="24" class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
          </div>
          <div class="absolute -inset-2 bg-gradient-to-r from-blue-500/20 to-blue-600/20 rounded-2xl blur opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
        </div>
        <h3 class="text-xl font-bold text-gray-800 mb-3">Lightning Fast</h3>
        <p class="text-gray-600 leading-relaxed">Optimized algorithms and efficient indexing for sub-second search results.</p>
      </div>

      <div class="glass rounded-3xl p-8 shadow-xl text-center group hover:scale-105 transition-all duration-500">
        <div class="relative mb-6">
          <div class="w-16 h-16 mx-auto bg-gradient-to-br from-green-500 to-green-600 rounded-2xl flex items-center justify-center shadow-lg group-hover:shadow-xl transition-all duration-300">
            <svg width="24" height="24" class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
            </svg>
          </div>
          <div class="absolute -inset-2 bg-gradient-to-r from-green-500/20 to-green-600/20 rounded-2xl blur opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
        </div>
        <h3 class="text-xl font-bold text-gray-800 mb-3">Intelligent Ranking</h3>
        <p class="text-gray-600 leading-relaxed">TF-IDF based scoring for highly relevant search results.</p>
      </div>

      <div class="glass rounded-3xl p-8 shadow-xl text-center group hover:scale-105 transition-all duration-500">
        <div class="relative mb-6">
          <div class="w-16 h-16 mx-auto bg-gradient-to-br from-purple-500 to-purple-600 rounded-2xl flex items-center justify-center shadow-lg group-hover:shadow-xl transition-all duration-300">
            <svg width="24" height="24" class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9v-9m0-9v9" />
            </svg>
          </div>
          <div class="absolute -inset-2 bg-gradient-to-r from-purple-500/20 to-purple-600/20 rounded-2xl blur opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
        </div>
        <h3 class="text-xl font-bold text-gray-800 mb-3">Web Crawling</h3>
        <p class="text-gray-600 leading-relaxed">Automated content discovery and indexing from any website.</p>
      </div>

      <div class="glass rounded-3xl p-8 shadow-xl text-center group hover:scale-105 transition-all duration-500">
        <div class="relative mb-6">
          <div class="w-16 h-16 mx-auto bg-gradient-to-br from-indigo-500 to-indigo-600 rounded-2xl flex items-center justify-center shadow-lg group-hover:shadow-xl transition-all duration-300">
            <svg width="24" height="24" class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4" />
            </svg>
          </div>
          <div class="absolute -inset-2 bg-gradient-to-r from-indigo-500/20 to-indigo-600/20 rounded-2xl blur opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
        </div>
        <h3 class="text-xl font-bold text-gray-800 mb-3">Scalable Architecture</h3>
        <p class="text-gray-600 leading-relaxed">Built with modern technologies for easy scaling and maintenance.</p>
      </div>

      <div class="glass rounded-3xl p-8 shadow-xl text-center group hover:scale-105 transition-all duration-500">
        <div class="relative mb-6">
          <div class="w-16 h-16 mx-auto bg-gradient-to-br from-yellow-500 to-yellow-600 rounded-2xl flex items-center justify-center shadow-lg group-hover:shadow-xl transition-all duration-300">
            <svg width="24" height="24" class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
            </svg>
          </div>
          <div class="absolute -inset-2 bg-gradient-to-r from-yellow-500/20 to-yellow-600/20 rounded-2xl blur opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
        </div>
        <h3 class="text-xl font-bold text-gray-800 mb-3">Secure & Reliable</h3>
        <p class="text-gray-600 leading-relaxed">Enterprise-grade security and 99.9% uptime reliability.</p>
      </div>

      <div class="glass rounded-3xl p-8 shadow-xl text-center group hover:scale-105 transition-all duration-500">
        <div class="relative mb-6">
          <div class="w-16 h-16 mx-auto bg-gradient-to-br from-red-500 to-red-600 rounded-2xl flex items-center justify-center shadow-lg group-hover:shadow-xl transition-all duration-300">
            <svg width="24" height="24" class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
            </svg>
          </div>
          <div class="absolute -inset-2 bg-gradient-to-r from-red-500/20 to-red-600/20 rounded-2xl blur opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
        </div>
        <h3 class="text-xl font-bold text-gray-800 mb-3">Real-time Monitoring</h3>
        <p class="text-gray-600 leading-relaxed">Live task monitoring and performance analytics.</p>
      </div>
    </div>

    <!-- Technology Stack -->
    <div class="mb-20">
      <div class="text-center mb-12">
        <h2 class="text-4xl font-bold mb-4 text-gray-800">Technology Stack</h2>
        <p class="text-gray-600 max-w-2xl mx-auto">Built with modern, scalable technologies for optimal performance</p>
      </div>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
        <div class="glass rounded-3xl p-8 shadow-xl">
          <h3 class="text-2xl font-bold text-gray-800 mb-6 flex items-center">
            <div class="w-10 h-10 bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl flex items-center justify-center mr-4 shadow-lg">
              <svg width="24" height="24" class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" />
              </svg>
            </div>
            Backend
          </h3>
          <ul class="space-y-4 text-gray-600">
            <li class="flex items-center">
              <div class="w-3 h-3 bg-blue-500 rounded-full mr-4"></div>
              <span class="font-medium">FastAPI</span> - Modern Python web framework
            </li>
            <li class="flex items-center">
              <div class="w-3 h-3 bg-blue-500 rounded-full mr-4"></div>
              <span class="font-medium">PostgreSQL</span> - Robust relational database
            </li>
            <li class="flex items-center">
              <div class="w-3 h-3 bg-blue-500 rounded-full mr-4"></div>
              <span class="font-medium">Redis</span> - High-performance caching
            </li>
            <li class="flex items-center">
              <div class="w-3 h-3 bg-blue-500 rounded-full mr-4"></div>
              <span class="font-medium">Celery</span> - Asynchronous task processing
            </li>
            <li class="flex items-center">
              <div class="w-3 h-3 bg-blue-500 rounded-full mr-4"></div>
              <span class="font-medium">NLTK</span> - Natural language processing
            </li>
          </ul>
        </div>

        <div class="glass rounded-3xl p-8 shadow-xl">
          <h3 class="text-2xl font-bold text-gray-800 mb-6 flex items-center">
            <div class="w-10 h-10 bg-gradient-to-br from-green-500 to-green-600 rounded-xl flex items-center justify-center mr-4 shadow-lg">
              <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zm0 0h12a2 2 0 002-2v-4a2 2 0 00-2-2h-2.343M11 7.343l1.657-1.657a2 2 0 012.828 0l2.829 2.829a2 2 0 010 2.828l-8.486 8.485M7 17v4a2 2 0 002 2h4M15 7l2-2 2 2m-2 2l-2-2" />
              </svg>
            </div>
            Frontend
          </h3>
          <ul class="space-y-4 text-gray-600">
            <li class="flex items-center">
              <div class="w-3 h-3 bg-green-500 rounded-full mr-4"></div>
              <span class="font-medium">Vue.js 3</span> - Progressive JavaScript framework
            </li>
            <li class="flex items-center">
              <div class="w-3 h-3 bg-green-500 rounded-full mr-4"></div>
              <span class="font-medium">TypeScript</span> - Type-safe development
            </li>
            <li class="flex items-center">
              <div class="w-3 h-3 bg-green-500 rounded-full mr-4"></div>
              <span class="font-medium">Tailwind CSS</span> - Utility-first styling
            </li>
            <li class="flex items-center">
              <div class="w-3 h-3 bg-green-500 rounded-full mr-4"></div>
              <span class="font-medium">Vite</span> - Lightning-fast build tool
            </li>
            <li class="flex items-center">
              <div class="w-3 h-3 bg-green-500 rounded-full mr-4"></div>
              <span class="font-medium">Axios</span> - HTTP client for API calls
            </li>
          </ul>
        </div>
      </div>
    </div>

    <!-- How It Works -->
    <div class="mb-20">
      <div class="text-center mb-12">
        <h2 class="text-4xl font-bold mb-4 text-gray-800">How It Works</h2>
        <p class="text-gray-600 max-w-2xl mx-auto">Simple three-step process from crawling to search results</p>
      </div>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
        <div class="text-center group">
          <div class="relative mb-6">
            <div class="w-20 h-20 mx-auto bg-gradient-to-br from-blue-500 to-blue-600 rounded-full flex items-center justify-center shadow-lg group-hover:shadow-xl transition-all duration-300">
              <span class="text-3xl font-bold text-white">1</span>
            </div>
            <div class="absolute -inset-2 bg-gradient-to-r from-blue-500/20 to-blue-600/20 rounded-full blur opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
          </div>
          <h3 class="text-xl font-bold text-gray-800 mb-3">Crawl</h3>
          <p class="text-gray-600 leading-relaxed">Our web crawler visits websites and extracts relevant content for indexing.</p>
        </div>
        <div class="text-center group">
          <div class="relative mb-6">
            <div class="w-20 h-20 mx-auto bg-gradient-to-br from-green-500 to-green-600 rounded-full flex items-center justify-center shadow-lg group-hover:shadow-xl transition-all duration-300">
              <span class="text-3xl font-bold text-white">2</span>
            </div>
            <div class="absolute -inset-2 bg-gradient-to-r from-green-500/20 to-green-600/20 rounded-full blur opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
          </div>
          <h3 class="text-xl font-bold text-gray-800 mb-3">Process</h3>
          <p class="text-gray-600 leading-relaxed">Content is tokenized, cleaned, and indexed using advanced algorithms.</p>
        </div>
        <div class="text-center group">
          <div class="relative mb-6">
            <div class="w-20 h-20 mx-auto bg-gradient-to-br from-purple-500 to-purple-600 rounded-full flex items-center justify-center shadow-lg group-hover:shadow-xl transition-all duration-300">
              <span class="text-3xl font-bold text-white">3</span>
            </div>
            <div class="absolute -inset-2 bg-gradient-to-r from-purple-500/20 to-purple-600/20 rounded-full blur opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
          </div>
          <h3 class="text-xl font-bold text-gray-800 mb-3">Search</h3>
          <p class="text-gray-600 leading-relaxed">Users search and get relevant results ranked by relevance and importance.</p>
        </div>
      </div>
    </div>

    <!-- Call to Action -->
    <div class="text-center">
      <div class="glass rounded-3xl p-12 shadow-2xl bg-gradient-to-r from-blue-600/90 to-indigo-600/90 backdrop-blur-sm">
        <h3 class="text-3xl font-bold text-white mb-4">Ready to Get Started?</h3>
        <p class="text-blue-100 mb-8 text-lg">Try our search engine and experience the difference.</p>
        <router-link 
          to="/" 
          class="inline-flex items-center px-8 py-4 bg-white text-blue-600 rounded-2xl hover:bg-gray-50 transition-all duration-300 font-semibold shadow-lg hover:shadow-xl hover:scale-105"
        >
          <svg class="w-5 h-5 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
          Start Searching
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import Menu from '@/components/Menu.vue'
</script>

<style>
@media (min-width: 1024px) {
  .about {
    min-height: 100vh;
    display: flex;
    align-items: center;
  }
}
</style>
