<template>
  <div 
    class="group glass rounded-3xl p-8 shadow-xl hover:shadow-2xl transition-all duration-500 transform hover:-translate-y-2 hover:scale-[1.02]"
    :style="{ animationDelay: `${(index || 0) * 150}ms` }"
  >
    <!-- Title and URL -->
    <div class="mb-6">
      <h3 class="text-2xl font-bold text-gray-900 mb-3 group-hover:text-blue-600 transition-colors duration-300 line-clamp-2">
        <a :href="doc.url" target="_blank" rel="noopener noreferrer" class="hover:underline">
          {{ doc.title }}
        </a>
      </h3>
      
      <!-- URL with icon -->
      <div class="flex items-center space-x-3 text-sm text-gray-500">
        <div class="relative">
          <svg width="24" height="24" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1" />
          </svg>
          <div class="absolute -inset-1 bg-blue-500 rounded-full opacity-0 group-hover:opacity-20 blur transition-opacity duration-300"></div>
        </div>
        <a 
          :href="doc.url" 
          target="_blank" 
          rel="noopener noreferrer"
          class="hover:text-blue-600 transition-colors duration-300 truncate font-medium"
        >
          {{ formatUrl(doc.url) }}
        </a>
      </div>
    </div>

    <!-- Snippet -->
    <p class="text-gray-700 leading-relaxed line-clamp-3 mb-6 text-lg">
      {{ doc.snippet }}
    </p>

    <!-- Action Buttons -->
    <div class="flex items-center justify-between">
      <div class="flex items-center space-x-4">
        <a 
          :href="doc.url" 
          target="_blank" 
          rel="noopener noreferrer"
          class="inline-flex items-center px-6 py-3 bg-gradient-to-r from-blue-600 to-indigo-600 text-white text-sm font-semibold rounded-xl hover:from-blue-700 hover:to-indigo-700 transition-all duration-300 shadow-lg hover:shadow-xl hover:scale-105"
        >
          <svg width="24" height="24" class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
          </svg>
          Visit Site
        </a>
        
        <button 
          @click="copyUrl"
          class="inline-flex items-center px-4 py-3 bg-white/80 backdrop-blur-sm text-gray-700 text-sm font-medium rounded-xl hover:bg-white hover:text-blue-600 transition-all duration-300 shadow-md hover:shadow-lg border border-white/20"
          :title="copyStatus"
        >
          <svg v-if="!copied" width="24" height="24" class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
          </svg>
          <svg v-else width="24" height="24" class="w-4 h-4 mr-2 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
          </svg>
          {{ copied ? 'Copied!' : 'Copy URL' }}
        </button>
      </div>

      <!-- Result ID (for debugging) -->
      <div class="text-xs text-gray-400 font-mono bg-white/50 backdrop-blur-sm px-3 py-2 rounded-lg border border-white/20">
        #{{ doc.id }}
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';

interface Props {
  doc: {
    id: string;
    title: string;
    url: string;
    snippet: string;
  };
  index?: number;
}

const props = defineProps<Props>();
const copied = ref(false);
const copyStatus = ref('Copy URL');

const formatUrl = (url: string): string => {
  try {
    const urlObj = new URL(url);
    return urlObj.hostname + urlObj.pathname;
  } catch {
    return url;
  }
};

const copyUrl = async () => {
  try {
    await navigator.clipboard.writeText(props.doc.url);
    copied.value = true;
    copyStatus.value = 'Copied!';
    
    setTimeout(() => {
      copied.value = false;
      copyStatus.value = 'Copy URL';
    }, 2000);
  } catch (err) {
    console.error('Failed to copy URL:', err);
    copyStatus.value = 'Failed to copy';
  }
};
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* Animation for staggered entrance */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.group {
  animation: fadeInUp 0.8s ease-out forwards;
  opacity: 0;
}
</style>
  