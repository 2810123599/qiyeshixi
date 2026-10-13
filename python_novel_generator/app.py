from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import json
import re
from urllib.parse import urlparse

ROOT = Path(__file__).parent
HTML_PATH = ROOT / "templates" / "index.html"


def clean(value, fallback, limit=80):
    text = str(value or "").strip()
    text = re.sub(r"[<>]", "", text)
    return (text[:limit] or fallback)


def generate_story(payload):
    topic = clean(payload.get("topic"), "一座会发光的旧城市")
    genre = clean(payload.get("genre"), "科幻")
    hero = clean(payload.get("protagonist"), "林墨")
    try:
        length = max(3, min(8, int(payload.get("length", 5))))
    except (TypeError, ValueError):
        length = 5

    scenes = [
        f"清晨，{hero}在窗边发现了一枚与{topic}有关的旧徽章。{genre}世界里沉睡多年的传闻，忽然有了真实的重量。",
        f"{hero}沿着地图上不存在的小路出发。路旁的风像是在低声提醒：真正的答案，总要先经过一次选择。",
        f"当{hero}抵达{topic}的入口，守门人提出了一个问题：如果知道终点会失去最珍贵的东西，还要不要继续？",
        f"{hero}没有立即回答，而是把徽章放进门上的凹槽。{topic}亮起温柔的光，尘封的记忆像潮水一样涌来。",
        f"危机在夜色中降临。{hero}用一路上遇见的人教会自己的勇气，找到了破解谜团的关键。",
        f"最后，{hero}明白{topic}并不是一件物品，而是每个人愿意守护的愿望。城市重新亮起，新的故事从此开始。",
        f"多年以后，人们仍会讲起这段旅程。每当有人问起结局，{hero}总是微笑着说：结局只是下一章的开头。",
        f"风穿过街道，带走了旧日的尘埃，也把{hero}的名字写进了{topic}的新历史。",
    ]
    selected = scenes[:length]
    title = f"《{topic}：{hero}的{genre}旅程》"
    return {"title": title, "genre": genre, "paragraphs": selected, "wordCount": sum(len(p) for p in selected)}


class Handler(BaseHTTPRequestHandler):
    def send_json(self, status, data):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if urlparse(self.path).path != "/":
            self.send_json(404, {"error": "页面不存在"})
            return
        body = HTML_PATH.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        if urlparse(self.path).path != "/api/generate":
            self.send_json(404, {"error": "接口不存在"})
            return
        try:
            size = int(self.headers.get("Content-Length", "0"))
            payload = json.loads(self.rfile.read(size) or b"{}")
            self.send_json(200, generate_story(payload))
        except (ValueError, json.JSONDecodeError):
            self.send_json(400, {"error": "请求内容不是有效 JSON"})

    def log_message(self, *_):
        return


if __name__ == "__main__":
    server = ThreadingHTTPServer(("127.0.0.1", 8000), Handler)
    print("AI 小说生成器运行中：http://127.0.0.1:8000")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n服务已停止")
        server.server_close()

