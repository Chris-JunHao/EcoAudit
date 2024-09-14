<script setup lang="ts">
import { ref, watch } from 'vue'
import router from '@/router'
const props=defineProps({routeName:{ type:String,default:'profile'}})

interface Menu {
    id: string
    name: string
    path: string
}
const menuList = ref<Menu[]>([
    { id: '0', name: '我的信息', path: '/user/profile' },
    { id: '1', name: 'GPT设置', path: '/user/gpt' }
])

const activeMenu = ref('0')
const handleMenuChange = (menu: Menu) => {
    activeMenu.value = menu.id
    router.push({ path: menu.path })
}


</script>

<template>
    <transition appear name="a">
    <div class="setting-view-wrapper">
        <div class="setting-view">
            <div class="title">个人设置</div>
            <el-card class="setting-panel-wrapper">
                <div class="setting-panel">
                    <div class="side-menu">
                        <div :class="['menu-item', menu.id === activeMenu ? 'active' : '']" v-for="menu in menuList"
                            :key="menu.id" @click="handleMenuChange(menu)">
                            {{ menu.name }}
                        </div>
                    </div>
                    <div class="content-panel">
                        <router-view></router-view>
                    </div>
                </div>
            </el-card>
        </div>
    </div>
    </transition>
</template>

<style scoped lang="scss">
.setting-view-wrapper {
    display: flex;
    justify-content: center;
    width: 100vw;

    .setting-view {
        .title {
            font-size: 22px;
            margin: 40px 0 20px 0;
            color: aliceblue;
        }

        .setting-panel-wrapper {
            width: 40vw;

            .setting-panel {
                display: flex;

                .side-menu {
                    width: 150px;

                    .menu-item:nth-child(1){
                        margin-top: 0;
                    }
                    .menu-item {

                        width: 100px;
                        text-align: center;
                        margin-top: 20px;
                        height: 40px;
                        line-height: 40px;
                        border-radius: 20px;

                        &.active {

                            background-color: rgb(233, 240, 255);
                            color: rgb(75, 133, 245);
                        }
                    }
                }
            }
        }
    }

}

//wxs
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
//wxs
</style>