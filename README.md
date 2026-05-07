# Dethikiemthu

Bài tập Kiểm thử (Python) — chạy bộ `unittest` trong một file duy nhất.

## Yêu cầu
- Python 3.11+
- Không có thư viện ngoài (chỉ dùng standard library)

## Cách chạy
Trong thư mục project:

```powershell
c:/Python/KiemThuApp/.venv/Scripts/python.exe BTLkiemthu.py
```

Hoặc nếu bạn đang dùng Python hệ thống:

```powershell
python BTLkiemthu.py
```

## Ghi chú
- Kết quả `OK (expected failures=3)` là bình thường: 3 test negative được đánh dấu `expectedFailure` để minh hoạ lỗi alpha (cố ý).

## Severity (tham khảo)

| Severity | Lỗi |
|---|---|
| Critical | Search timeout |
| Major | Booking tạo < 7 ngày không truy xuất/xác nhận được |
| Minor | Airline data thiếu một phần (một số hãng trả rỗng) |
| Trivial | UI/format |
