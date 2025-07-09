<template>
  <BaseCard pageTitle="Connexion réussie" class="bg-secondary">
    <h1 class="text-center text-2xl font-bold mb-4">Vous êtes connecté</h1>    
   <footer class="text-center text-sm text-text/60 space-y-1">
        <NuxtLink to="/" class="text-tertiary underline">Retour à la page de Connexion</NuxtLink>
    </footer>
  </BaseCard>
</template>

<script setup lang="ts">
import BaseCard from '../components/utils/BaseCard.vue';
</script>