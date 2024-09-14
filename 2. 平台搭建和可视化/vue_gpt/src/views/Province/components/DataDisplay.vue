<script lang="ts" setup>
import { ref } from 'vue'

// 定义每行数据的接口
interface WaterQualityData {
  river: string;
  basin: string;
  sectionName: string;
  monitorTime: string;
  pH: number;
  oxygen: number;
  waterTemp: number;
  conductivity: number;
}

// 导入 JSON 文件
import tableDataJson from '@/assets/json/浙江杭州202201-202203_en_complete_v2.json'

// 使用 ref 包装 JSON 数据，并应用类型
const tableData = ref<WaterQualityData[]>(tableDataJson)
console.log("DataDisplay.vue component loaded");
</script>


<template>
  <div>
    <h3>浙江杭州 202201-202203 水质数据</h3>
    <table>
      <thead>
      <tr>
        <th>河流</th>
        <th>流域</th>
        <th>断面名称</th>
        <th>监测时间</th>
        <th>pH 值</th>
        <th>溶解氧 (mg/L)</th>
        <th>水温 (℃)</th>
        <th>电导率 (µS/cm)</th>
      </tr>
      </thead>
      <tbody>
      <tr v-for="(row, index) in tableData" :key="index">
        <td>{{ row.river }}</td>
        <td>{{ row.basin }}</td>
        <td>{{ row.sectionName }}</td>
        <td>{{ row.monitorTime }}</td>
        <td>{{ row.pH }}</td>
        <td>{{ row.oxygen }}</td>
        <td>{{ row.waterTemp }}</td>
        <td>{{ row.conductivity }}</td>
      </tr>
      </tbody>
    </table>
  </div>
</template>

<style scoped>
table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  border: 1px solid #ddd;
  padding: 8px;
}

th {
  background-color: #f4f4f4;
}

h3 {
  color: #f2f2f2;
}
</style>