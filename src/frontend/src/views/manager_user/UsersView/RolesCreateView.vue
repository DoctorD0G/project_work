<script setup>
import {onMounted, computed} from 'vue';
import RolesCreateForm from '@/components/manager_user/RolesEdit/RolesCreateForm.vue';

const crumbs = computed(() => [
  { route: {name: 'roles-tab'}, label: 'Роли' },
  {
    label: 'Создание роли',
  },
]);

onMounted(async () => {
});
</script>

<template>
  <BreadCrumbs :crumbs="crumbs" />

  <q-separator class="q-mb-md"></q-separator>
  <roles-create-form :success-route="{name: 'roles-tab'}" :cancel-route="{name: 'roles-tab'}"></roles-create-form>
</template>

<style src="./UsersView.scss" lang="scss"></style>
