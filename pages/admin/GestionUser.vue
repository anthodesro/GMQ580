<script setup lang="ts">
import { useRouter } from 'vue-router';
import { onMounted } from 'vue';

const router = useRouter();

onMounted(() => {
  // Vérifie d'abord dans localStorage, sinon prend la valeur de sessionStorage
  const userRole = localStorage.getItem("role") || sessionStorage.getItem("role");

  // Vérifie le rôle et redirige en fonction
  if (userRole === 'admin') {
    router.push('/admin/dashboard');
  } else {
    router.push('/dashboard/index'); // Redirige vers la page d'accueil si aucun rôle spécifique
  }
});
</script>

<template>
  <v-row>
    <v-col cols="12" sm="12" lg="8">
      <ProfitExpanse />
    </v-col>
    <v-col cols="12" sm="12" lg="4">
      <div class="mb-6">
        <TrafficDistribution />
      </div>
      <div>
        <ProductSales />
      </div>
    </v-col>
    <v-col cols="12" sm="12" lg="4">
      <UpcommingSchedule />
    </v-col>
    <v-col cols="12" sm="12" lg="8">
      <TopPayingClients />
    </v-col>
    <v-col cols="12" sm="12" lg="12">
      <ProductCards />
    </v-col>
    <v-col class="text-center mt-2 justify-space-between d-flex">
      <p class="text-muted">
        Destributed by
        <a
          flat
          variant="text"
          href="https://www.themewagon.com/"
          target="_blank"
          class="pl-1 text-primary"
          >ThemeWagon</a
        >
      </p>
      <p class="text-muted">
        Design and Developed by
        <a
          flat
          variant="text"
          href="https://www.wrappixel.com/"
          target="_blank"
          class="pl-1 text-primary"
          >wrappixel.com</a
        >
      </p>
    </v-col>
  </v-row>
</template>
