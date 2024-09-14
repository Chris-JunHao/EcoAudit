<script setup lang="ts">
import logo from '../../assets/login/logo.jpg'
import router from '@/router'

//写好后端取消注释
// import { useUserStore } from '@/stores/user'
// import { toRefs } from 'vue'
// const userStore = useUserStore()
// userStore.getInfo()
// const { userInfo } = toRefs(userStore)

const switchRoute = (path: string) => {
    router.push({ path })
    console.log(path)
}
</script>

<template>
    <img class="homeBackground" src="../../assets/home/Background.png" alt="Background">
    <transition appear name="a">
    <div class="index-view">
        <div class="header-wrapper">
            <div class="header">
                <div class="logo-wrapper" @click="switchRoute('/home')">
                    <img class="logo" src="../../assets/logo/logo4.png" alt="logo">
                    <!-- <div class="name">旅慧智库</div> -->
                </div>
                <div class="avatar-wrapper">
                    <div class="nickname">{{ '测试用户' }}</div>
                    <!-- 写好后端需要取消注释 -->
                    <!-- <div class="nickname">{{ userInfo.nickname||userInfo.nickname }}</div> -->
                    <el-dropdown>
                        <!-- 头像 -->
                        <el-avatar :src="logo" shape="square" :size="40"></el-avatar>
                        <!-- 写好后端取消注释 -->
                        <!-- <el-avatar :src="userInfo.avatar||'logo'" shape="square" :size="30"></el-avatar> -->
                        <template #dropdown>
                            <el-dropdown-menu>
                                <el-dropdown-item @click="switchRoute('/user/profile')">
                                    个人设置
                                </el-dropdown-item>
                                <el-dropdown-item @click="switchRoute('/login')">
                                    退出登录
                                </el-dropdown-item>
                            </el-dropdown-menu>
                        </template>
                    </el-dropdown>
                </div>
            </div>
        </div>
        <el-container class="scrollable-container">
            <router-view></router-view>
        </el-container>
    </div>
    </transition>
</template>

<style lang="scss" scoped>
.homeBackground{
    position: fixed;
    width: 100vw;
    height: auto;
    z-index: -10;
    background-position:top;
}
.header-wrapper {
    background-color: rgb(0, 0, 0);
    color: white;

    .header {
        padding: 10px;
        display: flex;
        justify-content: space-between;
        align-items: center;

        .logo-wrapper {
            display: flex;
            align-items: center;

            .logo {
                width: 100px;
                height: auto;
            }
        }

        .avatar-wrapper {
            display: flex;
            align-items: center;

            .nickname {
                margin-right: 10px;
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