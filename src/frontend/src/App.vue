<script setup>
import {useMeta} from 'quasar'
import router from '@/router';
import {useAppStore} from '@/stores/app';

const appstore = useAppStore();

useMeta(() => {
  return {
    title: router.currentRoute.value.meta.title,
    titleTemplate: title => `${title} | ${appstore.appTitle}`,
  }
})
</script>

<template>
  <router-view/>
</template>
