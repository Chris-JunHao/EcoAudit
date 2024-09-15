import { createRouter, createWebHistory } from 'vue-router';
import Login from '../components/Login.vue';
import Main from '../views/Main.vue';  // 主页面放在 views 中
import ProvinceDetail from '../views/ProvinceDetail.vue';
import RiverDetail from '../views/RiverDetail.vue';

const routes = [
  { path: '/', component: Login },
  { path: '/main', component: Main },
  { path: '/province/:province', name: 'ProvinceDetail', component: ProvinceDetail, props: true },
  { path: '/river/:river', name: 'RiverDetail', component: RiverDetail, props: true },
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
