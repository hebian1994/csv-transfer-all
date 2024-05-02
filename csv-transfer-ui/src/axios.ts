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
    // 判断如果是上传文件的请求，设置Content-Type为multipart/form-data
    if (config.url === '/uploadFile') {
      config.headers['Content-Type'] = 'multipart/form-data';
      config.headers['responseType'] = 'blob';
      console.log(config, '111')
    }
    console.log(config, '111')
    return config;
  },
  (error: any) => {
    // 对请求错误做些什么
    return Promise.reject(error);
  }
);

// 响应拦截器
api.interceptors.response.use(
  (response: any) => {
    // 对响应数据做点什么
    const contentType = response.headers['content-type'];
    if (contentType && contentType.includes('text/csv')) {
      // 如果响应是CSV，则触发下载
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      console.log(response.headers,'response.headers')
      const contentDisposition = response.headers['content-disposition'];
      let filename = 'A.csv'; // 默认文件名
      console.log(contentDisposition,'contentDisposition')
      if (contentDisposition) {
        const filenameMatch = contentDisposition.match(/filename=(["']?)([^"]+)/);
        if (filenameMatch) {
          filename = filenameMatch[2]; // 使用后端提供的文件名
        }
      }
      link.href = url;
      link.setAttribute('download', filename); // 文件名
      document.body.appendChild(link);
      link.click();

      // 清理链接和URL对象
      if (link.parentNode) {
        link.parentNode.removeChild(link);
      }
      window.URL.revokeObjectURL(url);
    }


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
