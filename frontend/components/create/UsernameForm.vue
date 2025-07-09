<template>
    <div class="space-y-4">
      <FormKit
        type="form"
        :onSubmit="handleSubmit"
        :actions="false"
        class="space-y-4"
      >
        <FormKit
          type="text"
          v-model="currentUsername"
          name="username"
          label="Nom d’utilisateur"
          validation="required"
          input-class="border border-muted p-3 rounded-lg w-full mb-4"
          label-class="block mb-1 text-text"
        />
        <FormKit
          type="submit"
          label="Valider"
          input-class="bg-accent text-text font-semibold mt-2 p-3 rounded-full w-full hover:bg-accent/90 transition"
        />
      </FormKit>
    </div>
  </template>
  
  <script setup lang="ts">
  import { ref } from 'vue'
  
  const emit = defineEmits<{ (e: 'create:qrcode', username: string): void }>()
  
  const currentUsername = ref('')
  
  function handleSubmit() {
    emit('create:qrcode', currentUsername.value)
  }
  </script>
  