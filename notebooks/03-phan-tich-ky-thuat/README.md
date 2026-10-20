# Track 3 — Phân tích kỹ thuật và backtest

Bốn notebook về **135 hàm TA-Lib** trong `finlens`, ở hai tầng: `df.finlens.*`
(75 chỉ báo, tự tách theo mã) và `finlens.ta.*` (74 chỉ báo + 61 mẫu nến, bám sát
TA-Lib).

| Notebook | Bạn học được |
|---|---|
| [`31_chi_bao_ky_thuat.ipynb`](31_chi_bao_ky_thuat.ipynb) | Hai tầng chỉ báo · warm-up · `NaN` lan · **24/75 hàm có trạng thái không ổn định** · dữ liệu chưa sắp xếp |
| [`32_mau_nen.ipynb`](32_mau_nen.ipynb) | 61 mẫu nến · dạng dài vs dạng rộng · **`signal` không chỉ có ±100** · event study |
| [`33_screener_tin_hieu.ipynb`](33_screener_tin_hieu.ipynb) | **Sản phẩm 3** — quét 6 tín hiệu trên toàn sàn HOSE, đo hiệu quả từng tín hiệu |
| [`34_backtest_chien_luoc.ipynb`](34_backtest_chien_luoc.ipynb) | Backtest vectorised · tránh look-ahead · chi phí theo quay vòng · CAGR/MDD/Sharpe |

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

## Ba con số đáng nhớ

- **`talib.RSI` trên frame nhiều mã**: mã đầu đúng hoàn toàn, **mã thứ hai sai
  174/250 dòng**, lệch tới 18 điểm RSI — và mọi giá trị sai đều nằm trong khoảng
  0–100 hợp lệ. Dùng `df.finlens.rsi(14)`; nó tự tách nhóm.
- **`df[df.signal == 100]`** đánh rơi ~6% tín hiệu tăng trên tổng thể, nhưng
  **hai phần ba** nếu mẫu bạn dùng là Engulfing hay Harami. Lọc bằng `direction`.
- **Backtest**: cùng một chiến lược cho CAGR **−3,93%** khi đo đúng và **+1,77%**
  khi mắc ba lỗi phổ biến (nhìn trước ở bộ lọc vũ trụ, khớp ở giá đóng cửa phiên
  tín hiệu, bỏ chi phí). Khoảng cách 5,70 điểm phần trăm đó là *phương pháp*,
  không phải chiến lược. Mục 10 đo thêm bốn lỗi mà chính bản "đúng" trước đây
  mắc, tìm ra khi notebook `86` dựng lại nó bằng backtrader.

← [Track 2](../02-phan-tich-co-ban/) · → [Track 4 — Intraday, phái sinh, vĩ mô](../04-intraday-phai-sinh-vi-mo/)
