# Track 1 — Thị trường và dòng tiền nhà đầu tư

Bốn notebook dựng bức tranh thị trường hằng ngày: giá và chỉ số, sức mạnh ngành
ICB, dòng tiền khối ngoại và tự doanh, rồi ghép tất cả thành một **báo cáo thị
trường một trang xuất ra HTML**.

| Notebook | Bạn học được |
|---|---|
| [`11_gia_va_dien_bien.ipynb`](11_gia_va_dien_bien.ipynb) | OHLCV nhiều mã trong một request · `interval` (`1d`/`1w`/`1mo`) · **giá điều chỉnh vs giá thô** · chuẩn hoá gốc 100 |
| [`12_ban_do_nganh_icb.ipynb`](12_ban_do_nganh_icb.ipynb) | Cây ngành ICB cấp 2 và cấp 4 · chỉ số 19 ngành · heatmap · **độ rộng thị trường (breadth)** |
| [`13_dong_tien_nha_dau_tu.ipynb`](13_dong_tien_nha_dau_tu.ipynb) | Khối ngoại · tự doanh · bốn nhóm chi tiết · dòng tiền theo ngành · tương quan với giá |
| [`14_dashboard_hang_ngay.ipynb`](14_dashboard_hang_ngay.ipynb) | **Sản phẩm 1** — báo cáo thị trường một trang, 8 lời gọi API, xuất HTML tự chứa |

## Cạm bẫy được chứng minh bằng số

- **Giá điều chỉnh vs giá thô**: đo trên VNM hai năm, lợi suất lệch **14,27 điểm
  phần trăm**. Chọn nhầm không có cảnh báo nào.
- **Bốn nhóm nhà đầu tư chi tiết cộng lại bằng 0**: đo trên 114 phiên HPG, tổng
  lệch tối đa **2 VND**. Cộng chúng với nhóm `foreign` là đếm hai lần.
- **Mã chỉ số**: `VNINDEX` · `VN30` · `HNXINDEX` · `HNX30` · `UPINDEX`. Hai tên
  có gạch nối trong README của thư viện (`HNX-INDEX`, `UPCOM-INDEX`) trả về
  `InvalidSymbolError`.

← [Track 0](../00-bat-dau/) · → [Track 2 — Phân tích cơ bản](../02-phan-tich-co-ban/)
