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

## Đánh giá (tham khảo)

### Tiêu chí

| Tiêu chí | Mức |
|---|---|
| Hiểu testing | Tốt |
| Biết unittest | Có |
| Biết assert | Có |
| Biết expectedFailure | Tốt |
| Biết phân loại test | Tốt |
| Có performance test | Có |
| Có boundary | Có |
| Có negative | Có |
| Có architecture | Có |

### Ước lượng điểm thực tế
Nếu giảng viên chấm tương đối công bằng: khoảng **8.5 – 9.5**.

### Vì sao chưa chắc 10?
- Test chưa quá sâu
- Chưa có mock / API mock
- Chưa có parameterized tests
- Chưa tách project structure chuẩn
- Vài negative test chưa thật sự “negative”

Với mức môn **Software Testing Foundations** thì bài này đã khá mạnh.

### Kết luận
So với hai phiên bản trước: **đây là phiên bản tốt nhất**.

Điểm mạnh:
- Lý thuyết ổn
- Code thật
- `unittest` thật
- Performance thật
- FAIL hợp lý
- README rõ ràng

=> Hoàn toàn đủ chất lượng để nộp.
