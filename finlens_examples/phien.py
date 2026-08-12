"""Mốc thời gian suy từ đồng hồ của server, không phải đồng hồ máy bạn.

Lý do có module này: notebook viết `start="2026-01-01"` sẽ chết dần theo thời
gian, còn `datetime.now()` trên máy đặt sai múi giờ cho ra một ngày lệch. FinLens
trả `server_time` kèm offset +07 trong `whoami()` — đó là mốc đúng.
"""

from __future__ import annotations

import datetime as _dt

import pandas as pd


def hom_nay(client) -> _dt.date:
    """Ngày hiện tại theo đồng hồ server FinLens (múi giờ +07).

    Tốn đúng một request. Gọi một lần ở đầu notebook rồi truyền xuống.
    """
    return _dt.datetime.fromisoformat(client.whoami()["server_time"]).date()


def lui_ngay(moc: _dt.date, *, nam: float = 0, thang: int = 0, ngay: int = 0) -> str:
    """Lùi `moc` về quá khứ, trả về chuỗi ``YYYY-MM-DD`` để truyền vào ``start=``.

    ``nam`` nhận số thực (``0.5`` = sáu tháng). Phép lùi tính bằng ngày lịch chứ
    không phải phiên giao dịch — dùng để mở rộng cửa sổ tải, không dùng để đếm.
    """
    tong_ngay = int(round(nam * 365.25)) + thang * 30 + ngay
    return (moc - _dt.timedelta(days=tong_ngay)).isoformat()


def ngay_giao_dich_gan_nhat(df: pd.DataFrame, cot: str = "date") -> pd.Timestamp:
    """Phiên gần nhất *thực sự có trong dữ liệu*.

    Không dùng ``hom_nay()`` cho việc này: thứ Bảy, ngày lễ, hay một phiên chưa
    kịp về đều làm lệch. Hỏi chính cái frame vừa tải.
    """
    if df.empty:
        raise ValueError("Frame rỗng — không có phiên nào để lấy.")
    return pd.Timestamp(df[cot].max())
