// import HomeView from '@/views/home/HomeView.vue'
// import IndexView from '@/views/index/IndexView.vue'
// import LoginView from '@/views/login/LoginView.vue'
// import RegisterView from '@/views/register/Register.vue'
// import UserSettingView from '@/views/user/UserSettingView.vue'
// import ProfileView from '@/views/user/profile/ProfileView.vue'
// import GPTSettingView from '@/views/user/gpt/GPTSettingView.vue'
// import { Router, createRouter, createWebHistory } from 'vue-router'
//
// const router = createRouter({
//   history: createWebHistory(),
//   routes: [
//     {
//       path: '/',
//       component: IndexView,
//       redirect: 'home',
//       children: [
//         {
//           path: 'home',
//           component: HomeView
//         },
//         {
//           path:'user',
//           component:UserSettingView,
//           redirect:'/user/profile',//默认显示内容
//           children:[
//             {
//               path:'profile',
//               component:ProfileView
//             },
//             {
//               path:'gpt',
//               component:GPTSettingView
//             }
//           ]
//         }
//       ]
//     },
//     {
//       path: '/login',
//       name: 'login',
//       component: LoginView
//     },
//     {
//       path:'/register',
//       name:'register',
//       component:RegisterView
//     }
//   ]
// })
//
// export default router


import HomeView from '@/views/home/HomeView.vue'
import IndexView from '@/views/index/IndexView.vue'
import LoginView from '@/views/login/LoginView.vue'
import RegisterView from '@/views/register/Register.vue'
import UserSettingView from '@/views/user/UserSettingView.vue'
import ProfileView from '@/views/user/profile/ProfileView.vue'
import GPTSettingView from '@/views/user/gpt/GPTSettingView.vue'

// 修改后的路径，指向 src/views/home/ProvinceDetailPage.vue
import ProvinceDetailPage from '@/views/Province/ProvinceDetailPage.vue';

import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      component: IndexView,
      redirect: 'home',
      children: [
        {
          path: 'home',
          component: HomeView
        },
        {
          path: 'user',
          component: UserSettingView,
          redirect: '/user/profile', // 默认显示内容
          children: [
            {
              path: 'profile',
              component: ProfileView
            },
            {
              path: 'gpt',
              component: GPTSettingView
            }
          ]
        },
        // 正确导入的省份路由
        {
          path: 'province/:name',
          component: ProvinceDetailPage
        }
      ]
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterView
    }
  ]
})

export default router
