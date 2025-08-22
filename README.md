# Plagiarism Checker Pro
## Giới thiệu
Plagiarism Checker Pro là một công cụ kiểm tra đạo văn tiên tiến được phát triển bởi **LE VAN HUNG**. Ứng dụng sử dụng Google Custom Search API để phát hiện nội dung có thể đã được sao chép từ các nguồn trực tuyến.

![UI Screenshot](Bản%20GUI%20đẹp/UI1.png)
![UI Screenshot](Bản%20GUI%20đẹp/UI2.png)
![UI Screenshot](Bản%20GUI%20đẹp/UI3.png)
![UI Screenshot](Bản%20GUI%20đẹp/UI4.png)

## Tính năng chính
- **Phát hiện đạo văn thông minh**: Sử dụng nhiều thuật toán để tính toán độ tương tự
- **Giao diện hiện đại**: GUI được thiết kế chuyên nghiệp với Tkinter
- **Phân tích chi tiết**: Báo cáo đầy đủ với mức độ rủi ro và đề xuất cải thiện
- **Xuất báo cáo**: Hỗ trợ xuất kết quả ra file text
- **Theo dõi tiến trình**: Hiển thị tiến trình phân tích theo thời gian thực
## Yêu cầu hệ thống
- Python 3.7 trở lên
- Kết nối Internet
- Google Custom Search API key
- Windows/Linux/macOS
## Cài đặt
1. Chạy file `install.bat`
2. Script sẽ tự động kiểm tra Python và cài đặt các thư viện cần thiết
3. **Hoặc là Cài đặt thư viện qua terminal**:
   ```bash
   pip install -r requirements.txt
   ```
## Cấu hình API
1. Mở file `config.py`
2. Cập nhật thông tin API:
   ```python
   API_KEY = "your_google_api_key_here"
   SEARCH_ENGINE_ID = "your_search_engine_id_here"
   ```
# 🔑 HƯỚNG DẪN CHI TIẾT LẤY GOOGLE CUSTOM SEARCH API
## 📋 MỤC TIÊU
Sau khi hoàn thành hướng dẫn này, bạn sẽ có được:
- **API Key**: `AIzaSyB...` (dạng 39 ký tự)
- **Search Engine ID**: `017576662...` (dạng 21 ký tự)
- **Base URL**: `https://www.googleapis.com/customsearch/v1`
## 🚀 PHẦN 1: TẠO GOOGLE CLOUD PROJECT VÀ API KEY
### Bước 1: Chuẩn bị
- **Cần có**: Gmail account
- **Thời gian**: 10-15 phút
- **Chi phí**: Miễn phí (100 searches/ngày)
### Bước 2: Truy cập Google Cloud Console
1. Mở trình duyệt web
2. Vào địa chỉ: **https://console.cloud.google.com/**
3. Đăng nhập bằng Gmail của bạn
4. Nếu lần đầu sử dụng, chấp nhận "Terms of Service"
### Bước 3: Tạo Project mới
1. **Tìm dropdown "Select a project"** (góc trên bên trái, bên cạnh logo Google Cloud)
2. **Click "NEW PROJECT"**
3. **Điền thông tin:**
   - Project name: `Plagiarism Checker` (hoặc tên bất kỳ)
   - Location: Để mặc định "No organization"
