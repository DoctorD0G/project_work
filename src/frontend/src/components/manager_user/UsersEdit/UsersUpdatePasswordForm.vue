<script setup>
import {onMounted, ref} from 'vue';
// eslint-disable-next-line no-unused-vars
import {useRouter} from 'vue-router';
import {useAppStore} from '@/stores/app';
import {useManagerUserStore, useUserStore} from '@/stores/manager-user';
import {FormValidationError} from 'cism-front-base';
import {helpers, maxLength, required} from "@vuelidate/validators";

const props = defineProps({
  id: String,
  successRoute: Object,
  cancelRoute: Object,
})

const router = useRouter();
const store = useAppStore();
const managerUserStore = useManagerUserStore();
const userStore = useUserStore();

const formFields = ref([
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
      managerUserStore.updateUserPasswordAction(props.id, formData.value.password).then((data) => {
       resolve(data);
       router.push(props.successRoute);
      }).catch((error) => {
        reject(error);
      })
    }
  })
};
</script>

<template>
  <div class="row justify-center">
    <div class="col-12 col-xl-4 col-md-8">
      <q-card class="column full-height">
        <q-card-section>
          <div class="row items-center no-wrap">
            <div class="col">
              <div class="text-h6">Изменение пароля пользователя</div>
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
