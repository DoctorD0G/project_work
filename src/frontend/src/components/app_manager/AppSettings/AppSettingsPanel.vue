<script setup>
import { computed, onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAppManagerStore } from '@/stores/app-manager';
import { hasAccess, appPermissions } from '@/utils/perms';

const router = useRouter();
const appManagerStore = useAppManagerStore();

const DEBUGGING = 1
const PAUSING = 5
const RUNNING = 10
const activity_options = ref([
  {'id': DEBUGGING, 'name': 'В режиме отладки'},
  {'id': PAUSING, 'name': 'Приостановлен'},
  {'id': RUNNING, 'name': 'Активен'}
]);

const formData = ref({});
const currentAppSettings = ref({});
const submitting = ref(false);
const loading = ref(false);

const onCancel = () => {
  formData.value.status = currentAppSettings.value.status;
};

const onSubmit = async () => {
  try {
    submitting.value = true;
    currentAppSettings.value = await appManagerStore.updateAppSettings(formData.value);
  } finally {
    submitting.value = false;
  }
};

const loadAppSettings = async () => {
  loading.value = true;
  currentAppSettings.value = await appManagerStore.getAppSettings();
  formData.value.status = currentAppSettings.value.status;
  loading.value = false;
};


const hasAppSettingsEdit = computed(() => hasAccess(appPermissions.APP_SETTINGS_EDIT_PERMISSION));

onMounted(async () => {
  await loadAppSettings();
});
</script>

<template>
  <q-card class=" ">
      <q-card-section>
        <div>Настройки сервиса</div>
      </q-card-section>
      <q-card-section>
        <q-linear-progress v-if="loading" rounded  indeterminate  :value="loading" class="q-mt-md" />
        <q-select
          v-else
          v-model="formData.status"
          :options="activity_options"
          label="Статус"
          option-value="id"
          option-label="name"
          emit-value
          map-options
          :disable="!hasAppSettingsEdit"
        >
          <template v-slot:before>
            <q-icon v-if="formData.status === DEBUGGING" name="bug_report" size="sm" />
            <q-icon v-if="formData.status === PAUSING" name="pause" size="sm" style="color: #ff0000d6" />
            <q-icon v-if="formData.status === RUNNING" name="directions_run" size="sm" />
          </template>
        </q-select>
      </q-card-section>
      <q-card-actions v-if="currentAppSettings.status !== formData.status">
        <q-btn
          label="Изменить"
          class="q-ml-sm"
          @click="onSubmit"
          :loading="submitting"
        />
        <q-btn
          label="Отмена"
          flat
          class="q-ml-sm"
          @click="onCancel"
        />
      </q-card-actions>
  </q-card>
</template>

<style src="./AppSettingsPanel.scss" lang="scss"></style>
