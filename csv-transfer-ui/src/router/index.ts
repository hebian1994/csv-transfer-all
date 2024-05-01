import { createRouter, createWebHistory } from 'vue-router';
import Users from '@/views/Users.vue';
import Welcome from '@/views/Welcome.vue';
import Home from '@/views/Home.vue';
import FileList from '@/views/FileList.vue';
import DefineConfig from '@/views/DefineConfig.vue';
import TemplateList from '@/views/TemplateList.vue';

const routes = [
  {
    path: '/',
    component: Home
  },
  {
    path: '/home',
    component: Home,
    redirect: '/welcome',
    children: [
      { path: '/file-list', component: FileList },
      { path: '/define-config', component: DefineConfig },
      { path: '/list-config', component: TemplateList },
      { path: '/welcome', component: Welcome },
      { path: '/users', component: Users }
    ]
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
