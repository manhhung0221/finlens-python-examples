# Track 7 — Nghiên cứu học thuật

Ba track trước trả lời câu hỏi của nhà đầu tư. Track này trả lời câu hỏi của **hội đồng
chấm luận văn**: mẫu lấy thế nào, biến đo bằng gì, mô hình nào phù hợp, và vì sao.

Điểm khác biệt không nằm ở kinh tế lượng — phần đó giống hệt Stata. Nó nằm ở chỗ bước
tốn nhiều thời gian nhất của một luận văn định lượng biến mất: **dựng bộ dữ liệu**.

| Notebook | Nội dung |
|---|---|
| [`71_luan_van_no_xau_va_hieu_qua_ngan_hang.ipynb`](71_luan_van_no_xau_va_hieu_qua_ngan_hang.ipynb) | Panel 24 NHTM niêm yết × 11 năm · thống kê mô tả · tương quan · VIF · Pooled/FEM/REM · F-test, Breusch–Pagan LM, **Hausman** · kiểm định khuyết tật · **đọc kết quả bằng lời** · xuất `.xlsx` + `.dta` |

## Cần thêm gói

```bash
pip install linearmodels
```

Kéo theo `statsmodels` và `scipy`. Bảng tương ứng với Stata:

| Stata | Notebook |
|---|---|
| `xtset bank_id year` | `df.set_index(["symbol", "year"])` |
| `xtreg y x, fe` | `PanelOLS(y, X, entity_effects=True).fit()` |
| `xtreg y x, re` | `RandomEffects(y, X).fit()` |
| `hausman fe re` | hàm `hausman()` trong notebook |
| `xttest0` | hàm `breusch_pagan_lm()` |
| `xttest3` | hàm `wald_phuong_sai()` |
| `xtserial y x` | hàm `wooldridge_ar1()` |
| `xtreg y x, fe vce(cluster bank_id)` | `.fit(cov_type="clustered", cluster_entity=True)` |

## Ba chỗ dễ sai trong một luận văn dữ liệu bảng

**1. Đơn vị.** Mọi chỉ tiêu `unit = "ratio"` là **phân số**: `roa = 0.0167` nghĩa là
1,67%. Quên nhân 100 thì hệ số hồi quy in ra `-0.0027` và bị làm tròn về `0.000` khi
xuất bảng Word. Nhân 100 là phép đổi thang tuyến tính — không đổi dấu, p-value, $R^2$
hay bất kỳ kiểm định nào.

**2. Độ phủ trước khi hồi quy.** CAR do từng ngân hàng tự công bố và không đều. Đưa
thẳng vào mô hình thì mất quan sát mà không ai báo lỗi. Notebook in bảng độ phủ **trước**
khi chạy mô hình, và tự chuyển sang ETA khi CAR phủ dưới 80% — kèm dòng ghi chú để chép
vào phần Hạn chế.

**3. Hausman phải chạy trên ước lượng chưa hiệu chỉnh.** Công thức Hausman dựa trên tính
hiệu quả của REM dưới $H_0$, nên hai ước lượng đưa vào phải là loại **không robust**.
Hiệu chỉnh sai số chuẩn vững nhóm chỉ áp dụng **sau khi** đã chọn xong mô hình.

## Dùng cho lớp học

- **Ra đề:** đổi `NAM_CUOI`, đổi biến phụ thuộc, hoặc đổi `npl_ratio` → `group2_ratio`
  là có một đề tài khác, với đáp án kiểm chứng được.
- **Sinh viên không dùng Python:** chạy đến bước 4 rồi mở `output/panel_ngan_hang_npl.dta`
  bằng Stata, gõ `xtset bank_id year` và học tiếp phần kinh tế lượng.
- **Tái lập:** sang năm chạy lại `Run All` là có bộ số liệu cập nhật, cùng một khung
  phân tích.
