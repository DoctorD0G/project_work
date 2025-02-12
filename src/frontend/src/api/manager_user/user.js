import { api } from '../axios';


const API_ROOT = '/user-auth';

export const userLoginApi = async ({username, password}) => {
  const params = new URLSearchParams();
  params.append('username', username);
  params.append('password', password);

  const {data} = await api.post(`${API_ROOT}/token/`, params, {
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    }
  });
  return data;
};

export const getUserPermissionsApi = async () => {
  const {data} = await api.get(`${API_ROOT}/user/permissions/`);
  return data.result;
};
