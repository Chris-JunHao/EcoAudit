<!--<script lang="ts" setup>-->
<!--import { ref, onMounted } from 'vue'-->
<!--import { useRoute } from 'vue-router'-->

<!--// 获取路由参数-->
<!--const route = useRoute()-->
<!--const provinceName = ref(route.params.name)-->

<!--// 假设每个省份的水质数据-->
<!--const provinceData = ref({-->
<!--  pH: 7.5,-->
<!--  oxygen: 8.0,-->
<!--  conductivity: 1.2-->
<!--})-->

<!--// 模拟省份的数据-->
<!--onMounted(() => {-->
<!--  // 这里你可以根据省份名称去设置具体的数据-->
<!--})-->
<!--</script>-->

<!--<template>-->
<!--  <div class="province-detail-page">-->
<!--    <h2>{{ provinceName }}省水质监测详情</h2>-->
<!--    <div class="water-data">-->
<!--      <p>PH 值: {{ provinceData.pH }}</p>-->
<!--      <p>溶解氧: {{ provinceData.oxygen }} mg/L</p>-->
<!--      <p>电导率: {{ provinceData.conductivity }} S/m</p>-->
<!--    </div>-->
<!--  </div>-->
<!--</template>-->

<!--<style scoped>-->
<!--.province-detail-page {-->
<!--  padding: 20px;-->
<!--  text-align: center;-->
<!--  background-image: url('@/assets/home/Background.png'); /* 引用图片 */-->
<!--  background-size: cover; /* 确保背景图片覆盖整个区域 */-->
<!--  background-position: center; /* 图片居中 */-->
<!--}-->

<!--.water-data {-->
<!--  margin-top: 20px;-->
<!--  font-size: 18px;-->
<!--}-->
<!--</style>-->


<!--<script lang="ts" setup>-->
<!--import { ref, computed, onMounted } from 'vue'-->
<!--import { useRoute } from 'vue-router'-->

<!--// 获取路由参数-->
<!--const route = useRoute()-->
<!--const provinceName = ref(route.params.name)-->

<!--// 假设每个省份的水质数据-->
<!--const provinceData = ref({-->
<!--  pH: 7.5,-->
<!--  oxygen: 8.0,-->
<!--  conductivity: 1.2-->
<!--})-->

<!--// 模拟省份的数据-->
<!--onMounted(() => {-->
<!--  // 这里你可以根据省份名称去设置具体的数据-->
<!--})-->

<!--// 当前选择的功能模块-->
<!--const currentTab = ref<'dataDisplay' | 'dataUpdate' | 'riverSelection'>('dataDisplay')-->

<!--// 动态组件-->
<!--const components: Record<'dataDisplay' | 'dataUpdate' | 'riverSelection', () => Promise<typeof import('*.vue')>> = {-->
<!--  dataDisplay: () => import('./components/DataDisplay.vue'),-->
<!--  dataUpdate: () => import('./components/DataUpdate.vue'),-->
<!--  riverSelection: () => import('./components/RiverSelection.vue')-->
<!--}-->

<!--// 计算当前显示的组件-->
<!--const currentComponent = computed(() => components[currentTab.value])-->
<!--</script>-->
<!--<template>-->
<!--  <div class="province-detail-page">-->
<!--    <div class="sidebar">-->
<!--      <ul>-->
<!--        <li @click="currentTab = 'dataDisplay'" :class="{ active: currentTab === 'dataDisplay' }">数据展示</li>-->
<!--        <li @click="currentTab = 'dataUpdate'" :class="{ active: currentTab === 'dataUpdate' }">数据更新</li>-->
<!--        <li @click="currentTab = 'riverSelection'" :class="{ active: currentTab === 'riverSelection' }">河流选择</li>-->
<!--      </ul>-->
<!--    </div>-->
<!--    <div class="main-content">-->
<!--      <component :is="currentComponent"></component>-->
<!--    </div>-->
<!--  </div>-->
<!--</template>-->

