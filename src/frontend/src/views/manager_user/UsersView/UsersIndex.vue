<script setup>
import {onMounted, computed, ref} from 'vue';



const crumbs = computed(() => [
  {
    label: `Пользователи`
  },
]);
onMounted(async () => {
});
</script>

<template>
  <BreadCrumbs class="q-mt-md"  :crumbs="crumbs"/>

  <q-separator class="q-mb-md"></q-separator>

  <q-card>
    <q-tabs align="left" class="q-mb-md">
      <q-route-tab :to="{name: 'users-tab'}" label="Пользователи" />
      <q-route-tab :to="{name: 'roles-tab'}" label="Роли" />
    </q-tabs>
    <div class="q-pa-sm">
      <router-view/>
    </div>
  </q-card>
</template>

<style src="./UsersView.scss" lang="scss"></style>
