<script setup lang="ts">
import { ref } from 'vue'
import Dashboard from '../views/Dashboard.vue'

const activeMenu = ref('dashboard')
const city = ref('成都市')
const year = ref('2025')
</script>

<template>
  <div class="min-h-screen bg-bg-documentary text-text-primary">
    <div class="flex min-h-screen">
      <aside class="w-64 border-r border-white/10 bg-card-surface/90 backdrop-blur">
        <div class="px-6 py-6">
          <p class="font-serif text-xl tracking-wide">ZhiCe · 智策良育</p>
          <p class="mt-2 text-sm text-text-muted">区域生育政策仿真平台</p>
        </div>
        <nav class="mt-6 space-y-2 px-4">
          <button
            type="button"
            class="group flex w-full items-center gap-3 rounded-sm px-3 py-2 text-left transition"
            :class="activeMenu === 'dashboard' ? 'bg-white/5' : 'hover:bg-white/5'"
            @click="activeMenu = 'dashboard'"
          >
            <span
              class="h-5 w-1 rounded-sm"
              :class="activeMenu === 'dashboard' ? 'bg-data-birth' : 'bg-transparent'"
            ></span>
            <span class="text-sm">模拟沙盘</span>
          </button>
          <button
            type="button"
            class="group flex w-full items-center gap-3 rounded-sm px-3 py-2 text-left transition"
            :class="activeMenu === 'policy' ? 'bg-white/5' : 'hover:bg-white/5'"
            @click="activeMenu = 'policy'"
          >
            <span
              class="h-5 w-1 rounded-sm"
              :class="activeMenu === 'policy' ? 'bg-data-birth' : 'bg-transparent'"
            ></span>
            <span class="text-sm">政策库</span>
          </button>
        </nav>
      </aside>

      <div class="flex flex-1 flex-col">
        <header class="flex items-center justify-between border-b border-white/10 px-8 py-6">
          <div>
            <h1 class="font-serif text-2xl">智策良育</h1>
            <p class="mt-1 text-sm text-text-muted">区域生育政策仿真平台 · 决策沙盘</p>
          </div>
          <div class="rounded-sm border border-white/10 bg-card-surface px-4 py-2">
            <p class="text-xs text-text-muted">当前推演</p>
            <p class="text-sm">
              <span class="text-data-policy">{{ city }}</span>
              <span class="mx-2 text-text-muted">/</span>
              <span class="text-data-birth">{{ year }}</span>
            </p>
          </div>
        </header>

        <main class="flex-1 px-8 py-6">
          <Dashboard v-if="activeMenu === 'dashboard'" />
          <div v-else class="rounded-sm border border-white/10 bg-card-surface p-6 text-sm text-text-muted">
            政策库模块正在建设中，后续将支持政策模板与历史成效对比。
          </div>
        </main>
      </div>
    </div>
  </div>
</template>
