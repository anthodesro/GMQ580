<script setup lang="ts">
import { UserIcon, MailIcon, ListCheckIcon } from 'vue-tabler-icons';
import { useRouter } from "vue-router";

const router = useRouter();

const logout = () => {
  // Supprimer les données de l'utilisateur
  localStorage.removeItem("token");
  localStorage.removeItem("role");
  
  sessionStorage.removeItem("token");
  sessionStorage.removeItem("role");

  router.push("/auth/login"); // Rediriger vers la page de login après la déconnexion
};

</script>

<template>
    <v-menu :close-on-content-click="false">
        <template v-slot:activator="{ props }">
            <v-btn variant="text" v-bind="props" icon>
                <v-avatar size="35">
                    <img src="/images/profile/user-1.jpg" height="35" alt="user" />
                </v-avatar>
            </v-btn>
        </template>
        <v-sheet rounded="xl" width="200" elevation="10" class="mt-2">
            <v-list class="py-0" lines="one" density="compact">
                <v-list-item value="item1" color="primary">
                    <template v-slot:prepend>
                        <UserIcon stroke-width="1.5" size="20"/>
                    </template>
                    <v-list-item-title class="pl-4 text-body-1">Mon Profile</v-list-item-title>
                </v-list-item>
                <v-list-item value="item2" color="primary"> 
                    <template v-slot:prepend>
                        <ListCheckIcon stroke-width="1.5" size="20"/>
                    </template>
                    <v-list-item-title class="pl-4 text-body-1">My Task</v-list-item-title>
                </v-list-item>
            </v-list>
            <div class="pt-4 pb-4 px-5 text-center">
                <v-btn 
                    color="primary" 
                    variant="outlined" 
                    class="rounded-pill" 
                    block 
                    @click="logout"
                >
                    Déconnexion
                </v-btn>
            </div>
        </v-sheet>
    </v-menu>
</template>
