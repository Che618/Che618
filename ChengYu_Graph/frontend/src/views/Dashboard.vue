<script setup lang="ts">
import { ref } from 'vue'

type PolicyInput = {
  key: string
  label: string
  unit: string
  value: number
  min: number
  max: number
}

const policies = ref<PolicyInput[]>([
  { key: 'subsidy', label: '育儿补贴金额', unit: '元/年', value: 6000, min: 0, max: 20000 },
  { key: 'leave', label: '产假天数', unit: '天', value: 180, min: 120, max: 240 },
  { key: 'housing', label: '购房优惠', unit: '%', value: 10, min: 0, max: 30 },
  { key: 'care', label: '托育服务覆盖率', unit: '%', value: 45, min: 10, max: 90 }
])
</script>

<template>
  <div class="grid gap-6 lg:grid-cols-[320px_1fr]">
    <section class="space-y-6 rounded-sm border border-white/10 bg-card-surface p-6">
      <div>
        <h2 class="font-serif text-lg">政策控制台</h2>
        <p class="mt-1 text-sm text-text-muted">
          拖动滑块调整政策参数，系统将暂存当前方案用于推演。
        </p>
      </div>

      <div class="space-y-5">
        <div v-for="policy in policies" :key="policy.key" class="space-y-2">
          <div class="flex items-center justify-between text-sm">
            <span>{{ policy.label }}</span>
            <span class="text-text-muted">{{ policy.value }} {{ policy.unit }}</span>
          </div>
          <input
            v-model="policy.value"
            :min="policy.min"
            :max="policy.max"
            type="range"
            class="h-1 w-full cursor-pointer accent-data-policy"
          />
        </div>
      </div>

      <button
        type="button"
        class="w-full rounded-sm border border-data-policy/60 px-4 py-2 text-sm text-data-policy transition hover:bg-data-policy/10"
      >
        预览政策组合
      </button>
    </section>

    <section class="space-y-6">
      <div class="rounded-sm border border-white/10 bg-card-surface p-6">
        <div class="flex items-start justify-between">
          <div>
            <h2 class="font-serif text-lg">出生率趋势模拟</h2>
            <p class="mt-1 text-sm text-text-muted">
              基准趋势与政策干预后的走势对比，体现政策弹性带来的变化。
            </p>
          </div>
          <div class="text-xs text-text-muted">未来 5-10 年</div>
        </div>
        <div class="mt-6 h-64 rounded-sm border border-dashed border-white/10 bg-bg-documentary/40">
          <div class="flex h-full items-center justify-center text-sm text-text-muted">
            折线图占位（ECharts）
          </div>
        </div>
        <div class="mt-4 flex items-center gap-4 text-xs text-text-muted">
          <span class="flex items-center gap-2">
            <span class="h-2 w-6 rounded-sm bg-text-muted/50"></span>
            基准趋势
          </span>
          <span class="flex items-center gap-2">
            <span class="h-2 w-6 rounded-sm bg-data-birth"></span>
            政策干预
          </span>
        </div>
      </div>

      <div class="rounded-sm border border-white/10 bg-card-surface p-6">
        <div class="flex items-start justify-between">
          <div>
            <h2 class="font-serif text-lg">区域响应热力图</h2>
            <p class="mt-1 text-sm text-text-muted">
              观察四川省各市州对政策的响应程度，支持区域差异对比。
            </p>
          </div>
          <div class="text-xs text-text-muted">四川省</div>
        </div>
        <div class="mt-6 h-64 rounded-sm border border-dashed border-white/10 bg-bg-documentary/40">
          <div class="flex h-full items-center justify-center text-sm text-text-muted">
            热力地图占位（ECharts）
          </div>
        </div>
      </div>
    </section>
  </div>
</template>
