<script setup lang="ts">
import { ref } from 'vue';

const firstName = ref('');
const lastName = ref('');
const email = ref('');
const password = ref('');
const selectedRole = ref('');
const errorMessage = ref(''); // Message d'erreur ou de succès
const isSuccess = ref(false); // Détermine si l'inscription a réussi
const loading = ref(false); // État de chargement
const formErrors = ref({
  firstName: false,
  lastName: false,
  email: false,
  password: false,
  selectedRole: false,
});

const register = async () => {
  // Réinitialiser les erreurs avant chaque soumission
  formErrors.value = {
    firstName: false,
    lastName: false,
    email: false,
    password: false,
    selectedRole: false,
  };

  // Vérification des champs obligatoires
  if (!firstName.value || !lastName.value || !email.value || !password.value || !selectedRole.value) {
    formErrors.value.firstName = !firstName.value;
    formErrors.value.lastName = !lastName.value;
    formErrors.value.email = !email.value;
    formErrors.value.password = !password.value;
    formErrors.value.selectedRole = !selectedRole.value;
    errorMessage.value = 'Tous les champs sont obligatoires.';
    isSuccess.value = false; // Échec
    return;
  }

  try {
    loading.value = true; // Indiquer que l'inscription est en cours
    const response = await fetch('http://127.0.0.1:5000/register', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        firstName: firstName.value,
        lastName: lastName.value,
        email: email.value,
        password: password.value,
        role: selectedRole.value,
      }),
    });

    const result = await response.json();
    loading.value = false; // Fin du chargement
    if (response.ok) {
      errorMessage.value = result.message;
      isSuccess.value = true;
      // Réinitialisation des champs après succès
      firstName.value = '';
      lastName.value = '';
      email.value = '';
      password.value = '';
      selectedRole.value = '';
      
      // Réinitialiser les erreurs
      formErrors.value = {
        firstName: false,
        lastName: false,
        email: false,
        password: false,
        selectedRole: false,
      };
    } else {
      errorMessage.value = result.error;
      isSuccess.value = false;
    }
  } catch (error) {
    loading.value = false;
    console.error('Erreur lors de l\'inscription :', error);
    errorMessage.value = 'Une erreur est survenue. Veuillez réessayer.';
    isSuccess.value = false;
  }
};
</script>

<template>
  <v-row class="d-flex mb-3">
    <v-col cols="12">
      <v-text-field
        v-model="firstName"
        :readonly="loading"
        class="mb-2"
        label="Prénom"
        clearable
      ></v-text-field>
    </v-col>
    <v-col cols="12">
      <v-text-field
        v-model="lastName"
        :readonly="loading"
        class="mb-2"
        label="Nom"
        clearable
      ></v-text-field>
    </v-col>
    <v-col cols="12">
      <v-text-field
        v-model="email"
        :readonly="loading"
        class="mb-2"
        label="Adresse courriel"
        clearable
      ></v-text-field>
    </v-col>
    <v-col cols="12">
      <v-text-field
        v-model="password"
        :readonly="loading"
        class="mb-2"
        label="Mot de passe"
        clearable
      ></v-text-field>
    </v-col>
    <v-col cols="12">
      <v-select
        clearable
        label="Rôle"
        :items="[ { text: 'Utilisateur', value: 'user' }, { text: 'Gestionnaire', value: 'gestio' }, { text: 'Administrateur', value: 'admin' } ]"
        item-title="text"
        item-value="value"
        v-model="selectedRole"
        variant="outlined"
      />
    </v-col>
    <v-col cols="12">
      <v-btn
        @click="register"
        :disabled="loading || !firstName || !lastName || !email || !password || !selectedRole"
        :loading="loading"
        color="primary"
        rounded="pill"
        size="large"
        type="submit"
        variant="elevated"
        block
        flat
      >
        Ajouter
      </v-btn>
    </v-col>
    <v-col cols="12">
      <p v-if="errorMessage" :class="{'text-error': !isSuccess, 'text-success': isSuccess}">{{ errorMessage }}</p>
    </v-col>
  </v-row>
</template>
