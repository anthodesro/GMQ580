<script setup lang="ts">
definePageMeta({
  layout: "blank",
});
</script>
<template>
    <div class="d-flex justify-center align-center text-center h-100">
        <div>
            <img src="/images/backgrounds/errorimg.svg" width="500" alt="404" />
            <h1 class="text-h1 pt-3">Vous n'avez pas les droits d'accès !</h1>
            <h4 class="text-h4 my-8">Contactez votre administrateur si vous pensez qu'il s'agit d'une erreur.</h4>
            <v-btn rounded="pill" color="primary" class="mb-4" to="/">Retour</v-btn>
        </div>
    </div>
</template>
