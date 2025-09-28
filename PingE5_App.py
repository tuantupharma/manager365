import requests
import os
import json
import time
import random
from pathlib import Path

from dotenv import load_dotenv
load_dotenv()  # Tự động load biến môi trường từ file .env


client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
tenant_id = os.getenv("TENANT_ID")
user_email = os.getenv("USER_EMAIL")

# Step 1 - Get token
token_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
scopes = ["https://graph.microsoft.com/.default"]
data = {
    "client_id": client_id,
    "scope": " ".join(scopes),
    "client_secret": client_secret,
    "grant_type": "client_credentials"
}
print("🔐 Đang lấy access_token...")
resp = requests.post(token_url, data=data)
token = resp.json().get("access_token")
if not token:
    print("❌ Lỗi lấy token:", resp.text)
    exit()

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

def safe_get(url, label):
    try:
        res = requests.get(url, headers=headers)
        print(f"{label} → Status:", res.status_code)
        return res
    except Exception as e:
        print(f"{label} → Lỗi:", e)

# Step 2 - Gửi mail tới nhiều người
recipients = os.getenv("EMAIL_RECIPIENTS").split(",")

mail_payload = {
  "message": {
    "subject": "Testing Mail khen thưởng nội bộ và ngoài hệ thống",
    "body": {
      "contentType": "Text",
      "content": (
        "Chào buổi sáng cả nhà,\n\n"
        "Hy vọng mọi người có một khởi đầu ngày mới thật nhiều năng lượng!\n\n"
        "Tôi muốn dành vài phút để gửi lời khen thưởng đặc biệt đến toàn thể đội ngũ về những nỗ lực và thành quả xuất sắc trong tháng vừa qua."
        " Nhờ sự cống hiến không ngừng nghỉ và tinh thần làm việc nhóm tuyệt vời của các bạn, chúng ta đã đạt được những mục tiêu ấn tượng và vượt qua nhiều thử thách.\n\n"
        "Thật sự tự hào khi được làm việc cùng một tập thể tài năng và nhiệt huyết như các bạn. Hãy cùng nhau giữ vững phong độ này và tiếp tục gặt hái thêm nhiều thành công hơn nữa trong thời gian tới nhé!\n\n"
        "Chúc các bạn một ngày làm việc hiệu quả và tràn đầy niềm vui!\n\n"
        "Trân trọng,"
      )
    },
    "toRecipients": [{"emailAddress": {"address": email}} for email in recipients]
  }
}

print("📬 Gửi mail nội bộ và ngoài hệ thống ...")
res = requests.post(
    f"https://graph.microsoft.com/v1.0/users/{user_email}/sendMail",
    headers=headers,
    json=mail_payload
)
print("📤 Trạng thái gửi mail:", res.status_code)

# Step 3 - Ping Graph API nhiều dịch vụ
safe_get(f"https://graph.microsoft.com/v1.0/users/{user_email}", "👤 User info")
safe_get(f"https://graph.microsoft.com/v1.0/users/{user_email}/drive", "📁 OneDrive")
safe_get(f"https://graph.microsoft.com/v1.0/users/{user_email}/mailFolders", "📨 MailFolders")
safe_get(f"https://graph.microsoft.com/v1.0/users/{user_email}/mailFolders/inbox/messages?$top=1", "📥 Inbox latest")
safe_get(f"https://graph.microsoft.com/v1.0/users/{user_email}/joinedTeams", "💬 Teams")
safe_get(f"https://graph.microsoft.com/v1.0/users/{user_email}/calendars", "📅 Calendar list")
safe_get(f"https://graph.microsoft.com/v1.0/sites/root/lists", "list")
safe_get(f"https://graph.microsoft.com/v1.0/sites/root", "root list")
safe_get(f"https://graph.microsoft.com/v1.0/sites/root/drives", "dive list")
safe_get(f"https://graph.microsoft.com/beta/me/outlook/masterCategories", "outlook")

# Step 4 - Xoá nội dung thư mục OneDrive và tạo file giả trực tiếp trên cloud

remote = os.getenv("RCLONE_REMOTE")
folder = os.getenv("RCLONE_FOLDER")
rclone = os.getenv("RCLONE_PATH")
print(f"🧹 Xoá toàn bộ nội dung trong thư mục {folder} (giữ nguyên thư mục)...")
os.system(f"{rclone} delete {remote}:/{folder}")


print("📄 Tạo ngẫu nhiên 3-4 file giả trực tiếp trên OneDrive...")
for i in range(random.randint(3, 4)):
    filename = f"note_{random.randint(1000, 9999)}.txt"
    content = f"Đây là file giả số {i+1} để kiểm tra hệ thống giữ OneDrive hoạt động."
    upload_url = f"https://graph.microsoft.com/v1.0/users/{user_email}/drive/root:/Anh_code77/{filename}:/content"
    res = requests.put(upload_url, headers=headers, data=content.encode("utf-8"))
    print(f"📎 Upload {filename} → Status:", res.status_code)

