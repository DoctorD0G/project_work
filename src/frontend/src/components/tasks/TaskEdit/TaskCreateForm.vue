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
  {
    name: 'name', label: 'Имя', type: 'input', init: null,
    valid_rules: {
      maxLength: helpers.withMessage("Введите не более 20 символов", maxLength(20)),
      requiredField: helpers.withMessage("Обязательное поле", required),
    }
  },
  {
    name: 'test_number', label: 'Test number', type: 'number', init: null,
    valid_rules: {
      requiredField: helpers.withMessage("Обязательное поле", required),
    }
  },
  {
    name: 'inn', label: 'ИНН (пример с маской)', type: 'text', init: null, mask: '############',
    valid_rules: {
      maxLength: helpers.withMessage("Введите не более 12 символов", maxLength(12)),
      minLength: helpers.withMessage("Введите не менее 10 символов", minLength(10)),
      requiredField: helpers.withMessage("Обязательное поле", required),
    }
  },
  {name: 'test_select', label: 'Test select', type: 'select', init: "1", items: [{label: "1", value: "1"},{label: "2", value: "2"}]},
  {name: 'test_multiple_select', label: 'Test multiple select', type: 'multiple-select', init: ["1", "2"], items: [{label: "1", value: "1"},{label: "2", value: "2"}]},
])

const submitFormAction = function (formData) {
  return new Promise((resolve, reject) => {
    taskStore.createTaskAction(formData.value.name).then((data) => {
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
              <div class="text-h6">Создание задачи</div>
            </div>
          </div>
        </q-card-section>

        <q-card-section class="col q-pt-none q-w-p50">
          <base-form :fields="formFields" :submit-action="submitFormAction" :cancel-route="cancelRoute">
            <template v-slot:field-test_number="props">
                <q-input
                  v-model="props.formData[props.field.name]"
                  :label="props.field.label"
                  :type="props.field.type"
                  variant="underlined"
                  :error="props.error"
                  :error-message="props.errorsText"
                ></q-input>
            </template>
          </base-form>
        </q-card-section>
      </q-card>
    </div>
  </div>
</template>

<style src="./TaskEditForm.scss" lang="scss"></style>
