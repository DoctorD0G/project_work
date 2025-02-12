<script setup>
import { onMounted, ref } from 'vue';
import { menuList } from '@/utils/menu';
import { useAppStore } from '@/stores/app';
import { hasAccess } from '@/utils/perms';
import SidebarMenuItem from '@/components/sidebar/SidebarMenu/SidebarMenuItem.vue';

const appstore = useAppStore();
const menuLinks = ref([]);

onMounted(async () => {
  menuLinks.value = menuList.filter((item) => (item.perms ? hasAccess(item.perms) : Boolean));
});
</script>

<template>
  <q-drawer show-if-above v-model="appstore.isVisibleMenu" side="left" bordered class="primary">
    <q-scroll-area class="fit">
      <q-list padding class="text-black">
        <sidebar-menu-item
          v-for="link in menuLinks"
          :key="link"
          v-bind="link"
        ></sidebar-menu-item>
      </q-list>
    </q-scroll-area>
  </q-drawer>
</template>

<style src="./SidebarMenu.scss" lang="scss"></style>
