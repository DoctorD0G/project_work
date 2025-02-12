import {createRouter, createWebHistory} from 'vue-router';
import routes from './routes';
import {hasAccess} from '@/utils/perms';
import { useUserStore } from '@/stores/manager-user';

const webHistory = createWebHistory("#")

const router = createRouter({
  history: webHistory,
  routes,
});

router.beforeEach((to, _from, next) => {
  const store = useUserStore();

  const getAccessRedirect = () => {
    if (to?.meta?.perms) {
      const canAccess = hasAccess(to.meta.perms);
      if (!canAccess) next({path: '/'});
      else next();
    } else {
      next();
    }
  };

  if (to.path === '/auth' && store.authData.isAuthenticated) {
    return next('/');
  }

  if (to.path !== '/auth') {
    if (store.authData.isAuthenticated) {
      getAccessRedirect();
    } else {
      next({
        path: '/auth',
        query: to.fullPath === '/' ? null : {redirect: to.fullPath},
      });
    }
  } else {
    next();
  }
  next();
});


export default router;
