# Track 4 — Intraday, phái sinh, chứng quyền và vĩ mô

Bốn notebook cho các bề mặt dữ liệu còn lại: khớp lệnh tick-by-tick, hợp đồng
tương lai VN30F1M, chứng quyền có bảo đảm, và **3.348 chuỗi chỉ tiêu vĩ mô** từ
Tổng cục Thống kê và Ngân hàng Nhà nước.

| Notebook | Bạn học được |
|---|---|
| [`41_intraday_order_flow.ipynb`](41_intraday_order_flow.ipynb) | Tick · **ba giá trị của `side`** · VWAP · ba đại lượng "chủ động" khác nhau · `max_intraday_days` |
| [`42_phai_sinh_va_basis.ipynb`](42_phai_sinh_va_basis.ipynb) | VN30F1M · basis EOD và 1 phút · vì sao `basis()` không có `interval` · hai nhóm nhà đầu tư |
| [`43_chung_quyen.ipynb`](43_chung_quyen.ipynb) | **Bẫy đơn vị 1000 lần** · 311 chứng quyền · moneyness · thanh khoản là rủi ro chính |
| [`44_vi_mo_va_thi_truong.ipynb`](44_vi_mo_va_thi_truong.ipynb) | **Sản phẩm 4** — CPI/GDP/tín dụng/tỷ giá/OMO/xuất nhập khẩu đặt cạnh VNINDEX |

## Bốn phát hiện đo được trong Track này

- **`side` có ba giá trị**, không phải hai: `buy`, `sell`, và **`auction`** (khớp
  lệnh định kỳ ATO/ATC). Phiên định kỳ chiếm hai chữ số phần trăm khối lượng ở
  nhiều mã — không giấu được vào rổ mua hay rổ bán.
- **`active_volume()` chia đôi khối lượng định kỳ** vào hai rổ mua/bán:
  `active_buy − buy = auction ÷ 2`, khớp **18/18** quan sát. Chênh lệch ròng vẫn
  đúng, nhưng *tỷ lệ* mua chủ động bị thổi phồng (46,72% so với 43,23%).
- **Đơn vị chứng quyền là VND thô**, cổ phiếu là nghìn VND. `meta.warrants()`
  **không có tỷ lệ chuyển đổi**, nên tính được moneyness nhưng không tính được
  premium.
- **`client.macro` là namespace duy nhất mà `unit` là một CỘT**, không phải thuộc
  tính của cả bảng. Mọi phép tính phải bắt đầu bằng `groupby("code")`.

← [Track 3](../03-phan-tich-ky-thuat/) · [Về mục lục chính](../../README.md)
