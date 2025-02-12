import {defineStore} from 'pinia';
import {
  getPaginableUsersApi,
  changeUserAdminStateApi,
  createUserApi,
  deleteUserApi,
  getUserByIdApi,
  updateUserApi,
  updateUserPasswordApi
} from '@/api/manager_user/manager';
import {
  getAllRolesApi,
  getAllPermissionsApi,
  getPaginableRolesApi,
  deleteRoleApi,
  createRoleApi,
  getRoleByIdApi,
  updateRoleApi
} from '@/api/manager_user/role';
import { userLoginApi, getUserPermissionsApi } from '@/api/manager_user/user';

// eslint-disable-next-line no-unused-vars
import {ErrorHandle, NotifyHandle} from 'cism-front-base';

export const useUserStore = defineStore('user', {
  state: () => ({
    authData: {
      accessToken: '',
      isAuthenticated: false,
      isLoading: false,
      isAdmin: false,
    },
    userName: '',
    userPermissions: [],
  }),
  persist: {
    paths: ['authData', 'userName', 'userPermissions'],
  },
  actions: {
    setToken(data) {
      this.authData.accessToken = data.access_token || '';
      this.authData.isAuthenticated = true;
    },
    setPermission(data){
      this.authData.isAdmin = data.is_admin;
    },
    setUserName(name) {
      this.userName = name;
    },
    logout() {
      this.authData.accessToken = '';
      this.authData.isAuthenticated = false;
      this.userPermissions = [];
    },
    async userAuth({ username, password }) {
      try {
        this.authData.isLoading = true;
        const data = await userLoginApi({ username, password });
        this.setToken(data);
        this.setPermission(data);
        this.setUserName(username);
        new NotifyHandle('Вы успешно авторизовались!');
      } catch (error) {
        throw new ErrorHandle(error, 'Ошибка авторизации');
      } finally {
        this.authData.isLoading = false;
      }
    },
    async getPermissions() {
      try {
        this.userPermissions = await getUserPermissionsApi();
      } catch (error) {
        throw new ErrorHandle(error, 'Произошла ошибка при загрузке прав пользователя');
      }
    },
  },
});


export const useManagerUserStore = defineStore('manager-user', {
  state: () => ({}),
  actions: {
    async getPaginableUsers(page, rowsPerPage, sortBy, descending, filter) {
      try {
        return await getPaginableUsersApi(page, rowsPerPage, sortBy, descending, filter);
      } catch (error) {
        throw new ErrorHandle(error, error.message);
      } finally {
      }
    },
    async changeAdminStateAction(id, is_admin) {
      try {
        return await changeUserAdminStateApi({user_id: id, is_admin: is_admin});
      } catch (error) {
        throw new ErrorHandle(error, error.message);
      } finally {
      }
    },
    async createUserAction(formData) {
      try {
        await createUserApi(formData);
        new NotifyHandle('Пользователь успешно создан');
      } catch (error) {
        throw new ErrorHandle(error, 'Произошла ошибка при создании пользователя');
      } finally {
      }
    },
    async deleteUserAction(id) {
      try {
        await deleteUserApi(id);
        new NotifyHandle('Пользователь успешно удален');
      } catch (error) {
        throw new ErrorHandle(error, 'Произошла ошибка при удалении пользователя');
      }
    },
    async getUserByIdAction(id) {
      try {
        return await getUserByIdApi(id);
      } catch (error) {
        throw new ErrorHandle(error, error.message);
      }
    },
    async updateUserAction(id, formData) {
      try {
        await updateUserApi(id, formData);
        new NotifyHandle('Пользователь успешно отредактирован');
      } catch (error) {
        throw new ErrorHandle(error, 'Произошла ошибка при редактировании пользователя');
      } finally {
      }
    },
    async updateUserPasswordAction(id, password) {
      console.log(id)
      try {
        await updateUserPasswordApi(id, password);
        new NotifyHandle('Пароль пользователя успешно изменен');
      } catch (error) {
        throw new ErrorHandle(error, 'Произошла ошибка при изменении пароля пользователя');
      } finally {
      }
    },
  }
});


export const useManagerRoleStore = defineStore('manager-role', {
  state: () => ({}),
  actions: {
    async getAllRolesAction() {
      try {
        return await getAllRolesApi();
      } catch (error) {
        throw new ErrorHandle(error, error.message);
      } finally {
      }
    },
    async getAllPermissionsAction() {
      try {
        return await getAllPermissionsApi();
      } catch (error) {
        throw new ErrorHandle(error, error.message);
      } finally {
      }
    },
    async getPaginableRoles(page, rowsPerPage, sortBy, descending, filter) {
      try {
        return await getPaginableRolesApi(page, rowsPerPage, sortBy, descending, filter);
      } catch (error) {
        throw new ErrorHandle(error, error.message);
      } finally {
      }
    },
    async deleteRoleAction(id) {
      try {
        await deleteRoleApi(id);
        new NotifyHandle('Роль успешно удалена');
      } catch (error) {
        throw new ErrorHandle(error, 'Произошла ошибка при удалении роли');
      }
    },
    async createRoleAction(formData) {
      try {
        await createRoleApi(formData);
        new NotifyHandle('Роль успешно создана');
      } catch (error) {
        throw new ErrorHandle(error, 'Произошла ошибка при создании роли');
      } finally {
      }
    },
    async getRoleByIdAction(id) {
      try {
        return await getRoleByIdApi(id);
      } catch (error) {
        throw new ErrorHandle(error, error.message);
      }
    },
    async updateRoleAction(id, formData) {
      try {
        await updateRoleApi(id, formData);
        new NotifyHandle('Роль успешно отредактирована');
      } catch (error) {
        throw new ErrorHandle(error, 'Произошла ошибка при редактировании роли');
      } finally {
      }
    },
  }
});
