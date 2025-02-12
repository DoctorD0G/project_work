import {createApp} from 'vue';
import {createPinia} from 'pinia';
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate';
import * as Sentry from "@sentry/vue";
import {Dialog, Meta, Notify, Quasar} from 'quasar';
import lang from 'quasar/lang/ru';
import VueKeycloakJs from '@dsb-norge/vue-keycloak-js'
import CismBase from 'cism-front-base'

import App from './App.vue';
import router from './router';


// Import icon libraries
import '@quasar/extras/material-icons/material-icons.css';

// Import Quasar css
import 'quasar/src/css/index.sass';

// Import app css
import './assets/styles/index.scss';

const app = createApp(App);
const pinia = createPinia();
pinia.use(piniaPluginPersistedstate);

Sentry.init({
  app,
  dsn: import.meta.env.VITE_SENTRY_DSN || config.VITE_SENTRY_DSN,
  integrations: [
    new Sentry.BrowserTracing({
      routingInstrumentation: Sentry.vueRouterInstrumentation(router),
    }),
    new Sentry.Replay(),
  ]
});

app.use(Quasar, {
  plugins: {
    Notify,
    Dialog,
    Meta
  },
  lang: lang,
});
app.use(pinia);
app.use(CismBase);

app.use(router);
  app.mount('#app');
