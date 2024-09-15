<template>
  <div>
    <h2>{{ river }}的水质监测数据</h2>

    <!-- 日期范围选择 -->
    <div class="date-picker">
      <label for="start-date">开始日期:</label>
      <input type="date" id="start-date" v-model="startDate" />
      
      <label for="end-date">结束日期:</label>
      <input type="date" id="end-date" v-model="endDate" />
      
      <button @click="filterData">筛选</button>
    </div>

    <div id="chart" style="width: 100%; height: 400px;"></div>
  </div>
</template>

<script>
import * as echarts from 'echarts';
import Papa from 'papaparse';
import axios from 'axios';

export default {
  props: ['river'],
  data() {
    return {
      csvData: [], // 用于存储从后端获取的水质监测数据
      filteredData: [], // 存储筛选后的数据
      startDate: '', // 用户选择的开始日期
      endDate: '', // 用户选择的结束日期
    };
  },
  mounted() {
    this.fetchData();
  },
  methods: {
    // 从后端获取CSV数据并解析
    async fetchData() {
      // 请求CSV文件
      const response = await axios.get('/public/东苕溪202101-202112.csv');
      // 使用 PapaParse 解析 CSV 数据
      Papa.parse(response.data, {
        header: true,
        dynamicTyping: true,
        complete: (result) => {
          this.csvData = this.processCSV(result.data);
          this.filteredData = this.csvData; // 初始显示全部数据
          this.initChart();
        },
      });
    },
    // 处理解析后的CSV数据
    processCSV(data) {
      return data.map(item => ({
        time: item['监测时间'],
        pH: item['pH'],
        dissolvedOxygen: item['溶解氧'],
        conductivity: item['电导率'],
      }));
    },
    // 初始化ECharts图表
    initChart() {
      const chart = echarts.init(document.getElementById('chart'));

      const times = this.filteredData.map(item => item.time);
      const phValues = this.filteredData.map(item => item.pH);
      const dissolvedOxygenValues = this.filteredData.map(item => item.dissolvedOxygen);
      const conductivityValues = this.filteredData.map(item => item.conductivity);

      const option = {
        title: { text: `${this.river} 水质监测数据` },
        tooltip: { trigger: 'axis' },
        legend: { data: ['pH', '溶解氧', '电导率'] },
        xAxis: {
          type: 'category',
          data: times,
          axisLabel: { rotate: 45, interval: 10 },
        },
        yAxis: [{ type: 'value', name: '数值' }],
        series: [
          { name: 'pH', type: 'line', data: phValues },
          { name: '溶解氧', type: 'line', data: dissolvedOxygenValues },
          { name: '电导率', type: 'line', data: conductivityValues },
        ],
      };

      chart.setOption(option);
    },
    // 根据日期范围筛选数据
    filterData() {
      const start = new Date(this.startDate);
      const end = new Date(this.endDate);
      
      // 过滤数据，确保时间在选择的范围内
      this.filteredData = this.csvData.filter(item => {
        const itemDate = new Date(item.time);
        return itemDate >= start && itemDate <= end;
      });

      // 重新绘制图表
      this.initChart();
    },
  },
};
</script>

<style scoped>
#chart {
  width: 100%;
  height: 400px;
}

.date-picker {
  margin: 20px 0;
}

.date-picker label {
  margin-right: 10px;
}

.date-picker input {
  margin-right: 20px;
  padding: 5px;
}

button {
  background-color: #42b983;
  color: white;
  border: none;
  padding: 10px 15px;
  cursor: pointer;
  border-radius: 5px;
}

button:hover {
  background-color: #2a9662;
}
</style>
