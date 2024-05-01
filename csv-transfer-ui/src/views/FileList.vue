<template>
    <div>
        <el-input v-model="template_id" placeholder="template_id"></el-input>
        <el-upload class="upload-demo" ref="upload" :on-preview="handlePreview" :on-remove="handleRemove"
            :file-list="fileList" :auto-upload="false" multiple="true" :on-success="handleSelected"
            :on-change="handleSelected">
            <el-button type="primary">选取文件</el-button>
        </el-upload>
        <el-button type="success" @click="submitUpload">上传到服务器</el-button>

    </div>
</template>
<script setup>
import { ref, inject } from 'vue';

const template_id = ref('')
const fileList = ref([]);
const fileListWaitUpload = ref([]);

const $axios = inject("$axios");

function handleSelected(file) {
    console.log('handleSelected', file);
    console.log(file);
    console.log(file.name);
    console.log(typeof file);
    fileListWaitUpload.value.push(file.name);
    console.log(typeof fileListWaitUpload.value);
}

function submitUpload() {
    console.log('submitUpload');
    console.log($axios)
    try {
        const response = $axios.post('/uploadFile', { 'data': fileListWaitUpload.value, 'templateId': template_id.value });
        console.log(response.data);
    } catch (error) {
        console.error(error);
    }
}

function handleRemove(file, fileList) {
    console.log('handleRemove');
    console.log(file, fileList);
}

function handlePreview(file) {
    console.log('handlePreview');
    console.log(file);
    fileListWaitUpload.value = file;
}

// 处理其他参数
function handleOtherParams(params) {
    const formData = new FormData();
    if (typeof params === 'object' && params) {
        Object.keys(params).forEach(k => {
            formData.append(k, params[k]);
        });
    }
    return formData;
}

</script>
