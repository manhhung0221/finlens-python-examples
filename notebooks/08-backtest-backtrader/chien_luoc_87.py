"""Chiến lược đi kèm notebook ``87_toi_uu_va_walk_forward.ipynb``.

Vì sao nằm trong file ``.py`` mà không nằm trong notebook: ``cerebro.run(maxcpus>1)``
dùng ``multiprocessing``, và trên Windows tiến trình con được **spawn** — một
Python mới tinh, chỉ nhận lớp strategy dưới dạng *tên* đã pickle
(``__main__.GiaoCatSMA``). Lớp định nghĩa trong một cell không tồn tại ở
``__main__`` của tiến trình con, nên mọi worker chết lúc unpickle và pool đẻ
worker mới mãi mãi — notebook treo, không báo lỗi. Đặt lớp vào một module có
tên thì tiến trình con chỉ việc ``import chien_luoc_87``.
"""

from __future__ import annotations

import backtrader as bt

from finlens_examples.bt_vn import lam_tron_lo


class GiaoCatSMA(bt.Strategy):
    """Rổ nhiều mã, mỗi mã giữ khi SMA nhanh nằm trên SMA chậm, đứng ngoài khi ngược lại.

    Mỗi mã được cấp một suất cố định ``ty_le / số mã`` giá trị danh mục lúc vào
    lệnh, làm tròn xuống lô 100. Luật theo **trạng thái** (nhanh > chậm) chứ không
    theo sự kiện giao cắt, nên mã niêm yết muộn tự vào cuộc khi đủ dữ liệu.
    """

    params = (("nhanh", 10), ("cham", 50), ("ty_le", 0.95), ("lo", 100))

    def __init__(self) -> None:
        self.tren = {
            d: bt.ind.SMA(d.close, period=self.p.nhanh) > bt.ind.SMA(d.close, period=self.p.cham)
            for d in self.datas
        }

    def prenext(self) -> None:
        # Mã niêm yết muộn giữ cả chiến lược ở prenext — vẫn phải giao dịch các mã đã đủ dữ liệu.
        self.next()

    def next(self) -> None:
        suat = self.broker.getvalue() * self.p.ty_le / len(self.datas)
        for d in self.datas:
            if len(d) < self.p.cham:
                continue
            dang_giu = self.getposition(d).size
            if self.tren[d][0] and not dang_giu:
                sl = lam_tron_lo(suat / d.close[0], self.p.lo)
                if sl > 0:
                    self.buy(data=d, size=sl)
            elif not self.tren[d][0] and dang_giu:
                self.close(data=d)
