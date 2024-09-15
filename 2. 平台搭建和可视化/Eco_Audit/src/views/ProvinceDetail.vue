<template>
    <div>
      <h2>{{ province }}的水质监测</h2>
      <ul>
        <li v-for="river in rivers" :key="river" @click="selectRiver(river)">
          {{ river }}
        </li>
      </ul>
    </div>
  </template>
  
  <script>
  export default {
    props: ['province'],
    data() {
      return {
        rivers: ['河流A', '河流B', '河流C'],
      };
    },
    methods: {
      selectRiver(river) {
        this.$router.push({ name: 'RiverDetail', params: { river } });
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
  