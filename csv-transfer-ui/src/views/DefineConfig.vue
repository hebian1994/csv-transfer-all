<template>
    <el-form ref="ruleFormRef" style="max-width: 600px" :model="ruleForm" :rules="rules" label-width="auto"
        label-position="left" class="demo-ruleForm" :size="formSize" status-icon>
        <el-form-item label="Template name" prop="templateName">
            <el-input v-model="ruleForm.templateName" />
        </el-form-item>
        <el-form-item label="Header line number" prop="headerLineNum">
            <el-input v-model="ruleForm.headerLineNum" />
        </el-form-item>
        <el-form-item label="Rows num delete from head" prop="rowDelFromHead">
            <el-input v-model="ruleForm.rowDelFromHead" />
        </el-form-item>
        <el-form-item label="Rows num delete from tail" prop="rowDelFromTail">
            <el-input v-model="ruleForm.rowDelFromTail" />
        </el-form-item>

        <el-form-item label="Columns delete" prop="colDeleted">
            <div v-for="(input, index) in ruleForm.colDeleted" :key="index">
                <el-input v-model="ruleForm.colDeleted[index]" />
                <el-button @click="addInput" type="primary" size="small">add</el-button>
                <el-button @click="removeInput(index)" type="danger" size="small">del</el-button>
            </div>
        </el-form-item>

        <el-form-item label="Columns transfer">
            <el-row v-for="(item, index) in ruleForm.colTransfer" :key="index">
                <el-col :span="5">
                    <el-input v-model="item.colName" placeholder="name"></el-input>
                </el-col>
                <el-col :span="5">
                    <!-- <el-input v-model="item.tranType" placeholder="type"></el-input> -->
                    <el-select v-model="item.tranType" placeholder="type">
                        <el-option label="text: Replace A with B" value="text1"></el-option>
                        <el-option label="text: Substring and retain [1,5]" value="text2"></el-option>
                        <el-option label="date: yyyyMMdd to ddMMyyyy" value="date1"></el-option>
                        <el-option label="date: yyyy-MM-dd to ddMMyyyy" value="date2"></el-option>
                        <el-option label="decimal: Keep N decimal places" value="decimal"></el-option>
                    </el-select>
                </el-col>
                <el-col :span="14">
                    <el-input v-model="item.reg" placeholder="json"></el-input>
                </el-col>

                <el-button type="primary" @click="addRow" size="small">add</el-button>
                <el-button type="danger" @click="deleteRow(index)" size="small">del</el-button>
            </el-row>
        </el-form-item>


        <el-form-item label="Columns rename" prop="colRename">
            <el-row v-for="(item, index) in ruleForm.colRename" :key="index">
                <el-col :span="8">
                    <el-input v-model="item.nowColName" placeholder="current name"></el-input>
                </el-col>
                <el-col :span="8">
                    <el-input v-model="item.newColName" placeholder="new name"></el-input>
                </el-col>
                <el-button type="primary" @click="addRowRn" size="small">add</el-button>
                <el-button type="danger" @click="deleteRn(index)" size="small">del</el-button>
            </el-row>
        </el-form-item>


        <el-form-item>
            <el-button type="primary" @click="submitForm(ruleFormRef)">
                Create
            </el-button>
            <el-button @click="resetForm(ruleFormRef)">Reset</el-button>
        </el-form-item>
    </el-form>
</template>

<script lang="ts" setup>
import { reactive, ref, inject } from 'vue'
import type { ComponentSize, FormInstance, FormRules } from 'element-plus'


interface ColumnTransferRow {
    colName: string;
    tranType: string;
    reg: string;
}

interface ColumnRenameRow {
    nowColName: string;
    newColName: string;
}

interface RuleForm {
    templateName: string
    headerLineNum: string
    rowDelFromHead: string
    rowDelFromTail: string
    colDeleted: string[]
    colTransfer: ColumnTransferRow[]
    colRename: ColumnRenameRow[]
}

const formSize = ref<ComponentSize>('default')
const ruleFormRef = ref<FormInstance>()
const ruleForm = reactive<RuleForm>({
    templateName: '',
    headerLineNum: '',
    rowDelFromHead: '',
    rowDelFromTail: '',
    colDeleted: [""],
    colTransfer: [
        { colName: '', tranType: '', reg: '' } // 初始化一行，每个列都有一个空字符串
    ],
    colRename: [{ nowColName: '', newColName: '' }],
})

