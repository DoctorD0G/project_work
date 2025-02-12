<script setup>
import _ from 'lodash';
import {onMounted, computed, ref} from 'vue';
// eslint-disable-next-line no-unused-vars
import {useRouter} from 'vue-router';
import {useAppStore} from '@/stores/app';
import {useManagerUserStore, useManagerRoleStore, useUserStore} from '@/stores/manager-user';
import {hasAccess, appPermissions} from '@/utils/perms';

const router = useRouter();
const store = useAppStore();
const managerUserStore = useManagerUserStore();
const managerRoleStore = useManagerRoleStore();
const userStore = useUserStore();

// Has Access
const hasUserEdit = computed(() => hasAccess(appPermissions.CISM_USER_EDIT_PERMISSION));
const confirmDialog = ref()
const tableRef = ref()
const submitting = ref(false)

const allRoles = ref(null)

const tableColumns = ref([
  {
    name: 'fio',
    field: 'fio',
    label: 'ФИО',
    align: 'left',
  },
  {
    name: 'username',
    field: 'username',
    label: 'Логин',
    align: 'center',
  },
  {
    name: 'role_id',
    field: 'role_id',
    label: 'Роль',
    align: 'center',
  },
  {
    name: 'is_admin',
    field: 'is_admin',
    label: 'Админ',
    align: 'center',
  },
  {
    name: 'actions',
    align: 'center',
  },
]);

const changeIsAdmin = async (id, is_admin) => {
  confirmDialog.value?.showDialog(
    "Подтверждение",
    `Вы действительно хотите изменить статус пользователя?`
  ).then(
    async (result) => {
      if (result) {
        try {
          submitting.value = true
          const state = await managerUserStore.changeAdminStateAction(id, is_admin)
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
const confirmDeleteUser = async (id, username) => {
  confirmDialog.value?.showDialog(
    "Подтверждение",
    `Вы действительно хотите удалить пользователя ${username}?`
  ).then(
    async (result) => {
      if (result) {
        try {
          submitting.value = true
          const state = await managerUserStore.deleteUserAction(id)
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
    managerUserStore.getPaginableUsers(page, rowsPerPage, sortBy, descending, filter).then((data) => {
      resolve(data);
    }).catch((error) => {
      reject(error);
    })
  })
}

const loadRoles = async () => {
  allRoles.value = await managerRoleStore.getAllRolesAction()
}

const getRoleNameById = (id) => {
  const role = _.find(allRoles.value, ['id', id])
  return role ? role.name : '---'
}

onMounted(async () => {
  await loadRoles()
})
</script>

<template>
  <base-table ref="tableRef" :loadTableItemsFunction="loadTableItems" :columns="tableColumns">
    <template v-slot:top-right>
      <q-btn outline title="Добавить пользователя" color="dark" :disable="!hasUserEdit" label="Добавить" @click="router.push({name: 'create-user'})" icon="add"/>
    </template>
    <template v-slot:body-cell-role_id="props">
      <q-td :props="props">
        {{ getRoleNameById(props.row.role_id) }}
      </q-td>
    </template>
    <template v-slot:body-cell-is_admin="props">
      <q-td :props="props">
        <q-btn flat round :icon="props.row.is_admin? 'check_circle_outline': 'highlight_off'"
               :disable="props.row.username==userStore.userName || !hasUserEdit"
               color="dark"
               :title="props.row.is_admin? 'Администратор': 'Не администратор'"
               @click="changeIsAdmin(props.row.id, !props.row.is_admin)"/>
      </q-td>
    </template>
    <template v-slot:body-cell-actions="props">
      <q-td :props="props">
        <q-btn
          color="dark"
          title="Редактировать пользователя"
          @click.stop="router.push({name: 'update-user', params: {id: props.row.id}})"
          icon="edit"
          class="q-mr-sm"
          flat
          round
          :disable="!hasUserEdit"
        />
        <q-btn
          color="dark"
          title="Изменить пароль пользователя"
          :disable="!hasUserEdit"
          @click.stop="router.push({name: 'update-user-password', params: {id: props.row.id}})"
          icon="password"
          round
          flat
        />
        <q-btn
          color="dark"
          title="Удалить пользователя"
          :disable="props.row.username==userStore.userName || !hasUserEdit"
          @click.stop="confirmDeleteUser(props.row.id, props.row.username)"
          icon="delete_forever"
          round
          flat
        />
      </q-td>
    </template>
  </base-table>
  <ConfirmDlg ref="confirmDialog" :submitting="submitting"></ConfirmDlg>
</template>

<style src="./UsersTable.scss" lang="scss"></style>
