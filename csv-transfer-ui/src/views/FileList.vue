<template>
    <el-input v-model="template_id" placeholder="template_id"></el-input>
    <el-upload ref="uploadRef" class="upload-demo" :auto-upload="false" :http-request="customUpload">
        <template #trigger>
            <el-button type="primary">Select file</el-button>
        </template>

        <el-button class="ml-3" type="success" @click="submitUpload">
            Upload to server
        </el-button>

    </el-upload>
</template>

<script lang="ts" setup>
import { reactive, ref, inject, onMounted } from 'vue'
import type { UploadInstance, UploadRequestOptions } from 'element-plus'
const $axios = inject("$axios");

const uploadRef = ref<UploadInstance>()
const template_id = ref('')
const submitUpload = () => {
    uploadRef.value!.submit();
}

const customUpload = async (options: UploadRequestOptions) => {
    const { file } = options;
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);
    formData.append('template_id', template_id.value);

    try {
        await $axios.post('/uploadFile', formData, {
            headers: {
                'Content-Type': 'multipart/form-data'
            },
        })
        alert('File uploaded successfully');
    } catch (error) {
        alert('File upload failed');
        console.error('File upload failed', error);
    }
}
</script>