# 学习计划生成器

一个可在本地 Node.js 服务和 GitHub Pages 静态托管上运行的学习计划生成器。

## 本地运行

```powershell
node server.js
```

打开 http://127.0.0.1:3000 。本地服务提供 `/api/plan`，浏览器无法访问 API 时会自动切换到前端生成逻辑，因此静态部署仍然可用。

## GitHub Pages 部署

1. 将本目录中的 `index.html`、`package.json`、`server.js` 和 `public/` 推送到 GitHub 仓库。
2. 在仓库进入 **Settings → Pages**。
3. 在 **Build and deployment** 中选择 **Deploy from a branch**。
4. 选择 `main` 分支和 `/ (root)` 目录并保存。
5. 等待部署完成，打开 GitHub Pages 显示的域名。

GitHub Pages 使用根目录的 `index.html`；`server.js` 用于本地演示，不需要在 Pages 上运行。
