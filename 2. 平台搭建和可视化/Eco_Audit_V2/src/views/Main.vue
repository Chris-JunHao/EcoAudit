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
  background-color: rgb(250, 243, 243);
  display: flex;
  justify-content: space-between;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1); /* 增加轻微的阴影效果 */
}

.left-panel {
  background-color: rgb(250, 243, 243);
  width: 24%; /* 左侧省份选择区域宽度 */
  padding-right: 20px;
}

h2 {
  font-size: 24px;
  margin-bottom: 15px;
  color: #333;
  border-bottom: 2px solid #e0e0e0;
}

.scroll-container {
  max-height: 800px; /* 控制左侧省份列表的高度，超出时滚动 */
  overflow-y: auto;
  border: 1px solid #ccc; /* 可选的样式 */
  padding: 10px;
  border-radius: 8px; /* 增加圆角 */
  background: linear-gradient(135deg, #fdfbfb 0%, #ebedee 100%); /* 增加渐变背景 */
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  cursor: pointer;
  padding: 10px;
  border-bottom: 1px solid #ccc;
  transition: background-color 0.3s, font-weight 0.3s; /* 增加平滑的过渡效果 */
}

li:hover {
  background-color: #e0e0e0;
  font-weight: bold; /* 鼠标悬停时字体加粗 */
}

.right-panel {
  width: 70%; /* 右侧图片展示区域宽度 */
  text-align: center;
  background-color: rgb(250, 243, 243);
  border-radius: 10px;
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
  padding: 20px;
}

.main-image {
  max-width: 95%;
  height: auto;
  border-radius: 10px; /* 增加图片的圆角 */
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1); /* 为图片增加轻微阴影 */
}
</style>
