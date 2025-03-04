<script setup lang="ts">
import { ref, computed, shallowRef } from 'vue';
import sidebarItems from '@/components/Layout/Full/vertical-sidebar/sidebarItem';
// Icon Imports
import { Menu2Icon } from 'vue-tabler-icons';

const sDrawer = ref(true);

// Simuler le rôle de l'utilisateur connecté (à remplacer par l'authentification réelle)
const userRole = ref("admin"); // Exemple : 'admin', 'user', 'guest'

// Filtrer les items du menu en fonction du rôle de l'utilisateur
const sidebarMenu = computed(() => {
  return sidebarItems.filter(item => !item.roles || item.roles.includes(userRole.value));
});

</script>

<template>
    <v-navigation-drawer left v-model="sDrawer" app class="leftSidebar ml-sm-5 mt-sm-5 bg-containerBg" elevation="10"
        width="270">
        <div class="pa-5 pl-4 ">
            <LayoutFullLogoDark />
        </div>
        <perfect-scrollbar class="scrollnavbar bg-containerBg overflow-y-hidden">
            <v-list class="py-4 px-4 bg-containerBg">
                <template v-for="(item, i) in sidebarMenu">
                    <LayoutFullVerticalSidebarNavGroup :item="item" v-if="item.header" :key="item.title" />
                    <LayoutFullVerticalSidebarNavItem :item="item" v-else class="leftPadding" />
                </template>
            </v-list> 
        </perfect-scrollbar>
    </v-navigation-drawer>
    <div class="container verticalLayout">
        <div class="maxWidth">
            <v-app-bar elevation="0" height="70">
                <div class="d-flex align-center justify-space-between w-100">
                    <div>
                        <v-btn class="hidden-lg-and-up text-muted" @click="sDrawer = !sDrawer" icon
                            variant="flat" size="small">
                            <Menu2Icon size="20" stroke-width="1.5" />
                        </v-btn>
                        <!-- Notification -->
                        <LayoutFullVerticalHeaderNotificationDD />
                    </div>
                    <div>
                        <!-- User Profile -->
                        <LayoutFullVerticalHeaderProfileDD />
                    </div>
                </div>
            </v-app-bar>
        </div>
    </div>
</template>