<!--<style scoped>-->
<!--.province-detail-page {-->
<!--  display: flex;-->
<!--  height: 100vh;-->
<!--}-->

<!--.sidebar {-->
<!--  width: 200px;-->
<!--  background: #f4f4f4;-->
<!--  padding: 10px;-->
<!--  display: flex;-->
<!--  flex-direction: column;-->
<!--}-->

<!--.sidebar ul {-->
<!--  list-style-type: none;-->
<!--  padding: 0;-->
<!--}-->

<!--.sidebar li {-->
<!--  padding: 10px;-->
<!--  cursor: pointer;-->
<!--}-->

<!--.sidebar li.active {-->
<!--  background: #ddd;-->
<!--  font-weight: bold;-->
<!--}-->

<!--.main-content {-->
<!--  flex: 1;-->
<!--  padding: 20px;-->
<!--  text-align: center;-->
<!--  background-image: url('@/assets/home/Background.png'); /* 引用图片 */-->
<!--  background-size: cover; /* 确保背景图片覆盖整个区域 */-->
<!--  background-position: center; /* 图片居中 */-->
<!--}-->

<!--.water-data {-->
<!--  margin-top: 20px;-->
<!--  font-size: 18px;-->
<!--}-->
<!--</style>-->


<!--<script lang="ts" setup>-->
<!--import { ref, computed, onMounted } from 'vue'-->
<!--import { useRoute, useRouter } from 'vue-router'-->

<!--// 获取路由参数-->
<!--const route = useRoute()-->
<!--const router = useRouter()-->
<!--const provinceName = ref(route.params.name)-->

<!--// 假设每个省份的水质数据-->
<!--const provinceData = ref({-->
<!--  pH: 7.5,-->
<!--  oxygen: 8.0,-->
<!--  conductivity: 1.2-->
<!--})-->

<!--// 模拟省份的数据-->
<!--onMounted(() => {-->
<!--  // 这里你可以根据省份名称去设置具体的数据-->
<!--})-->

<!--// 当前选择的功能模块-->
<!--const currentTab = ref<'dataDisplay' | 'dataUpdate' | 'riverSelection'>('dataDisplay')-->

<!--// 动态组件-->
<!--const components: Record<'dataDisplay' | 'dataUpdate' | 'riverSelection', () => Promise<typeof import('*.vue')>> = {-->
<!--  dataDisplay: () => import('../home/components/DataDisplay.vue'),-->
<!--  dataUpdate: () => import('../home/components/DataUpdate.vue'),-->
<!--  riverSelection: () => import('../home/components/RiverSelection.vue')-->
<!--}-->

<!--// 计算当前显示的组件-->
<!--const currentComponent = computed(() => components[currentTab.value])-->

<!--// 返回主页的方法-->
<!--const goBack = () => {-->
<!--  router.push('/home') // 这里假设 '/home' 是你的主页的路由路径-->
<!--}-->
<!--</script>-->

<!--<template>-->
<!--  <div class="province-detail-page">-->
<!--    <div class="sidebar">-->
<!--      <ul>-->
<!--        <li @click="currentTab = 'dataDisplay'" :class="{ active: currentTab === 'dataDisplay' }">数据展示</li>-->
<!--        <li @click="currentTab = 'dataUpdate'" :class="{ active: currentTab === 'dataUpdate' }">数据更新</li>-->
<!--        <li @click="currentTab = 'riverSelection'" :class="{ active: currentTab === 'riverSelection' }">河流选择</li>-->
<!--      </ul>-->
<!--    </div>-->
<!--    <div class="main-content">-->
<!--      <button @click="goBack" class="back-button">返回主页</button>-->
<!--      <component :is="currentComponent"></component>-->
<!--    </div>-->
<!--  </div>-->
<!--</template>-->

