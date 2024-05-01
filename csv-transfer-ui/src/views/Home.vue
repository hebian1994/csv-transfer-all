<template>
  <el-row>
    <el-col :span="3">
      <el-aside>
        <el-radio-group v-model="isCollapse" style="margin-bottom: 20px">
          <el-radio-button :value="false">expand</el-radio-button>
          <el-radio-button :value="true">collapse</el-radio-button>
        </el-radio-group>
        <el-menu default-active="2" class="el-menu-vertical-demo" :collapse="isCollapse" @open="handleOpen"
          @close="handleClose" :router="true">
          <el-sub-menu index="1">
            <template #title>
              <!-- <el-icon>
                <location />
              </el-icon> -->
              <span>File transfer</span>
            </template>
            <el-menu-item-group>
              <!-- <el-menu-item index="/users">item one</el-menu-item> -->
              <el-menu-item index="/define-config">ConfigDefine</el-menu-item>
              <el-menu-item index="/list-config">ConfigList</el-menu-item>
              <el-menu-item index="/file-list">FileList</el-menu-item>
            </el-menu-item-group>
          </el-sub-menu>
        </el-menu>
      </el-aside>
    </el-col>
    <el-col :span="10">
      <!-- 右侧内容主体区域 -->
      <el-main>
        <!-- 路由占位符 -->
        <router-view></router-view>
      </el-main>
    </el-col>
  </el-row>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import {
  Document,
  Menu as IconMenu,
  Location,
  Setting,
} from '@element-plus/icons-vue'

const isCollapse = ref(false)
const handleOpen = (key: string, keyPath: string[]) => {
  console.log(key, keyPath)
}
const handleClose = (key: string, keyPath: string[]) => {
  console.log(key, keyPath)
}
</script>

<style>
.el-menu-vertical-demo:not(.el-menu--collapse) {
  width: 200px;
  min-height: 400px;
}
</style>
