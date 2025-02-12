<script setup>
import { hasAccess, appPermissions } from '@/utils/perms';
import {computed} from "vue";
import TaskTable from "@/components/tasks/TaskTable/TaskTable.vue";

const crumbs = computed(() => [
  {
    label: 'Задачи',
  },
]);
</script>

<template>
  <BreadCrumbs class="q-mt-md" :crumbs="crumbs"/>

  <q-separator class="q-mb-md"></q-separator>
  <q-card>
    <q-card-section>
      <task-table></task-table>
    </q-card-section>
  </q-card>
</template>

<style src="./TaskView.scss" lang="scss"></style>
