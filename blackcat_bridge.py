from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os
import subprocess

CONFIG_FILE = os.path.expanduser("~/.blackcat_control_config.json")

DEFAULT_CONFIG = {
    "sms_bot_active": True,
    "mail_bot_active": True,
    "notify_every_reply": True,
    "notifications_enabled": True,
    "custom_rules": []
}

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return DEFAULT_CONFIG.copy()

def save_config(cfg):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=4, ensure_ascii=False)

def apply_system_changes(cfg):
    # Zarządzanie procesem SMS bota
    if cfg["sms_bot_active"]:
        out = subprocess.getoutput("pgrep -f autobot_v13.py")
        if not out.strip():
            subprocess.Popen(["nohup", "python", "autobot_v13.py"], stdout=open("bot_sms_v13.log", "a"), stderr=subprocess.STDOUT)
    else:
        subprocess.run(["pkill", "-f", "autobot_v13.py"])

    # Zarządzanie procesem Mail bota
    if cfg["mail_bot_active"]:
        out = subprocess.getoutput("pgrep -f blackcat_hunter_v12.py")
        if not out.strip():
            subprocess.Popen(["nohup", "python", "blackcat_hunter_v12.py"], stdout=open("bot_mail_v12.log", "a"), stderr=subprocess.STDOUT)
    else:
        subprocess.run(["pkill", "-f", "blackcat_hunter_v12.py"])

class BridgeHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/status":
            cfg = load_config()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(cfg).encode("utf-8"))

    def do_POST(self):
        if self.path == "/update":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            incoming = json.loads(post_data.decode("utf-8"))
            
            cfg = load_config()
            cfg["sms_bot_active"] = incoming.get("sms_bot_active", cfg["sms_bot_active"])
            cfg["mail_bot_active"] = incoming.get("mail_bot_active", cfg["mail_bot_active"])
            cfg["notify_every_reply"] = incoming.get("notify_every_reply", cfg["notify_every_reply"])
            cfg["notifications_enabled"] = incoming.get("notifications_enabled", cfg["notifications_enabled"])
            
            cmd = incoming.get("custom_command", "")
            if cmd:
                cfg["custom_rules"].append(cmd)
                if cmd == "restart_all":
                    subprocess.run(["pkill", "-f", "autobot_v13.py"])
                    subprocess.run(["pkill", "-f", "blackcat_hunter_v12.py"])

            save_config(cfg)
            apply_system_changes(cfg)

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ok"}).encode("utf-8"))

if __name__ == "__main__":
    print("[BLACK CAT BRIDGE] Nasłuch na porcie 8765 dla aplikacji APK...")
    server = HTTPServer(("127.0.0.1", 8765), BridgeHandler)
    server.serve_forever()
