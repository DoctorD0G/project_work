<script setup>
import { hasAccess, appPermissions } from '@/utils/perms';
import {computed} from "vue";
import AppSettingsPanel from '@/components/app_manager/AppSettings/AppSettingsPanel.vue';

const crumbs = computed(() => [
  {
    label: `Главная`
  },
]);

const hasAppSettingsView = computed(() => hasAccess(appPermissions.APP_SETTINGS_VIEW_PERMISSION));
</script>

<template>
  <BreadCrumbs class="q-mt-md" :crumbs="crumbs"/>
  <q-separator class="q-mb-md"></q-separator>
  <div class="row">
    <div class="col-4">
    <app-settings-panel v-if="hasAppSettingsView"/>
    </div>
  </div>
</template>

<style src="./MainView.scss" lang="scss"></style>
