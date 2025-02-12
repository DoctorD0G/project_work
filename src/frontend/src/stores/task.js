import {defineStore} from 'pinia';
import {
  getTaskListApi,
  createTaskApi,
  updateTaskApi,
  getTaskByIdApi,
  deleteTaskApi,
  uploadFileApi
} from '@/api/tasks';
// eslint-disable-next-line no-unused-vars
import {ErrorHandle, NotifyHandle, FormValidationError} from 'cism-front-base';


export const useTaskStore = defineStore('task_store', {
  state: () => ({}),
  actions: {
    async getTaskList(page, rowsPerPage, sortBy, descending, filter) {
      try {
        return await getTaskListApi(page, rowsPerPage, sortBy, descending, filter);
      } catch (error) {
        throw new ErrorHandle(error, error.message);
      } finally {
      }
    },
    async createTaskAction(name) {
      try {
        await createTaskApi(name);
        new NotifyHandle('Задача успешно создана');
      } catch (error) {
        if (error.response.status === 422){
          throw new FormValidationError('Произошла ошибка при создании задачи', error.response.data);
        }
        else{
          throw new ErrorHandle(error, 'Произошла ошибка при создании задачи');
        }
      } finally {
      }
    },
    async updateTaskAction(id, formData) {
      try {
        formData.id = id;
        await updateTaskApi(formData);
        new NotifyHandle('Задача успешно отредактирована');
      } catch (error) {
        if (error.response.status === 422){
          throw new FormValidationError('Произошла ошибка при изменении задачи', error.response.data);
        }
        else{
          throw new ErrorHandle(error, 'Произошла ошибка при изменении задачи');
        }
      } finally {
      }
    },
    async getTaskByIdAction(id) {
      try {
        return await getTaskByIdApi(id);
      } catch (error) {
        throw new ErrorHandle(error, error.message);
      }
    },
    async deleteTaskAction(id) {
      try {
        return await deleteTaskApi(id);
      } catch (error) {
        throw new ErrorHandle(error, error.message);
      }
    },
    async uploadFile(formData){
      try {
        await uploadFileApi(formData);
        new NotifyHandle('Файл успешно загружен');
      } catch (error) {
        throw new ErrorHandle(error, 'Произошла ошибка при загрузке файла');
      } finally {
      }
    },
  }
});
