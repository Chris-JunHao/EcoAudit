import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
//引入路由器
import router from './router'

/* 引入 ElementPlus */
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

import { MdPreview } from 'md-editor-v3'
import 'md-editor-v3/lib/preview.css'

//创建一个应用
const app= createApp(App)
//使用路由器
app.use(router)

app.use(createPinia())

app.use(ElementPlus)

app.component('MdPreview', MdPreview)

app.mount('#app')
