<script setup>
import {onMounted, ref} from 'vue';
// eslint-disable-next-line no-unused-vars
import {useRouter} from 'vue-router';
import {helpers, required, minLength, maxLength, minValue, maxValue, integer, between} from "@vuelidate/validators";
import {useTaskStore} from '@/stores/task'

const props = defineProps({
  successRoute: Object,
  cancelRoute: Object,
})

const router = useRouter();
const taskStore = useTaskStore();

const formFields = ref([
  {name: 'name', label: 'Наименование', type: 'input', init: null,
    valid_rules: {
      requiredField: helpers.withMessage("Обязательное поле", required),
    }
  },
  {name: 'file', label: 'Файл', type: 'file', init: null,
    valid_rules: {
      requiredField: helpers.withMessage("Обязательное поле", required),
    }
  },
])

const submitFormAction = function (formData) {
  return new Promise((resolve, reject) => {
    taskStore.uploadFile(formData.value).then((data) => {
       resolve(data);
       router.push(props.successRoute);
    }).catch((error) => {
      reject(error);
    })
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
              <div class="text-h6">Пример загрузки файла</div>
            </div>
          </div>
        </q-card-section>

        <q-card-section class="col q-pt-none q-w-p50">
          <base-form :fields="formFields" :submit-action="submitFormAction" :cancel-route="cancelRoute">
          </base-form>
        </q-card-section>
      </q-card>
    </div>
  </div>
</template>

<style src="./TaskEditForm.scss" lang="scss"></style>
