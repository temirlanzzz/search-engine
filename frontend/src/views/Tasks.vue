<!-- src/pages/Tasks.vue -->
<template>
  <div class="max-w-6xl mx-auto">
    <Menu />
    
    <!-- Page Header -->
    <div class="text-center mb-16">
      <div class="relative inline-block mb-6">
        <h1 class="text-5xl md:text-6xl font-bold mb-6 bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-600 bg-clip-text text-transparent">
          Task Management
        </h1>
        <div class="absolute -inset-4 bg-gradient-to-r from-blue-600/20 via-indigo-600/20 to-purple-600/20 rounded-full blur-3xl opacity-50"></div>
      </div>
      <p class="text-xl md:text-2xl text-gray-600 max-w-3xl mx-auto leading-relaxed font-light">
        Monitor and manage background crawling and indexing tasks with real-time updates
      </p>
    </div>

    <!-- Main Content -->
    <div class="glass rounded-3xl p-8 shadow-2xl">
      <TaskMonitor />
    </div>
  </div>
</template>
  
<script setup lang="ts">
import TaskMonitor from "@/components/TaskMonitor.vue"
import Menu from '@/components/Menu.vue'
</script>
  