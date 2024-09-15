
<template>
  <div class="main-container">
    <h2>{{ province }}的水质监测</h2>

    <!-- 控件按钮 -->
    <div class="buttons">
      <button @click="showOverview">数据概览</button>
      <button @click="showModify">数据修改</button>
      <button @click="showRiverDetails">河流详情</button>
    </div>

    <!-- 数据概览 -->
    <div v-if="showSection === 'overview'">
      <h3>数据概览</h3>
      <p>这是{{ province }}的水质监测数据概览。</p>
    </div>

    <!-- 数据修改 -->
    <div v-if="showSection === 'modify'">
      <h3>数据修改</h3>
      <p>数据修改功能尚未实现。</p>
    </div>

    <!-- 河流详情 -->
    <div v-if="showSection === 'riverDetails'">
      <h3>河流详情</h3>

      <!-- 选择河流的form -->
      <div class="river-select">
        <label for="river">选择河流:</label>
        <select id="river" v-model="selectedRiver">
          <option v-for="river in rivers" :key="river" :value="river">{{ river }}</option>
        </select>
        <button @click="fetchRiverData">显示河流数据</button>
      </div>

      <!-- 如果选择了东苕溪，显示日期选择和图表 -->
      <div v-if="selectedRiver === '东苕溪' && showChart">
        <h3>{{ selectedRiver }}的水质监测数据</h3>

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
    </div>
  </div>
</template>

<script>
import * as echarts from 'echarts';
import Papa from 'papaparse';
import axios from 'axios';

export default {
  props: ['province'],
  data() {
    return {
      rivers: ['东苕溪', '河流B', '河流C'], // 省份下的河流列表
      selectedRiver: null, // 选中的河流
      showSection: '', // 控制显示哪个控件
      csvData: [], // 存储从后端获取的水质监测数据
      filteredData: [], // 存储筛选后的数据
      startDate: '', // 用户选择的开始日期
      endDate: '', // 用户选择的结束日期
      showChart: false, // 是否显示图表
    };
  },
  methods: {
    // 显示数据概览
    showOverview() {
      this.showSection = 'overview';
    },
    // 显示数据修改
    showModify() {
      this.showSection = 'modify';
    },
    // 显示河流详情的控件
    showRiverDetails() {
      this.showSection = 'riverDetails';
    },
    // 根据选择的河流获取对应的CSV数据

async fetchRiverData() {
   if (!this.selectedRiver) {
     alert('请选择河流');
     return;
   }
   if (this.selectedRiver === '东苕溪') {
     try {
       const response = await axios.get('/public/东苕溪202101-202112.csv');
       console.log(response.data); // 调试
       Papa.parse(response.data, {
         header: true,
         dynamicTyping: true,
         complete: (result) => {
           this.csvData = this.processCSV(result.data);
           this.filteredData = this.csvData;
           this.showChart = true; // 显示图表
           this.$nextTick(() => { 
             this.initChart();
           });
         },
       });
     } catch (error) {
       console.error('数据加载失败', error);
     }
   }
 

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
        title: { text: `${this.selectedRiver} 水质监测数据` },
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
.main-container {
  padding: 20px;
}

.buttons {
  margin-bottom: 20px;
}

button {
  background-color: #42b983;
  color: white;
  border: none;
  padding: 15px 15px;
  cursor: pointer;
  border-radius: 10px;
  margin-right: 10px;
}

button:hover {
  background-color: #2a9662;
}

.river-select {
  margin-top: 20px;
}

.date-picker {
  margin: 20px 0;
}

.date-picker label {
  margin-right: 20px;
}

.date-picker input {
  margin-right: 20px;
  padding: 20px;
}

#chart {
  width: 100%;
  height: 400px;
}


</style>


  