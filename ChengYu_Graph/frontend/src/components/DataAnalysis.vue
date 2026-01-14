<template>
  <div class="data-analysis">
    <div class="analysis-header">
      <h3>成渝地区产业数据统计分析</h3>
    </div>
    
    <div class="analysis-content">
      <!-- 产业分布饼图 -->
      <div class="chart-container">
        <h4>产业分布</h4>
        <div ref="industryChartRef" class="chart"></div>
      </div>
      
      <!-- 城市企业数量柱状图 -->
      <div class="chart-container">
        <h4>城市企业数量分布</h4>
        <div ref="cityChartRef" class="chart"></div>
      </div>
      
      <!-- 产业专利数量柱状图 -->
      <div class="chart-container">
        <h4>产业专利数量统计</h4>
        <div ref="patentChartRef" class="chart"></div>
      </div>
      
      <!-- 企业注册资本分布图 -->
      <div class="chart-container">
        <h4>企业注册资本分布</h4>
        <div ref="capitalChartRef" class="chart"></div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import * as echarts from 'echarts'
import axios from 'axios'

// 图表容器引用
const industryChartRef = ref(null)
const cityChartRef = ref(null)
const patentChartRef = ref(null)
const capitalChartRef = ref(null)

// 图表实例
const industryChart = ref(null)
const cityChart = ref(null)
const patentChart = ref(null)
const capitalChart = ref(null)

// 获取数据
const fetchData = async () => {
  try {
    const companiesResponse = await axios.get('http://localhost:5000/api/companies')
    const industriesResponse = await axios.get('http://localhost:5000/api/industries')
    
    return {
      companies: companiesResponse.data,
      industries: industriesResponse.data
    }
  } catch (error) {
    console.error('获取数据失败:', error)
    return { companies: [], industries: [] }
  }
}

// 初始化产业分布饼图
const initIndustryChart = (companies, industries) => {
  if (!industryChartRef.value) return
  
  // 计算各产业企业数量
  const industryCount = {}  
  industries.forEach(ind => {
    industryCount[ind.industry_name] = 0
  })
  
  companies.forEach(comp => {
    if (industryCount[comp.industry_name] !== undefined) {
      industryCount[comp.industry_name]++
    }
  })
  
  // 准备图表数据
  const chartData = Object.entries(industryCount).map(([name, value]) => {
    return { name, value }
  })
  
  // 图表配置
  const option = {
    tooltip: {
      trigger: 'item',
      formatter: '{a} <br/>{b}: {c} ({d}%)'
    },
    legend: {
      orient: 'vertical',
      left: 10,
      data: Object.keys(industryCount)
    },
    series: [
      {
        name: '产业分布',
        type: 'pie',
        radius: ['40%', '70%'],
        avoidLabelOverlap: false,
        itemStyle: {
          borderRadius: 10,
          borderColor: '#fff',
          borderWidth: 2
        },
        label: {
          show: false,
          position: 'center'
        },
        emphasis: {
          label: {
            show: true,
            fontSize: 20,
            fontWeight: 'bold'
          }
        },
        labelLine: {
          show: false
        },
        data: chartData
      }
    ]
  }
  
  // 创建图表实例
  industryChart.value = echarts.init(industryChartRef.value)
  industryChart.value.setOption(option)
}

// 初始化城市企业数量柱状图
const initCityChart = (companies) => {
  if (!cityChartRef.value) return
  
  // 计算各城市企业数量
  const cityCount = { '成都': 0, '重庆': 0 }
  
  companies.forEach(comp => {
    if (cityCount[comp.city] !== undefined) {
      cityCount[comp.city]++
    }
  })
  
  // 图表配置
  const option = {
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      }
    },
    xAxis: {
      type: 'category',
      data: Object.keys(cityCount)
    },
    yAxis: {
      type: 'value'
    },
    series: [
      {
        name: '企业数量',
        type: 'bar',
        data: Object.values(cityCount),
        itemStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: '#5B8FF9' },
            { offset: 1, color: '#5AD8A6' }
          ])
        }
      }
    ]
  }
  
  // 创建图表实例
  cityChart.value = echarts.init(cityChartRef.value)
  cityChart.value.setOption(option)
}

