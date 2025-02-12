<script setup>
import {onMounted, ref} from 'vue';
// eslint-disable-next-line no-unused-vars
import {useRouter} from 'vue-router';
import {useAppStore} from '@/stores/app';
import {useManagerUserStore, useManagerRoleStore, useUserStore} from '@/stores/manager-user';
import {helpers, maxLength, required, sameAs} from "@vuelidate/validators";
import {FormValidationError} from 'cism-front-base';


const props = defineProps({
  successRoute: Object,
  cancelRoute: Object,
})

const router = useRouter();
const store = useAppStore();
const managerUserStore = useManagerUserStore();
const managerRoleStore = useManagerRoleStore();
const userStore = useUserStore();

const formData = ref({});
const allRoles = ref([])

const formFields = ref([
  {name: 'fio', label: 'ФИО', type: 'input', init: null,
    valid_rules: {
      maxLength: helpers.withMessage("Введите не более 20 символов", maxLength(20)),
      requiredField: helpers.withMessage("Обязательное поле", required),
    }
  },
  {name: 'username', label: 'Логин', type: 'input', init: null,
    valid_rules: {
      maxLength: helpers.withMessage("Введите не более 10 символов", maxLength(10)),
      requiredField: helpers.withMessage("Обязательное поле", required),
    }
  },
  {name: 'role_id', label: 'Роль', type: 'select', init: null,
    items: allRoles,
    valid_rules: {
      requiredField: helpers.withMessage("Обязательное поле", required),
    }
  },
  {name: 'password', label: 'Пароль', type: 'password', init: null,
    valid_rules: {
      requiredField: helpers.withMessage("Обязательное поле", required),
    }
  },
  {name: 'confirmPassword', label: 'Подтверждение пароля', type: 'password', init: null,
    valid_rules: {
      requiredField: helpers.withMessage("Обязательное поле", required)
    },
  },
])

const submitFormAction = function (formData) {
  return new Promise((resolve, reject) => {
    if (formData.value.password != formData.value.confirmPassword){
      reject(new FormValidationError("error", {confirmPassword: "Пароли не совпадают"}))
    }else{
      managerUserStore.createUserAction(formData.value).then((data) => {
       resolve(data);
       router.push(props.successRoute);
      }).catch((error) => {
        reject(error);
      })
    }
  })
};

const loadUserRoles = async () => {
  const rolesData = await managerRoleStore.getAllRolesAction()

  rolesData.forEach(function (role) {
    allRoles.value.push({label: role.name, value: role.id})
  })
}

onMounted(async () => {
  await loadUserRoles()
})
</script>

<template>
  <div class="row justify-center">
    <div class="col-12 col-xl-4 col-md-8">
      <q-card class="column full-height">
        <q-card-section>
          <div class="row items-center no-wrap">
            <div class="col">
              <div class="text-h6">Создание пользователя</div>
            </div>
          </div>
        </q-card-section>

        <q-card-section class="col q-pt-none q-w-p50">
          <base-form :fields="formFields" :submit-action="submitFormAction" :cancel-route="cancelRoute"></base-form>
        </q-card-section>
      </q-card>
    </div>
  </div>
</template>

<style src="./UsersEditForm.scss" lang="scss"></style>
