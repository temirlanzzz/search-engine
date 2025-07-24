<template>
  <div class="glass rounded-3xl p-8 shadow-xl custom-container">
    <div class="flex items-center mb-6" style="justify-content: center;">
      <h3 class="text-2xl font-bold text-gray-800">Task Progress</h3>
      <button 
        @click="refreshTasks"
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

    <div v-else-if="activeTasks.length > 0" class="space-y-4">
      <div 
        v-for="task in activeTasks" 
        :key="task.id"
        class="bg-white/50 rounded-2xl p-6 border border-white/20"
      >
        <div class="flex items-center justify-between mb-4">
          <div class="flex items-center space-x-3">
            <div class="w-3 h-3 rounded-full" :class="getStatusColor(task.status)"></div>
            <h4 class="text-lg font-semibold text-gray-800">{{ task.type }}</h4>
          </div>
          <span class="text-sm text-gray-500">{{ formatTime(task.created_at) }}</span>
        </div>
        
        <div class="mb-4">
          <div class="flex justify-between text-sm text-gray-600 mb-2">
            <span>Progress</span>
            <span>{{ getProgressText(task) }}</span>
          </div>
          <div class="w-full bg-gray-200 rounded-full h-2">
            <div 
              class="h-2 rounded-full transition-all duration-500"
              :class="getProgressBarColor(task.status)"
              :style="{ width: getProgressWidth(task) }"
            ></div>
          </div>
        </div>
        
        <div v-if="task.result" class="text-sm text-gray-600">
          <div v-if="task.result.terms_indexed" class="mb-2">
            <span class="font-medium">Terms indexed:</span> {{ task.result.terms_indexed }}
          </div>
          <div v-if="task.result.stats" class="mb-2">
            <span class="font-medium">Documents:</span> {{ task.result.stats.total_documents }}
          </div>
        </div>
        
        <div v-if="task.error" class="text-sm text-red-600 bg-red-50 p-3 rounded-lg">
          {{ task.error }}
        </div>
      </div>
    </div>

    <!-- No Active Tasks -->
    <div v-else class="text-center py-8" style="display: flex; justify-content: center;">
        <svg class="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
        </svg>
      <p class="text-gray-500">No active tasks. Start crawling or rebuilding to see progress.</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue';
import axios from 'axios';

interface TaskResult {
  status: string;
  terms_indexed?: number;
  stats?: {
    total_documents: number;
  };
  error?: string;
}

interface Task {
  id: string;
  type: string;
  status: string;
  created_at: string;
  result?: TaskResult;
  error?: string;
}

const activeTasks = ref<Task[]>([]);
const loading = ref(false);
const refreshInterval = ref<number | null>(null);

const fetchTasks = async () => {
  loading.value = true;
  
  try {
    // In a real implementation, you would fetch active tasks from the backend
    // For now, we'll simulate with local storage or a simple API
    const response = await axios.get('/api/tasks/active');
    activeTasks.value = response.data.tasks || [];
  } catch (err) {
    console.error('Error fetching tasks:', err);
    // For demo purposes, show some mock tasks
    activeTasks.value = [];
  } finally {
    loading.value = false;
  }
};

const refreshTasks = () => {
  fetchTasks();
};

const getStatusColor = (status: string) => {
  switch (status) {
    case 'PENDING': return 'bg-yellow-500';
    case 'PROGRESS': return 'bg-blue-500';
    case 'SUCCESS': return 'bg-green-500';
    case 'FAILURE': return 'bg-red-500';
    default: return 'bg-gray-500';
  }
};

const getProgressBarColor = (status: string) => {
  switch (status) {
    case 'PENDING': return 'bg-yellow-500';
    case 'PROGRESS': return 'bg-blue-500';
    case 'SUCCESS': return 'bg-green-500';
    case 'FAILURE': return 'bg-red-500';
    default: return 'bg-gray-500';
  }
};

const getProgressWidth = (task: Task) => {
  switch (task.status) {
    case 'PENDING': return '10%';
    case 'PROGRESS': return '50%';
    case 'SUCCESS': return '100%';
    case 'FAILURE': return '100%';
    default: return '0%';
  }
};

const getProgressText = (task: Task) => {
  switch (task.status) {
    case 'PENDING': return 'Queued';
    case 'PROGRESS': return 'In Progress';
    case 'SUCCESS': return 'Completed';
    case 'FAILURE': return 'Failed';
    default: return 'Unknown';
  }
};

const formatTime = (timeString: string) => {
  const date = new Date(timeString);
  return date.toLocaleTimeString();
};

onMounted(() => {
  fetchTasks();
  
  // Refresh every 5 seconds
  refreshInterval.value = setInterval(() => {
    fetchTasks();
  }, 5000);
});

onUnmounted(() => {
  if (refreshInterval.value) {
    clearInterval(refreshInterval.value);
  }
});
</script> 