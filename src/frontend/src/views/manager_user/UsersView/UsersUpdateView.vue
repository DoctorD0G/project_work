<script setup>
import {onMounted, computed} from 'vue';
import {useRoute} from 'vue-router';
import UsersUpdateForm from "@/components/manager_user/UsersEdit/UsersUpdateForm.vue";

const route = useRoute();

const crumbs = computed(() => [
  { route: {name: 'users-tab'}, label: 'Пользователи' },
  {
    label: 'Редактирование пользователя',
  },
]);

onMounted(async () => {
});
</script>

<template>
  <BreadCrumbs :crumbs="crumbs" />

  <q-separator class="q-mb-md"></q-separator>
  <users-update-form :id="route.params.id" :success-route="{name: 'users-tab'}" :cancel-route="{name: 'users-tab'}"></users-update-form>
</template>

<style src="./UsersView.scss" lang="scss"></style>
