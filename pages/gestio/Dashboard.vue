<script setup>
import { useRouter } from 'vue-router';
import { onMounted } from 'vue';

const router = useRouter();

onMounted(() => {
  // Vérifie d'abord dans localStorage, sinon prend la valeur de sessionStorage
  const userRole = localStorage.getItem("role") || sessionStorage.getItem("role");

  // Vérifie le rôle et redirige en fonction
  if (userRole === 'gestio') {
    router.push('/gestio/dashboard');
  } else if (userRole === 'admin') {
    router.push('/admin/dashboard');
  } else {
    router.push('/dashboard/index'); // Redirige vers la page d'accueil si aucun rôle spécifique
  }
});
</script>

<template>
  <div>
    <h5 class="text-h5 mb-1 font-weight-semibold">Console Gestionnaire</h5>
  </div>
</template>
