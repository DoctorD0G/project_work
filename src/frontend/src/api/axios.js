import axios from 'axios';
import { useUserStore } from '@/stores/manager-user';

export const api = axios.create({
  baseURL: config.VITE_FRONT_API_URL || import.meta.env.VITE_FRONT_API_URL,
  headers: { 'Content-Type': 'application/json' },
});


api.interceptors.request.use(
(config) => {
    config.withCredentials = true;

    const store = useUserStore();
    if (store.authData.isAuthenticated) {
      const token = store.authData.accessToken || '';
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (err) => Promise.reject(err)
);

api.interceptors.response.use(
  (res) => res,
  async (err) => {
    if (err.response) {
      if (err.response.status === 401 && window.location.pathname !== '/auth') {
        const store = useUserStore();
        store.logout();
        const fullPath = router.currentRoute.value.fullPath;
        void router.push({
          path: '/auth',
          query: fullPath === '/' ? null : {redirect: fullPath},
        });
      }
    }
    return Promise.reject(err);
  }
);
