<script setup>
import {onMounted, computed} from 'vue';
import {useRoute} from 'vue-router';
import TaskUploadFileForm from '@/components/tasks/TaskEdit/TaskUploadFileForm.vue';

const route = useRoute();

const crumbs = computed(() => [
  {route: {name: 'tasks-lists'}, label: 'Задачи'},
  {label: 'Загрузка файла'},
]);

onMounted(async () => {
});
</script>

<template>
  <BreadCrumbs :crumbs="crumbs"/>

  <q-separator class="q-mb-md"></q-separator>
  <task-upload-file-form :success-route="{name: 'tasks-lists'}" :cancel-route="{name: 'tasks-lists'}"></task-upload-file-form>
</template>

<style src="./TaskView.scss" lang="scss"></style>
