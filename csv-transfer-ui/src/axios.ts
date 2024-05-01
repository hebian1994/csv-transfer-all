// src/axios.ts
import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse } from 'axios';

const api: AxiosInstance = axios.create({
  baseURL: 'http://localhost:5000/api',
  timeout: 1000,
});

// 请求拦截器
api.interceptors.request.use(
  (config: any) => {
    // 在发送请求前做些什么
    // 比如添加认证信息到headers
    config.headers.Authorization = `Bearer ${localStorage.getItem('token')}`;
    // 设置允许跨域的头部（这通常是在服务器端设置的，客户端设置可能不会生效）
    config.headers['Access-Control-Allow-Origin'] = '*';
    return config;
  },
  (error: any) => {
    // 对请求错误做些什么
    return Promise.reject(error);
  }
);

// 响应拦截器
api.interceptors.response.use(
  (response: AxiosResponse) => {
    // 对响应数据做点什么
    return response;
  },
  (error: any) => {
    // 对响应错误做点什么
    if (error.response && error.response.status === 401) {
      // 处理认证失败
    }
    return Promise.reject(error);
  }
);

export default api;
