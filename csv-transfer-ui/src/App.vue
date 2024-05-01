<template>
  <div id="app">
    <!-- 路由出口，路由匹配的组件将渲染在这里 -->
    <router-view></router-view>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import Home from './views/Home.vue';
export default defineComponent({
  name: 'App'
});
</script>

