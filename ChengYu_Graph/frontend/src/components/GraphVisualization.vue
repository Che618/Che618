<template>
  <div class="graph-container">
    <div class="graph-header">
      <h3>成渝地区双城经济圈产业关系图谱</h3>
      <div class="graph-controls">
        <button @click="refreshGraph" class="control-btn">刷新图谱</button>
        <button @click="resetZoom" class="control-btn">重置缩放</button>
      </div>
    </div>
    <div ref="graphRef" class="graph-content"></div>
    <div v-if="selectedNode" class="node-detail">
      <h4>企业详情</h4>
      <p><strong>企业名称:</strong> {{ selectedNode.label }}</p>
      <p><strong>所属产业:</strong> {{ selectedNode.industry }}</p>
      <p><strong>所在城市:</strong> {{ selectedNode.city }}</p>
      <p><strong>注册资本:</strong> {{ selectedNode.registered_capital }} 万元</p>
      <p><strong>专利数量:</strong> {{ selectedNode.patent_count }}</p>
      <p><strong>员工数量:</strong> {{ selectedNode.employee_count }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import * as G6 from '@antv/g6'
import axios from 'axios'

const graphRef = ref(null)
const graph = ref(null)
const selectedNode = ref(null)

// 图谱配置
const graphConfig = {
  container: null,
  width: 800,
  height: 600,
  modes: {
    default: [
      'drag-canvas',
      'zoom-canvas',
      'drag-node',
      'click-select'
    ]
  },
  defaultNode: {
    type: 'circle',
    size: [60, 60],
    style: {
      fill: '#C6E5FF',
      stroke: '#5B8FF9',
      lineWidth: 2
    },
    labelCfg: {
      style: {
        fill: '#000',
        fontSize: 12
      }
    }
  },
  defaultEdge: {
    type: 'polyline',
    style: {
      radius: 10,
      offset: 20,
      endArrow: true,
      stroke: '#aaa'
    },
    labelCfg: {
      autoRotate: true,
      style: {
        fill: '#666',
        fontSize: 10
      }
    }
  },
  layout: {
    type: 'force',
    preventOverlap: true,
    nodeSpacing: 80,
    linkDistance: 120
  }
}

// 获取图谱数据
const fetchGraphData = async () => {
  try {
    const response = await axios.get('http://localhost:5000/api/graph-data')
    return response.data
  } catch (error) {
    console.error('获取图谱数据失败:', error)
    return { nodes: [], edges: [] }
  }
}

// 初始化图谱
const initGraph = async () => {
  if (!graphRef.value) return
  
  // 获取数据
  const graphData = await fetchGraphData()
  
  // 配置容器
  graphConfig.container = graphRef.value
  graphConfig.width = graphRef.value.offsetWidth
  graphConfig.height = graphRef.value.offsetHeight
  
  // 创建图谱实例
  graph.value = new G6.Graph(graphConfig)
  
  // 注册节点类型
  G6.registerNode('company-node', {
    draw(cfg, group) {
      const { label = '', industry, city } = cfg
      const nodeSize = [80, 40]
      
      // 根据产业设置不同颜色
      const industryColors = {
        '电子信息': '#5B8FF9',
        '汽车制造': '#5AD8A6',
        '软件服务': '#F6BD16',
        '新材料': '#E86452',
        '生物医药': '#6DC8EC',
        '新能源': '#9270CA',
        '物流运输': '#FF9D4D',
        '航空航天': '#269A99',
        '数字经济': '#FF99C3'
      }
      
      const color = industryColors[industry] || '#5B8FF9'
      
      // 创建节点矩形
      const rect = group.addShape('rect', {
        attrs: {
          x: -nodeSize[0] / 2,
          y: -nodeSize[1] / 2,
          width: nodeSize[0],
          height: nodeSize[1],
          radius: 5,
          fill: color,
          stroke: '#fff',
          lineWidth: 2
        },
        name: 'rect-shape'
      })
      
      // 添加企业名称标签
      group.addShape('text', {
        attrs: {
          text: label,
          x: 0,
          y: 0,
          fontSize: 12,
          fill: '#fff',
          textAlign: 'center',
          textBaseline: 'middle'
        },
        name: 'label-shape'
      })
      
      return rect
    }
  })
  
  // 注册边类型
  G6.registerEdge('company-relation', {
    draw(cfg, group) {
      const { startPoint, endPoint } = cfg
      const controlPoints = [
        {
          x: (startPoint.x + endPoint.x) / 2,
          y: startPoint.y
        },
        {
          x: (startPoint.x + endPoint.x) / 2,
          y: endPoint.y
        }
      ]
      
      const path = [
        ['M', startPoint.x, startPoint.y],
        ['Q', controlPoints[0].x, controlPoints[0].y, (startPoint.x + endPoint.x) / 2, (startPoint.y + endPoint.y) / 2],
        ['Q', controlPoints[1].x, controlPoints[1].y, endPoint.x, endPoint.y]
      ]
      
      // 根据关系类型设置不同颜色
      const relationColors = {
        'SUPPLY': '#5B8FF9',
        'INVEST': '#F6BD16',
        'COLLABORATE': '#5AD8A6',
        'TECHNICAL_SUPPORT': '#E86452'
      }
      
      const color = relationColors[cfg.type] || '#aaa'
      
      // 创建边
      const edge = group.addShape('path', {
        attrs: {
          path,
          stroke: color,
          lineWidth: 2,
          endArrow: {
            path: G6.Arrow.triangle(5, 10, 0),
            fill: color
          }
        },
        name: 'edge-path'
      })
      
      // 添加关系类型标签
      group.addShape('text', {
        attrs: {
          text: cfg.type || '',
          x: (startPoint.x + endPoint.x) / 2,
          y: (startPoint.y + endPoint.y) / 2 - 10,
          fontSize: 10,
          fill: '#666',
          textAlign: 'center',
          textBaseline: 'middle'
        },
        name: 'edge-label'
      })
      
      return edge
    }
  })
  
  // 处理节点点击事件
  graph.value.on('node:click', (e) => {
    selectedNode.value = e.item.getModel()
    
    // 高亮选中节点
    graph.value.getNodes().forEach(node => {
      node.setState('selected', false)
    })
    e.item.setState('selected', true)
  })
  
  // 渲染图谱
  graph.value.data(graphData)
  graph.value.render()
}

// 刷新图谱
const refreshGraph = async () => {
  if (!graph.value) return
  
  const graphData = await fetchGraphData()
  graph.value.changeData(graphData)
}

// 重置缩放
const resetZoom = () => {
  if (graph.value) {
    graph.value.fitView()
  }
}

// 响应窗口大小变化
const handleResize = () => {
  if (graph.value && graphRef.value) {
    graph.value.changeSize(graphRef.value.offsetWidth, graphRef.value.offsetHeight)
  }
}

// 组件挂载时初始化
onMounted(() => {
  initGraph()
  window.addEventListener('resize', handleResize)
})

// 组件卸载时清理
watch(() => null, () => {
  window.removeEventListener('resize', handleResize)
  if (graph.value) {
    graph.value.destroy()
  }
})
</script>

<style scoped>
.graph-container {
  width: 100%;
  height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: #f5f5f5;
}

.graph-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 20px;
  background-color: #fff;
  border-bottom: 1px solid #e0e0e0;
}

.graph-header h3 {
  margin: 0;
  color: #333;
}

.graph-controls {
  display: flex;
  gap: 10px;
}

.control-btn {
  padding: 6px 12px;
  background-color: #1890ff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

.control-btn:hover {
  background-color: #40a9ff;
}

.graph-content {
  flex: 1;
  overflow: hidden;
}

.node-detail {
  position: absolute;
  top: 80px;
  right: 20px;
  width: 280px;
  background-color: white;
  padding: 15px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  z-index: 100;
}

.node-detail h4 {
  margin-top: 0;
  color: #333;
  border-bottom: 1px solid #e0e0e0;
  padding-bottom: 8px;
}

.node-detail p {
  margin: 8px 0;
  color: #666;
}
</style>