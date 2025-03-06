<script setup lang="ts">
import { ref, onMounted } from 'vue';
import axios, { AxiosError } from 'axios'; // Importation du type AxiosError
import UiChildCard from '@/components/shared/UiChildCard.vue';
import { EditIcon, TrashIcon } from 'vue-tabler-icons'; // Importation des icônes

import { useRouter } from 'vue-router';

const router = useRouter();

definePageMeta({
  middleware: ['role']
});

// Liste des utilisateurs et autres variables
const users = ref([]); // Liste des utilisateurs
const headers = ref([
    { title: "Courriel", key: "email", align: "start", sortable: true },
    { title: "Rôle", key: "role", align: "start", sortable: true },
    { title: "Action", key: "action", align: "center", sortable: false } // Nouvelle colonne Action
]);

const sortBy = ref([{ key: "email", order: "asc" }]); // Tri initial sur "Email"
const searchQuery = ref(""); // Variable pour le champ de recherche

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
    } catch (error: unknown) {  // TypeScript : Déclaration du type 'unknown' pour l'erreur
        if (error instanceof AxiosError) {
            console.error("Erreur lors de la récupération des utilisateurs :", error.response ? error.response.data : error.message);
        } else {
            console.error("Erreur inconnue :", error);
        }
    }
};

// Récupérer les utilisateurs à l'initialisation du composant
onMounted(fetchUsers);

// Fonction pour obtenir le nom du rôle à partir de la valeur brute
const getRoleName = (role: string) => {
    switch(role) {
        case 'admin': return 'Administrateur';
        case 'gestio': return 'Gestionnaire';
        case 'user': return 'Utilisateur';
        default: return 'Non spécifié';
    }
};

// Fonction pour gérer la couleur en fonction du rôle
const getRoleColor = (role: string) => {
    switch(role) {
        case 'admin': return '#FF3D00'; // Rouge
        case 'gestio': return '#2979FF'; // Bleu
        case 'user': return '#00C853'; // Vert
        default: return '#BDBDBD'; // Gris
    }
};

// Fonction pour ajouter un utilisateur (placeholder)
const addUser = () => {
    console.log("Ajouter un utilisateur");
};

// Fonction pour supprimer un utilisateur
const deleteUser = (userId: string) => {
    console.log("Supprimer l'utilisateur avec l'ID :", userId);
};

// Fonction pour modifier un utilisateur
const editUser = (userId: string) => {
    console.log("Modifier l'utilisateur avec l'ID :", userId);
};
</script>

<template>
    <v-row class="maxWidth">
        <v-col cols="12">
            <UiChildCard title="Registre des utilisateurs">
                <v-row class="mb-4">
                    <!-- Champ de recherche -->
                    <v-col cols="12" sm="6">
                        <v-text-field
                            v-model="searchQuery"
                            label="Rechercher un utilisateur"
                            clearable
                            prepend-inner-icon="mdi-magnify"
                        />
                    </v-col>

                    <!-- Bouton Ajouter avec un margin-top ajusté -->
                    <v-col cols="12" sm="6" class="d-flex justify-start">
                        <v-btn
                            color="primary"
                            @click="addUser"
                            style="margin-top: 6px;"
                        >
                            Ajouter
                        </v-btn>
                    </v-col>
                </v-row>

                <!-- Table des utilisateurs -->
                <v-data-table
                    v-model:sort-by="sortBy"
                    :headers="headers"
                    :items="users"
                    item-key="id"
                    class="custom-table"
                    :search="searchQuery"
                >
                    <!-- Slot pour afficher le rôle avec couleur -->
                    <template v-slot:item.role="{ item }">
                        <v-chip :color="getRoleColor(item.role)" class="ma-2">
                            {{ getRoleName(item.role) }}
                        </v-chip>
                    </template>

                    <!-- Slot pour afficher les actions -->
                    <template v-slot:item.action="{ item }">
                        <div class="d-flex justify-center">
                            <EditIcon 
                                class="mr-2" 
                                style="cursor: pointer;" 
                                @click="editUser(item.id)" 
                                :color="'#0085db'"
                            />
                            <TrashIcon 
                                style="cursor: pointer;" 
                                @click="deleteUser(item.id)" 
                                :color="'#fb977d'"
                            />
                        </div>
                    </template>
                </v-data-table>
            </UiChildCard>
        </v-col>
    </v-row>
</template>

<style scoped>
/* Définir la taille des icônes en utilisant la classe spécifique */
.icon {
    width: 20px;
    height: 20px;
}
</style>
