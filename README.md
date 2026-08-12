# finlens examples — 26 notebook phân tích dữ liệu chứng khoán Việt Nam bằng Python

**Bộ ví dụ thực chiến cho thư viện Python [`finlens`](https://pypi.org/project/finlens/)** —
dữ liệu chứng khoán Việt Nam (HOSE, HNX, UPCOM) trả về thẳng dưới dạng
`pandas.DataFrame`. 26 Jupyter notebook đi từ lời gọi API đầu tiên tới các sản
phẩm dùng được hằng ngày: **dashboard thị trường**, **screener định giá**,
**screener tín hiệu kỹ thuật**, **dashboard vĩ mô**, và **bảng theo dấu dòng
tiền quỹ đầu tư** — cộng một chuỗi bài dạy **pandas 3.0** qua chính dữ liệu đó.

Mọi notebook chạy trên **dữ liệu thật**, đã thực thi từ đầu tới cuối, không có số
bịa và không có file `.csv` mẫu.

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue)](https://www.python.org/)
[![finlens](https://img.shields.io/badge/finlens-1.4.0-brightgreen)](https://pypi.org/project/finlens/)
[![pandas](https://img.shields.io/badge/pandas-3.0%2B-150458)](https://pandas.pydata.org/)
[![Plotly](https://img.shields.io/badge/Plotly-6.0%2B-3f4f75)](https://plotly.com/python/)
[![VS Code Extension](https://img.shields.io/badge/VS%20Code-FinLens-007ACC)](https://marketplace.visualstudio.com/items?itemName=FinLens.finlens)

> *26 hands-on Jupyter notebooks for the `finlens` Python library — Vietnam stock
> market data (HOSE, HNX, UPCOM) as pandas DataFrames. Covers EOD and intraday
> prices, tick data, foreign investor flows, financial statements, 181
> pre-computed financial ratios, 135 TA-Lib indicators, derivatives, covered
> warrants, and 3,348 macroeconomic series. All notebooks run on live data.*

---

## Mục lục

- [finlens là gì](#finlens-là-gì)
- [Chạy thử trong ba phút](#chạy-thử-trong-ba-phút)
- [Lấy API key — bốn cách](#lấy-api-key--bốn-cách)
- [Bản đồ 26 notebook](#bản-đồ-26-notebook)
- [Năm điều sẽ làm bạn mất tiền nếu bỏ qua](#năm-điều-sẽ-làm-bạn-mất-tiền-nếu-bỏ-qua)
- [Cấu trúc dự án](#cấu-trúc-dự-án)
- [Câu hỏi thường gặp](#câu-hỏi-thường-gặp)

---

## finlens là gì

`finlens` là **thư viện Python lấy dữ liệu thị trường chứng khoán Việt Nam**.
Nó trả về `pandas.DataFrame` trần — không wrapper, không lớp con — nên mọi
tutorial pandas bạn từng đọc đều dùng được.

Bề mặt dữ liệu có trong phiên bản `1.4.0`:

| Namespace | Dữ liệu | Repo này dùng ở |
|---|---|---|
| `client.eod.*` | Giá cuối ngày cổ phiếu, chỉ số, phái sinh, chứng quyền, chỉ số ngành ICB; dòng tiền nhà đầu tư; sổ lệnh đặt; khối lượng chủ động | Track 1, 2, 4 |
| `client.intraday.*` | OHLCV trong phiên (1 phút → 4 giờ), **khớp lệnh tick-by-tick**, giá trị mua/bán chủ động, basis phái sinh | Track 4 |
| `client.financials.*` | Báo cáo tài chính từ 2004, **181 chỉ tiêu tính sẵn** cho 4 loại hình doanh nghiệp | Track 2 |
| `client.macro.*` | **3.348 chuỗi vĩ mô** — CPI, GDP, tín dụng, tỷ giá, lãi suất, OMO, xuất nhập khẩu | Track 4 |
| `client.meta.*` | 1.645 mã chứng khoán, 125 ngành ICB, chứng quyền đang lưu hành | mọi Track |
| `client.funds.*` | **188 quỹ đầu tư** — NAV từ 1995, danh mục nắm giữ, và tra ngược *mã này quỹ nào nắm* | Track 6 |
| `df.finlens.*` | **135 hàm TA-Lib** — 75 chỉ báo tự tách theo mã + 61 mẫu nến | Track 3 |

Phủ **HOSE (HSX), HNX và UPCOM**, hợp đồng phái sinh `VN30F1M`, và năm chỉ số
`VNINDEX` · `VN30` · `HNXINDEX` · `HNX30` · `UPINDEX`.

---

## Chạy thử trong ba phút

```bash
git clone https://github.com/manhhung0221/finlens-python-examples.git
cd finlens-python-examples
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Đặt API key (xem [bốn cách bên dưới](#lấy-api-key--bốn-cách)), rồi mở notebook:

```bash
jupyter lab notebooks/
```

Bắt đầu ở [`notebooks/00-bat-dau/00_bat_dau.ipynb`](notebooks/00-bat-dau/00_bat_dau.ipynb).

Notebook **tự tìm thư mục gốc** để `import finlens_examples` — không cần
`pip install -e .`, không cần đặt `PYTHONPATH`, mở từ thư mục nào cũng chạy.

---

## Lấy API key — bốn cách

Khoá API FinLens có dạng `flk_...`. Thư viện tìm khoá theo thứ tự ưu tiên:

**`api_key=` → `FINLENS_API_KEY` → file cấu hình.**

### Cách 1 — Extension VS Code FinLens (khuyến nghị nếu bạn dùng VS Code)

[![Cài từ Marketplace](https://img.shields.io/badge/Marketplace-FinLens.finlens-007ACC?logo=visualstudiocode)](https://marketplace.visualstudio.com/items?itemName=FinLens.finlens)

Extension **[FinLens for Visual Studio Code](https://marketplace.visualstudio.com/items?itemName=FinLens.finlens)**
cấp và quản lý khoá cho bạn, không cần vào web.

1. Cài extension `FinLens.finlens` từ Marketplace.
2. Mở Command Palette (`Ctrl+Shift+P`) → **`FinLens: Đăng nhập`** — bằng email
   hoặc Google.
3. **`FinLens: Tạo API key`** — extension cấp khoá mới và lưu vào **VS Code
   SecretStorage** (kho bí mật của hệ điều hành).
4. ⚠️ **Bước bắt buộc cho notebook:** chạy
   **`FinLens: Ghi API key ra file cấu hình (cho notebook và terminal ngoài)`**.

**Vì sao bước 4 là bắt buộc.** VS Code SecretStorage chỉ extension đọc được.
Kernel Jupyter là một **tiến trình Python riêng** không có đường nào tới kho bí
mật đó — chạy cell mà bỏ qua bước 4 thì `finlens.client()` ném lỗi `FL_CONFIG`.
Lệnh ở bước 4 ghi khoá ra file cấu hình máy, nơi thư viện Python đọc được:

| Hệ điều hành | Đường dẫn file cấu hình |
|---|---|
| Windows | `%APPDATA%\finlens\config.toml` |
| macOS / Linux | `$XDG_CONFIG_HOME/finlens/config.toml`, mặc định `~/.config/finlens/config.toml` |

Extension hiện một hộp thoại xác nhận nói rõ cái giá phải trả trước khi ghi.
**Không cần khởi động lại kernel** — `finlens.client()` đọc file cấu hình ở *mỗi*
lần gọi, không phải lúc `import finlens`.

⚠️ **Đánh đổi cần biết:** khoá nằm **plaintext trên đĩa**, không còn được kho bí
mật của hệ điều hành bảo vệ, và **mọi tiến trình Python trên máy đọc được nó** —
kể cả sau khi bạn gỡ VS Code. Thu hồi bằng
**`FinLens: Xoá API key khỏi file cấu hình`**.

Hai lệnh hữu ích khác:

| Lệnh | Chức năng |
|---|---|
| `FinLens: Nhập API key` | Dán khoá có sẵn vào SecretStorage |
| `FinLens: Kiểm tra cấu hình` | Chẩn đoán: SDK, môi trường Python, trạng thái khoá |

Extension còn cho **bảng giá realtime**, **chèn code Python theo dataset**,
**xem trước dữ liệu ngay trong editor** và **biểu đồ kỹ thuật** — nhưng để chạy
26 notebook này thì bốn bước trên là đủ.

### Cách 2 — Biến môi trường

Hợp với CI, container, script tự động:

```bash
set FINLENS_API_KEY=flk_...
```

### Cách 3 — File cấu hình, tự tạo tay

Cùng đường dẫn ở bảng trên:

```toml
[default]
api_key = "flk_..."
```

⚠️ **Đừng tạo `./finlens.toml` trong thư mục dự án.** **File đầu tiên tìm thấy
là file duy nhất được đọc — không merge**, nên một file cục bộ che *hoàn toàn*
cấu hình máy bạn, kể cả những khoá nó không khai. `.gitignore` đã chặn nó khỏi
git, nhưng nó vẫn che.

### Cách 4 — Truyền thẳng trong code

Chỉ dùng để thử nhanh; đừng commit:

```python
client = finlens.client(api_key="flk_...")
```

Chưa có tài khoản? Đăng ký tại **[finlens.vn](https://finlens.vn)**.

---

## Bản đồ 26 notebook

Notebook chia thành **7 thư mục theo chủ đề**. Mỗi thư mục có README riêng.

### [Track 0 — Bắt đầu](notebooks/00-bat-dau/)

| Notebook | Nội dung |
|---|---|
| [`00_bat_dau`](notebooks/00-bat-dau/00_bat_dau.ipynb) | Khoá API · `whoami`/`limits` · lời gọi đầu tiên · **đơn vị và `df.attrs`** · cây ngoại lệ · `on_error` · cache |

### [Track 1 — Thị trường và dòng tiền](notebooks/01-thi-truong-va-dong-tien/)

| Notebook | Nội dung |
|---|---|
| [`11_gia_va_dien_bien`](notebooks/01-thi-truong-va-dong-tien/11_gia_va_dien_bien.ipynb) | OHLCV nhiều mã một request · `interval` · giá điều chỉnh vs giá thô · chuẩn hoá gốc 100 |
| [`12_ban_do_nganh_icb`](notebooks/01-thi-truong-va-dong-tien/12_ban_do_nganh_icb.ipynb) | Cây ngành ICB · sức mạnh 19 ngành · heatmap · độ rộng thị trường |
| [`13_dong_tien_nha_dau_tu`](notebooks/01-thi-truong-va-dong-tien/13_dong_tien_nha_dau_tu.ipynb) | Khối ngoại · tự doanh · bốn nhóm chi tiết · dòng tiền theo ngành |
| [`14_dashboard_hang_ngay`](notebooks/01-thi-truong-va-dong-tien/14_dashboard_hang_ngay.ipynb) | **Sản phẩm 1** — báo cáo thị trường một trang, xuất HTML |

### [Track 2 — Phân tích cơ bản và định giá](notebooks/02-phan-tich-co-ban/)

| Notebook | Nội dung |
|---|---|
| [`21_bao_cao_tai_chinh`](notebooks/02-phan-tich-co-ban/21_bao_cao_tai_chinh.ipynb) | `statement` dạng long · cây chỉ tiêu · common-size · bốn loại hình doanh nghiệp |
| [`22_chi_so_va_dupont`](notebooks/02-phan-tich-co-ban/22_chi_so_va_dupont.ipynb) | 181 chỉ tiêu tính sẵn · `formula` & `higher_is_better` · DuPont ba và năm tầng |
| [`23_screener_dinh_gia`](notebooks/02-phan-tich-co-ban/23_screener_dinh_gia.ipynb) | **Sản phẩm 2** — chấm điểm toàn sàn, z-score trong ngành, xuất Excel |
| [`24_deep_dive_ngan_hang`](notebooks/02-phan-tich-co-ban/24_deep_dive_ngan_hang.ipynb) | NIM · NPL · bao phủ nợ xấu · CIR · LDR trên 28 ngân hàng niêm yết |

### [Track 3 — Phân tích kỹ thuật và backtest](notebooks/03-phan-tich-ky-thuat/)

| Notebook | Nội dung |
|---|---|
| [`31_chi_bao_ky_thuat`](notebooks/03-phan-tich-ky-thuat/31_chi_bao_ky_thuat.ipynb) | `df.finlens.*` vs `finlens.ta.*` · warm-up · `NaN` lan · chỉ báo bất ổn định |
| [`32_mau_nen`](notebooks/03-phan-tich-ky-thuat/32_mau_nen.ipynb) | 61 mẫu nến · `signal` không chỉ có ±100 · event study có sai số chuẩn |
| [`33_screener_tin_hieu`](notebooks/03-phan-tich-ky-thuat/33_screener_tin_hieu.ipynb) | **Sản phẩm 3** — quét 6 tín hiệu toàn sàn HOSE, đo hiệu quả từng tín hiệu |
| [`34_backtest_chien_luoc`](notebooks/03-phan-tich-ky-thuat/34_backtest_chien_luoc.ipynb) | Backtest vectorised · tránh look-ahead · chi phí theo quay vòng · CAGR/MDD/Sharpe |

### [Track 4 — Intraday, phái sinh, vĩ mô](notebooks/04-intraday-phai-sinh-vi-mo/)

| Notebook | Nội dung |
|---|---|
| [`41_intraday_order_flow`](notebooks/04-intraday-phai-sinh-vi-mo/41_intraday_order_flow.ipynb) | Tick · ba giá trị `side` · VWAP · ba đại lượng "chủ động" khác nhau |
| [`42_phai_sinh_va_basis`](notebooks/04-intraday-phai-sinh-vi-mo/42_phai_sinh_va_basis.ipynb) | VN30F1M · basis EOD và 1 phút · dòng tiền phái sinh |
| [`43_chung_quyen`](notebooks/04-intraday-phai-sinh-vi-mo/43_chung_quyen.ipynb) | **Bẫy đơn vị 1000 lần** · moneyness · thanh khoản chứng quyền |
| [`44_vi_mo_va_thi_truong`](notebooks/04-intraday-phai-sinh-vi-mo/44_vi_mo_va_thi_truong.ipynb) | **Sản phẩm 4** — CPI/GDP/tỷ giá/OMO/xuất nhập khẩu đặt cạnh VNINDEX |

### [Track 5 — pandas 3.0 từ cơ bản tới nâng cao](notebooks/05-pandas-3/)

Chuỗi bài dạy **pandas 3.0** qua dữ liệu thị trường thật. pandas 3.0 xoá thật
nhiều API, và mã pandas 2.x chạy vào là gãy — hoặc **im lặng không làm gì**.

| Notebook | Nội dung |
|---|---|
| [`51_cau_truc_va_dtype`](notebooks/05-pandas-3/51_cau_truc_va_dtype.ipynb) | Series · DataFrame · Index · **`str` thay `object`** · `pd.NA` và logic ba giá trị · đo bộ nhớ |
| [`52_chon_loc_va_cow`](notebooks/05-pandas-3/52_chon_loc_va_cow.ipynb) | `.loc`/`.iloc` · boolean mask · `query()` · ⚠️ **Copy-on-Write** — ba tình huống, một cái không cảnh báo |
| [`53_bien_doi_cot`](notebooks/05-pandas-3/53_bien_doi_cot.ipynb) | `assign` · **năm cách tính một cột, đo tốc độ cả năm** · `np.select`/`pd.cut` · `.str` |
| [`54_mini_project_chuan_bi_du_lieu`](notebooks/05-pandas-3/54_mini_project_chuan_bi_du_lieu.ipynb) | **Sản phẩm 5** — hàm `chuan_bi_du_lieu()` dán được vào dự án: kiểm chất lượng, tối ưu kiểu, thêm cột phái sinh |
| [`55_groupby`](notebooks/05-pandas-3/55_groupby.ipynb) | `agg`/`transform`/`filter` · ⚠️ **`observed=` đổi mặc định** · bẫy ranh giới nhóm |
| [`56_reshape_long_wide`](notebooks/05-pandas-3/56_reshape_long_wide.ipynb) | `pivot`/`melt`/`stack`/`unstack` · ⚠️ **`stack()` giờ giữ `NaN`** · ma trận tương quan |
| [`57_ghep_du_lieu`](notebooks/05-pandas-3/57_ghep_du_lieu.ipynb) | Bốn kiểu join · ⚠️ **`validate=`** · `merge_asof` cho dữ liệu tick |
| [`58_time_series`](notebooks/05-pandas-3/58_time_series.ipynb) | ⚠️ **Bảy mã tần suất bị xoá** · `resample` · `rolling(closed="left")` · múi giờ |

Notebook cuối (`59_di_tru_va_hieu_nang`) đang được viết tiếp: bảng tra đầy đủ
những API pandas 3.0 đã xoá, cách bắt chúng trong test, và tối ưu hiệu năng.

### [Track 6 — Quỹ đầu tư](notebooks/06-quy-dau-tu/)

Bề mặt mới của **finlens 1.4.0**: 188 quỹ Việt Nam, và phép **tra ngược** cổ
phiếu ↔ tổ chức mà bốn nhóm dữ liệu cũ không có.

| Notebook | Nội dung |
|---|---|
| [`61_quy_dau_tu`](notebooks/06-quy-dau-tu/61_quy_dau_tu.ipynb) | NAV và hiệu suất so với VNINDEX · danh mục nắm giữ · **`holders()` — mã này quỹ nào nắm** · theo dấu quỹ gom/xả |

Mỗi thư mục có `README.md` riêng liệt kê notebook và các cạm bẫy của nhóm đó.

---

## Năm điều sẽ làm bạn mất tiền nếu bỏ qua

Mỗi điều dưới đây được **đo bằng số trong notebook**, không phải kể lại.

### 1. Đơn vị sai âm thầm — không exception nào

Giá cổ phiếu tính bằng **nghìn VND** (`23.17` = 23.170 đ), giá chứng quyền bằng
**VND thô**, giá phái sinh bằng **điểm chỉ số**. Đọc
`df.attrs["finlens"]["units"]` thay vì đoán — và nhớ rằng **`attrs` không sống
sót qua `pd.concat` hay `merge`**.

Đo được: HPG hiện ra `22,1` còn CHPG2525 hiện ra `1.630,0` trong cùng một cột
`close` sau `pd.concat`. Cả hai đều là số hợp lệ.
→ [`43_chung_quyen`](notebooks/04-intraday-phai-sinh-vi-mo/43_chung_quyen.ipynb)

### 2. Chỉ báo kỹ thuật trên frame nhiều mã

`talib.RSI(df["close"])` trên frame nhiều mã lấy 13 giá cuối của mã trước để tính
cửa sổ đầu của mã sau. Đo trên frame HPG+VCB 500 dòng: **mã đầu đúng hoàn toàn,
mã thứ hai sai 174/250 dòng**, lệch tới 18 điểm RSI — và mọi giá trị sai đều nằm
trong khoảng 0–100 hợp lệ nên không phép kiểm tự động nào bắt được.

Dùng `df.finlens.rsi(14)`; nó tự tách nhóm.
→ [`31_chi_bao_ky_thuat`](notebooks/03-phan-tich-ky-thuat/31_chi_bao_ky_thuat.ipynb)

### 3. Kỳ của chỉ số tài chính khác nhau theo loại hình doanh nghiệp

Trong `period="quarterly"`: `pe`/`eps` luôn là **4 quý gần nhất**, còn `roe`/`roa`
thì **tuỳ loại hình** — `CT` phi tài chính cho giá trị **riêng quý đó**
(Q4 ÷ năm ≈ 0,27), `NH`/`CK`/`BH` cho giá trị **đã quy về năm** (≈ 1,00).

Hệ quả: screener xếp hạng ROE quý đặt *mọi* ngân hàng lên trên *mọi* doanh nghiệp
thường. VCB hiện 18,0%, FPT hiện 6,3% — trong khi ROE **năm** của FPT là 21,4%.
**Dùng `period="annual"` khi so cắt ngang.**
→ [`22_chi_so_va_dupont`](notebooks/02-phan-tich-co-ban/22_chi_so_va_dupont.ipynb)

### 4. Bốn nhóm nhà đầu tư chi tiết cộng lại bằng 0

Mua ròng của nhóm này chính là bán ròng của nhóm kia, nên cộng chúng với nhóm
`foreign` là đếm hai lần. Đo trên 114 phiên HPG: tổng bốn nhóm lệch tối đa
**2 VND**.
→ [`13_dong_tien_nha_dau_tu`](notebooks/01-thi-truong-va-dong-tien/13_dong_tien_nha_dau_tu.ipynb)

### 5. Backtest không đo giả định của chính nó

Cùng một chiến lược đà tăng cho **CAGR −5,70%** khi đo đúng và **+3,04%** khi mắc
ba lỗi phổ biến: nhìn trước ở bộ lọc vũ trụ, khớp lệnh cùng phiên tín hiệu, và bỏ
qua chi phí giao dịch. Khoảng cách 8,7 điểm phần trăm đó là **phương pháp**,
không phải chiến lược.
→ [`34_backtest_chien_luoc`](notebooks/03-phan-tich-ky-thuat/34_backtest_chien_luoc.ipynb)

---

## Cấu trúc dự án

```
finlens_examples/            hàm dùng chung, không chứa tri thức nghiệp vụ
├── charts.py                theme Plotly + 6 hàm vẽ, bảng màu đã qua validator
├── dinh_dang.py             đọc df.attrs → nhãn đơn vị; VND → tỷ đồng
├── phien.py                 mốc thời gian lấy từ đồng hồ server, không từ máy bạn
└── vu_tru.py                dựng universe mã + lọc thanh khoản
notebooks/
├── 00-bat-dau/              1 notebook
├── 01-thi-truong-va-dong-tien/   4 notebook
├── 02-phan-tich-co-ban/          4 notebook
├── 03-phan-tich-ky-thuat/        4 notebook
└── 04-intraday-phai-sinh-vi-mo/  4 notebook
output/                      file notebook sinh ra (đã .gitignore)
```

Thêm notebook mới: đặt vào đúng thư mục chủ đề, đánh số tiếp theo trong nhóm
(`15_`, `25_`, `35_`, `45_`), và thêm một dòng vào README của thư mục đó.

### Màu trong biểu đồ

Quy ước thị trường Việt Nam là xanh tăng / đỏ giảm, nhưng cặp xanh lá `#0ca30c`
với đỏ `#d03b3b` chỉ cách nhau **ΔE 4,1** dưới mắt người mù màu deutan — khoảng
8% nam giới nhìn hai cột thấy gần như một màu. Bảng màu ở `charts.py` dùng aqua
`#1baf7a` thay cho xanh lá: vẫn đọc là "xanh tăng", nhưng **ΔE 9,9**, vượt ngưỡng
8. Đây là kết quả chạy validator, không phải cảm nhận bằng mắt.

Aqua có tương phản 2,74:1 trên nền sáng, dưới ngưỡng 3:1 — nên mọi hàm vẽ ở đây
**luôn in con số cạnh mảng màu**. Màu là kênh phụ; số mới là kênh chính.

---

## Câu hỏi thường gặp

### finlens khác gì các thư viện dữ liệu chứng khoán Việt Nam khác?

Trả về `pandas.DataFrame` trần thay vì wrapper; **nhiều mã trong một request HTTP**
(50 mã = 1 lời gọi, không phải 50); **đơn vị được khai báo** trong
`df.attrs["finlens"]["units"]` thay vì để bạn đoán; và **135 hàm TA-Lib tự tách
theo mã** ở tầng `df.finlens.*`.

### Cần trả phí không? Gói miễn phí lấy được gì?

Cần tài khoản tại [finlens.vn](https://finlens.vn). Hạn mức của gói bạn nằm ở
`client.whoami()["limits"]`. Repo này kiểm chứng trên gói **premium**: 50.000
request/ngày · 100 mã/request · tối đa 100.000 dòng mỗi response · tối đa 10 ngày
intraday mỗi lời gọi · lịch sử không giới hạn.

### Lấy được dữ liệu từ năm nào?

Giá cuối ngày cổ phiếu từ **2007**, chỉ số ngành ICB từ **2000**, khối ngoại từ
**2010**, báo cáo tài chính từ **2004**, tick trong phiên từ **2022**. Nhóm nhà
đầu tư chi tiết (cá nhân/tổ chức × trong nước/nước ngoài) từ **2024** và **chỉ có
ở HOSE**.

### Chạy notebook trong VS Code được không?

Được, và đó là cách tiện nhất. Cài
[extension FinLens](https://marketplace.visualstudio.com/items?itemName=FinLens.finlens),
chạy `FinLens: Đăng nhập` → `FinLens: Tạo API key` →
`FinLens: Ghi API key ra file cấu hình`. Bước cuối là **bắt buộc**: kernel Jupyter
không đọc được VS Code SecretStorage.

### Sau khi ghi API key ra file cấu hình có phải khởi động lại kernel không?

**Không.** `finlens.client()` gọi hàm phân giải cấu hình ở *mỗi lần gọi*, không
phải lúc `import finlens`. Chạy lại cell là đủ.

### `finlens.client()` báo lỗi thiếu khoá thì kiểm ở đâu?

Thông báo lỗi nói rõ nó đã tìm ở đâu và **file nào che file nào**. Nguyên nhân
phổ biến nhất: một `./finlens.toml` trong thư mục làm việc che mất file cấu hình
máy. Trong VS Code, chạy `FinLens: Kiểm tra cấu hình` để chẩn đoán.

### Vì sao chỉ số HNX gọi là `HNXINDEX` chứ không phải `HNX-INDEX`?

Vì đó là mã API thật. Năm chỉ số hợp lệ là `VNINDEX`, `VN30`, `HNXINDEX`,
`HNX30`, `UPINDEX`. Các biến thể có gạch nối trả về `InvalidSymbolError`.

### Notebook có chạy lại được không, hay chỉ để đọc?

Chạy lại được toàn bộ. Không cell nào cần sửa tay: ngày tháng suy từ
`client.whoami()["server_time"]`, mã chứng khoán lấy từ `client.meta.symbols()`,
kỳ báo cáo hỏi từ dữ liệu. Notebook không chết vào tháng sau.

### Backtest trong repo này có phải chiến lược sinh lời không?

**Không, và đó là chủ ý.** Chiến lược đà tăng ở
[`34_backtest_chien_luoc`](notebooks/03-phan-tich-ky-thuat/34_backtest_chien_luoc.ipynb)
cho CAGR −5,70% khi đo đúng. Notebook giữ nguyên kết quả thua để chỉ ra rằng ba
lỗi phương pháp phổ biến biến chính chiến lược đó thành +3,04%. Bộ khung đo lường
mới là thứ đáng mang đi.

### Repo này dùng thư viện vẽ biểu đồ nào?

**Plotly** — biểu đồ tương tác, zoom và hover ngay trong notebook. Theme và bảng
màu dùng chung nằm ở `finlens_examples/charts.py`.

### Làm sao biết quỹ nào đang nắm một mã cổ phiếu?

`client.funds.holders("HPG")` trả về danh sách quỹ đang nắm mã đó, kèm tỷ trọng
trong danh mục và số lượng cổ phiếu. Đây là bề mặt mới của `finlens 1.4.0`.

⚠️ Cột `date` của kết quả là kỳ công bố **của riêng từng quỹ**, không phải một kỳ
chung — trong một lời gọi có thể có nhiều kỳ cách nhau nhiều năm. Lọc theo tuổi
vị thế trước khi cộng; xem
[`61_quy_dau_tu`](notebooks/06-quy-dau-tu/61_quy_dau_tu.ipynb).

### Có ví dụ cho trái phiếu doanh nghiệp không?

Chưa, nhưng dữ liệu đã có. `client.bonds.*` phát hành ở `finlens 1.4.0` với
`bonds.list()` và `bonds.issuers()`. Hai bề mặt mới khác cũng chưa có notebook:
`client.financials.notes()` (thuyết minh BCTC tổ chức tín dụng) và năm cột mới
của `meta.warrants()`.

---

## Phiên bản kiểm chứng

| Thành phần | Phiên bản |
|---|---|
| `finlens` | 1.4.0 |
| `pandas` | 3.0.5 |
| `plotly` | 6.x |
| Python | 3.12 (thư viện yêu cầu 3.11+) |
| Extension VS Code | `FinLens.finlens` 0.2.7 |

Toàn bộ notebook đã chạy sạch từ đầu tới cuối bằng
`jupyter nbconvert --to notebook --execute`, 0 lỗi.

---

## Tài nguyên

- **Thư viện Python**: [pypi.org/project/finlens](https://pypi.org/project/finlens/)
- **Tài liệu**: [docs.finlens.vn/python-sdk](https://docs.finlens.vn/python-sdk)
- **Extension VS Code**: [marketplace.visualstudio.com](https://marketplace.visualstudio.com/items?itemName=FinLens.finlens)
- **Trang chủ**: [finlens.vn](https://finlens.vn)

---

<!--
Từ khoá: dữ liệu chứng khoán Việt Nam Python, thư viện Python chứng khoán Việt
Nam, API chứng khoán Việt Nam, finlens, finlens python, hướng dẫn finlens, ví dụ
finlens, notebook chứng khoán Việt Nam, phân tích chứng khoán bằng Python, lấy dữ
liệu VNINDEX Python, giá cổ phiếu lịch sử HOSE HNX UPCOM, dữ liệu intraday tick
by tick Việt Nam, khớp lệnh từng lệnh, khối ngoại mua ròng, tự doanh, dòng tiền
nhà đầu tư, báo cáo tài chính doanh nghiệp niêm yết, chỉ số tài chính ROE ROA P/E
P/B, phân tích DuPont, screener cổ phiếu Python, screener định giá, ngành ICB,
chứng quyền có bảo đảm CW, phái sinh VN30F1M, basis phái sinh, chỉ báo kỹ thuật
TA-Lib Python, RSI MACD Bollinger Bands, mẫu hình nến, backtest chiến lược chứng
khoán, look-ahead bias, dữ liệu vĩ mô Việt Nam, CPI GDP tỷ giá lãi suất, nghiệp
vụ thị trường mở OMO, xuất nhập khẩu, pandas DataFrame, Jupyter notebook, Plotly,
VS Code extension chứng khoán, API key finlens.

Keywords: Vietnam stock market data Python library, Vietnamese stocks API,
finlens python examples, finlens tutorial, HOSE HNX UPCOM historical data,
VNINDEX historical data Python, intraday tick data Vietnam, foreign investor
flows Vietnam, Vietnamese financial statements API, financial ratios ROE ROA PE
PB, DuPont analysis Python, stock screener Python, ICB sector classification,
covered warrants Vietnam, VN30F1M futures basis, TA-Lib technical indicators
pandas, candlestick patterns, backtesting framework look-ahead bias, Vietnam
macroeconomic data, CPI GDP FX interest rates, open market operations, pandas
DataFrame, Jupyter notebooks, Plotly charts, VS Code extension API key setup.
-->

**Giấy phép**: MIT
