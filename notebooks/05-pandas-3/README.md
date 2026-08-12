# Track 5 — pandas 3.0 từ cơ bản tới nâng cao

Chuỗi bài dạy **pandas 3.0** qua dữ liệu chứng khoán Việt Nam thật. Không có
`pd.DataFrame({"a": [1, 2, 3]})` — mọi ví dụ chạy trên frame lấy từ `finlens`,
nên bạn học pandas và học dữ liệu thị trường cùng lúc.

## Vì sao chuỗi này tồn tại

pandas 3.0 **xoá thật** nhiều thứ, và mã pandas 2.x chạy vào là gãy — hoặc tệ
hơn, **im lặng không làm gì**. Đo trên `pandas 3.0.5`:

```python
df['a'][0] = 100        # giá trị KHÔNG đổi, chỉ có ChainedAssignmentError
df[mask]['a'] = 100     # KHÔNG cảnh báo, và cũng không ghi vào frame gốc
applymap(...)           # AttributeError — đã xoá
fillna(method='ffill')  # TypeError — đã xoá
DataFrame.append(...)   # AttributeError — đã xoá
freq='M' / 'Q' / 'A'    # ValueError — dùng 'ME' / 'QE' / 'YE'
pd.Series(['HPG']).dtype  # 'str', không còn 'object'
```

Hai dòng đầu nguy hiểm nhất: chúng từng là code đúng.

## Nhóm cơ bản — nền tảng

| Notebook | Nội dung |
|---|---|
| [`51_cau_truc_va_dtype.ipynb`](51_cau_truc_va_dtype.ipynb) | Series · DataFrame · Index · **`str` thay `object`** · hai kiểu chuỗi `str` và `string` · `pd.NA` so với `np.nan` và logic ba giá trị · đo bộ nhớ |
| [`52_chon_loc_va_cow.ipynb`](52_chon_loc_va_cow.ipynb) | `[]` · `.loc` · `.iloc` · boolean mask · `query()` · ⚠️ **Copy-on-Write** — ba tình huống, một trong ba không có cảnh báo nào |
| [`53_bien_doi_cot.ipynb`](53_bien_doi_cot.ipynb) | `assign` nối chuỗi · **năm cách tính một cột, đo tốc độ cả năm** · `np.where`/`np.select`/`pd.cut` · `.str` · `applymap` đã bị xoá |
| [`54_mini_project_chuan_bi_du_lieu.ipynb`](54_mini_project_chuan_bi_du_lieu.ipynb) | **Sản phẩm** — ghép cả ba thành một hàm `chuan_bi_du_lieu()` dán được vào dự án: kiểm chất lượng, tối ưu kiểu, thêm cột phái sinh, lưu và nạp lại |

## Nhóm trung cấp — thứ dùng hằng ngày

| Notebook | Nội dung |
|---|---|
| [`55_groupby.ipynb`](55_groupby.ipynb) | `agg`/`transform`/`filter`/`apply` · ⚠️ **`observed=` đổi mặc định thành `True`** · bẫy ranh giới nhóm · `category` làm groupby nhanh gấp 2,8 lần |
| [`56_reshape_long_wide.ipynb`](56_reshape_long_wide.ipynb) | `pivot`/`pivot_table`/`melt`/`stack`/`unstack` · ⚠️ **`stack()` giờ GIỮ `NaN`** · ma trận tương quan · backtest vectorised |
| [`57_ghep_du_lieu.ipynb`](57_ghep_du_lieu.ipynb) | Bốn kiểu join · ⚠️ **`validate=`** · `indicator=` · `merge_asof` cho tick · `attrs` sau `concat` |
| [`58_time_series.ipynb`](58_time_series.ipynb) | ⚠️ **Bảy mã tần suất bị xoá** · `resample` với `label`/`closed` · `rolling(closed="left")` · múi giờ |

## Nhóm nâng cao — sắp có

| Notebook | Nội dung dự kiến |
|---|---|
| `59_di_tru_va_hieu_nang` | Bảng đầy đủ những gì bị xoá · `Pandas4Warning` · bật deprecation thành lỗi trong test · `category` so với `str` · backend pyarrow |

## Năm con số đáng nhớ từ nhóm cơ bản

- **`apply(axis=1)` chậm hàng trăm lần** so với vectorised trên cùng phép tính và
  cùng kết quả. Notebook `53` đo cả năm cách trên một frame gần 30.000 dòng.
- **Cột `symbol` dạng `category` nhẹ hơn `str` hàng chục lần** — vài trăm giá trị
  khác nhau lặp lại hàng trăm nghìn lần, đúng hình dạng `category` sinh ra để xử lý.
- **`pd.options.mode.copy_on_write = False` vẫn nhận giá trị nhưng vô hiệu.** Code
  cũ đặt dòng đó để giữ hành vi pandas 2.x sẽ chạy trơn tru và không đạt được gì.
- **Quên `groupby("symbol")` khi tính `pct_change` cho ra lợi suất bịa tới
  2.881%** trên 198/199 mã — notebook `54` khẳng định điều đó bằng `assert`.
- **CSV quên hết kiểu dữ liệu**: frame phình từ 13,3 MB lên 31,3 MB khi nạp lại,
  `date` thành chuỗi, và `category` có thứ tự mất thứ tự.

## Bốn thay đổi phá vỡ tương thích, đo trong nhóm trung cấp

- **`groupby` trên `category` đổi mặc định thành `observed=True`.** Báo cáo cần
  đủ mọi hạng mục — kể cả ngành hôm nay không mã nào giao dịch — sẽ **âm thầm
  mất dòng**. Luôn viết rõ `observed=`.
- **`stack()` giờ GIỮ ô `NaN`**, ngược hẳn pandas 2.x, và tham số `dropna` bị xoá
  hẳn (`ValueError` nếu truyền). Đo trên bảng 499×119: `stack()` cho **59.381**
  dòng thay vì **58.468**. Muốn hành vi cũ thì viết `.stack().dropna()`.
- **Bảy mã tần suất bị xoá**: `M` `Q` `A` `Y` `H` `T` `S` → `ME` `QE` `YE` `YE`
  `h` `min` `s`. `resample("M")` ném `ValueError` ngay dòng đầu.
- **`pivot` chỉ nhận tham số bằng từ khoá.** Cú pháp vị trí ném `TypeError`.

## Hai thứ không đổi nhưng vẫn cắn

- **`rolling(20).max()` gồm cả dòng hiện tại**, nên điều kiện "vượt đỉnh 20
  phiên" cho **0 tín hiệu** thay vì 69. Cần `closed="left"`.
- **`merge_asof` từ chối ghép hai kiểu chuỗi khác nhau** — `assign(symbol="HPG")`
  ra kiểu `str`, cột từ finlens là `string`. `merge` thường thì tự ép và chạy
  tiếp, nên bạn có thể đã ghép sai nhiều lần mà không biết.

← [Track 4](../04-intraday-phai-sinh-vi-mo/) · [Về mục lục chính](../../README.md)
