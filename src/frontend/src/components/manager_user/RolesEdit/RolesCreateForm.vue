<script setup>
import {onMounted, ref} from 'vue';
// eslint-disable-next-line no-unused-vars
import {useRouter} from 'vue-router';
import {useAppStore} from '@/stores/app';
import {useManagerRoleStore, useUserStore} from '@/stores/manager-user';
import {helpers, maxLength, required} from "@vuelidate/validators";

const props = defineProps({
  successRoute: Object,
  cancelRoute: Object,
})

const router = useRouter();
const store = useAppStore();
const managerRoleStore = useManagerRoleStore();
const userStore = useUserStore();

const allPermissions = ref([])

const formFields = ref([
  {name: 'name', label: 'Наименование', type: 'input', init: null,
    valid_rules: {
      maxLength: helpers.withMessage("Введите не более 20 символов", maxLength(20)),
      requiredField: helpers.withMessage("Обязательное поле", required),
    }
  },
  {name: 'permissions', label: 'Права', type: 'multiple-select', init: null, items: allPermissions,
    valid_rules: {
      requiredField: helpers.withMessage("Обязательное поле", required),
    }
  },
])

const submitFormAction = function (formData) {
  return new Promise((resolve, reject) => {
    managerRoleStore.createRoleAction(formData.value).then((data) => {
     resolve(data);
     router.push(props.successRoute);
    }).catch((error) => {
      reject(error);
    })
  })
};
const loadPermissions = async () => {
  const permissions = await managerRoleStore.getAllPermissionsAction()

  permissions.forEach(function (permission) {
    allPermissions.value.push({label: permission.title, value: permission.name})
  })
}
onMounted(async () => {
  await loadPermissions()
})
</script>

<template>
  <div class="row justify-center">
    <div class="col-12 col-xl-4 col-md-8">
      <q-card class="column full-height">
        <q-card-section>
          <div class="row items-center no-wrap">
            <div class="col">
              <div class="text-h6">Создание роли</div>
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

<style src="./RolesEditForm.scss" lang="scss"></style>
