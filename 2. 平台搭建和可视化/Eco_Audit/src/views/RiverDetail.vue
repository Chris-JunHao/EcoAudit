<template>
  <div class="main-container">
    <div class="sidebar">
      <h2 >功能栏</h2>
      <ul>
        <!-- 数据展示控件 -->
        <li @click="showDataDisplay">数据展示</li>

        <!-- 数据统计控件 -->
        <li @click="toggleDataStats">数据统计</li>
        <div v-if="showStatsSection" class="submenu">
          <!-- 属性选择和日期选择 -->
          <label for="attribute">选择属性:</label>
          <select id="attribute" v-model="selectedAttribute">
            <option v-for="attr in attributes" :key="attr" :value="attr">{{ attr }}</option>
          </select>

          <label for="start-date">开始日期:</label>
          <input type="date" id="start-date" v-model="startDate" min="2021-01-01" max="2021-12-31" />

          <label for="end-date">结束日期:</label>
          <input type="date" id="end-date" v-model="endDate" min="2021-01-01" max="2021-12-31" />

          <button @click="showAttributeChart">显示属性图表</button>
        </div>

        <!-- 数据审查控件 -->
        <li @click="showDataReview">数据审查</li>
      </ul>
    </div>

    <div class="content">
      <!-- 数据展示部分 -->
      <div v-if="showSection === 'display'">
        <h3>数据展示</h3>
        <div class="table-container">
          <table>
            <thead>
              <tr>
                <th v-for="(header, index) in tableHeaders" :key="index">{{ header }}</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(row, index) in paginatedData" :key="index">
                <td v-for="(value, key) in row" :key="key">{{ value }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- 数据统计部分 -->
      <div v-if="showSection === 'stats'">
        <h3>{{ selectedAttribute }} 图表</h3>
        <div id="chart" style="width: 100%; height: 400px;"></div>
      </div>

      <!-- 数据审查部分 -->
      <div v-if="showSection === 'review'">
        <h3>异常数据审查</h3>
        <div v-if="showTable" class="table-container">
          <table>
            <thead>
              <tr>
                <th v-for="(header, index) in reviewHeaders" :key="index">{{ header }}</th>
                <th>操作</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(row, index) in filteredData" :key="index">
                <td v-for="(header, idx) in reviewHeaders" :key="idx">{{ row[header] }}</td>
                <td>
                  <button @click="showSHAPChart(index)">显示 SHAP 图表</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <div v-else>
          <div id="shap-chart" style="width: 100%; height: 400px;"></div>
          <button @click="showTable = true">返回表格</button>
        </div>
      </div>
    </div>
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
      csvData: [],
      tableHeaders: [],
      attributes: ['水质类别', '水温', 'pH', '溶解氧', '高锰酸钾', '氨氮', '总磷', '总氮', '电导率', '浊度'],
      shapAttributes: ['SHAP_水温', 'SHAP_pH', 'SHAP_溶解氧', 'SHAP_高锰酸钾', 'SHAP_氨氮', 'SHAP_总磷', 'SHAP_总氮', 'SHAP_电导率', 'SHAP_浊度'],
      selectedAttribute: null,
      showStatsSection: false,
      showSection: '',
      startDate: '2021-01-01',
      endDate: '2021-12-31',
      showChart: false,
      isChartVisible: [],
      currentPage: 1,
      pageSize: 50,
      showTable: true,
      reviewHeaders: [
        '城市', '河流', '流域', '断面名称', '监测时间',
        '水质类别', '水温', 'pH', '溶解氧', '高锰酸钾',
        '氨氮', '总磷', '总氮', '电导率', '浊度'
      ],
      filteredData: [], // 存储异常数据
    };
  },
  computed: {
    paginatedData() {
      const start = (this.currentPage - 1) * this.pageSize;
      const end = start + this.pageSize;
      return this.csvData.slice(start, end);
    },
    totalPages() {
      return Math.ceil(this.csvData.length / this.pageSize);
    },
  },
  methods: {
    async showDataDisplay() {
      this.showSection = 'display';
      try {
        const response = await axios.get(`/public/province/Zhejiang/${encodeURIComponent(this.river)}202101-202112.csv`);
        Papa.parse(response.data, {
          header: true,
          dynamicTyping: true,
          complete: (result) => {
            this.csvData = result.data;
            this.tableHeaders = Object.keys(result.data[0]);
            this.initAutoScroll();
          },
        });
      } catch (error) {
        console.error('数据加载失败', error);
      }
    },

    async showDataReview() {
      this.showSection = 'review';
      try {
        const response = await axios.get(`/public/province/Zhejiang/Anomaly/${encodeURIComponent(this.river)}.csv`);
        Papa.parse(response.data, {
          header: true,
          dynamicTyping: true,
          complete: (result) => {
            this.filteredData = result.data.filter(row => row.Anomaly);
            this.isChartVisible = this.filteredData.map(() => false);
            this.showTable = true; // 默认显示表格
          },
        });
      } catch (error) {
        console.error('异常数据加载失败', error);
      }
    },

    showSHAPChart(index) {
      this.showTable = false;
      this.$nextTick(() => {
        const chartContainer = document.getElementById('shap-chart');
        if (chartContainer) {
          const chart = echarts.init(chartContainer);
          const selectedRow = this.filteredData[index];
          const shapData = this.shapAttributes.map(attr => {
            const value = selectedRow[attr];
            return value < 0 ? 0 : value;
          });

          const option = {
            title: { text: 'SHAP 值分析' },
            tooltip: { trigger: 'axis' },
            xAxis: { type: 'category', data: this.shapAttributes },
            yAxis: { type: 'value' },
            series: [
              {
                name: 'SHAP 值',
                type: 'bar',
                data: shapData.sort((a, b) => b - a),
              },
            ],
          };
          chart.setOption(option);
        }
      });
    },

    initAutoScroll() {
      const tableContainer = document.querySelector('.table-container');
      let scrollAmount = 0;
      const step = () => {
        scrollAmount += 1;
        tableContainer.scrollTop = scrollAmount;
        if (scrollAmount >= tableContainer.scrollHeight - tableContainer.clientHeight) {
          scrollAmount = 0;
        }
        requestAnimationFrame(step);
      };
      requestAnimationFrame(step);
    },

    toggleDataStats() {
      this.showStatsSection = !this.showStatsSection;
      this.showSection = 'stats';
    },

    async showAttributeChart() {
      if (!this.selectedAttribute) {
        alert('请选择属性');
        return;
      }
      try {
        const response = await axios.get(`/public/province/Zhejiang/${encodeURIComponent(this.river)}202101-202112.csv`);
        Papa.parse(response.data, {
          header: true,
          dynamicTyping: true,
          complete: (result) => {
            this.csvData = this.processCSV(result.data);
            this.filteredData = this.filterDataByDate();
            this.showChart = true;
            this.$nextTick(() => {
              this.initChart();
            });
          },
        });
      } catch (error) {
        console.error('数据加载失败', error);
      }
    },

    processCSV(data) {
      return data.map(item => ({
        time: item['监测时间'],
        waterQuality: item['水质类别'],
        waterTemperature: item['水温'],
        pH: item['pH'],
        dissolvedOxygen: item['溶解氧'],
        potassiumPermanganate: item['高锰酸钾'],
        ammoniaNitrogen: item['氨氮'],
        totalPhosphorus: item['总磷'],
        totalNitrogen: item['总氮'],
        conductivity: item['电导率'],
        turbidity: item['浊度'],
        ...this.shapAttributes.reduce((acc, attr) => {
          acc[attr] = item[attr];
          return acc;
        }, {}),
      }));
    },

    initChart() {
      const chart = echarts.init(document.getElementById('chart'));
      const attributeMap = {
        '水质类别': 'waterQuality',
        '水温': 'waterTemperature',
        'pH': 'pH',
        '溶解氧': 'dissolvedOxygen',
        '高锰酸钾': 'potassiumPermanganate',
        '氨氮': 'ammoniaNitrogen',
        '总磷': 'totalPhosphorus',
        '总氮': 'totalNitrogen',
        '电导率': 'conductivity',
        '浊度': 'turbidity',
      };

      if (this.selectedAttribute === '水质类别') {
        const waterQualityCount = {};
        this.filteredData.forEach(item => {
          const category = item.waterQuality;
          if (category) {
            waterQualityCount[category] = (waterQualityCount[category] || 0) + 1;
          }
        });
        const pieData = Object.keys(waterQualityCount).map(category => ({
          name: category,
          value: waterQualityCount[category],
        }));

        const option = {
          title: { text: `${this.selectedAttribute} 数据`, left: 'center' },
          tooltip: { trigger: 'item' },
          legend: { orient: 'vertical', left: 'left' },
          series: [
            {
              name: '水质类别',
              type: 'pie',
              radius: '50%',
              data: pieData,
              emphasis: {
                itemStyle: {
                  shadowBlur: 10,
                  shadowOffsetX: 0,
                  shadowColor: 'rgba(0, 0, 0, 0.5)',
                },
              },
            },
          ],
        };
        chart.setOption(option);
      } else {
        const times = this.filteredData.map(item => item.time);
        const values = this.filteredData.map(item => item[attributeMap[this.selectedAttribute]]);

        const option = {
          title: { text: `${this.selectedAttribute} 数据` },
          tooltip: { trigger: 'axis' },
          xAxis: { type: 'category', data: times },
          yAxis: { type: 'value' },
          series: [
            {
              name: this.selectedAttribute,
              type: 'line',
              data: values,
            },
          ],
        };
        chart.setOption(option);
      }
    },

    filterDataByDate() {
      const start = new Date(this.startDate);
      const end = new Date(this.endDate);
      return this.csvData.filter(item => {
        const itemDate = new Date(item.time);
        return itemDate >= start && itemDate <= end;
      });
    },
  },
};
</script>