# Step 5 - Upload ảnh từ thư mục local
print("🖼️ Upload ảnh từ local thư mục D:\\xxxxx lên thumuccuaban...")
#os.system(r'rclone copy "Thu muc may ban" rclonecuaban:thucmuctrenonedriver --transfers=4 --checkers=8 --fast-list')
thumuc_anh = os.getenv("LOCAL_UPLOAD-FOLDER")
isgitaction = os.environ.get('REMOTE_GIT',1)
print(f"dang hoạt động ở chế độ : {isgitaction} " )
if not isgitaction:
    if not thumuc_anh:
        raise ValueError("thumuc_anh environment variable is missing or empty")
    if not rclone:
        raise ValueError("RCLONE_REMOTE environment variable is missing or empty")
    os.system(f"{rclone} copy {thumuc_anh} {remote}:/{folder} --transfers=4 --checkers=8 --fast-list")
#os.system(r'I:\rclone-v1.65.1-windows-amd64\autosave.bat') 

#more function
print("📏 Lấy dung lượng thư mục cụ thể...")
def get_folder_size(folder_path):
    url = f"https://graph.microsoft.com/v1.0/users/{user_email}/drive/root:/{folder_path}"
    res = safe_get(url, f"📦 Folder size for '{folder_path}'")
    if res.status_code == 200:
        data = res.json()
        size_bytes = data.get("size", 0)
        print(f"📏 Folder '{folder_path}' size: {size_bytes / (1024 * 1024):.2f} MB")
    else:
        print("❌ Failed to get folder size:", res.text)



def list_folders_in_onedrive():
    url = f"https://graph.microsoft.com/v1.0/users/{user_email}/drive/root/children"
    res = safe_get(url, "📁 Listing folders in OneDrive")
    if res.status_code == 200:
        items = res.json().get("value", [])
        folders = [item for item in items if "folder" in item]
        print(f"📦 Found {len(folders)} folders:")
        for folder in folders:
            print(f" - {folder['name']}")
    else:
        print("❌ Failed to list folders:", res.text)

import csv

def export_folders_size_to_csv():
    url = f"https://graph.microsoft.com/v1.0/users/{user_email}/drive/root/children"
    res = safe_get(url, "📁 Lấy danh sách thư mục OneDrive")
    if res.status_code == 200:
        items = res.json().get("value", [])
        folders = [item for item in items if "folder" in item]
        folder_data = []
        for folder in folders:
            folder_name = folder['name']
            # Lấy thông tin chi tiết từng thư mục để lấy size
            folder_url = f"https://graph.microsoft.com/v1.0/users/{user_email}/drive/root:/{folder_name}"
            folder_res = safe_get(folder_url, f"📦 Lấy size cho '{folder_name}'")
            if folder_res.status_code == 200:
                size_bytes = folder_res.json().get("size", 0)
                size_mb = round(size_bytes / (1024 * 1024), 2)
                folder_data.append({"name": folder_name, "size_mb": size_mb})
            else:
                folder_data.append({"name": folder_name, "size_mb": "Lỗi"})
        # Xuất ra file CSV
        with open("folder_list.csv", "w", newline='', encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=["name", "size_mb"])
            writer.writeheader()
            for row in folder_data:
                writer.writerow(row)
        print("✅ Đã xuất danh sách thư mục và dung lượng ra file folder_list.csv")
    else:
        print("❌ Không lấy được danh sách thư mục:", res.text)

#export_folders_size_to_csv()

import csv

def export_subfolders_size_in_folder(parent_folder):
    # Lấy danh sách các item trong thư mục chỉ định
    url = f"https://graph.microsoft.com/v1.0/users/{user_email}/drive/root:/{parent_folder}:/children"
    res = safe_get(url, f"📁 Lấy danh sách thư mục con trong '{parent_folder}'")
    if res.status_code == 200:
        items = res.json().get("value", [])
        folders = [item for item in items if "folder" in item]
        folder_data = []
        for folder in folders:
            folder_name = folder['name']
            # Lấy thông tin chi tiết từng thư mục con để lấy size
            folder_url = f"https://graph.microsoft.com/v1.0/users/{user_email}/drive/root:/{parent_folder}/{folder_name}"
            folder_res = safe_get(folder_url, f"📦 Lấy size cho '{folder_name}'")
            if folder_res.status_code == 200:
                size_bytes = folder_res.json().get("size", 0)
                size_mb = round(size_bytes / (1024 * 1024), 2)
                folder_data.append({"name": folder_name, "size_mb": size_mb})
            else:
                folder_data.append({"name": folder_name, "size_mb": "Lỗi"})
        # Xuất ra file CSV
        with open("folder_list.csv", "w", newline='', encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=["name", "size_mb"])
            writer.writeheader()
            for row in folder_data:
                writer.writerow(row)
        print(f"✅ Đã xuất danh sách thư mục con và dung lượng ra file folder_list.csv cho thư mục '{parent_folder}'")
    else:
        print("❌ Không lấy được danh sách thư mục con:", res.text)

# Ví dụ sử dụng:
export_subfolders_size_in_folder(folder)  # hoặc bất kỳ tên thư mục nào trong root
