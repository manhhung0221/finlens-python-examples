# Track 0 — Bắt đầu với thư viện finlens

Notebook nền tảng cho toàn bộ 16 notebook còn lại. Chạy hết trong **dưới một phút**.

| Notebook | Nội dung |
|---|---|
| [`00_bat_dau.ipynb`](00_bat_dau.ipynb) | Khoá API (4 cách) · `whoami()` / `limits()` · lời gọi API đầu tiên · **đơn vị dữ liệu và `df.attrs`** · cây ngoại lệ `FinLensError` · tham số `on_error` · cache |

## Ba điều notebook này thiết lập cho mọi notebook sau

1. **Đọc đơn vị từ `df.attrs["finlens"]["units"]`, đừng nhớ.** Giá cổ phiếu Việt
   Nam tính bằng **nghìn VND**, giá chứng quyền bằng **VND thô**, giá phái sinh
   bằng **điểm chỉ số**. Nhầm chỗ này sai đúng 1000 lần và không có exception nào.
2. **`df.attrs` không sống sót qua `pd.concat` hay `merge`.** Đọc đơn vị *trước*
   khi ghép frame.
3. **Không tự chia lô mã.** Thư viện tự cắt theo `max_symbols_per_request` và gọi
   song song — bạn cứ truyền cả danh sách 400 mã.

→ Tiếp theo: [Track 1 — Thị trường và dòng tiền](../01-thi-truong-va-dong-tien/)
