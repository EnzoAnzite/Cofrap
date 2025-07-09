<template>
  <div class="space-y-6 text-center">
    <button
      @click="showPwd = !showPwd"
      class="bg-accent text-text font-semibold mt-2 p-3 rounded-full w-full hover:bg-accent/90 transition"
    >
      {{ showPwd ? 'Masquer le mot de passe' : 'Afficher le mot de passe' }}
    </button>
    <img
      v-if="showPwd"
      :src="qrPassword"
      alt="QR Code mot de passe"
      class="mx-auto max-w-full h-auto"
    />

    <button
      @click="show2FA = !show2FA"
      class="bg-accent text-text font-semibold mt-2 p-3 rounded-full w-full hover:bg-accent/90 transition"
    >
      {{ show2FA ? 'Masquer le secret 2FA' : 'Afficher le secret 2FA' }}
    </button>
    <img
      v-if="show2FA"
      :src="qr2Fa"
      alt="QR Code secret 2FA"
      class="mx-auto max-w-full h-auto"
    />
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{
  qrPassword: string
  qr2Fa:      string
}>()

import { ref } from 'vue'

const showPwd = ref(false)
const show2FA = ref(false)
</script>
