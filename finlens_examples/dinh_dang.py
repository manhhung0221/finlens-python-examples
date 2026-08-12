"""Định dạng số và đọc đơn vị ra nhãn người đọc hiểu được.

Đơn vị là nguồn lỗi số một khi làm việc với dữ liệu chứng khoán Việt Nam và nó
sai *âm thầm*. Mọi hàm ở đây đọc `df.attrs["finlens"]["units"]` chứ không đoán.
"""

from __future__ import annotations

import pandas as pd

# Nhãn tiếng Việt cho từng mã đơn vị FinLens phát ra.
_NHAN: dict[str, str] = {
    "kVND": "nghìn VND",
    "VND": "VND",
    "share": "cổ phiếu",
    "contract": "hợp đồng",
    "index_point": "điểm chỉ số",
    "pct": "%",
    "VND/share": "VND/cổ phiếu",
    "x": "lần",
    "USD": "USD",
}


def doc_don_vi(df: pd.DataFrame, cot: str) -> str | None:
    """Đơn vị FinLens khai cho một cột, hoặc ``None`` nếu cột không mang đơn vị.

    ⚠️ ``DataFrame.attrs`` **không sống sót** qua ``pd.concat`` hay ``merge``.
    Gọi hàm này *trước* khi ghép frame, rồi giữ kết quả trong một biến.
    """
    meta = df.attrs.get("finlens") or {}
    return (meta.get("units") or {}).get(cot)


def nhan_don_vi(df: pd.DataFrame, cot: str) -> str:
    """Nhãn tiếng Việt để gắn lên trục biểu đồ. Rỗng nếu cột không có đơn vị."""
    ma = doc_don_vi(df, cot)
    if ma is None:
        return ""
    return _NHAN.get(ma, ma)


def ty_dong(gia_tri: float | pd.Series, *, chu_so: int = 1) -> str | pd.Series:
    """Đổi VND sang tỷ đồng để in ra cho người đọc.

    Cột tiền của FinLens tính bằng VND trần, nên ``5.66e10`` xuất hiện khắp nơi.
    Con số đó không đọc được bằng mắt; ``-56,6`` tỷ thì đọc được.
    """
    if isinstance(gia_tri, pd.Series):
        return (gia_tri / 1e9).round(chu_so)
    return f"{gia_tri / 1e9:,.{chu_so}f}"


def dinh_dang_bang(
    df: pd.DataFrame,
    *,
    tien: tuple[str, ...] = (),
    phan_tram: tuple[str, ...] = (),
    chu_so: int = 2,
) -> pd.io.formats.style.Styler:
    """Tô màu và định dạng một bảng nhỏ để trình bày trong notebook.

    ``tien`` là các cột VND sẽ được đổi sang tỷ đồng; ``phan_tram`` là các cột
    thang 0–100 sẽ có dấu ``%``. Cột số âm tô đỏ, dương tô xanh.
    """
    ban_sao = df.copy()
    for cot in tien:
        if cot in ban_sao.columns:
            ban_sao[cot] = ban_sao[cot] / 1e9

    dinh_dang: dict[str, str] = {}
    for cot in ban_sao.columns:
        if cot in phan_tram:
            dinh_dang[cot] = "{:,.2f}%"
        elif pd.api.types.is_numeric_dtype(ban_sao[cot]):
            dinh_dang[cot] = f"{{:,.{chu_so}f}}"

    def _mau(v: object) -> str:
        if isinstance(v, (int, float)) and not pd.isna(v):
            if v < 0:
                return "color: #d62728"
            if v > 0:
                return "color: #2ca02c"
        return ""

    cot_so = [c for c in ban_sao.columns if pd.api.types.is_numeric_dtype(ban_sao[c])]
    return ban_sao.style.format(dinh_dang, na_rep="—").map(_mau, subset=cot_so)
