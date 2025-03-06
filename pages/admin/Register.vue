<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import UiChildCard from '@/components/shared/UiChildCard.vue';

// Liste des utilisateurs et autres variables
const users = ref([]); // Liste des utilisateurs
const headers = ref([
    { title: "Username", key: "username", align: "start", sortable: true },
    { title: "Role", key: "role", align: "start", sortable: true },
]);

const sortBy = ref([{ key: "username", order: "asc" }]); // Tri initial sur "Username"

// Fonction pour récupérer les utilisateurs depuis l'API Flask
const fetchUsers = async () => {
    try {
        const token = sessionStorage.getItem('token') || localStorage.getItem('token');
        const response = await axios.get('http://127.0.0.1:5000/api/users', {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        });
        users.value = response.data;
    } catch (error) {
        console.error("Erreur lors de la récupération des utilisateurs :", error.response ? error.response.data : error.message);
    }
};

// Récupérer les utilisateurs à l'initialisation du composant
onMounted(fetchUsers);

// Fonction pour gérer la couleur en fonction du rôle
const getRoleColor = (role) => {
    switch(role) {
        case 'admin': return 'red';
        case 'gestio': return 'blue';
        case 'user': return 'green';
        default: return 'grey';
    }
};
</script>

<template>
  <v-row class="maxWidth">
        <!-- Section de la Table des Utilisateurs -->
        <v-col cols="12" sm="12">
            <UiChildCard title="Table des utilisateurs">
                <v-data-table
                    v-model:sort-by="sortBy"
                    :headers="headers"
                    :items="users"
                    item-key="id"
                    class="custom-table"
                    :sort-by="['username']"
                >
                    <template v-slot:item.role="{ item }">
                        <v-chip :color="getRoleColor(item.role)" class="ma-2">{{ item.role }}</v-chip>
                    </template>
                </v-data-table>
            </UiChildCard>
        </v-col>

        <!-- Section pour l'authentification -->
        <v-col class="authentication">
            <v-container fluid class="pa-3">
                <v-row class="h-100vh d-flex justify-center align-center">
                    <v-col cols="12" class="d-flex align-center">
                        <div class="boxed-auth-wrap">
                            <v-card rounded="xl" elevation="10" class="px-sm-1 px-0  mx-auto index-2" max-width="450">
                                <v-card-item class="pa-sm-8">
                                    <div class="d-flex justify-center mb-5">
                                        <LayoutFullLogoDark />
                                    </div>
                                    <div class="d-flex align-center text-center mb-6">
                                        <div class="text-h6 w-100 px-5 font-weight-regular auth-divider position-relative">
                                            <span
                                                class="bg-surface px-5 py-3 position-relative text-subtitle-1 text-grey100">Gestionnaire des utilisateurs</span>
                                        </div>
                                    </div>
                                    <AuthRegisterForm />
                                </v-card-item>
                            </v-card>
                        </div>
                    </v-col>
                </v-row>
            </v-container>
        </v-col>
  </v-row>
</template>
