<script setup>
import {onMounted, computed} from 'vue';
import UsersCreateForm from '@/components/manager_user/UsersEdit/UsersCreateForm.vue';

const crumbs = computed(() => [
  {route: {name: 'users-tab'}, label: 'Пользователи'},
  {label: 'Создание пользователя'},
]);

onMounted(async () => {
});
</script>

<template>
  <BreadCrumbs :crumbs="crumbs"/>

  <q-separator class="q-mb-md"></q-separator>
  <users-create-form :success-route="{name: 'users-tab'}" :cancel-route="{name: 'users-tab'}"></users-create-form>
</template>

<style src="./UsersView.scss" lang="scss"></style>
