<script setup>
import { computed, onBeforeUnmount, onMounted, reactive, ref, watch } from 'vue'
import * as echarts from 'echarts'

const chartRef = ref(null)
const heatmapRef = ref(null)
let trendChart
let heatmapChart

const policyInputs = reactive([
  { key: 'subsidy', label: '育儿补贴金额', min: 0, max: 5000, unit: '元/月', value: 2000, elasticity: 0.00008 },
  { key: 'leave', label: '产假天数', min: 90, max: 240, unit: '天', value: 120, elasticity: 0.0012 },
  { key: 'housing', label: '购房优惠', min: 0, max: 30, unit: '%', value: 8, elasticity: 0.0024 },
  { key: 'nursery', label: '托育覆盖率', min: 10, max: 90, unit: '%', value: 35, elasticity: 0.0018 },
])

const baseTrend = [1.0, 1.01, 1.015, 1.02, 1.025]
const years = ['2025', '2026', '2027', '2028', '2029']

const policyImpact = computed(() =>
  policyInputs.reduce((sum, item) => sum + item.value * item.elasticity, 0)
)

const interventionTrend = computed(() =>
  baseTrend.map((value, index) => Number((value * (1 + policyImpact.value * 0.1) + index * 0.002).toFixed(3)))
)

const kpiCards = computed(() => [
  {
    title: '政策弹性强度',
    value: policyImpact.value.toFixed(2),
    unit: '指数',
    description: '弹性越高，代表政策杠杆对出生率的放大效应越强。',
  },
  {
    title: '模拟净增出生率',
    value: (interventionTrend.value[4] - baseTrend[4]).toFixed(3),
    unit: '指数',
    description: '对比基准趋势的最终增幅，用于衡量五年政策收益。',
  },
  {
    title: '政策稳定性',
    value: (100 - Math.min(policyImpact.value * 12, 35)).toFixed(1),
    unit: '%',
    description: '反映政策投入波动对地区系统韧性的影响。',
  },
])

const heatmapData = computed(() => {
  const cities = ['成都', '绵阳', '德阳', '宜宾', '南充', '乐山', '泸州']
  return cities.flatMap((city, xIndex) =>
    ['高新', '主城', '近郊'].map((district, yIndex) => [
      xIndex,
      yIndex,
      Number((Math.abs(Math.sin(policyImpact.value + xIndex + yIndex)) * 100).toFixed(1)),
      `${city}${district}`,
    ])
  )
})

const initCharts = () => {
  if (chartRef.value) {
    trendChart = echarts.init(chartRef.value)
    trendChart.setOption({
      backgroundColor: 'transparent',
      tooltip: { trigger: 'axis', backgroundColor: 'rgba(47,45,45,0.9)', textStyle: { color: '#E6E0D6' } },
      legend: {
        textStyle: { color: '#9CA3AF' },
        data: ['基准趋势', '干预趋势'],
      },
      grid: { left: '5%', right: '5%', bottom: '8%', top: '15%', containLabel: true },
      xAxis: {
        type: 'category',
        data: years,
        axisLine: { lineStyle: { color: '#9CA3AF' } },
      },
      yAxis: {
        type: 'value',
        axisLine: { lineStyle: { color: '#9CA3AF' } },
        splitLine: { lineStyle: { color: 'rgba(255,255,255,0.08)' } },
      },
      series: [
        {
          name: '基准趋势',
          type: 'line',
          smooth: true,
          data: baseTrend,
          lineStyle: { color: '#9CA3AF', width: 2 },
          itemStyle: { color: '#9CA3AF' },
        },
        {
          name: '干预趋势',
          type: 'line',
          smooth: true,
          data: interventionTrend.value,
          lineStyle: { color: '#E07A5F', width: 3 },
          itemStyle: { color: '#E07A5F' },
          areaStyle: { color: 'rgba(224, 122, 95, 0.15)' },
          symbol: 'circle',
          symbolSize: 8,
        },
      ],
    })
  }

  if (heatmapRef.value) {
    heatmapChart = echarts.init(heatmapRef.value)
    heatmapChart.setOption({
      backgroundColor: 'transparent',
      tooltip: {
        formatter: ({ data }) => `${data[3]}：${data[2]}%`,
        backgroundColor: 'rgba(47,45,45,0.9)',
        textStyle: { color: '#E6E0D6' },
      },
      grid: { top: 40, left: 80, right: 20, bottom: 20 },
      xAxis: {
        type: 'category',
        data: ['成都', '绵阳', '德阳', '宜宾', '南充', '乐山', '泸州'],
        axisLine: { lineStyle: { color: '#9CA3AF' } },
        axisLabel: { color: '#9CA3AF' },
      },
      yAxis: {
        type: 'category',
        data: ['高新', '主城', '近郊'],
        axisLine: { lineStyle: { color: '#9CA3AF' } },
        axisLabel: { color: '#9CA3AF' },
      },
      visualMap: {
        min: 0,
        max: 100,
        orient: 'horizontal',
        left: 'center',
        bottom: 0,
        textStyle: { color: '#9CA3AF' },
        inRange: {
          color: ['#2F2D2D', '#81B29A'],
        },
      },
      series: [
        {
          type: 'heatmap',
          data: heatmapData.value,
          label: {
            show: true,
            color: '#E6E0D6',
          },
        },
      ],
    })
  }
}

