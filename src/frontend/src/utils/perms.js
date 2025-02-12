import {useUserStore} from '@/stores/manager-user';

export const appPermissions = {
  IS_AUTHENTICATED: 'is_authenticated',
  IS_ADMIN: 'admin',

  CISM_USER_EDIT_PERMISSION: 'cism_user:edit',
  CISM_USER_READ_PERMISSION: 'cism_user:read',

  APP_SETTINGS_VIEW_PERMISSION: 'app_settings:read',
  APP_SETTINGS_EDIT_PERMISSION: 'app_settings:edit',

  TASK_VIEW_PERMISSION: 'task:read',
  TASK_EDIT_PERMISSION: 'task:edit',
}
export const hasAccess = (pemSlug) => {
  const store = useUserStore();
  const permissions = store.userPermissions || [];

  if (store.authData.isAdmin) {
    return true
  } else if (pemSlug === appPermissions.IS_AUTHENTICATED) {
    return store.authData.isAuthenticated
  } else {
    return permissions.includes(pemSlug);
  }
}

