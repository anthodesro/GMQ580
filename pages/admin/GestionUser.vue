<script setup lang="ts">
import { useRouter } from 'vue-router';
import { onMounted } from 'vue';

const router = useRouter();
</script>

<template>
  <v-row>
    <v-col class="authentication">
            <v-container fluid class="pa-3">
                <v-row class="h-100vh d-flex justify-center align-center">
                    <v-col cols="12" class="d-flex align-center">
                        <div class="boxed-auth-wrap">
                            <v-card rounded="x1" elevation="10" class="px-sm-1 px-0  mx-auto index-2" max-width="450">
                                <v-card-item class="pa-sm-8">
                                    <div class="d-flex justify-center mb-5">
                                        <LayoutFullLogoDark />
                                    </div>
                                    <div class="d-flex align-center text-center mb-6">
                                        <div class="text-h6 w-100 px-5 font-weight-regular auth-divider position-relative">
                                            <span
                                                class="bg-surface px-5 py-3 position-relative text-subtitle-1 text-grey100">Your
                                                Social Campaigns</span>
                                        </div>
                                    </div>
                                    <AuthRegisterForm />
                                    <h6 class="text-subtitle-1  text-grey100 d-flex justify-center align-center mt-3">
                                        Already have an Account?
                                        <v-btn variant="plain" to="/auth/login"
                                            class="text-primary text-body-1 opacity-1 font-weight-medium pl-2">Sign In</v-btn>
                                    </h6>
                                </v-card-item>
                            </v-card>
                        </div>
                    </v-col>
                </v-row>
            </v-container>
        </v-col>
  </v-row>
</template>
