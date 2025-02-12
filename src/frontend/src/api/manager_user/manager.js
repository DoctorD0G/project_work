import { api } from '../axios';

const API_ROOT = '/user-manager';

export const getPaginableUsersApi = async (page, rowsPerPage, sortBy, descending, filter) => {
  const params = {page: page, size: rowsPerPage}
  const {data} = await api.get(`${API_ROOT}/user/`, {params: params});
  return data;
};

export const changeUserAdminStateApi = async (data) => {
  return await api.post(`${API_ROOT}/user/set-unset/admin/`, data);
};

export const createUserApi = async (formData) => {
  const { data } = await api.post(`${API_ROOT}/user/create/`, formData);
  return data;
};

export const deleteUserApi = async (id) => {
  return await api.delete(`${API_ROOT}/user/${id}/`);
};

export const getUserByIdApi = async (id) => {
  const { data } = await api.get(`${API_ROOT}/user/${id}/`, {});
  return data;
};

export const updateUserApi = async (id, formData) => {
  const { data } = await api.post(`${API_ROOT}/user/update/${id}/`, formData);
  return data;
};

export const updateUserPasswordApi = async (id, password) => {
  const { data } = await api.post(`${API_ROOT}/user/change-passwd/`, {user_id: id, password: password});
  return data;
};
