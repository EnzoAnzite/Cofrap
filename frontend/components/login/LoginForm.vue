<template>
    <FormKit
      type="form"
      :onSubmit="submit"
      :actions="false"
      class="space-y-4"
    >
      <FormKit
        type="text"
        v-model="username"
        name="username"
        label="Nom d’utilisateur"
        validation="required"
        input-class="border border-muted p-3 rounded-lg w-full"
        label-class="block mb-1 text-text mt-4"
      />
      <FormKit
        type="password"
        v-model="password"
        name="password"
        label="Mot de passe"
        validation="required"
        input-class="border border-muted p-3 rounded-lg w-full mb-4"
        label-class="block mb-1 text-text mt-4"
      />
      <FormKit
        type="submit"
        label="Connexion"
        input-class="bg-accent text-text font-semibold mt-2 p-3 rounded-full w-full hover:bg-accent/90 transition"
      />
    </FormKit>
  </template>
  
  <script setup lang="ts">
  import { ref, defineEmits } from 'vue'
  
  const emit = defineEmits<{
    (e: 'step1', payload: { username: string; password: string }): void
  }>()
  
  const username = ref('')
  const password = ref('')
  
  function submit() {
    emit('step1', { username: username.value, password: password.value })
  }
  </script>
  