4. **Click "CREATE"**
5. **Đợi 10-30 giây** cho project được tạo
6. **Click "SELECT PROJECT"** khi xuất hiện thông báo hoàn thành
### Bước 4: Enable Custom Search API
1. **Mở menu hamburger** ☰ (góc trên bên trái)
2. **Chọn "APIs & Services"** → **"Library"**
3. **Tìm kiếm "Custom Search API"** trong ô search
4. **Click vào "Custom Search API"** trong kết quả
5. **Click nút "ENABLE"** màu xanh
6. **Đợi vài giây** để API được kích hoạt
### Bước 5: Tạo API Key
1. **Vào "APIs & Services"** → **"Credentials"**
2. **Click "CREATE CREDENTIALS"** (nút xanh)
3. **Chọn "API key"** từ dropdown menu
4. **Popup hiện ra với API key** (dạng: AIzaSyB...)
5. **🔴 QUAN TRỌNG: Copy và lưu API key này!**
6. **Ghi lại**: `API_KEY = "AIzaSyB..."`
### Bước 6: Bảo mật API Key (Khuyến nghị)
1. **Click "RESTRICT KEY"** trong popup
2. **Application restrictions:**
   - Chọn "HTTP referrers (web sites)"
   - Website restrictions: nhập `*` (cho phép tất cả trang web)
3. **API restrictions:**
   - Chọn "Restrict key"
   - Select APIs: tick vào "Custom Search API"
4. **Click "SAVE"**
## 🔍 PHẦN 2: TẠO CUSTOM SEARCH ENGINE
### Bước 7: Truy cập Google Custom Search
1. **Mở tab mới** trong trình duyệt
2. **Vào địa chỉ: https://cse.google.com/**
3. **Đăng nhập** cùng Gmail account (nếu chưa đăng nhập)
### Bước 8: Tạo Search Engine mới
1. **Click "Add"** hoặc **"Get Started"**
2. **Nếu đã có search engine cũ**, click **"New search engine"**
### Bước 9: Cấu hình Search Engine
**Điền thông tin như sau:**
```
Sites to search: *.com
Language: English  
Search engine name: Plagiarism Checker
```
**Chi tiết từng trường:**
- **Sites to search**: Nhập chính xác `*.com` (để tìm kiếm toàn web)
- **Language**: Chọn "English" từ dropdown
- **Search engine name**: Nhập "Plagiarism Checker" (hoặc tên bạn muốn)
### Bước 10: Hoàn tất tạo Search Engine
1. **Click "CREATE"**
2. **Đợi vài giây** xử lý
3. **Click "Control Panel"** khi xuất hiện
### Bước 11: Lấy Search Engine ID
1. **Trong Control Panel**, tìm mục **"Search engine ID"**
2. **Copy ID này** (dạng: 017576662f6bb34f28)
3. **🔴 QUAN TRỌNG: Lưu Search Engine ID!**
4. **Ghi lại**: `SEARCH_ENGINE_ID = "017576662..."`
### Bước 12: Cấu hình nâng cao (Tùy chọn)
1. **Trong Setup tab:**
   - **Search the entire web**: Bật ON
   - **Image search**: Bật ON
   - **Safe Search**: Chọn "Medium"
2. **Click "Update"** nếu có thay đổi
## ✅ PHẦN 3: KIỂM TRA VÀ TEST
### Bước 13: Test API bằng URL
1. **Thay thế** YOUR_API_KEY và YOUR_CX trong URL sau:
```
https://www.googleapis.com/customsearch/v1?key=YOUR_API_KEY&cx=YOUR_CX&q=python
```
2. **Ví dụ URL hoàn chỉnh:**
```
https://www.googleapis.com/customsearch/v1?key=AIzaSyDSdgDhkqGcRJNDGl5nFVyhYYrTa_HLzW0&cx=55d79829f6bb34f28&q=python
```
3. **Paste URL vào trình duyệt** và Enter
### Bước 14: Kiểm tra kết quả
**✅ Thành công nếu thấy:**
```json
{
  "kind": "customsearch#search",
  "items": [
    {
      "title": "Python.org",
      "link": "https://www.python.org/",
      ...
    }
  ]
}
```
**❌ Lỗi thường gặp:**
- **403 Forbidden**: API key không đúng hoặc chưa enable API
- **400 Bad Request**: Search Engine ID không đúng
- **429 Too Many Requests**: Đã hết quota 100 searches/ngày
---
## 📊 PHẦN 4: THÔNG TIN QUAN TRỌNG
### 💰 Chi phí và Quota
- **Miễn phí**: 100 searches/ngày
- **Trả phí**: $5/1000 searches sau khi hết free quota
- **Reset**: Quota reset vào 12:00 AM Pacific Time
### 🌐 Giới hạn tìm kiếm
- **Chỉ tìm được**: Nội dung công khai đã được Google index
- **Không tìm được**: 
  - Trang web private/password protected
  - Nội dung behind paywall
  - Tài liệu internal/company
  - Content mới chưa được index
