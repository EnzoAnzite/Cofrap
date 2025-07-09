<template>
  <BaseCard pageTitle="Créer un compte" class="bg-secondary">
    <UsernameForm
      v-if="state === State.Username"
      @create:qrcode="HandleUsernameSubmit"
    />
    <Spinner v-if="state === State.Loading" />

    <!-- Affichage des deux QR codes (mot de passe & TOTP) -->
    <RenderCodes
      v-if="state === State.QrCode"
      :qr-password="qrPassword"
      :qr2Fa="qr2FA"
    />

    <footer class="text-center text-sm text-text/60 space-y-1">
      <NuxtLink to="/" class="text-tertiary underline">
        Retour à la page de Connexion
      </NuxtLink>
    </footer>
  </BaseCard>
</template>

<script setup lang="ts">
import { ref, onMounted, watchEffect } from 'vue'
import axios from 'axios'

import BaseCard from '../components/utils/BaseCard.vue'
import UsernameForm from '../components/create/UsernameForm.vue'
import Spinner from '../components/create/Spinner.vue'
import RenderCodes from '../components/create/RenderCodes.vue'

const enum State {
  Username = 'username',
  Loading  = 'loading',
  QrCode   = 'qrcode'
}

const state      = ref(State.Username)
const qrPassword = ref<string>('')
const qr2FA      = ref<string>('')


async function HandleUsernameSubmit(username: string) {
  state.value = State.Loading

  try {
    const resp = await axios.post(
      'http://127.0.0.1:8000/signup',
      { username }
    )
    qrPassword.value = resp.data.password_qr_uri
    qr2FA.value       = resp.data.totp_qr_uri
    state.value       = State.QrCode

  } catch (err) {
    console.error('Erreur lors du signup :', err)
    state.value = State.Username
  }
}

watchEffect(() => {
  console.log('Current state:', state.value)
})

onMounted(() => {
  state.value = State.Username
})
</script>
