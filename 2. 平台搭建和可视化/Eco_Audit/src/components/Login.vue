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
        <input type="password" v-model="password" id="password" required ref="passwordInput" />
      </div>
      <button type="submit">登录</button>
    </form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      username: '',
      password: '',
    };
  },
  methods: {
    login() {
      if (this.username === 'admin' && this.password === '123456') {
        this.$router.push('/main');
      } else {
        alert('用户名或密码错误，请重新输入。'); // 弹窗提示
        this.username = ''; // 清空用户名
        this.password = ''; // 清空密码
        this.$nextTick(() => {
          this.$refs.passwordInput.focus(); // 聚焦到密码输入框
        });
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
  background-color: white; /* 登录框背景色 */
}

body {
  background-color:rgb(193, 215, 248);/* 整体页面背景色为淡蓝色 */
}
</style>
