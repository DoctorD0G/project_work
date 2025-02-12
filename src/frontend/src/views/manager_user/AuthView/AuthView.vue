<script setup>
import {ref} from 'vue';
import { useRouter } from 'vue-router';
import {useUserStore} from '@/stores/manager-user';

const store = useUserStore();
const router = useRouter()

const username = ref('');
const pass = ref('');

const onSubmit = async () => {
  await store.userAuth({username: username.value, password: pass.value});
  await store.getPermissions();
  router.push('/');
};
</script>

<template>
    <div class="fixed-center auth-page">
        <q-card flat bordered>
          <q-card-section class="q-pt-none">
            <div class="auth-page__title-logo">
              <img src="~/cism-front-base/src/assets/images/logo_invert.svg" alt="Logo" />
            </div>

            <h5 class="auth-page__title">Войдите в систему</h5>

            <q-form class="auth-page__form" @submit="onSubmit">
              <q-input
                class="auth-page__field"
                v-model="username"
                placeholder="Логин"
                :rules="[(val) => (val || '').length || 'Обязательное поле']"
                :disable="store.authData.isLoading"
                lazy-rules
              />
              <q-input
                class="auth-page__field"
                v-model="pass"
                placeholder="Пароль"
                type="password"
                 lazy-rules
                :rules="[(val) => (val || '').length || 'Обязательное поле']"
                :disable="store.authData.isLoading"
              />
              <q-btn
                label="Войти"
                type="submit"
                outline
                :loading="store.authData.isLoading"
              />
            </q-form>
          </q-card-section>
        </q-card>
    </div>
</template>

<style src="./AuthView.scss" lang="scss"></style>
