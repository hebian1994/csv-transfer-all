import { createApp } from 'vue';
import App from './App.vue';
import ElementPlus from 'element-plus';
import api from './axios';

// main.js
import router from './router'; // 导入路由配置
import 'element-plus/dist/index.css';

createApp(App).provide('$axios', api).use(ElementPlus).use(router).mount('#app');

