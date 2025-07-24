<template>
  <div class="relative">
    <form @submit.prevent="onSubmit" class="relative">
      <div class="relative group" style="display: flex; justify-content: center;">

        <!-- Search Input -->
        <input
          v-model="query"
          type="text"
          placeholder="Search for anything..."
          class="w-full pl-16 pr-24 py-5 text-lg glass rounded-3xl shadow-2xl focus:outline-none focus:ring-4 focus:ring-blue-500/30 focus:border-blue-500/50 transition-all duration-500 placeholder-gray-400 group-hover:shadow-3xl group-focus-within:shadow-3xl group-focus-within:scale-[1.02]"
          @keydown.ctrl.k.prevent="focusInput"
          @input="handleInput"
        />

        <!-- Search Button -->
        <button 
          type="submit"
          class="custom-button"
          :disabled="!query.trim()"
        >
          <div class="flex items-center space-x-2">
            <span class="font-semibold">Search</span>
            <svg width="24" height="24" class="w-5 h-5 text-gray-400 group-focus-within:text-blue-500 transition-colors duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
          </div>
        </button>
      </div>
    </form>

    <!-- Keyboard Shortcut Hint -->
    <div class="absolute -bottom-10 left-1/2 transform -translate-x-1/2 text-xs text-gray-400 flex items-center space-x-1">
      <span>Press</span>
      <kbd class="px-2 py-1 bg-white/80 backdrop-blur-sm rounded-lg text-gray-600 shadow-sm border border-white/20">Ctrl</kbd>
      <span>+</span>
      <kbd class="px-2 py-1 bg-white/80 backdrop-blur-sm rounded-lg text-gray-600 shadow-sm border border-white/20">K</kbd>
      <span>to focus</span>
    </div>

    <!-- Search Suggestions (if any) -->
    <div v-if="showSuggestions" class="absolute top-full left-0 right-0 mt-4 glass rounded-2xl shadow-2xl z-20 border border-white/20">
      <div class="py-3">
        <!-- Loading indicator -->
        <div v-if="loadingSuggestions" class="px-6 py-4 flex items-center space-x-3">
          <div class="w-4 h-4 border-2 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
          <span class="text-gray-500">Loading suggestions...</span>
        </div>
        
        <!-- Suggestions list -->
        <div v-else-if="suggestions.length">
          <div 
            v-for="(suggestion, index) in suggestions" 
            :key="suggestion"
            @click="selectSuggestion(suggestion)"
            class="px-6 py-4 hover:bg-white/30 cursor-pointer transition-all duration-200 flex items-center space-x-3 group"
            :class="{ 'bg-white/20': index === selectedSuggestion }"
          >
            <div class="relative">
              <svg height="24" width="24" class="w-4 h-4 text-gray-400 group-hover:text-blue-500 transition-colors duration-200" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
              <div class="absolute -inset-1 bg-blue-500 rounded-full opacity-0 group-hover:opacity-20 blur transition-opacity duration-200"></div>
            </div>
            <span class="text-gray-700 group-hover:text-gray-900 transition-colors duration-200">{{ suggestion }}</span>
          </div>
        </div>
        
        <!-- No suggestions -->
        <div v-else class="px-6 py-4 text-gray-500">
          No suggestions found
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue';
import axios from 'axios';

const emit = defineEmits(['search']);
const query = ref('');
const suggestions = ref<string[]>([]);
const showSuggestions = ref(false);
const selectedSuggestion = ref(-1);
const loadingSuggestions = ref(false);

const focusInput = () => {
  const input = document.querySelector('input[type="text"]') as HTMLInputElement;
  if (input) {
    input.focus();
  }
};

const handleInput = async () => {
  if (query.value.trim() && query.value.length >= 2) {
    loadingSuggestions.value = true;
    try {
      const response = await axios.get(`/api/suggestions?q=${encodeURIComponent(query.value)}`);
      suggestions.value = response.data.suggestions || [];
      showSuggestions.value = suggestions.value.length > 0;
      selectedSuggestion.value = -1;
    } catch (error) {
      console.error('Error fetching suggestions:', error);
      suggestions.value = [];
      showSuggestions.value = false;
    } finally {
      loadingSuggestions.value = false;
    }
  } else {
    showSuggestions.value = false;
    suggestions.value = [];
  }
};

const selectSuggestion = (suggestion: string) => {
  query.value = suggestion;
  showSuggestions.value = false;
  onSubmit();
};

const onSubmit = () => {
  if (query.value.trim()) {
    emit('search', query.value);
    showSuggestions.value = false;
  }
};

// Keyboard event listeners
const handleKeydown = (event: KeyboardEvent) => {
  if (event.ctrlKey && event.key === 'k') {
    event.preventDefault();
    focusInput();
  }
  
  // Handle arrow keys for suggestions
  if (showSuggestions.value && suggestions.value.length > 0) {
    if (event.key === 'ArrowDown') {
      event.preventDefault();
      selectedSuggestion.value = Math.min(selectedSuggestion.value + 1, suggestions.value.length - 1);
    } else if (event.key === 'ArrowUp') {
      event.preventDefault();
      selectedSuggestion.value = Math.max(selectedSuggestion.value - 1, -1);
    } else if (event.key === 'Enter' && selectedSuggestion.value >= 0) {
      event.preventDefault();
      selectSuggestion(suggestions.value[selectedSuggestion.value]);
    }
  }
};

onMounted(() => {
  document.addEventListener('keydown', handleKeydown);
});

onUnmounted(() => {
  document.removeEventListener('keydown', handleKeydown);
});
</script>

<style scoped>
button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: scale(1) !important;
}

kbd {
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
  font-size: 0.75rem;
}

/* Custom shadow for hover effects */
.shadow-3xl {
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
}
</style>
  