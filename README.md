# 两个课程小项目

本仓库包含两个可以直接运行的全栈小项目，均不依赖第三方包，适合课堂演示和继续扩展。

## 项目一：Python AI 小说生成器

目录：`python_novel_generator`

使用 Python 标准库启动一个本地网页服务。用户输入主题、类型和主角，程序根据模板生成一篇短篇小说，并提供 JSON 接口。

```powershell
cd python_novel_generator
python app.py
```

浏览器打开 <http://127.0.0.1:8000>。

## 项目二：Node.js 学习计划生成器

目录：`node_study_planner`

使用 Node.js 内置 `http` 模块，根据学习目标、每天可用时间和周期拆解学习任务，生成按天排列的计划，并提供 JSON 接口。

```powershell
cd node_study_planner
node server.js
```

浏览器打开 <http://127.0.0.1:3000>。

## 适合课程展示的扩展方向

- 将本地模板替换为真实的大模型 API，并把 API Key 放在环境变量中。
- 给生成结果增加 SQLite 保存、历史记录和导出 Markdown 功能。
- 增加用户登录、任务完成状态和移动端布局。

