<template>
  <div class="main-container">
    <!-- 左边功能栏 -->
    <div class="sidebar">
      <h2>功能栏</h2>
      <ul>
        <!-- 数据概览部分 -->
        <li @click="toggleOverview">数据概览</li>
        <div v-if="showOverviewSection" class="submenu">
          <button class="big-button" @click="toggleStatsSection">数据统计</button>
          <div v-if="showStatsSection">
            <!-- 选择属性和日期 -->
            <label for="attribute">选择属性:</label>
            <select id="attribute" v-model="selectedAttribute">
              <option v-for="attr in attributes" :key="attr" :value="attr">{{ attr }}</option>
            </select>

            <label for="start-date">开始日期:</label>
            <input type="date" id="start-date" v-model="startDate" min="2021-01-01" max="2021-12-31" />

            <label for="end-date">结束日期:</label>
            <input type="date" id="end-date" v-model="endDate" min="2021-01-01" max="2021-12-31" />

            <button class="mid-button" @click="showAttributeChart">显示图表</button>
          </div>
          <button class="big-button" @click="showDataDisplay">数据展示</button>
        </div>

        <!-- 河流详情部分 -->
        <li @click="toggleRiverDetails">河流详情</li>
        <div v-if="showRiverSection" class="submenu">
          <h2>选择河流</h2>
          <div class="scroll-container">
            <ul>
              <li v-for="river in rivers" :key="river" @click="selectRiver(river)">
                {{ river }}
              </li>
            </ul>
          </div>
        </div>
      </ul>
    </div>

    <!-- 右侧内容 -->
    <div class="content">
      <!-- 省份地图 -->
      <div v-if="showSection === ''">
        <h2>{{ province }}的地图</h2>
        <img src="/Zhejiang.jpg" alt="Water Quality Image" class="main-image" />
      </div>

      <!-- 数据统计部分 -->
      <div v-if="showSection === 'stats'">
        <h3>{{ selectedAttribute }} 图表</h3>
        <div id="chart" style="width: 100%; height: 400px;"></div>
      </div>

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
      showOverviewSection: false,
      showStatsSection: false,
      showRiverSection: false,
      showSection: '',
      rivers: ['东苕溪', '分水江', '富春江', '京杭运河', '南苕溪', '千岛湖', '钱塘江', '浦阳江', '新安江'], // 河流列表
      selectedAttribute: null,
      csvData: [],
      tableHeaders: [],
      attributes: ['水质类别', '水温', 'pH', '溶解氧', '高锰酸钾', '氨氮', '总磷', '总氮', '电导率', '浊度'],
      startDate: '2021-01-01',
      endDate: '2021-12-31',
      currentPage: 1,
      pageSize: 50,
    };
  },
  computed: {
    paginatedData() {
      const start = (this.currentPage - 1) * this.pageSize;
      const end = start + this.pageSize;
      return this.csvData.slice(start, end);
    },
  },
  methods: {
    toggleOverview() {
      this.showOverviewSection = !this.showOverviewSection;
    },
    toggleStatsSection() {
      this.showStatsSection = !this.showStatsSection;
      this.showSection = 'stats';
    },
    toggleRiverDetails() {
      this.showRiverSection = !this.showRiverSection;
    },
    showDataDisplay() {
      this.showSection = 'display';
      this.loadExcelData();
    },
    async loadExcelData() {
      try {
        const response = await axios.get(`/public/province/Zhejiang/浙江杭州2021.csv`);
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
        console.error('加载数据失败:', error);
      }
    },
    showAttributeChart() {
      const chart = echarts.init(document.getElementById('chart'));
      const data = this.csvData.filter(row => {
        const date = new Date(row['监测时间']);
        return date >= new Date(this.startDate) && date <= new Date(this.endDate);
      });

      if (this.selectedAttribute === '水质类别') {
        const waterQualityCount = {};
        data.forEach(item => {
          const category = item['水质类别'];
          if (category) {
            waterQualityCount[category] = (waterQualityCount[category] || 0) + 1;
          }
        });

        const pieData = Object.keys(waterQualityCount).map(category => ({
          name: category,
          value: waterQualityCount[category],
        }));

        const option = {
          title: { text: '水质类别统计', left: 'center' },
          tooltip: { trigger: 'item' },
          series: [
            {
              name: '水质类别',
              type: 'pie',
              radius: '50%',
              data: pieData,
            },
          ],
        };

        chart.setOption(option);
      } else {
        const times = data.map(item => item['监测时间']);
        const values = data.map(item => item[this.selectedAttribute]);

        const option = {
          title: { text: `${this.selectedAttribute} 变化图` },
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
    selectRiver(river) {
      this.$router.push({ name: 'RiverDetail', params: { river } });
    },
  },
};
</script>

<style scoped>
.main-container {
  display: flex;
  background-color: #f9f9f9;
  height: 100vh;
}

.sidebar {
  width: 20%;
  background-color: #2c3e50; /* 使用深色背景 */
  color: #ecf0f1; /* 文字颜色改为浅色 */
  padding: 20px;
  box-shadow: 2px 0 10px rgba(0, 0, 0, 0.1); /* 增加较明显的阴影 */
  font-family: 'Arial', sans-serif;
  border-radius: 0 10px 10px 0; /* 增加圆角，柔化边缘 */
}
.sidebar h2 {
  font-size: 24px;
  color: #ecf0f1;
  margin-bottom: 15px;
  border-bottom: 1px solid #34495e;
  padding-bottom: 10px;
}

.content {
  width: 80%;
  padding: 20px;
  background-color: rgb(171, 212, 238);
}

.table-container {
  height: 750px;
  overflow: hidden;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 10px;
}

table {
  width: 100%;
  border-collapse: collapse;
  font-size: 14px;
}

th, td {
  border: 1px solid #ccc;
  padding: 10px;
  text-align: left;
}

thead {
  background-color: #7bd27f;
  color: #fff;
}

ul {
  list-style-type: none;
  padding: 0;
  margin-top: 20px;
}

li {
  cursor: pointer;
  padding: 15px 10px;
  background-color: #34495e; /* 列表项背景颜色加深 */
  margin-bottom: 10px;
  border-radius: 5px;
  transition: all 0.3s ease; /* 增加过渡效果 */
  display: flex;
  align-items: center; /* 居中对齐文字 */
  font-size: 16px;
}

li:hover {
  background-color: #1abc9c; /* 悬停时背景变为鲜艳的绿色 */
  color: white;
  transform: translateX(5px); /* 悬停时有轻微的移动效果 */
}


.submenu {
  margin-left: 20px;
  display: flex;
  flex-direction: column;
}


.submenu button {
  margin-top: 10px;
  background-color: #1abc9c;
  color: white;
  border: none;
  padding: 12px;
  border-radius: 5px;
  font-size: 16px;
  transition: background-color 0.3s ease;
}

.submenu button:hover {
  background-color: #16a085;
}

.scroll-container {
  max-height: 300px;
  overflow-y: auto;
  border: 1px solid #34495e;
  padding: 10px;
  border-radius: 5px;
  background-color: #34495e;
}

.main-image {
  max-width: 85%;
  height: auto;
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.big-button {
  padding: 12px;
}

.mid-button {
  padding: 8px;
  background-color: #42b983;
  color: #fff;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  transition: background-color 0.3s ease;
}

.mid-button:hover {
  background-color: #358d6a;
}
</style>
