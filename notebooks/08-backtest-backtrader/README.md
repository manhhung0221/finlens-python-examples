# Track 8 — Backtest hướng sự kiện với backtrader

Track 3 dạy backtest **vectorised**: nhanh, gọn, nhưng mọi luật khớp lệnh phải tự
mã hoá bằng phép dịch ma trận. Track này dạy cách còn lại — **hướng sự kiện**
bằng [backtrader](https://www.backtrader.com/): đi từng thanh, đặt lệnh, broker
giả lập khớp lệnh, tính phí, ghi giao dịch. Chậm hơn, nhưng đọc như luật chơi
thật và mô hình hoá được thứ vectorised làm rất khó: T+2, trần/sàn, lệnh giới
hạn, cắt lỗ, ký quỹ phái sinh.

Câu hỏi xuyên suốt: **finlens đưa dữ liệu gì, backtrader cần dữ liệu dạng gì, và
chỗ nối giữa hai bên sai âm thầm ở đâu.**

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

## Ba bậc, chín notebook

### Bậc 1 — Cơ bản: đặt một chiến lược lên dữ liệu Việt Nam cho đúng

| Notebook | Bạn học được |
|---|---|
| [`81_tu_finlens_toi_cerebro.ipynb`](81_tu_finlens_toi_cerebro.ipynb) | Frame finlens → `PandasData` dựng tay · `Cerebro` · chiến lược đầu tiên · **đối chiếu một giao dịch bằng tay** · bẫy kVND · phiên dở dang |
| [`82_giai_phau_strategy.ipynb`](82_giai_phau_strategy.ipynb) | `lines`, `[0]`/`[-1]` · `__init__` vs `next` · `minperiod`/`prenext` · `notify_*` · Market/Limit/Stop/StopTrail · **cheat-on-close** |
| [`83_luat_choi_viet_nam.ipynb`](83_luat_choi_viet_nam.ipynb) | Phí hai chiều + **thuế bán** · lô 100 · **trần/sàn trên giá thô** · **T+2** · không bán khống · "ngây thơ" vs "luật VN" |

### Bậc 2 — Trung cấp: đo cho đúng, đưa dữ liệu finlens vào quyết định

| Notebook | Bạn học được |
|---|---|
| [`84_analyzer_va_bao_cao.ipynb`](84_analyzer_va_bao_cao.ipynb) | Analyzer → pandas → plotly · VNINDEX làm benchmark · **lãi suất phi rủi ro từ `client.macro`** · một đường vốn, nhiều con số Sharpe |
| [`85_chi_bao_va_du_lieu_ngoai_gia.ipynb`](85_chi_bao_va_du_lieu_ngoai_gia.ipynb) | `bt.ind.*` vs `df.finlens.*` · line phụ · khối ngoại · P/E, ROE quý · **độ trễ công bố BCTC** |
| [`86_danh_muc_nhieu_ma.ipynb`](86_danh_muc_nhieu_ma.ipynb) | Nhiều feed · mã niêm yết muộn (`prenext`) · `order_target_percent` · **dựng lại notebook `34` và truy từng nguồn lệch** |

### Bậc 3 — Nâng cao: tối ưu không tự lừa mình, phái sinh, đưa ra dùng

| Notebook | Bạn học được |
|---|---|
| [`87_toi_uu_va_walk_forward.ipynb`](87_toi_uu_va_walk_forward.ipynb) | `optstrategy` · heatmap tham số · **walk-forward** · giá của overfitting · đa tiến trình trên Windows |
| [`88_phai_sinh_va_intraday.ipynb`](88_phai_sinh_va_intraday.ipynb) | VN30F1M: hệ số nhân, ký quỹ, long/short · dữ liệu 1/5 phút · `resampledata` · **múi giờ** · **nhảy giá ngày đáo hạn** |
| [`89_bang_lenh_cuoi_ngay.ipynb`](89_bang_lenh_cuoi_ngay.ipynb) | **Sản phẩm 6** — danh sách lệnh cho phiên mai, xuất HTML/Excel · nhật ký paper-trading cộng dồn |

Đọc theo thứ tự. Từ `83` trở đi các notebook import
[`finlens_examples/bt_vn.py`](../../finlens_examples/bt_vn.py) — module gom lại
đúng những thứ `81`–`83` dựng bằng tay.

## Cài thêm

```bash
pip install backtrader
```

Bản cuối trên PyPI là `1.9.78.123` và dự án không còn phát triển, nhưng chạy được
với Python 3.12 + pandas 3.0 + numpy 2.5. Mọi biểu đồ vẽ bằng plotly từ analyzer,
nên **không cần matplotlib**. Muốn dùng `cerebro.plot()` thì cài thêm
`matplotlib` (đã thử với 3.11.2).

## `bt_vn.py` — cầu nối finlens → backtrader

| Thành phần | Làm gì |
|---|---|
| `feed_tu_finlens(df, ma=, cot_phu=)` | Frame finlens → feed, quy giá **và line phụ đơn vị giá** từ kVND về VND, đọc `df.attrs` — từ chối đoán khi `attrs` đã mất |
| `bo_phien_chua_dong(df, client)` | Bỏ thanh của phiên đang chạy, theo đồng hồ server |
| `PhiCoPhieuVN` | Phí môi giới hai chiều + thuế 0,1% chỉ chiều bán |
| `LoVN`, `lam_tron_lo` | Làm tròn lô 100; chiều bán tôn trọng T+2 |
| `KhopTheoBienDo` | Filler: không khớp ở phiên trần/sàn trắng bên |
| `ChienLuocVN` | Strategy nền có sổ T+2: `ban_duoc()`, `ban()` |
| `tran_san`, `buoc_gia`, `BIEN_DO` | Giá trần/sàn và bước giá theo sàn — tính trên **giá thô** |
| `PhiPhaiSinhVN`, `gan_phi_phai_sinh` | Hợp đồng tương lai VN30: hệ số nhân 100.000, ký quỹ theo tỷ lệ, phí/HĐ |
| `them_analyzer`, `ket_qua`, `chi_so_hieu_qua` | Analyzer → pandas: lợi suất, đường vốn, giao dịch, CAGR/MDD/Sharpe |

## Những con số đáng nhớ

- **Giá kVND nạp thẳng vào backtrader** (`81`): chiến lược mua **4.487.482** cổ
  phiếu thay vì 4.487 — 11,37% khối lượng cả phiên. Tổng lợi suất gần như không
  đổi (−23,06% so với −23,05%) và không có lỗi nào, nên không ai phát hiện.
- **Cheat-on-close** (`82`): trên 15 mã × 5 năm, `set_coc(True)` đổi CAGR trung
  bình **1,22–1,45 điểm %/năm**, trong khi CAGR trung bình của chính chiến lược
  chỉ −0,18% và +0,25%. Lỗi lớn hơn cả tín hiệu.
- **Luật chơi Việt Nam** (`83`): cùng chiến lược trên 10 mã HOSE, CAGR trung bình
  rơi từ **7,12% xuống 3,44%** khi thêm phí, thuế bán, lô 100, trần/sàn và T+2 —
  cả 10 mã đều xấu đi. Trần/sàn tính trên giá điều chỉnh sai ở **87,5%** số phiên.
- **Một đường vốn, nhiều Sharpe** (`84`): cùng đường vốn, `SharpeRatio` cho từ
  −0,026 tới +0,129 tuỳ tham số; mặc định +0,041, còn Sharpe đúng (theo ngày, trừ
  lợi suất TPCP 1 năm, năm hoá) ≈ 0.
- **Nhìn trước báo cáo tài chính** (`85`): gắn số quý vào ngày cuối quý thay vì
  hạn công bố đẩy CAGR rổ 98 mã từ 9,24% lên **11,14%** — 1,90 điểm %/năm có được
  nhờ đọc báo cáo trước khi nó tồn tại.
- **backtrader vs vectorised** (`86`): cùng giả định, hai bộ máy cho CAGR lệch
  chỉ **0,02 điểm %** (−3,28% so với −3,26%) — bộ máy không phải nguồn lệch. Thêm
  luật chơi Việt Nam thì lệch **−0,72 điểm %** so với `34` (−3,93% → −4,65%),
  truy được từng phần: tự tính tín hiệu −0,49, phí + thuế bán −0,40, lệnh bị từ
  chối vì thiếu tiền −0,15, lô 100 +0,32. Mua trước bán sau làm 1.336 lệnh bị từ
  chối; viết mỗi `next()` thì **0 giao dịch trong 5 năm** vì một mã mới niêm yết
  giữ cả danh mục trong `prenext`.
- **Overfitting** (`87`): tham số tốt nhất trong 54 cho Sharpe 1,00 trong mẫu và
  0,57 ngoài mẫu; tham số trung vị chỉ rơi 0,41 → 0,37. `maxcpus>1` với strategy
  viết trong notebook **treo mà không báo lỗi** trên Windows; chuyển sang file
  `.py` thì 8 lõi nhanh 13–15 lần (tuỳ lần đo), kết quả giống hệt.
- **Ký quỹ phái sinh** (`88`): `CommInfo` định giá ký quỹ theo giá hiện tại làm
  lãi/lỗ chưa chốt của vị thế long phóng to 1,2 lần — tiền cuối vẫn đúng tới từng
  đồng, nhưng đường vốn lệch tới 3,52 triệu VND nên drawdown và Sharpe đều sai.
- **Trần/sàn trên bảng lệnh** (`89`): tính trên giá điều chỉnh thì **15/60** lệnh
  trong 6 tháng in sai trần/sàn, tệ nhất lệch 51,89% — nhưng ở phiên hôm nay thì
  0/30, nên kiểm danh sách của "hôm nay" không bắt được lỗi.

← [Track 7](../07-nghien-cuu-hoc-thuat/) · [Track 3 — backtest vectorised](../03-phan-tich-ky-thuat/)