<style scoped>
.main-container {
  display: flex;
  height: 100vh;
  background-color: #f9f9f9; /* 使用柔和的背景色 */
}

.sidebar {
  width: 20%;
  background-color: #34495e; /* 功能栏背景改为深色，提升整体对比度 */
  padding: 20px;
  color: #ecf0f1; /* 浅色字体 */
  box-shadow: 2px 0 8px rgba(0, 0, 0, 0.1); /* 增加阴影效果 */
  font-family: 'Arial', sans-serif;
}
.sidebar h2 {
  font-size: 24px;
  margin-bottom: 15px;
  border-bottom: 1px solid #2c3e50;
  padding-bottom: 10px;
}

.content {
  background-color: rgb(171, 212, 238);
  width: 80%;
  padding: 20px;
}

li {
  cursor: pointer;
  padding: 15px 10px;
  margin-bottom: 10px;
  background-color: #2c3e50; /* 列表项背景颜色 */
  border-radius: 5px;
  transition: background-color 0.3s, transform 0.3s ease; /* 添加平滑的过渡效果 */
}
li:hover {
  background-color: #1abc9c; /* 悬停时背景变为鲜明的绿色 */
  transform: translateX(5px); /* 悬停时有轻微的位移效果 */
  color: white; /* 悬停时文字变为白色 */
}
.submenu {
  margin-left: 10px;
  padding-left: 10px;
  border-left: 2px solid #2c3e50; /* 增加分隔线，清晰层次 */
  display: flex;
  flex-direction: column;
}
.submenu select,
.submenu input {
  margin-top: 10px;
  padding: 8px;
  background-color: #fff;
  border: 1px solid #ccc;
  border-radius: 4px;
}

button {
  margin-top: 15px;
  background-color: #1abc9c;
  color: white;
  border: none;
  padding: 12px 20px;
  font-size: 16px;
  cursor: pointer;
  border-radius: 5px;
  transition: background-color 0.3s ease; /* 增加按钮悬停效果 */
}

button:hover {
  background-color: #2a9662;
}

/* 数据展示部分样式 */
.table-container {
  height: 750px;
  overflow-y: auto; /* 实现垂直滚动 */
  padding: 10px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* 增加阴影效果 */
  background-color: rgb(193, 215, 248);

  /* 添加边框颜色和边框粗细 */
  border: 2px solid rgb(26, 27, 30); /* 设置边框颜色和粗细 */
}

.table-container table {
  width: 100%;
  border-collapse: collapse; /* 去掉单元格间隙 */
}

.table-container th, 
.table-container td {
  border: 2px solid rgb(39, 42, 48); /* 设置表格内部边框颜色和粗细 */
  padding: 8px;
  text-align: left;
}

thead {
  background-color: #1abc9c; /* 表头背景 */
  color: #fff;
}
h2{
  color: #ffffff;
}
</style>
