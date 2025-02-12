<script setup>
import {onMounted, computed, ref} from 'vue';
import UsersTable from '@/components/manager_user/UsersTable/UsersTable.vue';

onMounted(async () => {
});
</script>

<template>
  <div class="q-pa-md">
    <users-table/>
  </div>
</template>

<style src="./UsersView.scss" lang="scss"></style>
