import json
import re
from http.server import BaseHTTPRequestHandler, HTTPServer


TICKETS = {
    "T1001": {
        "ticket_id": "T1001",
        "owner_id": "U001",
        "title": "无法登录",
    }
}


class TicketHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        ticket_id = self.path.removeprefix("/tickets/")

        if not self.path.startswith("/tickets/") :
            self.send_json(404, {"error": "工单不存在"})
            return
        if not re.fullmatch(r"T\d{4}", ticket_id):
            self.send_json(400, {"error": "工单编号格式错误"})
            return

        if ticket_id not in TICKETS:
            self.send_json(404, {"error": "工单不存在"})
            return
        ticket = TICKETS[ticket_id]
        user_id = self.headers.get("X-User-Id")

        if user_id != ticket["owner_id"] and user_id != "admin":
            self.send_json(403, {"error": "无权访问"})
            return

        self.send_json(200, ticket)

    def send_json(self, status, body):
        data = json.dumps(body, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)


HTTPServer(("127.0.0.1", 8001), TicketHandler).serve_forever()