import { defineStore } from 'pinia';
import { getAppSettingsApi, updateAppSettingsApi } from '@/api/app_manager';
// eslint-disable-next-line no-unused-vars
import {ErrorHandle, NotifyHandle} from 'cism-front-base';


export const useAppManagerStore = defineStore('manager-app', {
  state: () => ({}),
  actions: {
    async getAppSettings() {
      try {
        return await getAppSettingsApi();
      } catch (error) {
        throw new ErrorHandle(error, error.message);
      } finally {
      }
    },
    async updateAppSettings(formData) {
      try {
        const app_settings = await updateAppSettingsApi(formData);
        new NotifyHandle('Настройки успешно применены');
        return app_settings;
      } catch (error) {
        throw new ErrorHandle(error, 'Произошла ошибка при редактировании настроек приложения');
      } finally {
      }
    },
  }
});
