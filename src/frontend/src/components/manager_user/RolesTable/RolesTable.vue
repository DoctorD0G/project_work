<script setup>
import _ from 'lodash';
import {computed, onMounted, ref} from 'vue';
// eslint-disable-next-line no-unused-vars
import {useRouter} from 'vue-router';
import {useAppStore} from '@/stores/app';
import {useManagerRoleStore, useUserStore} from '@/stores/manager-user';
import {hasAccess, appPermissions} from '@/utils/perms';

const router = useRouter();
const store = useAppStore();
const managerRoleStore = useManagerRoleStore();
const userStore = useUserStore();

// Has Access
const hasUserEdit = computed(() => hasAccess(appPermissions.CISM_USER_EDIT_PERMISSION));

const tableRef = ref()
const confirmDialog = ref()
const submitting = ref(false)
const allPermissions = ref(null)

const tableColumns = ref([
  {
    name: 'name',
    field: 'name',
    label: 'Наименование',
    align: 'left',
  },
  {
    name: 'permissions',
    field: 'permissions',
    label: 'Права',
    align: 'left'
  },
  {
    name: 'actions',
    align: 'center',
  },
]);

const confirmDeleteRole = async (id, name) => {
  confirmDialog.value?.showDialog(
    "Подтверждение",
    `Вы действительно хотите удалить роль ${name}?`
  ).then(
    async (result) => {
      if (result) {
        try {
          submitting.value = true
          const state = await managerRoleStore.deleteRoleAction(id)
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
    managerRoleStore.getPaginableRoles(page, rowsPerPage, sortBy, descending, filter).then((data) => {
      resolve(data);
    }).catch((error) => {
      reject(error);
    })
  })
}
const loadPermissions = async () => {
  allPermissions.value = await managerRoleStore.getAllPermissionsAction()
}
const getPermissionsByCode = (permissions) => {
  const perms = _.chain(allPermissions.value).keyBy('name').at(permissions).value()
  return _.map(perms, 'title')
}
onMounted(async () => {
  await loadPermissions()
})
</script>

<template>
    <base-table ref="tableRef" :loadTableItemsFunction="loadTableItems" :columns="tableColumns">
      <template v-slot:top-right>
        <q-btn outline title="Добавить роль" color="dark" :disable="!hasUserEdit" label="Добавить" @click="router.push({name: 'create-role'})" icon="add"/>
      </template>
      <template v-slot:body-cell-permissions="props">
        <q-td :props="props">
          <div v-for="perm in getPermissionsByCode(props.row.permissions)" :key="perm">
            {{perm}}
          </div>
        </q-td>
      </template>
      <template v-slot:body-cell-actions="props">
        <q-td :props="props">
          <q-btn
            title="Редактировать роль"
            @click.stop="router.push({name: 'update-role', params: {id: props.row.id}})"
            icon="edit"
            class="q-mr-sm"
            flat
            round
            :disable="!hasUserEdit"
          />
          <q-btn
            color="dark"
            title="Удалить роль"
            @click.stop="confirmDeleteRole(props.row.id, props.row.name)"
            icon="delete_forever"
            round
            flat
            :disable="!hasUserEdit"
          />
        </q-td>
      </template>
    </base-table>
    <ConfirmDlg ref="confirmDialog" :submitting="submitting"></ConfirmDlg>
</template>

<style src="./RolesTable.scss" lang="scss"></style>
