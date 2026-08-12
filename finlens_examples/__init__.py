"""Hàm dùng chung cho các notebook example của finlens.

Notebook nên gọn: phần đáng đọc là *cách dùng dữ liệu*, không phải bốn mươi dòng
định dạng trục biểu đồ lặp lại ở mười bảy chỗ. Mọi thứ ở đây là tiện ích thuần —
không có tri thức nghiệp vụ nào bị giấu, mỗi notebook vẫn tự gọi finlens.
"""

from __future__ import annotations

from finlens_examples.charts import (
    ap_dung_theme,
    bar_ngang,
    duong,
    heatmap,
    nen,
    thanh_doi_mau,
)
from finlens_examples.dinh_dang import (
    doc_don_vi,
    nhan_don_vi,
    ty_dong,
    dinh_dang_bang,
)
from finlens_examples.phien import (
    hom_nay,
    lui_ngay,
    ngay_giao_dich_gan_nhat,
)
from finlens_examples.vu_tru import (
    lay_client,
    universe_hose,
    loc_thanh_khoan,
)

__all__ = [
    "ap_dung_theme",
    "bar_ngang",
    "dinh_dang_bang",
    "doc_don_vi",
    "duong",
    "heatmap",
    "hom_nay",
    "lay_client",
    "loc_thanh_khoan",
    "lui_ngay",
    "nen",
    "ngay_giao_dich_gan_nhat",
    "nhan_don_vi",
    "thanh_doi_mau",
    "ty_dong",
    "universe_hose",
]
