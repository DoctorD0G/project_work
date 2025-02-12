<script setup>
import {onMounted, computed} from 'vue';
import {useRoute} from 'vue-router';
import UsersUpdatePasswordForm from "@/components/manager_user/UsersEdit/UsersUpdatePasswordForm.vue";

const route = useRoute();

const crumbs = computed(() => [
  { route: {name: 'users-tab'}, label: 'Пользователи' },
  {
    label: 'Изменение пароля пользователя',
  },
]);

onMounted(async () => {
});
</script>

<template>
  <BreadCrumbs :crumbs="crumbs" />

  <q-separator class="q-mb-md"></q-separator>
  <users-update-password-form :id="route.params.id" :success-route="{name: 'users-tab'}" :cancel-route="{name: 'users-tab'}"></users-update-password-form>
</template>

<style src="./UsersView.scss" lang="scss"></style>
