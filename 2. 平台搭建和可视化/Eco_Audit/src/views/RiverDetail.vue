<template >
  <div class="main-container">
    <div class="sidebar">
      <h2>功能栏</h2>
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
        <h3>数据审查</h3>
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
      csvData: [], // 存储水质监测数据
      tableHeaders: [], // 表头
      attributes: ['水质类别', '水温', 'pH', '溶解氧', '高锰酸钾', '氨氮', '总磷', '总氮', '电导率', '浊度'], // 属性列表
      selectedAttribute: null, // 选中的属性
      showStatsSection: false, // 控制数据统计部分显示/隐藏
      showSection: '', // 当前显示的部分（数据展示、数据统计等）
      startDate: '2021-01-01', // 用户选择的开始日期，默认值设为2021-01-01
      endDate: '2021-12-31', // 用户选择的结束日期，默认值设为2021-12-31
      showChart: false, // 是否显示图表
      currentPage: 1, // 当前页
      pageSize: 50, // 每页显示的数据数量
    };
  },
  computed: {
    // 计算当前页的数据
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
    // 显示数据展示部分
    async showDataDisplay() {
      this.showSection = 'display'; // 切换到数据展示部分
      try {
        const response = await axios.get(`/public/province/Zhejiang/${encodeURIComponent(this.river)}202101-202112.csv`);
        Papa.parse(response.data, {
          header: true,
          dynamicTyping: true,
          complete: (result) => {
            this.csvData = result.data;
            this.tableHeaders = Object.keys(result.data[0]); // 获取CSV文件中的表头
            this.initAutoScroll();
          },
        });
      } catch (error) {
        console.error('数据加载失败', error);
      }
    },

    // 初始化自动滚动功能
    initAutoScroll() {
      const tableContainer = document.querySelector('.table-container');
      let scrollAmount = 0;
      const step = () => {
        scrollAmount += 1;
        tableContainer.scrollTop = scrollAmount;
        if (scrollAmount >= tableContainer.scrollHeight - tableContainer.clientHeight) {
          scrollAmount = 0; // 当到达底部时，重新开始
        }
        requestAnimationFrame(step);
      };
      requestAnimationFrame(step);
    },

    // 显示数据统计部分
    toggleDataStats() {
      this.showStatsSection = !this.showStatsSection; // 显示/隐藏属性选择部分
      this.showSection = 'stats'; // 切换到统计部分
    },

    // 显示选择的属性的图表
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

    // 处理 CSV 数据
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
      }));
    },

    // 初始化ECharts图表
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

    // 根据日期筛选数据
    filterDataByDate() {
      const start = new Date(this.startDate);
      const end = new Date(this.endDate);
      return this.csvData.filter(item => {
        const itemDate = new Date(item.time);
        return itemDate >= start && itemDate <= end;
      });
    },

    // 显示数据审查部分
    showDataReview() {
      this.showSection = 'review';
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
  background-color: #f9f9f9;
  padding: 10px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* 增加阴影效果 */
  background-color:rgb(245, 235, 217);
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  border: 1px solid #ccc;
  padding: 10px;
  text-align: left;
}

thead {
  background-color: #1abc9c; /* 表头背景 */
  color: #fff;
}
</style>
