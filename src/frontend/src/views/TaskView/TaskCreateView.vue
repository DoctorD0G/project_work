<script setup>
import {onMounted, computed} from 'vue';
import TaskCreateForm from '@/components/tasks/TaskEdit/TaskCreateForm.vue';

const crumbs = computed(() => [
  {route: {name: 'tasks-lists'}, label: 'Задачи'},
  {label: 'Создание задачи'},
]);

onMounted(async () => {
});
</script>

<template>
  <BreadCrumbs :crumbs="crumbs"/>

  <q-separator class="q-mb-md"></q-separator>
  <task-create-form :success-route="{name: 'tasks-lists'}" :cancel-route="{name: 'tasks-lists'}"></task-create-form>
</template>

<style src="./TaskView.scss" lang="scss"></style>
