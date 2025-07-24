<template>
  <span 
    class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
    :class="getStatusClasses(status)"
  >
    <svg height="24" width="24" class="w-2 h-2 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path v-if="status === 'PENDING'" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
      <path v-else-if="status === 'STARTED'" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
      <path v-else-if="status === 'SUCCESS'" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
      <path v-else-if="status === 'FAILURE'" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
      <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
    </svg>
    {{ status }}
  </span>
</template>

<script setup lang="ts">
interface Props {
  status: string;
}

defineProps<Props>();

const getStatusClasses = (status: string) => {
  switch (status) {
    case 'PENDING':
      return 'bg-yellow-100 text-yellow-800';
    case 'STARTED':
      return 'bg-blue-100 text-blue-800';
    case 'SUCCESS':
      return 'bg-green-100 text-green-800';
    case 'FAILURE':
      return 'bg-red-100 text-red-800';
    default:
      return 'bg-gray-100 text-gray-800';
  }
};
</script> 