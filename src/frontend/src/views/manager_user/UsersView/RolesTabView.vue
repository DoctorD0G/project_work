<script setup>
import {onMounted, computed, ref} from 'vue';
import RolesTable from '@/components/manager_user/RolesTable/RolesTable.vue';

onMounted(async () => {
});
</script>

<template>
  <div class="q-pa-md">
    <roles-table/>
  </div>
</template>

<style src="./UsersView.scss" lang="scss"></style>
