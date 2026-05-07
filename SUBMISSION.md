# BÀI LÀM CUỐI KỲ - SOFTWARE TESTING FOUNDATIONS

## CÂU 1: PHÂN TÍCH HỆ THỐNG (2.0 điểm)

### 1) Xác định 3 loại lỗi tương ứng

1. **Không truy xuất được booking mới (< 7 ngày)**  
   → **Logic/Data Access Defect** (lỗi điều kiện truy vấn hoặc xử lý dữ liệu booking mới)

2. **Một số hãng hàng không không trả dữ liệu**  
   → **API Integration Defect** (lỗi tích hợp API bên thứ ba)

3. **Tìm kiếm theo địa điểm bị timeout**  
   → **Performance Defect** (độ trễ xử lý vượt ngưỡng SLA < 50ms)

### 2) Phân tích nguyên nhân khả dĩ

| Vấn đề | Nhóm nguyên nhân | Phân tích nguyên nhân khả dĩ |
|---|---|---|
| Không truy xuất được booking mới (<7 ngày) | Database / Logic | Câu lệnh SQL lọc sai toán tử ngày (`>` thay vì `>=`), lệch timezone giữa app và DB, index theo `created_at` không phù hợp, mapping ORM bỏ sót bản ghi mới |
| Một số hãng hàng không không trả dữ liệu | API | Sai API key/secret theo từng hãng, giới hạn rate-limit, contract API thay đổi field trả về, timeout phía đối tác, retry/backoff chưa cấu hình |
| Tìm kiếm theo địa điểm bị timeout | Performance / Database / API | Truy vấn không tối ưu (full scan), gọi tuần tự nhiều API ngoài thay vì song song, cache chưa có hoặc cache miss cao, dữ liệu địa điểm quá lớn nhưng không phân trang, network latency cao |

---

## CÂU 2: THIẾT KẾ TEST CASE (3.0 điểm)

> Format: **# | Module | Action | Expected Result | Actual Result | Status | Type**  
> Đảm bảo: 5 Functional, 3 Negative, 2 Boundary, 2 Performance và có cả PASS/FAIL.

| # | Module | Action | Expected Result | Actual Result | Status | Type |
|---|---|---|---|---|---|---|
| 1 | Air | Xác nhận booking `A001` tồn tại | Trả về `True` | `True` | PASS | Functional |
| 2 | Air | Xác nhận booking không tồn tại `A999` | Trả về `False` | `False` | PASS | Functional |
| 3 | Air | Tìm hãng theo từ khóa `Viet` | Có kết quả `VietJet Air` | Có kết quả | PASS | Functional |
| 4 | Air | Tìm chuyến `SGN -> HAN` | Có >=1 chuyến hợp lệ | Có 1 chuyến | PASS | Functional |
| 5 | Hotel | Tìm khách sạn `Da Nang`, `min_stars=4` | Danh sách không rỗng | Có 2 khách sạn | PASS | Functional |
| 6 | Hotel | Đặt phòng với `nights=0` | Báo lỗi đầu vào | Ném `ValueError` | PASS | Negative |
| 7 | Search & Plan | Tìm kiếm với keyword rỗng | Báo lỗi đầu vào | Ném `ValueError` | PASS | Negative |
| 8 | Search & Plan | Gợi ý cá nhân hóa thiếu `preferences` | Báo lỗi dữ liệu profile | Ném `ValueError` | PASS | Negative |
| 9 | Air | Gửi check-in reminder với `hours_before=0` | Hệ thống chấp nhận (biên dưới) | Reminder gửi thành công | PASS | Boundary |
| 10 | Hotel | Kiểm tra giá với `nights=1` | Giá = đơn giá x 1 đêm | `900000` | PASS | Boundary |
| 11 | Air | Đo thời gian tìm chuyến theo địa điểm | < 50ms | 4ms | PASS | Performance |
| 12 | Search & Plan | Đo thời gian tìm kiếm toàn hệ thống | < 50ms | 6ms | PASS | Performance |
| 13 | Air | Xác nhận booking tạo trong vòng 7 ngày | Truy xuất được | Không truy xuất được | FAIL | Functional |
| 14 | Air | Lấy danh sách hãng từ đối tác cụ thể | Trả dữ liệu đầy đủ | Một số hãng trả rỗng | FAIL | Integration |
| 15 | Search & Plan | Tìm kiếm theo địa điểm giờ cao điểm | < 50ms | Timeout | FAIL | Performance |

---

## CÂU 3: LẬP TRÌNH KIỂM THỬ PYTHON (4.0 điểm)

Đã triển khai trong repo:

- `src/services.py`
  - `AirService` (5 chức năng)
  - `HotelService` (5 chức năng)
  - `SearchPlanService` (5 chức năng)
- `tests/test_services.py`
  - Mỗi module có **5 test functions**
  - Bao gồm: Functional, Negative, Boundary, Performance

### Cách chạy test

```bash
python -m unittest discover -s tests -v
```

---

## CÂU 4: PHÂN TÍCH KẾT QUẢ KIỂM THỬ (1.0 điểm)

### 1) Tổng kết kết quả kiểm thử

- Tổng số test case thiết kế: **15**
- PASS: **12**
- FAIL: **3**
- Tỷ lệ pass: **80%**

### 2) Ít nhất 3 lỗi tìm được

1. Không truy xuất được booking mới (<7 ngày)  
2. Một số hãng hàng không không trả dữ liệu API  
3. Tìm kiếm theo địa điểm bị timeout

### 3) Phân loại mức độ lỗi

- **Critical**: Timeout tìm kiếm theo địa điểm (ảnh hưởng chức năng lõi tìm kiếm)
- **Major**: Booking tạo < 7 ngày không truy xuất/xác nhận được (ảnh hưởng truy xuất/xác nhận booking mới)
- **Minor**: Một số hãng không trả dữ liệu API (ảnh hưởng phạm vi kết quả)
- **Trivial**: Sai format thông báo/nhãn hiển thị (nếu có)

