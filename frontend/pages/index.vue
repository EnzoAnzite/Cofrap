<template>
  <BaseCard pageTitle="Connexion Sécurisée" class="bg-secondary">
    <!-- Étape 1 : username + password -->
    <div v-if="!step2" class="space-y-4">
      <FormKit
        type="form"
        :onSubmit="handleCredentials"
        :actions="false"
        class="space-y-4"
      >
        <FormKit
          type="text"
          v-model="credentials.username"
          name="username"
          label="Nom d’utilisateur"
          validation="required"
          input-class="border border-muted p-3 rounded-lg w-full"
          label-class="block mb-1 text-text mt-4"
        />
        <FormKit
          type="password"
          v-model="credentials.password"
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
    </div>

    <!-- Étape 2 : code TOTP -->
    <div v-else class="space-y-4">
      <FormKit
        type="form"
        :onSubmit="handle2FA"
        :actions="false"
        class="space-y-4"
      >
        <FormKit
          type="text"
          v-model="twoFACode"
          name="twofa"
          label="Code 2FA"
          help="Entrez le code à 6 chiffres généré par votre application d’authentification."
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
    </div>

    <!-- Footers -->
    <footer v-if="!step2" class="text-center text-sm text-text/60 space-y-1">
      <p>
        Mot de passe oublié ?
        <NuxtLink to="/expired" class="text-tertiary underline">Réinitialiser</NuxtLink>
      </p>
      <p>
        Pas encore de compte ?
        <NuxtLink to="/create" class="text-tertiary underline">Créer un compte</NuxtLink>
      </p>
    </footer>
    <footer v-else class="text-center text-sm space-y-1">
      <button class="text-tertiary underline" @click="reset()">Annuler</button>
    </footer>
  </BaseCard>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import BaseCard from '../components/utils/BaseCard.vue'

const step2 = ref(false)

const credentials = ref<{ username: string; password: string }>({
  username: '',
  password: ''
})

const twoFACode = ref('')

const router = useRouter()

async function handleCredentials() {
  try {
    await axios.post('http://127.0.0.1:8000/login', {
      username: credentials.value.username,
      password: credentials.value.password,
      totp_code: '000000'
    })
  } catch (err: any) {
    const detail = err.response?.data?.detail
    if (detail === 'Code TOTP invalide') {
      step2.value = true
      return
    }
    alert(detail || 'Identifiants invalides')
  }
}


async function handle2FA() {
  try {
    const res = await axios.post('http://127.0.0.1:8000/login', {
      username: credentials.value.username,
      password: credentials.value.password,
      totp_code: twoFACode.value
    })
    localStorage.setItem('access_token', res.data.access_token)
    router.push('/isConnected')
  } catch (err: any) {
    alert(err.response?.data?.detail || 'Code 2FA invalide')
    reset()
  }
}

function reset() {
  credentials.value = { username: '', password: '' }
  twoFACode.value = ''
  step2.value = false
}
</script>
