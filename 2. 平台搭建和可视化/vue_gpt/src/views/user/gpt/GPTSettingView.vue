<script setup lang="ts">

//加载片段 wxs
import {ref, onMounted } from 'vue';

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

//后端写好后取消注释
// const chatConfig = ref<ChatConfig>({
//   temperature: 0,
//   maxTokens: 2000,
//   presencePenalty: 0,
//   model: 0
// } as ChatConfig)
// onMounted(() => {
//   getUserChatConfig().then((res) => {
//     if (res.result) {
//       chatConfig.value = res.result
//     }
//   })
// })
// const submit = () => {
//   saveChatConfig(chatConfig.value).then((res) => {
//     assertSuccess(res).then((res) => {
//       chatConfig.value.id = res.result
//     })
//   })
// }
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
    <div class="gpt-view">
        <div class="title">GPT设置</div>
        <el-form label-position="top">
            <el-form-item label="GPT模型">
                <!-- 后端写好后替换 -->
                <!-- <el-select v-model="chatConfig.model"> -->
                <el-select>
                    <el-option v-for="model in models" :key="model.value" :value="model.value"
                        :label="model.label"></el-option>
                </el-select>
            </el-form-item>
            <el-form-item label="话题随机性">
                <!-- 后端写好后替换 -->
                <!-- <el-input-number :max="1" :min="0" :step="0.1" v-model="chatConfig.temperature"></el-input-number> -->
                <el-input-number :max="1" :min="0" :step="0.1"></el-input-number>
            </el-form-item>
            <el-form-item label="单词回复Token">
                <!-- 后端写好后替换 -->
                <!-- <el-input-number :max="4000" :min="0" :step="1" v-model="chatConfig.maxTokens"></el-input-number> -->
                <el-input-number :max="4000" :min="0" :step="1"></el-input-number>
            </el-form-item>
            <el-form-item label="话题新鲜度">
                <!-- 后端写好后替换 -->
                <!-- <el-input-number :max="2" :min="-2" :step="0.1" v-model="chatConfig.presencePenalty"></el-input-number> -->
                <el-input-number :max="2" :min="-2" :step="0.1"></el-input-number>
            </el-form-item>
            <el-form-item label="API Key">
                <!-- 后端写好后替换 -->
                <!-- <el-input v-model="chatConfig.apiKey" type="password"></el-input> -->
                <el-input type="password"></el-input>
            </el-form-item>
        </el-form>
        <!-- 后端写好后替换 -->
        <!-- <el-button type="success" @click="submit">提交保存</el-button> -->
        <el-button type="success">提交保存</el-button>
    </div>
    </Transition>
    </div>
</template>

<style scoped lang="scss">
.gpt-view{
    .title{
        font-size: 18px;
        margin-bottom: 20px;
    }
}

  //过渡动画样式 wxs
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