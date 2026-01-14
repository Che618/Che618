# ZhiCe: 智策良育·区域生育政策仿真平台

一个面向「挑战杯」场景的生育政策仿真沙盘原型，包含前端交互界面与后端投影服务骨架。

## 项目结构

```
ChengYu_Graph/
├─ backend/                 # Spring Boot 3 + Java 17 后端
│  ├─ pom.xml
│  └─ src/main/
│     ├─ java/com/zhice/platform
│     │  ├─ BirthPolicySimApplication.java
│     │  ├─ controller/SimulationController.java
│     │  ├─ model/Result.java
│     │  └─ service/SimulationService.java
│     └─ resources/db/schema.sql
└─ frontend/                # Vue 3 + Vite + ECharts 前端
   ├─ package.json
   ├─ tailwind.config.ts
   ├─ postcss.config.js
   └─ src/components/
      ├─ MainLayout.vue
      └─ Dashboard.vue
```

## 运行环境

- Node.js 18+
- Java 17+
- Maven 3.9+
- MySQL 8.0（用于后续数据落库，可先不启动）

## 前端启动

```bash
cd frontend
npm install
npm run dev
```

启动后访问：<http://localhost:5173>

## 后端启动

```bash
cd backend
mvn spring-boot:run
```

默认接口：

- `POST http://localhost:8080/api/simulation/projection`

请求示例：

```json
[
  {"name": "育儿补贴金额", "value": 2000, "elasticity": 0.00008},
  {"name": "产假天数", "value": 120, "elasticity": 0.0012}
]
```

响应示例：

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "years": [2025, 2026, 2027, 2028, 2029],
    "baseTrend": [1.0, 1.01, 1.02, 1.03, 1.04],
    "policyTrend": [1.024, 1.0342, 1.0445, 1.0547, 1.065]
  }
}
```

## 数据库初始化（可选）

```bash
mysql -u <user> -p <database> < backend/src/main/resources/db/schema.sql
```

## 注意事项

- 若 `npm install` 因网络策略失败，请使用可访问的 npm 镜像源或配置企业代理。
- 该原型以展示「政策弹性系数」驱动的投影逻辑为核心，后续可接入 MyBatis-Plus 与真实人口数据。
