"""Dựng "vũ trụ" mã để quét — và cắt nó xuống phần thực sự giao dịch được.

Quét 1.645 mã rồi xếp hạng theo tín hiệu cho ra một danh sách đứng đầu bởi những
mã UPCOM khớp vài trăm cổ phiếu một phiên. Tín hiệu ở đó là nhiễu chứ không phải
tin tức, nên bộ lọc thanh khoản không phải bước làm đẹp — nó là bước làm cho kết
quả có nghĩa.
"""

from __future__ import annotations

import finlens
import pandas as pd


def lay_client(**kwargs: object):
    """Tạo client FinLens. Không chạm mạng, đặt ở cell đầu notebook được.

    Khoá API tìm theo thứ tự: tham số ``api_key=`` → biến môi trường
    ``FINLENS_API_KEY`` → file cấu hình (``./finlens.toml``,
    ``%APPDATA%\\finlens\\config.toml``, ``~/.config/finlens/config.toml``).
    """
    return finlens.client(**kwargs)  # type: ignore[arg-type]


def universe_hose(
    client,
    *,
    kind: str = "stock",
    icb2: str | None = None,
) -> pd.DataFrame:
    """Danh mục mã HOSE kèm ngành ICB, đã bỏ chứng chỉ quỹ.

    ``kind="stock"`` loại 24 chứng chỉ quỹ niêm yết ra — quỹ không có báo cáo tài
    chính doanh nghiệp nên mọi screener cơ bản đều vấp ở đó.
    """
    df = client.meta.symbols(exchange="HOSE", kind=kind)
    if icb2 is not None:
        df = df[df["icb_level2"] == icb2]
    return df.reset_index(drop=True)


def loc_thanh_khoan(
    client,
    ma: list[str],
    *,
    start: str,
    end: str | None = None,
    gtgd_toi_thieu: float = 5e9,
) -> pd.DataFrame:
    """Giữ lại các mã có giá trị giao dịch trung bình ≥ ngưỡng.

    Giá trị giao dịch xấp xỉ bằng ``close × volume × 1.000`` — nhân 1.000 vì giá
    cổ phiếu tính bằng **nghìn VND** còn khối lượng tính bằng cổ phiếu. Bỏ số
    1.000 đó thì ngưỡng của bạn lệch đúng ba chữ số và bộ lọc không loại ai cả.

    Trả về frame ``symbol · gtgd_binh_quan · so_phien`` đã sắp giảm dần.
    """
    ohlcv = client.eod.stock.ohlcv(ma, start=start, end=end)
    if ohlcv.empty:
        return pd.DataFrame(columns=["symbol", "gtgd_binh_quan", "so_phien"])

    ohlcv = ohlcv.assign(gtgd=ohlcv["close"] * ohlcv["volume"] * 1_000)
    tom_tat = (
        ohlcv.groupby("symbol", observed=True)
        .agg(gtgd_binh_quan=("gtgd", "mean"), so_phien=("date", "count"))
        .reset_index()
    )
    return (
        tom_tat[tom_tat["gtgd_binh_quan"] >= gtgd_toi_thieu]
        .sort_values("gtgd_binh_quan", ascending=False)
        .reset_index(drop=True)
    )
