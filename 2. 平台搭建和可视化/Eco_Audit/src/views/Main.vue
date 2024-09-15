<template>
    <div>
      <h2>选择省份</h2>
      <ul>
        <li v-for="province in provinces" :key="province" @click="selectProvince(province)">
          {{ province }}
        </li>
      </ul>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        provinces: ['广东省', '广西省', '湖南省'],
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
  ul {
    list-style-type: none;
  }
  li {
    cursor: pointer;
    padding: 10px;
    border-bottom: 1px solid #ccc;
  }
  li:hover {
    background-color: #f0f0f0;
  }
  </style>
  