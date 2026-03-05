# Manager365

**Manager365** là một công cụ quản lý tự động hóa dành cho môi trường Windows 365. Ứng dụng viết chủ yếu bằng Python (99.7%) và một số script batch, với mục tiêu giúp tối ưu hoá quy trình làm việc, sao lưu và giám sát.

## ✅ Tính năng chính

- Tự động sao lưu và nén thư mục theo cấu hình
- Kiểm tra quy trình xử lý, dịch vụ hoặc ứng dụng chạy
- Kết nối và tương tác với Microsoft 365 qua Graph API (ví dụ: gửi thông báo, tạo lịch)
- Có thể mở rộng bằng các script Python hoặc batch tùy chỉnh

## 🛠️ Công nghệ và thành phần

- **Python 3.x** làm ngôn ngữ chính
- **Batchfile** để tích hợp với hệ điều hành Windows
- **Flask** cho phần demo `testing/graph.py` (Graph API OAuth)
- **dotenv** dùng để tải biến môi trường từ `.env`

## 🚀 Bắt đầu nhanh

1. **Sao chép repository**
    ```bash
    git clone https://github.com/tuantupharma/manager365.git
    cd manager365
    ```
2. **Thiết lập môi trường Python**
    ```bash
    python -m venv venv
    venv\Scripts\activate  # trên PowerShell
    pip install -r requirements.txt
    ```
3. **Cấu hình**
    - chỉnh `config.json` để chỉ định `folder_path` cần sao lưu.
    - thêm biến môi trường nếu cần (ví dụ khi dùng `testing/graph.py`).

4. **Chạy chương trình chính**
    ```bash
    python PingE5_App.py  # hoặc file entry point bạn muốn
    ```

> ❗ Tùy theo mục đích, có thể dùng các batchfile `run.bat`, `runcompress.bat`, `rungui.bat`.

## 📁 File cấu hình

- `config.json` – chứa đường dẫn thư mục sao lưu
- `.env` (tùy chọn) – chứa biến môi trường cho API/Microsoft 365

## 🤝 Đóng góp

Mọi đóng góp đều rất được hoan nghênh. Mở issue hoặc pull request để thêm tính năng, sửa lỗi hoặc nâng cao tài liệu.

## 📜 Giấy phép

Dự án được phát hành dưới giấy phép **MIT**. Xem [LICENSE](LICENSE) để biết chi tiết.

---

*Made with ❤️ by [tuantupharma](https://github.com/tuantupharma)*

