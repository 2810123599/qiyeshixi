const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = 3000;
const publicDir = path.join(__dirname, 'public');
const modules = [
  { name: '目标拆解', task: goal => `梳理“${goal}”的基础概念，列出需要掌握的关键词`, type: '理解' },
  { name: '资料整理', task: goal => `收集 ${goal} 的入门资料，完成一份知识地图`, type: '整理' },
  { name: '动手练习', task: goal => `围绕 ${goal} 完成一个最小练习项目`, type: '实践' },
  { name: '复盘输出', task: goal => `用自己的话总结 ${goal}，并记录三个待解决问题`, type: '复盘' },
  { name: '成果展示', task: goal => `完善 ${goal} 的练习成果，准备一次五分钟分享`, type: '展示' }
];

function clean(value, fallback, max = 80) {
  const text = String(value || '').replace(/[<>]/g, '').trim().slice(0, max);
  return text || fallback;
}

function makePlan(input) {
  const goal = clean(input.goal, 'JavaScript 基础');
  const level = clean(input.level, '零基础', 20);
  const days = Math.max(3, Math.min(30, Number.parseInt(input.days, 10) || 7));
  const minutes = Math.max(15, Math.min(480, Number.parseInt(input.minutes, 10) || 60));
  const plan = Array.from({ length: days }, (_, index) => {
    const item = modules[index % modules.length];
    const review = index > 0 ? '最后用 10 分钟复习昨天的笔记。' : '先建立学习记录，写下今天的疑问。';
    return { day: index + 1, title: item.name, type: item.type, task: item.task(goal), duration: minutes, review };
  });
  return { goal, level, days, minutes, plan, tip: `以${level}身份学习时，保持每天完成一个小成果，比一次安排过多内容更有效。` };
}

function sendJson(res, status, data) {
  const body = JSON.stringify(data);
  res.writeHead(status, { 'Content-Type': 'application/json; charset=utf-8', 'Content-Length': Buffer.byteLength(body) });
  res.end(body);
}

function handleApi(req, res) {
  let body = '';
  req.on('data', chunk => { body += chunk; if (body.length > 10000) req.destroy(); });
  req.on('end', () => {
    try { sendJson(res, 200, makePlan(JSON.parse(body || '{}'))); }
    catch { sendJson(res, 400, { error: '请求内容不是有效 JSON' }); }
  });
}

const server = http.createServer((req, res) => {
  if (req.method === 'POST' && req.url === '/api/plan') return handleApi(req, res);
  if (req.method !== 'GET' || req.url !== '/') { res.writeHead(404); return res.end('Not found'); }
  const file = fs.readFileSync(path.join(publicDir, 'index.html'));
  res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8', 'Content-Length': file.length });
  res.end(file);
});

server.listen(PORT, '127.0.0.1', () => console.log(`学习计划生成器运行中：http://127.0.0.1:${PORT}`));

