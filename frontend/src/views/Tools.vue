<!-- src/pages/Tools.vue -->
<template>
  <div class="max-w-6xl mx-auto" style="background-color: lightblue;">
    <Menu />
    

    <!-- Main Crawler Card -->
    <div class="glass rounded-3xl p-8 shadow-2xl mb-12">
      <div class="flex items-center space-x-4 mb-8" style="justify-content: center;">
        <div class="relative">
          <div class="w-12 h-12 bg-gradient-to-br from-purple-500 to-purple-600 rounded-2xl flex items-center justify-center shadow-lg">
            <svg width="24" height="24" class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9v-9m0-9v9" />
            </svg>
          </div>
          <div class="absolute -inset-2 bg-gradient-to-r from-purple-500/20 to-purple-600/20 rounded-2xl blur opacity-50"></div>
        </div>
        <h2 class="text-3xl font-bold text-gray-800" >Web Crawler</h2>
      </div>
      <TaskMonitor />
    </div>

    <!-- Statistics and Progress Section -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-12 custom-container">
      <CrawlStats />
      <TaskProgress />
    </div>

    <!-- Quick Stats -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-8 custom-container">
      <div class="glass rounded-3xl p-8 text-center group hover:scale-105 transition-all duration-500 shadow-xl hover:shadow-2xl">
        <div class="relative mb-6">
          <div class="w-16 h-16 mx-auto bg-gradient-to-br from-blue-500 to-blue-600 rounded-2xl flex items-center justify-center shadow-lg group-hover:shadow-xl transition-all duration-300">
            <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
          </div>
          <div class="absolute -inset-2 bg-gradient-to-r from-blue-500/20 to-blue-600/20 rounded-2xl blur opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
        </div>
        <div class="text-4xl font-bold text-blue-600 mb-3">Active</div>
        <p class="text-gray-600 font-medium">Tasks Running</p>
      </div>
      
      <div class="glass rounded-3xl p-8 text-center group hover:scale-105 transition-all duration-500 shadow-xl hover:shadow-2xl">
        <div class="relative mb-6">
          <div class="w-16 h-16 mx-auto bg-gradient-to-br from-green-500 to-green-600 rounded-2xl flex items-center justify-center shadow-lg group-hover:shadow-xl transition-all duration-300">
            <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <div class="absolute -inset-2 bg-gradient-to-r from-green-500/20 to-green-600/20 rounded-2xl blur opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
        </div>
        <div class="text-4xl font-bold text-green-600 mb-3">Complete</div>
        <p class="text-gray-600 font-medium">Tasks Finished</p>
      </div>
      
      <div class="glass rounded-3xl p-8 text-center group hover:scale-105 transition-all duration-500 shadow-xl hover:shadow-2xl">
        <div class="relative mb-6">
          <div class="w-16 h-16 mx-auto bg-gradient-to-br from-yellow-500 to-yellow-600 rounded-2xl flex items-center justify-center shadow-lg group-hover:shadow-xl transition-all duration-300">
            <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <div class="absolute -inset-2 bg-gradient-to-r from-yellow-500/20 to-yellow-600/20 rounded-2xl blur opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
        </div>
        <div class="text-4xl font-bold text-yellow-600 mb-3">Pending</div>
        <p class="text-gray-600 font-medium">Tasks Waiting</p>
      </div>
      
      <div class="glass rounded-3xl p-8 text-center group hover:scale-105 transition-all duration-500 shadow-xl hover:shadow-2xl">
        <div class="relative mb-6">
          <div class="w-16 h-16 mx-auto bg-gradient-to-br from-red-500 to-red-600 rounded-2xl flex items-center justify-center shadow-lg group-hover:shadow-xl transition-all duration-300">
            <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <div class="absolute -inset-2 bg-gradient-to-r from-red-500/20 to-red-600/20 rounded-2xl blur opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
        </div>
        <div class="text-4xl font-bold text-red-600 mb-3">Failed</div>
        <p class="text-gray-600 font-medium">Tasks Error</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import TaskMonitor from "@/components/TaskMonitor.vue"
import Menu from '@/components/Menu.vue'
import CrawlStats from '@/components/CrawlStats.vue'
import TaskProgress from '@/components/TaskProgress.vue'
</script>
  