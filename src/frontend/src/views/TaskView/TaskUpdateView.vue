<script setup>
import {onMounted, computed} from 'vue';
import {useRoute} from 'vue-router';
import TaskUpdateForm from '@/components/tasks/TaskEdit/TaskUpdateForm.vue';

const route = useRoute();

const crumbs = computed(() => [
  {route: {name: 'tasks-lists'}, label: 'Задачи'},
  {label: 'Редактирование задачи'},
]);

onMounted(async () => {
});
</script>

<template>
  <BreadCrumbs :crumbs="crumbs"/>

  <q-separator class="q-mb-md"></q-separator>
  <task-update-form :id="route.params.id" :success-route="{name: 'tasks-lists'}" :cancel-route="{name: 'tasks-lists'}"></task-update-form>
</template>

<style src="./TaskView.scss" lang="scss"></style>
