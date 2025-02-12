<script setup>
import {onMounted, ref} from 'vue';
// eslint-disable-next-line no-unused-vars
import {useRouter} from 'vue-router';
import {useAppStore} from '@/stores/app';
import {useManagerUserStore, useManagerRoleStore, useUserStore} from '@/stores/manager-user';
import {helpers, maxLength, required} from "@vuelidate/validators";

const props = defineProps({
  id: String,
  successRoute: Object,
  cancelRoute: Object,
})

const router = useRouter();
const store = useAppStore();
const managerUserStore = useManagerUserStore();
const managerRoleStore = useManagerRoleStore();
const userStore = useUserStore();

const loadInitData = ref(false)
const formFields = ref()

const submitFormAction = function (formData) {
  return new Promise((resolve, reject) => {
    managerUserStore.updateUserAction(props.id, formData.value).then((data) => {
     resolve(data);
     router.push(props.successRoute);
    }).catch((error) => {
      reject(error);
    })
  })
};

const loadingInitData = async () => {
  const rolesData = await managerRoleStore.getAllRolesAction()
  let rolesItems = []
  rolesData.forEach(function (role) {
    rolesItems.push({label: role.name, value: role.id})
  })
  const currentUser = await managerUserStore.getUserByIdAction(props.id)

  formFields.value = [
    {name: 'fio', label: 'ФИО', type: 'input', init: currentUser.fio,
      valid_rules: {
        maxLength: helpers.withMessage("Введите не более 20 символов", maxLength(20)),
        requiredField: helpers.withMessage("Обязательное поле", required),
      }
    },
    {name: 'username', label: 'Логин', type: 'input', init: currentUser.username,
      valid_rules: {
        maxLength: helpers.withMessage("Введите не более 10 символов", maxLength(10)),
        requiredField: helpers.withMessage("Обязательное поле", required),
      }
    },
    {name: 'role_id', label: 'Роль', type: 'select', init: currentUser.role_id,
      items: rolesItems,
      valid_rules: {
        requiredField: helpers.withMessage("Обязательное поле", required),
      }
    },
  ]
  loadInitData.value = true
}

onMounted(async () => {
  await loadingInitData()
})
</script>

<template>
  <div class="row justify-center">
    <div class="col-12 col-xl-4 col-md-8">
      <q-card class="column full-height">
        <q-card-section>
          <div class="row items-center no-wrap">
            <div class="col">
              <div class="text-h6">Редактирование пользователя</div>
            </div>
          </div>
        </q-card-section>

        <q-card-section class="col q-pt-none q-w-p50">
          <base-form v-if="loadInitData" :fields="formFields" :submit-action="submitFormAction" :cancel-route="cancelRoute"></base-form>
        </q-card-section>
      </q-card>
    </div>
  </div>
</template>

<style src="./UsersEditForm.scss" lang="scss"></style>