<!--<style scoped>-->
<!--.province-detail-page {-->
<!--  display: flex;-->
<!--  height: 100vh;-->
<!--}-->

<!--.sidebar {-->
<!--  width: 200px;-->
<!--  background: #f4f4f4;-->
<!--  padding: 10px;-->
<!--  display: flex;-->
<!--  flex-direction: column;-->
<!--}-->

<!--.sidebar ul {-->
<!--  list-style-type: none;-->
<!--  padding: 0;-->
<!--}-->

<!--.sidebar li {-->
<!--  padding: 10px;-->
<!--  cursor: pointer;-->
<!--}-->

<!--.sidebar li.active {-->
<!--  background: #ddd;-->
<!--  font-weight: bold;-->
<!--}-->

<!--.main-content {-->
<!--  flex: 1;-->
<!--  padding: 20px;-->
<!--  text-align: center;-->
<!--  background-image: url('@/assets/home/Background.png'); /* 引用图片 */-->
<!--  background-size: cover; /* 确保背景图片覆盖整个区域 */-->
<!--  background-position: center; /* 图片居中 */-->
<!--}-->

<!--.back-button {-->
<!--  margin-bottom: 20px;-->
<!--  padding: 10px 20px;-->
<!--  font-size: 16px;-->
<!--  color: #fff;-->
<!--  background-color: #007bff;-->
<!--  border: none;-->
<!--  border-radius: 5px;-->
<!--  cursor: pointer;-->
<!--}-->

<!--.back-button:hover {-->
<!--  background-color: #0056b3;-->
<!--}-->
<!--</style>-->

<!--<template>-->
<!--  <div class="province-detail-page">-->
<!--    <div class="sidebar">-->
<!--      <ul>-->
<!--        <li @click="currentTab = 'dataDisplay'" :class="{ active: currentTab === 'dataDisplay' }">数据展示</li>-->
<!--        <li @click="currentTab = 'dataUpdate'" :class="{ active: currentTab === 'dataUpdate' }">数据更新</li>-->
<!--        <li @click="currentTab = 'riverSelection'" :class="{ active: currentTab === 'riverSelection' }">河流选择</li>-->
<!--      </ul>-->
<!--    </div>-->
<!--    <div class="main-content">-->
<!--      <button @click="goBack" class="back-button">返回主页</button>-->
<!--      <component :is="currentComponent"></component>-->
<!--    </div>-->
<!--  </div>-->
<!--</template>-->

<!--<script lang="ts" setup>-->
<!--import { ref, computed } from 'vue'-->
<!--import { useRouter } from 'vue-router'-->

<!--const router = useRouter()-->
<!--const currentTab = ref('dataDisplay')-->

<!--const components = {-->
<!--  dataDisplay: () => import('./components/DataDisplay.vue'),-->
<!--  dataUpdate: () => import('./components/DataUpdate.vue'),-->
<!--  riverSelection: () => import('./components/RiverSelection.vue')-->
<!--}-->

<!--const currentComponent = computed(() => components[currentTab.value])-->

<!--const goBack = () => {-->
<!--  router.push('/home')-->
<!--}-->
<!--</script>-->
<!--<template>-->
<!--  <div class="province-detail-page">-->
<!--    <div class="sidebar">-->
<!--      <ul>-->
<!--        <li @click="currentTab = 'dataDisplay'" :class="{ active: currentTab === 'dataDisplay' }">数据展示</li>-->
<!--        <li @click="currentTab = 'dataUpdate'" :class="{ active: currentTab === 'dataUpdate' }">数据更新</li>-->
<!--        <li @click="currentTab = 'riverSelection'" :class="{ active: currentTab === 'riverSelection' }">河流选择</li>-->
<!--      </ul>-->
<!--    </div>-->
<!--    <div class="main-content">-->
<!--      <button @click="goBack" class="back-button">返回主页</button>-->
<!--      <component :is="currentComponent"></component>-->
<!--    </div>-->
<!--  </div>-->
<!--</template>-->

