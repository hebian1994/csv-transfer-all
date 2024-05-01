<template>
    <div>
        <el-table :data="tableData" style="width: 100%">
            <el-table-column prop="id" label="ID" width="180"></el-table-column>
            <el-table-column prop="t_name" label="Template Name" width="180"></el-table-column>
            <el-table-column label="Details" width="180">
                <template #default="scope">
                    <el-button @click="showDetail(scope.row)" type="text" size="small">Details</el-button>
                    <el-button @click="deleteRecord(scope.row)" type="text" size="small">Delete</el-button>
                </template>
            </el-table-column>
        </el-table>
    </div>
    <el-dialog v-model="dialogVisible" title="Template Details" width="500" :before-close="handleClose">
        <el-form :model="selectedRow" label-position="left" label-width="100px">
            <!-- <el-form-item v-for="(value, key) in selectedRow" :key="key" :label="key">
                <el-input v-model="selectedRow[key]" :disabled="true"></el-input>
            </el-form-item> -->
            <el-form-item label="id">
                <el-input v-model="selectedRow['id']" :disabled="true"></el-input>
            </el-form-item>
            <el-form-item label="name">
                <el-input v-model="selectedRow['t_name']" :disabled="true"></el-input>
            </el-form-item>
            <el-form-item label="config">
                <el-input v-model="selectedRow['json_config']" :disabled="true" style="width: 500px"
                    :autosize="{ minRows: 2, maxRows: 8 }" type="textarea"></el-input>
            </el-form-item>
        </el-form>
        <template #footer>
            <div class="dialog-footer">
                <el-button @click="dialogVisible = false">Cancel</el-button>
            </div>
        </template>
    </el-dialog>
</template>

<script lang="ts" setup>
import { reactive, ref, inject, onMounted } from 'vue'
import { ElMessageBox } from 'element-plus'


const tableData = ref()
const dialogVisible = ref(false)
const selectedRow = ref()
const $axios = inject("$axios");

const showDetail = (row: any) => {
    console.log("showDetail")
    console.log(row)
    selectedRow.value = row;
    selectedRow.value.json_config = JSON.stringify(JSON.parse(row.json_config), null, 2);
    dialogVisible.value = true;
}

const deleteRecord = async (row) => {
    console.log("deleteRecord");
    try {
        const response = await $axios.post('/template/delete', { 'id': row.id });
        if (response) {
            console.log("delete success");
            // 删除成功后，再调用 fetchData 来更新列表
            await fetchData();
            console.log("fetchData called after delete success");
        }
    } catch (error) {
        console.error('Error deleting record:', error);
    }
}

const fetchData = async () => {
    console.log("fetchData");
    try {
        const response = await $axios.get('/template/list-all');
        tableData.value = response.data.data;
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}


const handleClose = (done: () => void) => {
    ElMessageBox.confirm('Are you sure to close this dialog?')
        .then(() => {
            done()
        })
        .catch(() => {
            // catch error
        })
}

onMounted(fetchData)

</script>