const updateCharts = () => {
  if (trendChart) {
    trendChart.setOption({
      series: [
        { data: baseTrend },
        { data: interventionTrend.value },
      ],
    })
  }
  if (heatmapChart) {
    heatmapChart.setOption({
      series: [
        {
          data: heatmapData.value,
        },
      ],
    })
  }
}

watch(policyInputs, updateCharts, { deep: true })

onMounted(() => {
  initCharts()
  window.addEventListener('resize', updateCharts)
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', updateCharts)
  trendChart?.dispose()
  heatmapChart?.dispose()
})
</script>

<template>
  <div class="grid gap-6 lg:grid-cols-[320px_1fr]">
    <section class="glass-panel rounded-sm p-6">
      <header class="mb-6">
        <h2 class="font-serif text-xl">政策调节控制台</h2>
        <p class="text-sm text-text-muted">拖动滑块，实时模拟未来5年生育率曲线。</p>
      </header>

      <div class="mb-6 grid gap-4 md:grid-cols-3">
        <div
          v-for="card in kpiCards"
          :key="card.title"
          class="rounded-sm border border-text-muted/20 bg-card-surface/70 p-4"
        >
          <p class="text-xs text-text-muted">{{ card.title }}</p>
          <p class="mt-2 font-serif text-2xl text-text-primary">
            {{ card.value }}
            <span class="text-xs text-text-muted">{{ card.unit }}</span>
          </p>
          <p class="mt-2 text-xs text-text-muted">{{ card.description }}</p>
        </div>
      </div>

      <div class="space-y-6">
        <div
          v-for="item in policyInputs"
          :key="item.key"
          class="space-y-2"
        >
          <div class="flex items-center justify-between text-sm">
            <span>{{ item.label }}</span>
            <span class="text-text-muted">{{ item.value }} {{ item.unit }}</span>
          </div>
          <input
            v-model.number="item.value"
            type="range"
            class="w-full accent-data-birth"
            :min="item.min"
            :max="item.max"
          />
          <div class="flex justify-between text-xs text-text-muted">
            <span>{{ item.min }}</span>
            <span>{{ item.max }}</span>
          </div>
          <p class="text-[11px] text-text-muted">
            弹性系数：{{ item.elasticity }}（每增加 1 单位投入的出生率响应）
          </p>
        </div>
      </div>

      <div class="mt-8 rounded-sm border border-text-muted/30 p-4 text-sm">
        <p class="text-text-muted">综合政策强度指数</p>
        <p class="font-serif text-2xl text-data-policy">{{ policyImpact.toFixed(2) }}</p>
        <p class="mt-2 text-xs text-text-muted">指数越高，代表政策对出生率的正向影响越强。</p>
      </div>
      <div class="mt-6 rounded-sm border border-data-birth/30 bg-card-surface/60 p-4 text-xs text-text-muted">
        建议：当前组合更偏向短期激励，若要增强长期信心，可提高托育覆盖率与住房稳定因子。
      </div>
    </section>

    <section class="space-y-6">
      <div class="glass-panel rounded-sm p-6">
        <header class="mb-4 flex items-center justify-between">
          <h3 class="font-serif text-lg">出生率趋势对比</h3>
          <span class="text-xs text-text-muted">单位：标准化指数</span>
        </header>
        <p class="mb-4 text-xs text-text-muted">
          基准趋势呈现自然人口演化，干预趋势叠加政策弹性后生成，曲线的差距代表政策的累积影响。
        </p>
        <div ref="chartRef" class="h-72 w-full"></div>
      </div>

      <div class="glass-panel rounded-sm p-6">
        <header class="mb-4 flex items-center justify-between">
          <h3 class="font-serif text-lg">四川省响应热力矩阵</h3>
          <span class="text-xs text-text-muted">区域政策响应程度</span>
        </header>
        <p class="mb-4 text-xs text-text-muted">
          以地市为横轴、功能区为纵轴，颜色越深表示政策响应越积极。
        </p>
        <div ref="heatmapRef" class="h-64 w-full"></div>
      </div>
    </section>
  </div>
</template>
