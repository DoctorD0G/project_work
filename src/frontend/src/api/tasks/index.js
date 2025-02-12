import { api } from '../axios';

const API_ROOT = '/task';

export const getTaskListApi = async (page, rowsPerPage, sortBy, descending, filter) => {
  const params = {page: page, size: rowsPerPage, sort_field: sortBy, sort_descending: descending, filter: filter}
  const {data} = await api.get(`${API_ROOT}/`, {params: params});
  return data;
};

export const createTaskApi = async (name) => {
  const { data } = await api.post(`${API_ROOT}/`, {name: name});
  return data;
};

export const updateTaskApi = async (formData) => {
  const { data } = await api.put(`${API_ROOT}/`, formData);
  return data;
};

export const getTaskByIdApi = async (id) => {
  const { data } = await api.get(`${API_ROOT}/${id}/`, {});
  return data;
};

export const deleteTaskApi = async (id) => {
  const {data} = await api.delete(`${API_ROOT}/${id}/`, {});
  return data;
}

export const uploadFileApi = async (formData) => {
  const headers = {"Content-Type": "multipart/form-data", accept: 'application/json'}
  const { data } = await api.post(`${API_ROOT}/upload/file/`, formData, {headers: headers});
  return data;
};
