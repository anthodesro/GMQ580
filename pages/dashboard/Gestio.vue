<script setup>
import { useRouter } from 'vue-router';
import { onMounted } from 'vue';

definePageMeta({
  middleware: 'role', // Utilise le middleware 'role' pour contrôler l'accès
});

</script>

<template>
  <v-app>
    <h1 class="text-h1 pt-3">Tableau de bord (gestio)</h1>
  </v-app>
</template>
