<script setup>
import {onMounted} from 'vue';
import UsersTable from '@/components/manager_user/UsersTable/UsersTable.vue';
import RolesTable from '@/components/manager_user/RolesTable/RolesTable.vue';

onMounted(async () => {
});
</script>

<template>
  <div class="q-pa-md">
    <users-table/>
  </div>
  <div class="q-pa-md">
    <roles-table/>
  </div>
</template>

<style src="./UsersView.scss" lang="scss"></style>
