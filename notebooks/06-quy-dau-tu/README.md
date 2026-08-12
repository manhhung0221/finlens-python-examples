# Track 6 — Quỹ đầu tư

`client.funds.*` là bề mặt mới của **finlens 1.4.0**: 188 quỹ Việt Nam, NAV theo
ngày từ 1995, danh mục nắm giữ theo tháng từ 2014.

Thứ đáng giá nhất không phải NAV mà là **phép tra ngược**:

```python
client.funds.holders("HPG")   # 80 quỹ đang nắm HPG, kèm tỷ trọng và số lượng
```

Đây là cầu nối cổ phiếu ↔ tổ chức mà bốn nhóm dữ liệu cũ không có.

| Notebook | Nội dung |
|---|---|
| [`61_quy_dau_tu.ipynb`](61_quy_dau_tu.ipynb) | 188 quỹ · NAV và hiệu suất so với VNINDEX · danh mục nắm giữ · **tra ngược `holders()`** · theo dấu quỹ gom/xả · bảng dòng tiền tổ chức |

## Năm phương thức

| Gọi | Trả về |
|---|---|
| `funds.list(fund_type="Quỹ ETF")` | 188 quỹ × 28 cột |
| `funds.nav(ma_quy, start=…)` | NAV theo ngày, tự phân trang bằng cursor |
| `funds.holdings(quy, date=…)` | danh mục nắm giữ — **một** quỹ, **một** kỳ |
| `funds.holders(ma_ck, date=…)` | **quỹ nào đang nắm mã này** |
| `funds.managers(quy)` | người điều hành |

## ⚠️ Cạm bẫy lớn nhất — không có trong tài liệu

**Cột `date` của `holders()` khác nhau theo từng quỹ.** Nó là kỳ công bố gần
nhất *của riêng quỹ đó*, không phải một kỳ chung. Đo trên `holders("HPG")`:

```
80 quỹ · 5 kỳ báo cáo khác nhau trong CÙNG một lời gọi
  2020-04-30     1   ← sáu năm trước, vẫn nằm trong danh sách
  2026-03-31     1
  2026-04-30     1
  2026-06-30    76
  2026-07-14     1
```

Quỹ báo cáo lần cuối năm 2020 vẫn xuất hiện với **10,9 triệu cổ phiếu**, như thể
đó là vị thế hôm nay. Cộng thẳng `quantity` là trộn vị thế của nhiều thời điểm
cách nhau nhiều năm.

**Luôn lọc theo tuổi vị thế trước khi cộng** — notebook có sẵn hàm `holders_tuoi()`.

## Năm cạm bẫy khác, đo được

- **Mã quỹ không duy nhất.** `VVDIF` thuộc hai tổ chức → `AmbiguousFundError`.
  Ngoại lệ trả `organization_ids` kiểu **`int`**, nhưng phương thức chỉ nhận
  **chuỗi** — phải `str()`.
- **Mã quỹ giữ nguyên cách viết.** 53/188 mã chứa dấu cách, `+`, `-`, hoặc chữ
  thường. Và một mã chứa **non-breaking space** (`ETF\xa0FM`) — nhìn giống dấu
  cách thường nhưng gõ tay thì không khớp.
- **Tiền tệ là VND thô**, khác `kVND` của giá cổ phiếu. Bốn cột `_ratio` ở thang
  **0–1**, không phải phần trăm.
- **`discount_ratio` là `null` với quỹ không niêm yết**, không phải `0`. Thay
  `NaN` bằng 0 làm lệch trung bình 14% trong mẫu đo được.
- **Tổng tỷ trọng danh mục không bằng 100%** — 86,7% ở ví dụ đo. Phần còn lại là
  tiền mặt. Chuẩn hoá lại về 100% thổi phồng mọi khoản.

## Độ phủ

API **không** lọc quỹ thiếu dữ liệu. Kiểm `nav_point_count` và
`holding_period_count` trước mọi thống kê:

| | Số quỹ |
|---|---:|
| Tổng danh mục | 188 |
| Chưa có dòng NAV nào | 39 |
| Chưa có danh mục nắm giữ | 47 |
| Có **cả hai** | 141 |

← [Track 5](../05-pandas-3/) · [Về mục lục chính](../../README.md)
