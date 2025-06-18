import { publicApi } from './axios';

export const login = (credentials) => publicApi.post('users/login/', credentials);
export const signup = (userData) => publicApi.post('users/signup/', userData);