// 初始化产业专利数量柱状图
const initPatentChart = (companies, industries) => {
  if (!patentChartRef.value) return
  
  // 计算各产业专利总数
  const industryPatents = {}  
  industries.forEach(ind => {
    industryPatents[ind.industry_name] = 0
  })
  
  companies.forEach(comp => {
    if (industryPatents[comp.industry_name] !== undefined) {
      industryPatents[comp.industry_name] += comp.patent_count || 0
    }
  })
  
  // 图表配置
  const option = {
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      }
    },
    xAxis: {
      type: 'category',
      data: Object.keys(industryPatents),
      axisLabel: {
        rotate: 45
      }
    },
    yAxis: {
      type: 'value'
    },
    series: [
      {
        name: '专利数量',
        type: 'bar',
        data: Object.values(industryPatents),
        itemStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: '#F6BD16' },
            { offset: 1, color: '#E86452' }
          ])
        }
      }
    ]
  }
  
  // 创建图表实例
  patentChart.value = echarts.init(patentChartRef.value)
  patentChart.value.setOption(option)
}

// 初始化企业注册资本分布图
const initCapitalChart = (companies) => {
  if (!capitalChartRef.value) return
  
  // 按注册资本区间分组
  const capitalRanges = {
    '1000万以下': 0,
    '1000-3000万': 0,
    '3000-5000万': 0,
    '5000-1亿': 0,
    '1亿以上': 0
  }
  
  companies.forEach(comp => {
    const capital = comp.registered_capital || 0
    if (capital < 1000) {
      capitalRanges['1000万以下']++
    } else if (capital < 3000) {
      capitalRanges['1000-3000万']++
    } else if (capital < 5000) {
      capitalRanges['3000-5000万']++
    } else if (capital < 10000) {
      capitalRanges['5000-1亿']++
    } else {
      capitalRanges['1亿以上']++
    }
  })
  
  // 图表配置
  const option = {
    tooltip: {
      trigger: 'item',
      formatter: '{a} <br/>{b}: {c} ({d}%)'
    },
    legend: {
      orient: 'horizontal',
      bottom: 10,
      data: Object.keys(capitalRanges)
    },
    series: [
      {
        name: '注册资本分布',
        type: 'pie',
        radius: '60%',
        data: Object.entries(capitalRanges).map(([name, value]) => {
          return { name, value }
        }),
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.5)'
          }
        }
      }
    ]
  }
  
  // 创建图表实例
  capitalChart.value = echarts.init(capitalChartRef.value)
  capitalChart.value.setOption(option)
}

// 初始化所有图表
const initCharts = async () => {
  const data = await fetchData()
  
  initIndustryChart(data.companies, data.industries)
  initCityChart(data.companies)
  initPatentChart(data.companies, data.industries)
  initCapitalChart(data.companies)
}

// 响应窗口大小变化
const handleResize = () => {
  industryChart.value?.resize()
  cityChart.value?.resize()
  patentChart.value?.resize()
  capitalChart.value?.resize()
}

// 组件挂载时初始化图表
onMounted(() => {
  initCharts()
  window.addEventListener('resize', handleResize)
})

// 组件卸载时清理
watch(() => null, () => {
  window.removeEventListener('resize', handleResize)
  
  industryChart.value?.dispose()
  cityChart.value?.dispose()
  patentChart.value?.dispose()
  capitalChart.value?.dispose()
})
</script>

<style scoped>
.data-analysis {
  width: 100%;
  min-height: 100vh;
  background-color: #f5f5f5;
  padding: 20px;
}

.analysis-header {
  text-align: center;
  margin-bottom: 30px;
}

.analysis-header h3 {
  color: #333;
  margin: 0;
}

.analysis-content {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 20px;
}

.chart-container {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  padding: 20px;
}

.chart-container h4 {
  margin-top: 0;
  color: #333;
  text-align: center;
  margin-bottom: 20px;
}

.chart {
  height: 300px;
  width: 100%;
}

@media (max-width: 768px) {
  .analysis-content {
    grid-template-columns: 1fr;
  }
  
  .chart-container {
    padding: 15px;
  }
  
  .chart {
    height: 250px;
  }
}
</style>