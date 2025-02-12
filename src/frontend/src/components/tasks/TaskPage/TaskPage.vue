<script setup>
import _ from 'lodash';
import {onMounted, computed, ref} from 'vue';
// eslint-disable-next-line no-unused-vars
import {useRouter} from 'vue-router';
import {useTaskStore} from '@/stores/task'

const props = defineProps({
  id: String,
})

const router = useRouter();
const taskStore = useTaskStore();
const TaskData = ref(null);
const loadInitData = ref(false)

const loadTaskData = async () => {
  TaskData.value = await taskStore.getTaskByIdAction(props.id)
  loadInitData.value = true
}
onMounted(async () => {
  await loadTaskData()
})
</script>

<template>
  <div v-if="loadInitData">
    {{TaskData}}
  </div>

</template>

<style src="./TaskPage.scss" lang="scss"></style>