const locationOptions = ['Home', 'Company', 'School']

const rules = reactive<FormRules<RuleForm>>({
    // name: [
    //     { required: false, message: 'Please input Header row number', trigger: 'blur' },
    //     { min: 3, max: 5, message: 'Length should be 3 to 5', trigger: 'blur' },
    // ],
    // region: [
    //     {
    //         required: false,
    //         message: 'Please select Rows delete from head',
    //         trigger: 'change',
    //     },
    // ],
    // count: [
    //     {
    //         required: false,
    //         message: 'Please select Activity count',
    //         trigger: 'change',
    //     },
    // ],
    // date1: [
    //     {
    //         type: 'date',
    //         required: false,
    //         message: 'Please pick a date',
    //         trigger: 'change',
    //     },
    // ],
    // date2: [
    //     {
    //         type: 'date',
    //         required: false,
    //         message: 'Please pick a time',
    //         trigger: 'change',
    //     },
    // ],
    // location: [
    //     {
    //         required: false,
    //         message: 'Please select a location',
    //         trigger: 'change',
    //     },
    // ],
    // type: [
    //     {
    //         type: 'array',
    //         required: false,
    //         message: 'Please select at least one activity type',
    //         trigger: 'change',
    //     },
    // ],
    // resource: [
    //     {
    //         required: false,
    //         message: 'Please select activity resource',
    //         trigger: 'change',
    //     },
    // ],
    // desc: [
    //     { required: false, message: 'Please input activity form', trigger: 'blur' },
    // ],
})
const $axios = inject("$axios");
const submitForm = async (formEl: FormInstance | undefined) => {
    if (!formEl) return
    await formEl.validate((valid, fields) => {
        console.log('submit!', fields)
        if (valid) {
            console.log('submit!')
        } else {
            console.log('error submit!', fields)
        }
    })

    console.log(ruleForm)
    try {
        const response = await $axios.post('/template/create', { 'data': ruleForm });
        console.log(response.data);
    } catch (error) {
        console.error(error);
    }
}

const resetForm = (formEl: FormInstance | undefined) => {
    if (!formEl) return
    formEl.resetFields()
}

const addInput = () => {
    ruleForm.colDeleted.push(""); // 添加一个新的空字符串到数组中
}
const removeInput = (index: any) => {
    ruleForm.colDeleted.splice(index, 1); // 从数组中移除指定索引的输入框
}

const addRow = () => {
    ruleForm.colTransfer.push({ colName: '', tranType: '', reg: '' }); // 添加一个新行
}
const deleteRow = (index: any) => {
    ruleForm.colTransfer.splice(index, 1); // 删除指定索引的行
}

const addRowRn = () => {
    ruleForm.colRename.push({ nowColName: '', newColName: '' }); // 添加一个新行
}
const deleteRn = (index: any) => {
    ruleForm.colRename.splice(index, 1); // 删除指定索引的行
}

const options = Array.from({ length: 10000 }).map((_, idx) => ({
    value: `${idx + 1}`,
    label: `${idx + 1}`,
}))
</script>

<style>
/* 基本样式，确保所有标签具有相同的字体大小和行高 */
.el-form-item__label {
    font-size: 14px;
    /* 根据需要调整大小 */
    line-height: 1.5;
    /* 根据需要调整行高 */
}

/* 对于单行文本，使用text-align: justify并添加伪元素来对齐 */
.justify-label .el-form-item__label {
    text-align: justify;

    &:after {
        content: '';
        display: inline-block;
        width: 100%;
    }
}

/* 对于多单词文本，可能需要更复杂的解决方案来对齐 */
.multiword-label .el-form-item__label {
    display: flex;
    align-items: center;
}

/* 对于特定长度的单词，可以手动调整对齐 */
.id-card-label {
    padding-left: 20px;
    /* 调整这个值来实现对齐 */
}

.house-price-label {
    padding-left: 25px;
    /* 调整这个值来实现对齐 */
}
</style>