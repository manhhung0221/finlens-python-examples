# Track 0 — Bắt đầu với thư viện finlens

Notebook nền tảng cho toàn bộ 16 notebook còn lại. Chạy hết trong **dưới một phút**.

| Notebook | Nội dung |
|---|---|
| [`00_bat_dau.ipynb`](00_bat_dau.ipynb) | Khoá API (4 cách) · `whoami()` / `limits()` · lời gọi API đầu tiên · **đơn vị dữ liệu và `df.attrs`** · cây ngoại lệ `FinLensError` · tham số `on_error` · cache |

## Khoá API — khuyến nghị dùng extension FinLens cho VS Code

Cách tiện nhất để có khoá API là cài extension
**[FinLens cho VS Code](https://marketplace.visualstudio.com/items?itemName=FinLens.finlens)**: đăng nhập, tạo khoá và ghi khoá cho notebook
ngay trong editor, không phải sao chép khoá bằng tay. Hướng dẫn sử dụng:
**[docs.finlens.vn/vscode](https://docs.finlens.vn/vscode)**.

`Ctrl+Shift+P` → **`FinLens: Đăng nhập`** → **`FinLens: Tạo API key`** →
**`FinLens: Ghi API key ra file cấu hình`**. Bước cuối là **bắt buộc**: kernel
Jupyter không đọc được kho bí mật của VS Code, nên khoá phải được ghi ra file cấu
hình thì `finlens.client()` mới thấy. Các cách khác (biến môi trường, file cấu hình
tự tạo, truyền thẳng trong code) xem ở [README gốc](../../README.md#lấy-api-key--bốn-cách).

## Ba điều notebook này thiết lập cho mọi notebook sau

1. **Đọc đơn vị từ `df.attrs["finlens"]["units"]`, đừng nhớ.** Giá cổ phiếu Việt
   Nam tính bằng **nghìn VND**, giá chứng quyền bằng **VND thô**, giá phái sinh
   bằng **điểm chỉ số**. Nhầm chỗ này sai đúng 1000 lần và không có exception nào.
2. **`df.attrs` không sống sót qua `pd.concat` hay `merge`.** Đọc đơn vị *trước*
   khi ghép frame.
3. **Không tự chia lô mã.** Thư viện tự cắt theo `max_symbols_per_request` và gọi
   song song — bạn cứ truyền cả danh sách 400 mã.

→ Tiếp theo: [Track 1 — Thị trường và dòng tiền](../01-thi-truong-va-dong-tien/)
