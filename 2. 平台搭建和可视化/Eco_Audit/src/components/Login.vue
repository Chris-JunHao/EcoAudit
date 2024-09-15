<template>
    <div class="login">
      <h2>水质监测系统登录</h2>
      <form @submit.prevent="login">
        <div>
          <label for="username">用户名:</label>
          <input type="text" v-model="username" id="username" required />
        </div>
        <div>
          <label for="password">密码:</label>
          <input type="password" v-model="password" id="password" required />
        </div>
        <button type="submit">登录</button>
      </form>
      <p v-if="errorMessage">{{ errorMessage }}</p>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        username: '',
        password: '',
        errorMessage: '',
      };
    },
    methods: {
      login() {
        if (this.username === 'admin' && this.password === '123456') {
          this.$router.push('/main');
        } else {
          this.errorMessage = '用户名或密码错误';
        }
      },
    },
  };
  </script>
  
  <style scoped>
  .login {
    max-width: 300px;
    margin: 100px auto;
    padding: 20px;
    border: 1px solid #ccc;
    border-radius: 5px;
  }
  </style>
  