# BTLkiemthu

Bài tập Kiểm thử (Python) sử dụng `unittest` (standard library).

- Implementations: `src/services.py`
- Test suite: `tests/test_services.py`

## Yêu cầu
- Python 3.11+
- Không có thư viện ngoài (chỉ dùng standard library)

## Cách chạy
Trong thư mục repo:

```powershell
python BTLkiemthu.py
```

Hoặc chạy trực tiếp unittest discovery:

```powershell
python -m unittest discover -s tests -v
```

## Ghi chú
- Không cần thư viện ngoài.

## Severity (tham khảo)

| Severity | Lỗi |
|---|---|
| Critical | Search timeout |
| Major | Booking tạo < 7 ngày không truy xuất/xác nhận được |
| Minor | Airline data thiếu một phần (một số hãng trả rỗng) |
| Trivial | UI/format |

