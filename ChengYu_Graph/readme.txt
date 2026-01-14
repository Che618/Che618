


          
为了运行成渝地区双城经济圈产业知识图谱系统，您需要启动前后端两个服务。以下是详细的运行步骤：

### 1. 启动后端服务
后端服务是基于Flask的API服务，负责数据存储和业务逻辑处理：

**操作步骤：**
1. 打开终端，进入项目根目录：
   ```powershell
   cd d:/MySystem/ChengYu_Graph
   ```
2. 执行启动命令：
   ```powershell
   python app.py
   ```

**预期结果：**
- 控制台输出类似信息：
  ```
  * Serving Flask app 'app'
  * Debug mode: on
  WARNING: This is a development server. Do not use it in a production deployment.
  * Running on http://127.0.0.1:5000
  Press CTRL+C to quit
  ```
- 后端服务将在 `http://127.0.0.1:5000` 上运行

### 2. 启动前端服务
前端服务是基于Vue3的可视化界面，负责展示产业关系图谱和数据分析结果：

**操作步骤：**
1. 打开另一个终端，进入前端项目目录：
   ```powershell
   cd d:/MySystem/ChengYu_Graph/frontend
   ```
2. 执行启动命令：
   ```powershell
   npm run dev
   ```

**预期结果：**
- 控制台输出类似信息：
  ```
  VITE v7.3.0  ready in 870 ms
  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
  ```
- 前端服务将在 `http://localhost:5173` 上运行

### 3. 访问系统
1. 打开浏览器，访问 `http://localhost:5173`
2. 您将看到"成渝地区双城经济圈产业知识图谱"系统的主界面
3. 通过导航栏可以切换"产业关系图谱"和"数据分析"视图

### 注意事项
1. **端口占用问题**：
   - 如果5000端口被占用，可以修改 `app.py` 中的端口配置
   - 如果5173端口被占用，可以在前端目录执行 `npm run dev -- --port 新端口号`

2. **依赖问题**：
   - 首次运行或环境变化时，可能需要重新安装依赖：
     ```powershell
     # 后端依赖
     pip install flask flask_sqlalchemy flask_cors scikit-learn networkx numpy
     
     # 前端依赖
     cd frontend
     npm install
     ```

3. **数据库问题**：
   - 系统使用SQLite数据库，无需额外安装数据库服务
   - 数据库文件为 `chengyu_industry.db`，删除后重启服务会重新创建表结构和初始数据

### 停止服务
- 前端服务：在前端终端按 `Ctrl+C` 停止
- 后端服务：在后端终端按 `Ctrl+C` 停止

通过以上步骤，您可以轻松启动和运行整个产业知识图谱系统。如果在运行过程中遇到问题，可以查看终端输出的错误信息进行排查，或联系技术支持。
        