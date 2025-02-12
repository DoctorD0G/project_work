<script setup>
import { useRouter } from 'vue-router';
import { onMounted, ref } from 'vue';

const router = useRouter();

const emit = defineEmits(['showParentItem']);

const props = defineProps({
  title: {
    type: String,
    required: true,
  },
  link: {
    type: String,
    default: '#',
  },
  icon: {
    type: String,
    default: '',
  },
  level: {
    type: Number,
    default: 0,
  },
  children: {
    type: Array,
    default: [],
  },
});

const parentRef = ref();

const activeRoute = (route_link) => {
  let result = router.currentRoute.value.path.startsWith(route_link);

  return result;
};

onMounted(() => {
  if (router.currentRoute.value.path.startsWith(props.link)) {
    emit('showParentItem');
  }
});

const onShowParentItem = () => {
  if (parentRef.value)  {
    parentRef.value.show();
  }
  emit('showParentItem');
};
</script>

<template>
  <q-item
    v-if="children.length === 0"
    class="GNL__drawer-item"
    active-class="bg-blue-grey-1"
    v-ripple
    clickable
    :inset-level="level"
    :active="activeRoute(link)"
    :to="link"
  >
    <q-item-section avatar>
      <q-icon :name="icon"></q-icon>
    </q-item-section>
    <q-item-section>
      <q-item-label>
        {{ title }}
      </q-item-label>
    </q-item-section>
  </q-item>
  <q-expansion-item
    v-else-if="children.length > 0"
    class="GNL__drawer-item"
    :label="title"
    :icon="icon"
    :header-inset-level="level"
    :group="`menu-item-${level}`"
    ref="parentRef"
  >
    <sidebar-menu-item
      v-for="child in children"
      :key="child"
      v-bind="child"
      :level="level + 1"
      @show-parent-item="onShowParentItem"
    >
    </sidebar-menu-item>
  </q-expansion-item>
</template>

<style src="./SidebarMenu.scss" lang="scss"></style>
