import API from './api';

export const register = (userData: any) => {
  return API.post('/accounts/register/', userData);
};

export const login = (credentials: any) => {
  return API.post('/accounts/token/', credentials);
};

export const refreshToken = (refresh: string) => {
  return API.post('/accounts/token/refresh/', { refresh });
};
