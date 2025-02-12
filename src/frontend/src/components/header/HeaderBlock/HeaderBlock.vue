<script setup>
import {useAppStore} from '@/stores/app';
import {useRouter} from 'vue-router';
import {useUserStore} from '@/stores/manager-user';

const router = useRouter();
const appstore = useAppStore();
const userStore = useUserStore();

const logout = async () => {
  await userStore.logout();
  void router.push('/auth');
};
</script>

<template>
  <q-header reveal elevated class="bg-white text-black" height-hint="64">
    <q-toolbar class="GNL__toolbar">
      <q-btn dense flat round icon="menu" @click="appstore.toggleVisibleMenu"/>
      <q-btn href="/" title="На главную" flat no-caps no-wrap class="q-ml-none q-pl-none app-logo" v-if="$q.screen.gt.xs">
          <img alt="Название сервиса" src="~/cism-front-base/src/assets/images/logo_invert.svg" />
          <q-toolbar-title shrink class="q-ml-none q-pl-none app-logo-title">
            Название сервиса
          </q-toolbar-title>
        </q-btn>
      <q-space />
      <div class="row items-center no-wrap">
        <q-avatar size="25px">
          <img src="~/cism-front-base/src/assets/images/avatar.png">
        </q-avatar>
        <q-tooltip>
          {{ userStore.userName }}
        </q-tooltip>
      </div>
      <q-btn round flat icon="logout" title="Выйти" class="q-mr-lg" @click="logout"/>
    </q-toolbar>

  </q-header>
</template>

<style src="./HeaderBlock.scss" lang="scss"></style>
