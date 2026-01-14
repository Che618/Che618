<script setup>
import { ref } from 'vue'
import GraphVisualization from './components/GraphVisualization.vue'
import DataAnalysis from './components/DataAnalysis.vue'

// 当前激活的视图
const activeView = ref('graph')
</script>

<template>
  <div class="app-container">
    <!-- 导航栏 -->
    <nav class="navbar">
      <div class="navbar-brand">
        <h1>成渝地区双城经济圈产业知识图谱</h1>
      </div>
      <div class="navbar-nav">
        <button 
          @click="activeView = 'graph'"
          :class="['nav-btn', { 'active': activeView === 'graph' }]"
        >
          产业关系图谱
        </button>
        <button 
          @click="activeView = 'analysis'"
          :class="['nav-btn', { 'active': activeView === 'analysis' }]"
        >
          数据分析
        </button>
      </div>
    </nav>
    
    <!-- 主内容区域 -->
    <main class="main-content">
      <component :is="activeView === 'graph' ? GraphVisualization : DataAnalysis" />
    </main>
    
    <!-- 页脚 -->
    <footer class="footer">
      <p>成渝地区双城经济圈产业知识图谱系统 &copy; 2024</p>
    </footer>
  </div>
</template>

<style scoped>
.app-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.navbar {
  background-color: #1890ff;
  color: white;
  padding: 0 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

.navbar-brand h1 {
  margin: 0;
  font-size: 20px;
}

.navbar-nav {
  display: flex;
  gap: 10px;
}

.nav-btn {
  background-color: transparent;
  color: white;
  border: 1px solid white;
  border-radius: 4px;
  padding: 8px 16px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.3s;
}

.nav-btn:hover {
  background-color: rgba(255, 255, 255, 0.2);
}

.nav-btn.active {
  background-color: white;
  color: #1890ff;
}

.main-content {
  flex: 1;
  background-color: #f5f5f5;
}

.footer {
  background-color: #333;
  color: white;
  text-align: center;
  padding: 10px;
  font-size: 14px;
}
</style>
