import { api } from '../axios';

const API_ROOT = '/user-role';


export const getAllRolesApi = async () => {
  const {data} = await api.get(`${API_ROOT}/role-all/`, {});
  return data;
};

export const getAllPermissionsApi = async () => {
  const {data} = await api.get(`/user-auth/service/permissions/`, {});
  return data;
};

export const getPaginableRolesApi = async (page, rowsPerPage, sortBy, descending, filter) => {
  const params = {page: page, size: rowsPerPage}
  const {data} = await api.get(`${API_ROOT}/role/`, {params: params});
  return data;
};

export const deleteRoleApi = async (id) => {
  return await api.delete(`${API_ROOT}/role/${id}/`);
};

export const createRoleApi = async (formData) => {
  const { data } = await api.post(`${API_ROOT}/role/create/`, formData);
  return data;
};


export const getRoleByIdApi = async (id) => {
  const { data } = await api.get(`${API_ROOT}/role/${id}/`, {});
  return data;
};

export const updateRoleApi = async (id, formData) => {
  const { data } = await api.post(`${API_ROOT}/role/update/${id}/`, formData);
  return data;
};