## 🎯 KẾT QUẢ CUỐI CÙNG
Sau khi hoàn thành, bạn sẽ có 3 thông tin này:
```
API_KEY = "somethingsomethings"
SEARCH_ENGINE_ID = "somethingsomethings" 
BASE_URL = "https://www.googleapis.com/customsearch/v1"
```
**🎉 Chúc mừng! Bạn đã hoàn tất việc thiết lập Google Custom Search API!**

# MMMMMMMMMMMMMMMMMMMMMM

### Chạy ứng dụng
**Windows**: Click vào file đây
```bash
run.bat
```
**Linux/macOS**: Chạy terminal trỏ cd đến thư mục chứa file main.py
```bash
python main.py
```
### Hướng dẫn sử dụng
1. **Nhập văn bản**: Dán hoặc nhập văn bản cần kiểm tra vào ô text
2. **Tải file**: Sử dụng nút "Load File" để tải file .txt
3. **Mẫu văn bản**: Click "Sample" để tải văn bản mẫu
4. **Phân tích**: Click "Analyze Text" để bắt đầu kiểm tra
5. **Xem kết quả**: Kết quả sẽ hiển thị trong 3 tab:
   - **Summary**: Tổng quan kết quả
   - **Details**: Chi tiết các câu bị đánh dấu
   - **Recommendations**: Đề xuất cải thiện
## Cấu trúc dự án
```
plagiarism-checker/
├── main.py              # File chính để chạy ứng dụng
├── config.py            # Cấu hình API và thiết lập
├── api.py               # Xử lý Google Search API
├── analyzer.py          # Thuật toán phân tích văn bản
├── checker.py           # Logic kiểm tra đạo văn
├── gui.py               # Giao diện người dùng
├── requirements.txt     # Danh sách thư viện cần thiết
├── install.bat          # Script cài đặt tự động (Windows)
├── run.bat              # Script chạy ứng dụng (Windows)
└── README.md            # Tài liệu hướng dẫn
```
## Thuật toán phát hiện
Ứng dụng sử dụng 4 phương pháp tính toán độ tương tự:
1. **Sequence Similarity**: So sánh chuỗi ký tự trực tiếp
2. **Semantic Similarity**: Phân tích từ khóa và ngữ nghĩa
3. **Structural Similarity**: So sánh cấu trúc câu
4. **Lexical Similarity**: Tính toán cosine similarity
## Mức độ rủi ro
| Mức độ | Tỷ lệ đạo văn | Màu sắc | Mô tả |
|--------|---------------|---------|-------|
| SAFE | 0-5% | Xanh lá | An toàn, nội dung gốc |
| LOW | 5-15% | Xanh dương | Rủi ro thấp |
| MEDIUM | 15-25% | Vàng | Rủi ro trung bình |
| HIGH | 25-40% | Cam | Rủi ro cao |
| CRITICAL | >40% | Đỏ | Nguy hiểm, cần xử lý ngay |
## Giới hạn
- **API Requests**: 100 requests/ngày (Google Custom Search miễn phí)
- **Độ dài văn bản**: Tối thiểu 10 từ
- **Ngôn ngữ**: Chủ yếu hỗ trợ tiếng Anh
- **Nguồn kiểm tra**: Chỉ nội dung được Google index
## Giấy phép
Dự án này được phát triển cho mục đích giáo dục. Vui lòng tuân thủ các điều khoản sử dụng của Google API.
