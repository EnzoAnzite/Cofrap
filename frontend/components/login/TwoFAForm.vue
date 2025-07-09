<template>
    <FormKit
      type="form"
      :onSubmit="submit"
      :actions="false"
      class="space-y-4"
    >
      <FormKit
        type="text"
        v-model="code"
        name="twofa"
        label="Code 2FA"
        help="Entrez votre code à 6 chiffres"
        validation="required pattern:/^[0-9]{6}$/"
        input-class="border border-muted p-3 rounded-lg w-full mb-4"
        label-class="block mb-1 text-text"
        help-class="text-sm text-text/70"
      />
      <FormKit
        type="submit"
        label="Valider"
        input-class="bg-accent text-text font-semibold mt-2 p-3 rounded-full w-full hover:bg-accent/90 transition"
      />
    </FormKit>
  </template>
  
  <script setup lang="ts">
  import { ref, defineEmits } from 'vue'
  
  const emit = defineEmits<{
    (e: 'step2', payload: { totp_code: string }): void
  }>()
  
  const code = ref('')
  
  function submit() {
    emit('step2', { totp_code: code.value })
  }
  </script>
  