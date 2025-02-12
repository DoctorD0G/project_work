<script setup>
import _ from 'lodash';
import {onMounted, computed, ref} from 'vue';
// eslint-disable-next-line no-unused-vars
import {useRouter} from 'vue-router';
import {useTaskStore} from '@/stores/task'
import {hasAccess, appPermissions} from '@/utils/perms';
import {formatDateTime} from 'cism-front-base';

const router = useRouter();
const taskStore = useTaskStore();

// Has Access
const hasTaskEdit = computed(() => hasAccess(appPermissions.TASK_EDIT_PERMISSION));

const tableRef = ref()
const confirmDialog = ref()
const submitting = ref(false)
const tableSelected = computed(() => tableRef?.value?.tableSelected)

const tableFilterFields = ref([
  {name: 'name', label: 'Имя', type: 'input'},
  {name: 'box', label: 'Пример (не влияет на фильтр)', type: 'checkbox', init: null},
  {name: 'test', label: 'Пример (не влияет на фильтр)', type: 'select', items: [{label: "1", value: "1"},{label: "2", value: "2"}]},
])

const tableColumns = ref([
  {
    name: 'id',
    field: 'id',
    label: '#',
    align: 'left',
    sortable: false
  },
  {
    name: 'name',
    field: 'name',
    label: 'Название',
    align: 'center',
    sortable: true
  },
  {
    name: 'created_at',
    field: 'created_at',
    label: 'Дата создания',
    align: 'center',
    sortable: true
  },
  {
    name: 'actions',
    align: 'center',
    sortable: false
  },
]);


const confirmDeleteItems = async () => {
  confirmDialog.value?.showDialog(
    "Подтверждение",
    `Вы действительно хотите удалить (${tableSelected?.value.length} шт)?`
  ).then(
    async (result) => {
      if (result) {
        try {
          submitting.value = true
          let removeIds = []
          tableSelected.value.forEach(function (item) {
            removeIds.push(item.id)
          })
        } finally {
          submitting.value = false
          confirmDialog.value?.closeDialog()
          await tableRef.value.loadTableData()
          tableRef.value.tableSelected = []
        }
      } else {
        confirmDialog.value?.closeDialog()
      }
    }
  )
}


const confirmDeleteLimit = async (id) => {
  confirmDialog.value?.showDialog(
    "Подтверждение",
    `Вы действительно хотите удалить #${id}?`
  ).then(
    async (result) => {
      if (result) {
        try {
          submitting.value = true
          const state = await taskStore.deleteTaskAction(id)
        } finally {
          submitting.value = false
          confirmDialog.value?.closeDialog()
          tableRef.value.loadTableData()
        }
      } else {
        confirmDialog.value?.closeDialog()
      }
    }
  )
}

const loadTableItems = function (page, rowsPerPage, sortBy, descending, filter) {
  return new Promise((resolve, reject) => {
    taskStore.getTaskList(page, rowsPerPage, sortBy, descending, filter).then((data) => {
      resolve(data);
    }).catch((error) => {
      reject(error);
    })
  })
}


</script>

<template>
    <base-table  ref="tableRef" :loadTableItemsFunction="loadTableItems" :filter-fields="tableFilterFields" :columns="tableColumns" selection="multiple">
      <template v-slot:top-right>
        <q-btn outline title="Добавить задачу" color="dark" :disable="!hasTaskEdit"  label="Добавить" @click="router.push({name: 'create-task'})" icon="add"/>
        <q-btn outline class="q-ml-md" title="Загрузить файл" color="dark" :disable="!hasTaskEdit"  label="Загрузить" @click="router.push({name: 'upload-file'})" icon="upload"/>
        <q-btn
          v-if="hasTaskEdit && tableSelected?.length > 0"
          outline
          title="Удалить"
          color="dark"
          @click="confirmDeleteItems"
          label="Удалить"
          icon="delete">
        </q-btn>
      </template>
      <template v-slot:body-cell-id="tdProps">
        <q-td :props="tdProps">
          <a @click.stop="router.push({name: 'task-page', params: {id: tdProps.row.id}})" title="Страница задачи">{{tdProps.row.id}}</a>
        </q-td>
      </template>
      <template v-slot:body-cell-created_at="tdProps">
        <q-td :props="tdProps">
          {{formatDateTime(tdProps.row.created_at) }}
        </q-td>
      </template>
      <template v-slot:body-cell-actions="tdProps">
      <q-td :props="tdProps">
        <q-btn
            title="Редактировать"
            @click.stop="router.push({name: 'update-task', params: {id: tdProps.row.id}})"
            icon="edit"
            class="q-mr-sm"
            flat
            round
            :disable="!hasTaskEdit"
          />
        <q-btn
          color="dark"
          title="Удалить"
          @click.stop="confirmDeleteLimit(tdProps.row.id)"
          icon="delete_forever"
          round
          flat
          :disable="!hasTaskEdit"
        />
      </q-td>
    </template>
  </base-table>
  <ConfirmDlg ref="confirmDialog" :submitting="submitting"></ConfirmDlg>
</template>

<style src="./TaskTable.scss" lang="scss"></style>
