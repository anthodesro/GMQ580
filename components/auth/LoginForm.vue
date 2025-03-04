<script setup lang="ts">
import { ref } from "vue";
import axios from "axios";
import { useRouter } from "vue-router";
import { AxiosError } from "axios";

const router = useRouter();
const email = ref("");
const password = ref("");
const errorMessage = ref("");
const checkbox = ref(false);

// Validation du formulaire
const validateForm = (): boolean => {
  if (!email.value || !password.value) {
    errorMessage.value = "Les champs doivent être remplis.";
    return false;
  }
  return true;
};

// Fonction de connexion
const login = async () => {
  if (!validateForm()) return; // Validation du formulaire

  try {
    const response = await axios.post("http://127.0.0.1:5000/login", {
      email: email.value,
      password: password.value,
    });

    // Vérification de la présence du token et du rôle dans la réponse
    if (response.data && response.data.access_token && response.data.role) {
      // Déterminer si le stockage doit être persistant ou temporaire
      const storage = checkbox.value ? localStorage : sessionStorage;

      // Stocker le token et le rôle dans le bon stockage
      storage.setItem("token", response.data.access_token);
      storage.setItem("role", response.data.role);

      // Redirection vers la page d'accueil (peu importe le rôle)
      router.push('/');
    } else {
      errorMessage.value = "Une erreur est survenue lors de la connexion. Vérifiez vos identifiants.";
    }
  } catch (error: AxiosError | any) {
    // Gestion des erreurs de la requête
    errorMessage.value = error.response?.data?.message || "Identifiants incorrects.";
  }
};

</script>

<template>
  <div>
    <div class="d-flex align-center text-center mb-6">
      <div class="text-h6 w-100 px-5 font-weight-regular auth-divider position-relative">
        <span class="bg-surface px-5 py-3 position-relative text-subtitle-1 text-grey100">
          Gestion comptable
        </span>
      </div>
    </div>

    <div>
      <v-row class="mb-3">
        <v-col cols="12">
          <v-label class="font-weight-medium mb-1">Adresse courriel</v-label>
          <v-text-field
            v-model="email"
            variant="outlined"
            class="pwdInput"
            hide-details
            color="primary"
          ></v-text-field>
        </v-col>

        <v-col cols="12">
          <v-label class="font-weight-medium mb-1">Mot de passe</v-label>
          <v-text-field
            v-model="password"
            variant="outlined"
            class="border-borderColor"
            type="password"
            hide-details
            color="primary"
          ></v-text-field>
        </v-col>

        <v-col cols="12" class="py-0">
          <div class="d-flex flex-wrap align-center w-100">
            <v-checkbox v-model="checkbox" hide-details color="primary">
              <template v-slot:label>Mémoriser cet appareil</template>
            </v-checkbox>

            <div class="ml-sm-auto">
              <RouterLink
                to=""
                class="text-primary text-decoration-none text-body-1 opacity-1 font-weight-medium"
              >
                Mot de passe oublié ?
              </RouterLink>
            </div>
          </div>
        </v-col>

        <v-col cols="12">
          <v-btn
            size="large"
            rounded="pill"
            color="primary"
            class="rounded-pill"
            block
            type="submit"
            flat
            @click="login"
          >
            Connexion
          </v-btn>
        </v-col>

        <v-col cols="12">
          <p v-if="errorMessage" class="text-error">{{ errorMessage }}</p>
        </v-col>
      </v-row>
    </div>
  </div>
</template>

