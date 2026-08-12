# Track 2 — Phân tích cơ bản và định giá cổ phiếu

Bốn notebook khai thác **181 chỉ tiêu tài chính tính sẵn** của `finlens`, chia
theo bốn loại hình doanh nghiệp: `CT` phi tài chính (61), `NH` ngân hàng (43),
`CK` chứng khoán (38), `BH` bảo hiểm (39).

| Notebook | Bạn học được |
|---|---|
| [`21_bao_cao_tai_chinh.ipynb`](21_bao_cao_tai_chinh.ipynb) | `statement()` dạng long · cây `item_id`/`parent_id`/`level` · common-size · bốn cây chỉ tiêu khác nhau |
| [`22_chi_so_va_dupont.ipynb`](22_chi_so_va_dupont.ipynb) | `indicator_catalog()` với `formula` và `higher_is_better` · **bẫy kỳ báo cáo** · DuPont ba và năm tầng |
| [`23_screener_dinh_gia.ipynb`](23_screener_dinh_gia.ipynb) | **Sản phẩm 2** — chấm điểm toàn sàn HOSE, z-score trong ngành, xuất Excel |
| [`24_deep_dive_ngan_hang.ipynb`](24_deep_dive_ngan_hang.ipynb) | NIM = YOEA − COF · nợ xấu và nợ nhóm 2 · bao phủ nợ xấu · CIR · LDR · bảng điểm 28 ngân hàng |

## Cạm bẫy lớn nhất của Track này

⚠️ **Kỳ của chỉ số tài chính khác nhau theo loại hình doanh nghiệp.**

Trong `period="quarterly"`: `CT` phi tài chính cho ROE/ROA **riêng quý đó**
(Q4 ÷ năm ≈ 0,27), còn `NH`/`CK`/`BH` cho giá trị **đã quy về năm** (≈ 1,00).

Hệ quả đo được: xếp hạng ROE quý đặt VCB ở 18,0% và FPT ở 6,3% — trong khi ROE
**năm** của FPT là 21,4%, cao hơn VCB. Không có cảnh báo nào; cả hai đều mang
`unit="ratio"` và `period_type="quarterly"`.

→ **Dùng `period="annual"` cho mọi phép so sánh cắt ngang.**

← [Track 1](../01-thi-truong-va-dong-tien/) · → [Track 3 — Phân tích kỹ thuật](../03-phan-tich-ky-thuat/)
