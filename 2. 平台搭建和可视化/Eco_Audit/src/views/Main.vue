<!-- eslint-disable vue/multi-word-component-names -->
<template>
  <div class="main-container">
    <!-- 左侧省份选择 -->
    <div class="left-panel">
      <h2>选择省份</h2>
      <div class="scroll-container">
        <ul>
          <li v-for="province in provinces" :key="province" @click="selectProvince(province)">
            {{ province }}
          </li>
        </ul>
      </div>
    </div>

    <!-- 右侧图片展示 -->
    <div class="right-panel">
      <img src="/img.png" alt="Water Quality Image" class="main-image" />
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      provinces: [
        '浙江省', '天津市', '北京市', '山西省', '内蒙古自治区', '辽宁省', '吉林省', '黑龙江省',
        '上海市', '江苏省', '河北省', '安徽省', '福建省', '江西省', '山东省', '河南省', '湖北省',
        '湖南省', '广东省', '广西壮族自治区', '海南省', '重庆市', '四川省', '贵州省', '云南省', '西藏自治区',
        '陕西省', '甘肃省', '青海省', '宁夏回族自治区', '新疆维吾尔自治区', '香港特别行政区', '澳门特别行政区', '台湾省'
      ],
    };
  },
  methods: {
    selectProvince(province) {
      this.$router.push({ name: 'ProvinceDetail', params: { province } });
    },
  },
};
</script>

<style scoped>
.main-container {
  display: flex;
  background-color: rgb(171, 212, 238);
  height: 100vh; /* 满屏高度 */
  border-radius: 10px; /* 圆角 */
}

.left-panel {
  width: 20%; /* 左侧区域宽度 */
  background-color: #2c3e50; /* 深色背景 */
  color: #ecf0f1; /* 文字颜色 */
  padding: 20px;
  box-shadow: 2px 0 10px rgba(0, 0, 0, 0.1); /* 阴影效果 */
  border-radius: 10px 0 0 10px; /* 圆角 */
}

h2 {
  font-size: 24px;
  color: #ecf0f1;
  margin-bottom: 15px;
  border-bottom: 1px solid #34495e; /* 底部边框 */
  padding-bottom: 10px;
}

.scroll-container {
  max-height: 800px; /* 控制左侧列表高度 */
  overflow-y: auto; /* 纵向滚动 */
  border: 1px solid #34495e; /* 边框颜色 */
  padding: 10px;
  border-radius: 5px; /* 圆角 */
  background-color: #34495e; /* 背景色 */
}

ul {
  list-style-type: none;
  padding: 0;
  margin-top: 20px;
}

li {
  cursor: pointer;
  padding: 15px 10px;
  background-color: #34495e; /* 列表项背景色 */
  margin-bottom: 10px;
  border-radius: 5px;
  transition: all 0.3s ease; /* 平滑过渡 */
  color: #ecf0f1; /* 文字颜色 */
}

li:hover {
  background-color: #1abc9c; /* 悬停时背景色 */
  color: white; /* 悬停时文字颜色 */
  transform: translateX(5px); /* 悬停时移动效果 */
}

.right-panel {
  width: 70%; /* 右侧内容区域宽度 */
  text-align: center;
  background-color: rgb(171, 212, 238);
  border-radius: 10px; /* 圆角 */
  padding: 20px;
}

.main-image {
  max-width: 85%;
  height: auto;
  border-radius: 8px; /* 圆角 */
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1); /* 阴影效果 */
}

.table-container {
  height: 750px;
  overflow-y: auto; /* 纵向滚动 */
  padding: 10px;
  border-radius: 8px; /* 圆角 */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* 阴影效果 */
  background-color: rgb(193, 215, 248); /* 背景色 */
  border: 2px solid rgb(26, 27, 30); /* 边框颜色 */
}

.table-container th,
.table-container td {
  border: 2px solid rgb(39, 42, 48); /* 表格内部边框颜色 */
  padding: 8px;
  text-align: left;
}

table {
  width: 100%;
  border-collapse: collapse;
  font-size: 14px;
}

thead {
  background-color: #7bd27f; /* 表头背景色 */
  color: #fff; /* 表头文字颜色 */
}

.submenu {
  margin-left: 20px;
  display: flex;
  flex-direction: column;
}

.submenu button {
  margin-top: 10px;
  background-color: #1abc9c; /* 按钮背景色 */
  color: white; /* 按钮文字颜色 */
  border: none;
  padding: 12px;
  border-radius: 5px;
  font-size: 16px;
  transition: background-color 0.3s ease;
}

.submenu button:hover {
  background-color: #16a085; /* 悬停时按钮背景色 */
}
</style>
