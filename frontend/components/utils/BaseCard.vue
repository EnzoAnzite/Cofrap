<template>
  <div class="min-h-screen flex items-center justify-center bg-secondary px-4">
    <div class="w-full max-w-md bg-white rounded-2xl shadow-lg p-8 space-y-6">
      <header class="text-center space-y-2">
         <div class="rounded-full bg-primary px-4 py-1 flex items-center w-max mx-auto border border-tertiary">
            <ShieldCheckIcon class="w-6 h-6 mr-2 text-tertiary" />
            <h1 class="text-tertiary text-2xl font-bold ">COFRAP</h1>
          </div>
        <p class="text-xl font-bold">{{props.pageTitle}}</p>
      </header>
          <slot />
    </div>
  </div>
</template>


<script setup lang="ts">
  import { ShieldCheckIcon } from '@heroicons/vue/24/solid'
    const props = defineProps<{
        pageTitle : string;
        class?: string;
    }>();
</script>