<!--<style scoped>-->
<!--.province-detail-page {-->
<!--  display: flex;-->
<!--  height: 100vh;-->
<!--}-->

<!--.sidebar {-->
<!--  width: 200px;-->
<!--  background: #f4f4f4;-->
<!--  padding: 10px;-->
<!--  display: flex;-->
<!--  flex-direction: column;-->
<!--}-->

<!--.sidebar ul {-->
<!--  list-style-type: none;-->
<!--  padding: 0;-->
<!--}-->

<!--.sidebar li {-->
<!--  padding: 10px;-->
<!--  cursor: pointer;-->
<!--}-->

<!--.sidebar li.active {-->
<!--  background: #ddd;-->
<!--  font-weight: bold;-->
<!--}-->

<!--.main-content {-->
<!--  flex: 1;-->
<!--  padding: 20px;-->
<!--  text-align: center;-->
<!--  background-image: url('@/assets/home/Background.png');-->
<!--  background-size: cover;-->
<!--  background-position: center;-->
<!--}-->

<!--.back-button {-->
<!--  margin-bottom: 20px;-->
<!--  padding: 10px 20px;-->
<!--  border: none;-->
<!--  background-color: #007bff;-->
<!--  color: white;-->
<!--  font-size: 16px;-->
<!--  cursor: pointer;-->
<!--}-->

<!--.back-button:hover {-->
<!--  background-color: #0056b3;-->
<!--}-->
<!--</style>-->

<script lang="ts" setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'

// 使用联合类型定义 currentTab
const currentTab = ref<'dataDisplay' | 'dataUpdate' | 'riverSelection'>('dataDisplay')

// 定义动态组件映射
const components: Record<'dataDisplay' | 'dataUpdate' | 'riverSelection', () => Promise<typeof import('*.vue')>> = {
  dataDisplay: () => import('./components/DataDisplay.vue'),
  dataUpdate: () => import('./components/DataUpdate.vue'),
  riverSelection: () => import('./components/RiverSelection.vue')
}

// 使用类型断言解决索引类型问题
const currentComponent = computed(() => components[currentTab.value as 'dataDisplay' | 'dataUpdate' | 'riverSelection'])

const router = useRouter()

// 返回主页的函数
const goBack = () => {
  router.push('/home')
}
</script>

<template>
  <div class="province-detail-page">
    <div class="sidebar">
      <ul>
        <li @click="currentTab = 'dataDisplay'" :class="{ active: currentTab === 'dataDisplay' }">数据展示</li>
        <li @click="currentTab = 'dataUpdate'" :class="{ active: currentTab === 'dataUpdate' }">数据更新</li>
        <li @click="currentTab = 'riverSelection'" :class="{ active: currentTab === 'riverSelection' }">河流选择</li>
      </ul>
    </div>
    <div class="main-content">
      <button @click="goBack" class="back-button">返回主页</button>
      <component :is="currentComponent"></component>
    </div>
  </div>
</template>

<style scoped>
.province-detail-page {
  display: flex;
  height: 100vh;
}

.sidebar {
  width: 200px;
  background: #f4f4f4;
  padding: 10px;
  display: flex;
  flex-direction: column;
}

.sidebar ul {
  list-style-type: none;
  padding: 0;
}

.sidebar li {
  padding: 10px;
  cursor: pointer;
}

.sidebar li.active {
  background: #ddd;
  font-weight: bold;
}

.main-content {
  flex: 1;
  padding: 20px;
  text-align: center;
  background-image: url('@/assets/home/Background.png');
  background-size: cover;
  background-position: center;
}

.back-button {
  margin-bottom: 20px;
  padding: 10px 20px;
  border: none;
  background-color: #007bff;
  color: white;
  font-size: 16px;
  cursor: pointer;
}

.back-button:hover {
  background-color: #0056b3;
}
</style>
