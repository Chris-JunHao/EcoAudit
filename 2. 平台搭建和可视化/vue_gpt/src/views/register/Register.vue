<script lang="ts" setup>
import { onMounted, reactive } from 'vue';
import router from '@/router'
import { User } from '../../../typings'
import { loginUser } from '@/api/user'

const switchRoute = (path: string) => {
    router.push(path);
};
// onMounted(()=>{
//     setTimeout(()=>router.push('/home'),2000)
// })
const loginForm = reactive<Partial<User>>({ username: '', password: '' })
const registryForm = reactive({ username: '', password: '' })
const login = () => {
    loginUser(loginForm).then((res) => {
        if (res.success) {
            router.replace({ path: '/' })
            localStorage.setItem('token', res.result.tokenValue)
            console.log(res)
        }
    })
}

</script>

<template>
    <img class="mainbackground" src="../../assets/home/Background.png" alt="mainbackground">
    <Transition appear name="a">
        <div class="panel-warpper">
            <el-card class="panel">
                <div class="content">
                    <div class="panel-left">
                        <img class="logo" src="../../assets/logo/logo4.png" alt="logo" />
                        <div class="title">有什么旅游的问题，尽管问！</div>
                        <div class="description">&nbsp;&nbsp;&nbsp;&nbsp;想知道杭州有什么必去风景吗？</div>
                        <div class="description" id="description2">想知道甘肃有什么美食吗？</div>
                        <div class="description" id="description3">想知道西安大雁塔的历史吗？</div>
                        <div class="xihudiv">
                            <img class="xihu" src="../../assets/login/xihu.jpg" alt="xihu">
                        </div>
                        <div class="xihutext">杭州西湖</div>
                    </div>
                    <div class="panel-right">
                        <div class="title">注册</div>
                        <div class="description" id="description4">快来问出你的问题吧</div>
                        <el-form class="form" label-position="top" label-width="100px" :model="loginForm"
                            style="max-width: 460px;">
                            <el-form-item label="用户名">
                                <el-input v-model="loginForm.username" size="large" style="width: 400px" />
                            </el-form-item>
                            <el-form-item label="密码">
                                <el-input v-model="loginForm.password" size="large" style="width: 400px"
                                    type="password" />
                            </el-form-item>
                            <el-form-item label="确认密码">
                                <el-input v-model="loginForm.password" size="large" style="width: 400px"
                                    type="repassword" />
                            </el-form-item>
                            <!-- <el-form class="register">
                                <div class="registeritem">确认密码</div>
                                <div class="divtextitem">
                                    <input class="textitem" type="password" size="large">
                                </div>
                            </el-form> -->
                            <div class="button-wrapper">
                                <el-button class="register-button" size="large" style="width: 300px" type="primary"
                                    @click="login">
                                    注册
                                </el-button>
                                <el-button class="back-login-button" size="large" style="width: 300px" type="primary"
                                    @click="switchRoute('/login')">
                                    回到登录界面
                                </el-button>
                                <!-- <div>
                                    <button class="back-login-button" size="large" type="submit"
                                        @click="switchRoute('/login')">
                                        回到登录界面
                                    </button>
                                </div> -->
                            </div>
                        </el-form>
                    </div>
                </div>
            </el-card>
        </div>
    </Transition>
</template>

<style lang="scss" scoped>
//wxs
.a-enter-active {
    animation: bounce-in 0.5s;
}

.a-leave-active {
    animation: bounce-in 0.5s reverse;
}

@keyframes bounce-in {
    0% {
        transform: scale(0);
    }

    50% {
        transform: scale(1.25);
    }

    100% {
        transform: scale(1);
    }
}

//wxs

.mainbackground {
    position: fixed;
    width: 100vw;
    height: auto;
    z-index: -10;
}

.panel-warpper {
    display: flex;
    height: 100vh;
    align-items: center;
    justify-content: center;

    .panel {
        width: 50vw;
        min-width: 700px;
        min-height: 500px;
        box-shadow: 0 0 10px;


        .content {
            display: flex;

            .title {
                font-size: 22px;
                margin-top: 30px;
                font-weight: bold;
            }

            .description {
                margin-top: 20px;
                font-size: 18px;
                color: rgba($color: #000000, $alpha: 0.7);
            }

            .panel-left {
                box-sizing: border-box; //设置盒子不因为margin而改变大小
                padding: 20px;
                background-color: rgb(243, 245, 249);
                height: 100%;
                width: 50%;

                .logo {
                    width: auto;
                    height: 50px;
                    margin-top: 10px;
                }

                #description2 {
                    text-align: right;
                }

                #description3 {
                    text-align: center;
                }

                .xihudiv {
                    display: flex;
                    justify-content: center;

                    .xihu {
                        margin-top: 60px;
                        width: 90%;
                        height: auto;
                        justify-content: center;
                    }
                }

                .xihutext {
                    margin-left: 20px;
                    font-size: 12px;
                    color: rgba($color: #000000, $alpha: 0.5);
                }

            }

            .panel-right {
                box-sizing: border-box; //设置盒子不因为margin而改变大小
                padding: 30px;
                width: 50%;
                background-color: white;

                #description4 {
                    text-align: center;
                }

                .form {
                    margin-top: 30px;

                    .register {
                        .registeritem {
                            margin-left: 15px;
                            margin-top: 30px;
                            font-size: 18px;
                            color: rgba($color: #000000, $alpha: 0.7);
                        }

                        .divtextitem {
                            display: flex;
                            justify-content: center;

                            .textitem {
                                width: 90%;
                                height: 25px;
                                display: flex;
                                justify-content: center;
                            }
                        }

                    }


                    .button-wrapper {
                        padding-top: 10px;
                        justify-content: center;

                        .back-login-button {
                            margin-top: 30px;
                            margin-left: 0px;
                            width: 90%;
                            border: none;
                            background-color: rgb(0, 162, 255);
                            font-size: 22px;
                            color: aliceblue;
                        }

                        .back-login-button:active {
                            background-color: rgb(87, 185, 241);
                        }

                        .register-button {
                            margin-left: 0px;
                            width: 90%;
                            border: none;
                            background-color: rgb(0, 162, 255);
                            font-size: 22px;
                            color: aliceblue;
                        }

                        .login-button:active {
                            background-color: rgb(87, 185, 241);
                        }
                    }
                }


            }
        }

    }
}
</style>
