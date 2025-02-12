import { api } from '../axios';

const API_ROOT = '/app-manager';

export const getAppSettingsApi = async () => {
  const { data } = await api.get(`${API_ROOT}/`);
  return data;
};

export const updateAppSettingsApi = async (formData) => {
  const { data } = await api.put(`${API_ROOT}/`, formData);
  return data;
};
