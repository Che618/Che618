<script setup>
import { ref } from 'vue'
import Dashboard from './Dashboard.vue'

const activeMenu = ref('simulation')

const menuItems = [
  { key: 'simulation', label: '政策仿真沙盘' },
  { key: 'dataset', label: '人口底座数据' },
  { key: 'policy', label: '政策因子库' },
  { key: 'report', label: '评估报告' },
]
</script>

<template>
  <div class="min-h-screen bg-bg-documentary text-text-primary">
    <div class="flex min-h-screen">
      <aside class="glass-panel w-72 px-6 py-8 shadow-soft">
        <div class="mb-10">
          <p class="font-serif text-lg tracking-[0.2em] text-text-muted">ZhiCe Platform</p>
          <h1 class="font-serif text-2xl">智策良育</h1>
          <p class="text-sm text-text-muted">区域生育政策仿真平台</p>
        </div>
        <nav class="space-y-3">
          <button
            v-for="item in menuItems"
            :key="item.key"
            class="group flex w-full items-center gap-3 rounded-sm px-3 py-2 text-left text-sm transition"
            :class="activeMenu === item.key ? 'bg-card-surface text-text-primary' : 'text-text-muted hover:text-text-primary'"
            @click="activeMenu = item.key"
          >
            <span
              class="h-8 w-1 rounded-sm"
              :class="activeMenu === item.key ? 'bg-data-birth' : 'bg-transparent group-hover:bg-text-muted/40'"
            ></span>
            <span>{{ item.label }}</span>
          </button>
        </nav>
      </aside>

      <div class="flex flex-1 flex-col">
        <header class="glass-panel flex items-center justify-between px-10 py-6">
          <div>
            <p class="font-serif text-2xl">智策良育 · 区域生育政策仿真</p>
            <p class="text-sm text-text-muted">当前沙盘：成都市 / 2025-2030</p>
          </div>
          <div class="flex items-center gap-4">
            <button class="ghost-button">导出政策简报</button>
            <button class="ghost-button">保存当前方案</button>
          </div>
        </header>

        <main class="flex-1 bg-bg-documentary px-10 py-8">
          <Dashboard />
        </main>
      </div>
    </div>
  </div>
</template>
