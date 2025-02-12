<script setup>
import { hasAccess, appPermissions } from '@/utils/perms';
import {onMounted, computed, ref} from 'vue';
import TaskPage from "@/components/tasks/TaskPage/TaskPage.vue";
import {useRoute} from "vue-router";
import {useTaskStore} from "@/stores/task";

const route = useRoute();
const taskStore = useTaskStore();

let pageLabel = ref('Просмотр задачи');

const crumbs = computed(() => [
  {route: {name: 'tasks-lists'}, label: 'Задачи'},
  {label: pageLabel},
]);

const loadTaskData = async () => {
  const TaskData = await taskStore.getTaskByIdAction(route.params.id)

  pageLabel.value = `задача ${TaskData.name}`
}
onMounted(async () => {
  await loadTaskData()
})
</script>

<template>
  <BreadCrumbs :crumbs="crumbs"/>

  <q-separator class="q-mb-md"></q-separator>
  <task-page :id="route.params.id"></task-page>
</template>

<style src="./TaskView.scss" lang="scss"></style>
