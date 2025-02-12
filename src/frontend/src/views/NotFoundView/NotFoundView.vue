<template>
  <div class="q-pa-md fixed-center">
    <div class="row">
      <div class="col error-page text-center">
        <div class="error-page__number">404</div>
        <div class="error-page__detail">
          Извините, страница которую вы ищете не существует. <br>Перейдите по
          кнопке на главную страницу.
        </div>
        <q-btn outline label="На главную" to="/" />
      </div>
    </div>
  </div>
</template>

<style src="./NotFoundView.scss" lang="scss"></style>
