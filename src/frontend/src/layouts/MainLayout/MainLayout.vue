<script setup>
import HeaderBlock from '@/components/header/HeaderBlock/HeaderBlock.vue';
import SidebarMenu from '@/components/sidebar/SidebarMenu/SidebarMenu.vue';
import {useAppStore } from '@/stores/app';
import {menuList} from '@/utils/menu'
import { hasAccess } from '@/utils/perms';
const appstore = useAppStore();

</script>

<template>
  <main-layout>
    <template v-slot:header-block>
      <HeaderBlock />
    </template>
    <template v-slot:sidebar-menu>
      <SidebarMenu />
    </template>
  </main-layout>
</template>

