// nuxt.config.ts
import { defineNuxtConfig } from 'nuxt/config'

export default defineNuxtConfig({
  compatibilityDate: '2025-05-15',
  devtools: { enabled: true },

  css: ['~/assets/css/tailwind.css'],

  modules: [
    '@nuxtjs/tailwindcss',
    '@formkit/nuxt',
    '@pinia/nuxt'
  ],

})
