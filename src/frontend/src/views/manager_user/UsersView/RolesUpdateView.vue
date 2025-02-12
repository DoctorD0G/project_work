<script setup>
import {onMounted, computed} from 'vue';
import {useRoute} from 'vue-router';
import RolesUpdateForm from '@/components/manager_user/RolesEdit/RolesUpdateForm.vue';

const route = useRoute();

const crumbs = computed(() => [
  { route: {name: 'roles-tab'}, label: 'Роли' },
  {
    label: 'Редактирование роли',
  },
]);

onMounted(async () => {
});
</script>

<template>
  <BreadCrumbs :crumbs="crumbs" />

  <q-separator class="q-mb-md"></q-separator>
  <roles-update-form :id="route.params.id" :success-route="{name: 'roles-tab'}" :cancel-route="{name: 'roles-tab'}"></roles-update-form>
</template>

<style src="./UsersView.scss" lang="scss"></style>
