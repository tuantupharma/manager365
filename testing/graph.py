import os
import requests
from flask import Flask, redirect, request
import random
import string

app = Flask(__name__)

from dotenv import load_dotenv
load_dotenv()  # Tự động load biến môi trường từ file .env


client_id = os.getenv("CLIENT_ID365")
client_secret = os.getenv("CLIENT_SECRET365")
tenant_id = os.getenv("TENANT_ID")

redirect_uri = "http://localhost:8000/callback"

authorize_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/authorize"
token_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"

scopes = [
    "https://graph.microsoft.com/Mail.Send",
    "https://graph.microsoft.com/User.Read",
    "https://graph.microsoft.com/Files.ReadWrite",
    "https://graph.microsoft.com/Calendars.ReadWrite",
    "https://graph.microsoft.com/Group.ReadWrite.All",
    "https://graph.microsoft.com/ChannelMessage.Send"
]

@app.route("/")
def home():
    return redirect(
        f"{authorize_url}?client_id={client_id}&response_type=code"
        f"&redirect_uri={redirect_uri}&response_mode=query&scope={' '.join(scopes)}"
    )

@app.route("/callback")
def callback():
    code = request.args.get("code")
    token_data = {
        "client_id": client_id,
        "scope": " ".join(scopes),
        "code": code,
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code",
        "client_secret": client_secret
    }
    token_res = requests.post(token_url, data=token_data)
    token_json = token_res.json()
    access_token = token_json.get("access_token")

    # In access_token để bạn copy dùng Postman
    print("🔑 access_token:", access_token)

    if not access_token:
        return "❌ Không lấy được access_token: " + token_res.text

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }



   
    # Tạo calendar event
    calendar_payload = {
        "subject": "Ping Calendar",
        "start": {"dateTime": "2025-09-12T08:00:00", "timeZone": "UTC"},
        "end": {"dateTime": "2025-09-12T09:00:00", "timeZone": "UTC"}
    }
    calendar_resp = requests.post("https://graph.microsoft.com/v1.0/me/events", headers=headers, json=calendar_payload)

    # Gửi bài Teams (nếu có)
    team_id = os.getenv("TEAM_ID")      # ← điền ID nhóm nếu có
    channel_id = os.getenv("CHANNEL_ID")  # ← điền ID kênh nếu có
    teams_status = "⛔ Bỏ qua vì chưa có team_id"


    if team_id and channel_id:
        channels_url = f"https://graph.microsoft.com/v1.0/teams/{team_id}/channels"
        channels_resp = requests.get(channels_url, headers=headers)
        print("📋 Danh sách kênh:", channels_resp.json())

        msg_payload = {
            "body": {
                "content": "Ping bài đăng xác thực tài khoản trong Microsoft Teams"
            }
        }
        teams_url = f"https://graph.microsoft.com/v1.0/teams/{team_id}/channels/{channel_id}/messages"
        teams_res = requests.post(teams_url, headers=headers, json=msg_payload)
        print("📢 Teams response:", teams_res.status_code, teams_res.text)
        teams_status = f"{teams_res.status_code}"

    #uploads_str = "<br>".join([f"{f}: {s}" for f, s in uploads]) if uploads else "❌ Không có ảnh"

    return f"""
    ✅ Token OK<br>
    📅 Lịch: {calendar_resp.status_code}<br>
    📢 Bài đăng Teams: {teams_status}<br>
    🔑 Token đã in ra terminal để dùng Postman
    """

if __name__ == "__main__":
    print("⚡ Mở trình duyệt login tài khoản Microsoft 365...")
    app.run(host="0.0.0.0", port=8000)
