<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import UiChildCard from '@/components/shared/UiChildCard.vue';
import { EditIcon, TrashIcon } from 'vue-tabler-icons'; // Importation des icônes

// Liste des utilisateurs et autres variables
const users = ref([]); // Liste des utilisateurs
const headers = ref([
    { title: "Nom utilisateur", key: "username", align: "start", sortable: true },
    { title: "Rôle", key: "role", align: "start", sortable: true },
    { title: "Action", key: "action", align: "center", sortable: false } // Nouvelle colonne Action
]);

const sortBy = ref([{ key: "username", order: "asc" }]); // Tri initial sur "Username"
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
    } catch (error) {
        console.error("Erreur lors de la récupération des utilisateurs :", error.response ? error.response.data : error.message);
    }
};

// Récupérer les utilisateurs à l'initialisation du composant
onMounted(fetchUsers);

// Fonction pour obtenir le nom du rôle à partir de la valeur brute
const getRoleName = (role) => {
    switch(role) {
        case 'admin': return 'Administrateur';
        case 'gestio': return 'Gestionnaire';
        case 'user': return 'Utilisateur';
        default: return 'Non spécifié';
    }
};

// Fonction pour gérer la couleur en fonction du rôle
const getRoleColor = (role) => {
    switch(role) {
        case 'admin': return '#FF3D00'; // Rouge
        case 'gestio': return '#2979FF'; // Bleu
        case 'user': return '#00C853'; // Vert
        default: return '#BDBDBD'; // Gris
    }
};

// Fonctions placeholders pour supprimer et modifier un utilisateur
const deleteUser = (userId) => {
    // Logic for deleting user
    console.log("Delete user with ID:", userId);
};

const editUser = (userId) => {
    // Logic for editing user
    console.log("Edit user with ID:", userId);
};
</script>

<template>
    <v-row class="maxWidth">
        <v-col cols="12" sm="12">
            <UiChildCard title="Registre des utilisateurs">
                <v-row class="mb-4">
                    <!-- Champ de recherche et bouton Ajouter dans le même row -->
                    <v-col cols="12" sm="6" class="d-flex align-center"> <!-- Champ de recherche centré verticalement -->
                        <v-text-field
                            v-model="searchQuery"
                            label="Rechercher un utilisateur"
                            clearable
                            prepend-inner-icon="mdi-magnify"
                        />
                    </v-col>

                    <v-col cols="12" sm="6" class="d-flex align-center"> <!-- Le bouton est aligné à droite et centré verticalement -->
                        <v-btn color="primary" @click="addUser">
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
                    :sort-by="['Nom utilisateur']"
                    :search="searchQuery" 
                >
                    <template v-slot:default="{ item }">
                        <!-- Affichage du rôle -->
                        <v-chip :color="getRoleColor(item.role)" class="ma-2">{{ getRoleName(item.role) }}</v-chip>

                        <!-- Actions de l'utilisateur -->
                        <div class="d-flex justify-center">
                            <EditIcon 
                                class="mr-2" 
                                style="cursor: pointer;" 
                                @click="editUser(item.id)" 
                                color="#0085db"
                            />
                            <TrashIcon 
                                style="cursor: pointer;" 
                                @click="deleteUser(item.id)" 
                                color="#fb977d"
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
