<script setup lang="ts">
import { reactive, ref } from 'vue'
import { ElMessage } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'

import type { UploadProps } from 'element-plus'
import {Result} from '../../../../typings'
import { useUserStore } from '@/stores/user'


//加载片段 wxs
import { onMounted } from 'vue';

const isLoading = ref(true);
const Loading = ref(false);
onMounted(() => {
  setTimeout(() => {
    isLoading.value = false; 
    Loading.value = true;
}, 500);
});

const models = [
    { label: 'gpt-3.5-turbo', value: 0 },
    { label: 'gpt-4', value: 1 },
    { label: 'gpt-4-1106-preview', value: 2 }
]

//需要替换开始
const imageUrl = ref('')

const handleAvatarSuccess: UploadProps['onSuccess'] = (
    response,
    uploadFile
) => {
    imageUrl.value = URL.createObjectURL(uploadFile.raw!)
}
//需要替换结束

//写好后端后将注释掉的内容替换掉

// const {userInfo} = toRefs(useUserStore())

// const handleAvatarSuccess: UploadProps['onSuccess'] = (
//     response:Result<{url:string}>
// ) => {
//     user.value.avatar = response.result.url
// }
// const submit=()=>{
//     saveUser(userInfo.value).then((res)=>{
//         if(res.success){
//             ElMessage.success('提交成功')
//         }
//     })
// }



const beforeAvatarUpload: UploadProps['beforeUpload'] = (rawFile) => {
    if (rawFile.type !== 'image/jpeg') {
        ElMessage.error('Avatar picture must be JPG format!')
        return false
    } else if (rawFile.size / 1024 / 1024 > 2) {
        ElMessage.error('Avatar picture size can not exceed 2MB!')
        return false
    }
    return true
} 
</script>

<template>
    <!-- 加载动画 wxs -->
    <div v-if="isLoading">  
    <!-- 这里放置加载动画 -->
    <div class="loader-container">
      <div class="loader"></div>
    </div>
    </div>


    <div v-if="Loading">
    <Transition appear name="a">
    <div class="profile-view">
        <div class="title">我的信息</div>
        <el-form class="form" label-position="top">
            <el-form-item label="昵称">
                <!-- <el-input v-model="userInfo.nickname"></el-input> -->
                <el-input></el-input>
            </el-form-item>
            <el-form-item label="头像">
                <el-upload class="avatar-uploader" action="https://run.mocky.io/v3/9d059bf9-4660-45f2-925d-ce80ad6c4d15"
                    :show-file-list="false" :on-success="handleAvatarSuccess" :before-upload="beforeAvatarUpload">
                    <!-- <img v-if="userInfo.avatar" :src="userInfo.avatar" class="avatar" /> -->
                    <img v-if="imageUrl" :src="imageUrl" class="avatar" />
                    <el-icon v-else class="avatar-uploader-icon">
                        <Plus />
                    </el-icon>
                </el-upload>
            </el-form-item>
        </el-form>
        <!-- <el-button type="success" size="large" @click="submit">提交修改</el-button> -->
        <el-button type="success" size="large">提交修改</el-button>
    </div>
    </Transition>
    </div>
</template>

<style scoped lang="scss">
.profile-view {
    .title {
        font-size: 18px;
        margin-bottom: 20px;
    }

    .avatar-uploader .avatar {
        width: 120px;
        height: 120px;
        display: block;
    }
}
</style>

<style>
.avatar-uploader .el-upload {
    border: 1px dashed var(--el-border-color);
    border-radius: 6px;
    cursor: pointer;
    position: relative;
    overflow: hidden;
    transition: var(--el-transition-duration-fast);
}

.avatar-uploader .el-upload:hover {
    border-color: var(--el-color-primary);
}

.el-icon.avatar-uploader-icon {
    font-size: 28px;
    color: #8c939d;
    width: 120px;
    height: 120px;
    text-align: center;
}


/* 过渡动画样式 wxs */
  .loader {
  display: flex;
  width: 3.5em;
  height: 3.5em;
  border: 3px solid transparent;
  border-top-color: #3cefff;
  border-bottom-color: #3cefff;
  border-radius: 50%;
  animation: spin 1.5s linear infinite;
}

.loader:before {
  content: '';
  display: block;
  margin: auto;
  width: 0.75em;
  height: 0.75em;
  border: 3px solid #3cefff;
  border-radius: 50%;
  animation: pulse 1s alternate ease-in-out infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

@keyframes pulse {
  from {
    transform: scale(0.5);
  }
  to {
    transform: scale(1);
  }
}


.a-enter-active {
  transition: all 0.3s ease-out;
}

.a-leave-active {
  transition: all 0.8s cubic-bezier(1, 0.5, 0.8, 1);
}

.a-enter-from,
.a-leave-to {
  transform: translateX(20px);
  opacity: 0;
}

</style>