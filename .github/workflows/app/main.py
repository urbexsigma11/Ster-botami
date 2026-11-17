from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.switch import Switch
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
import json
import urllib.request

API_URL = "http://127.0.0.1:8765"

class BlackCatControlUI(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=20, spacing=15, **kwargs)

        self.add_widget(Label(text="[b]BLACK CAT - PANEL STEROWANIA[/b]", markup=True, font_size='22sp', size_hint_y=None, height=50))
        self.status_label = Label(text="Status: Oczekiwanie na połączenie z Termux...", color=(1, 0.8, 0, 1), size_hint_y=None, height=30)
        self.add_widget(self.status_label)

        row_sms = BoxLayout(size_hint_y=None, height=50)
        row_sms.add_widget(Label(text="Bot SMS (v13) Aktywny:"))
        self.sw_sms = Switch(active=True)
        self.sw_sms.bind(active=self.on_toggle)
        row_sms.add_widget(self.sw_sms)
        self.add_widget(row_sms)

        row_mail = BoxLayout(size_hint_y=None, height=50)
        row_mail.add_widget(Label(text="Bot Mailowy (v12) Aktywny:"))
        self.sw_mail = Switch(active=True)
        self.sw_mail.bind(active=self.on_toggle)
        row_mail.add_widget(self.sw_mail)
        self.add_widget(row_mail)

        row_reply_info = BoxLayout(size_hint_y=None, height=50)
        row_reply_info.add_widget(Label(text="Info o każdym odpisaniu:"))
        self.sw_reply_info = Switch(active=True)
        self.sw_reply_info.bind(active=self.on_toggle)
        row_reply_info.add_widget(self.sw_reply_info)
        self.add_widget(row_reply_info)

        row_notif = BoxLayout(size_hint_y=None, height=50)
        row_notif.add_widget(Label(text="Powiadomienia systemowe:"))
        self.sw_notif = Switch(active=True)
        self.sw_notif.bind(active=self.on_toggle)
        row_notif.add_widget(self.sw_notif)
        self.add_widget(row_notif)

        self.add_widget(Label(text="Szybka komenda / Nowa funkcja:", size_hint_y=None, height=30))
        self.cmd_input = TextInput(hint_text="np. restart_all", multiline=False, size_hint_y=None, height=45)
        self.add_widget(self.cmd_input)

        btn_send = Button(text="WYŚLIJ KONFIGURACJĘ", size_hint_y=None, height=55, background_color=(0.18, 0.42, 0.31, 1))
        btn_send.bind(on_press=self.send_config)
        self.add_widget(btn_send)

        self.sync_state()

    def get_payload(self):
        return {
            "sms_bot_active": self.sw_sms.active,
            "mail_bot_active": self.sw_mail.active,
            "notify_every_reply": self.sw_reply_info.active,
            "notifications_enabled": self.sw_notif.active,
            "custom_command": self.cmd_input.text.strip()
        }

    def on_toggle(self, instance, value):
        self.send_config(None)

    def send_config(self, instance):
        payload = self.get_payload()
        try:
            req = urllib.request.Request(
                f"{API_URL}/update",
                data=json.dumps(payload).encode('utf-8'),
                headers={'Content-Type': 'application/json'}
            )
            with urllib.request.urlopen(req, timeout=2) as resp:
                self.status_label.text = "Status: Zsynchronizowano z Termuxem ✓"
                self.status_label.color = (0.3, 1, 0.5, 1)
                self.cmd_input.text = ""
        except Exception:
            self.status_label.text = "Status: Brak połączenia z Termux (port 8765)"
            self.status_label.color = (1, 0.3, 0.3, 1)

    def sync_state(self):
        try:
            with urllib.request.urlopen(f"{API_URL}/status", timeout=2) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                self.sw_sms.active = data.get("sms_bot_active", True)
                self.sw_mail.active = data.get("mail_bot_active", True)
                self.sw_reply_info.active = data.get("notify_every_reply", True)
                self.sw_notif.active = data.get("notifications_enabled", True)
                self.status_label.text = "Status: Połączono z Black Cat Core ✓"
                self.status_label.color = (0.3, 1, 0.5, 1)
        except Exception:
            pass

class BlackCatApp(App):
    def build(self):
        self.title = "Black Cat Control"
        return BlackCatControlUI()

if __name__ == '__main__':
    BlackCatApp().run()
