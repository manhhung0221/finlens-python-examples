"""Cầu nối finlens → backtrader, kèm luật chơi của thị trường Việt Nam.

Track 8 dạy từng mảnh ở đây bằng tay trước (``81``–``83``), rồi các notebook sau
import lại từ module này. Không có gì bị giấu: mỗi lớp/hàm chỉ là thứ notebook
đã dựng và đo.

Quy ước đơn vị **bên trong backtrader là VND**. Giá cổ phiếu finlens tính bằng
nghìn VND nên được nhân 1.000 ngay ở bước tạo feed; vốn, phí và thuế khi đó đọc
thẳng ra đồng. Giá phái sinh (điểm chỉ số) giữ nguyên — hệ số nhân nằm ở
``PhiPhaiSinhVN``.
"""

from __future__ import annotations

import datetime as _dt
import math
import warnings
from collections import defaultdict, deque

import backtrader as bt
import numpy as np
import pandas as pd

# ── Đơn vị ──────────────────────────────────────────────────────────────────

_HE_SO_VE_VND: dict[str, float] = {"kVND": 1_000.0, "VND": 1.0}
_DON_VI_GIA_HOP_LE = frozenset({"kVND", "VND", "index_point"})
_COT_GIA = ("open", "high", "low", "close")

# ── Biên độ và bước giá theo sàn ────────────────────────────────────────────

BIEN_DO: dict[str, float] = {"HOSE": 0.07, "HNX": 0.10, "UPCOM": 0.15}
"""Biên độ dao động giá trong phiên so với giá tham chiếu (phiên thường)."""

LO_CHAN = 100
"""Lô giao dịch tối thiểu của phương thức khớp lệnh thường, cả ba sàn."""


def buoc_gia(gia: float, san: str = "HOSE") -> float:
    """Bước giá (VND) tại mức ``gia`` (VND).

    HOSE chia ba bậc 10 / 50 / 100 đồng theo ngưỡng 10.000 và 50.000; HNX và
    UPCOM dùng một bước 100 đồng cho cổ phiếu.
    """
    if san == "HOSE":
        if gia < 10_000:
            return 10.0
        if gia < 50_000:
            return 50.0
        return 100.0
    return 100.0


def tran_san(tham_chieu: float, san: str = "HOSE") -> tuple[float, float]:
    """Giá trần và giá sàn (VND) từ giá tham chiếu (VND).

    Trần làm tròn **xuống**, sàn làm tròn **lên** theo bước giá — vì giá đặt
    phải nằm *trong* biên độ. Chỉ đúng trên **giá thô**: giá điều chỉnh quyền
    làm lệch tham chiếu ở mọi phiên trước ngày GDKHQ.
    """
    bd = BIEN_DO[san]
    tran = tham_chieu * (1 + bd)
    san_ = tham_chieu * (1 - bd)
    b_tran = buoc_gia(tran, san)
    b_san = buoc_gia(san_, san)
    return math.floor(tran / b_tran + 1e-9) * b_tran, math.ceil(san_ / b_san - 1e-9) * b_san


def lam_tron_lo(so_cp: float, lo: int = LO_CHAN) -> int:
    """Làm tròn **xuống** về bội số của lô (giữ dấu)."""
    dau = -1 if so_cp < 0 else 1
    return dau * int(abs(so_cp) // lo) * lo


# ── Chuẩn bị frame ──────────────────────────────────────────────────────────


def bo_phien_chua_dong(
    df: pd.DataFrame,
    client,
    *,
    cot: str = "date",
    gio_dong: _dt.time = _dt.time(15, 0),
) -> pd.DataFrame:
    """Bỏ thanh của phiên **đang chạy**.

    Gọi finlens trong giờ giao dịch trả về cả thanh của hôm nay với khối lượng
    mới khớp được một phần. Backtest trên thanh đó là backtest trên một giá
    đóng cửa chưa tồn tại. Mốc "hôm nay" và "đã đóng cửa chưa" lấy từ đồng hồ
    server (+07), không phải đồng hồ máy bạn.
    """
    if df.empty:
        return df
    bay_gio = _dt.datetime.fromisoformat(client.whoami()["server_time"])
    if bay_gio.time() >= gio_dong:
        return df
    ngay = pd.to_datetime(df[cot])
    if ngay.dt.tz is not None:
        ngay = ngay.dt.tz_convert("Asia/Ho_Chi_Minh").dt.tz_localize(None)
    return df[ngay.dt.normalize() < pd.Timestamp(bay_gio.date())]


def chuan_bi_frame(
    df: pd.DataFrame,
    *,
    ma: str | None = None,
    don_vi_gia: str | None = None,
    cot_phu: tuple[str, ...] = (),
    don_vi_cot_phu: dict[str, str | None] | None = None,
) -> pd.DataFrame:
    """Frame finlens (dạng long) → frame một mã, index thời gian naive, giá VND.

    Đơn vị đọc từ ``df.attrs["finlens"]["units"]``. Nếu frame đã mất ``attrs``
    (sau ``pd.concat``/``merge``) thì **bắt buộc** truyền ``don_vi_gia`` — hàm
    từ chối đoán, vì đoán sai là lệch 1.000 lần mà không có lỗi nào. Đơn vị lạ
    (kể cả gõ sai hoa thường như ``"kvnd"``) cũng bị từ chối, cùng lý do.

    Line phụ mang đơn vị giá (``sma_20``, ``ema_12``… của ``df.finlens`` là
    kVND) được quy về VND như OHLC — không thì so ``close`` (VND) với ``sma_20``
    (kVND) cho "giá trên SMA" ở mọi phiên. Đơn vị của từng line phụ đọc từ
    ``attrs``; ``don_vi_cot_phu`` ghi đè (``None`` = không quy đổi). Cột không
    khai đơn vị nào được giữ nguyên.

    Cột thời gian ``date`` (EOD, naive) hoặc ``time`` (intraday, ``+07:00``):
    ``time`` được đổi về giờ Việt Nam rồi mới bỏ múi giờ, để thanh 09:15 vẫn là
    09:15 chứ không thành 02:15 UTC.
    """
    don_vi_attrs = ((df.attrs.get("finlens") or {}).get("units")) or {}
    if don_vi_gia is None:
        don_vi_gia = don_vi_attrs.get("close")
        if don_vi_gia is None:
            raise ValueError(
                "Frame không còn df.attrs['finlens'] (thường do pd.concat/merge). "
                "Truyền don_vi_gia='kVND' | 'VND' | 'index_point' cho rõ."
            )
    if don_vi_gia not in _DON_VI_GIA_HOP_LE:
        raise ValueError(f"don_vi_gia={don_vi_gia!r} không hợp lệ — chỉ nhận {sorted(_DON_VI_GIA_HOP_LE)}.")

    don_vi_phu = {c: don_vi_attrs.get(c) for c in cot_phu}
    don_vi_phu.update(don_vi_cot_phu or {})
    khong_ro = [c for c in cot_phu if c not in don_vi_attrs and c not in (don_vi_cot_phu or {})]
    if khong_ro and not don_vi_attrs:
        warnings.warn(
            f"Line phụ {khong_ro} không có đơn vị (frame đã mất attrs) nên được giữ nguyên. "
            "Nếu là cột giá kVND, truyền don_vi_cot_phu={cot: 'kVND'}; "
            "nếu không phải cột giá, truyền {cot: None} để tắt cảnh báo này.",
            stacklevel=3,
        )

    if ma is not None:
        df = df[df["symbol"] == ma]
    elif "symbol" in df.columns and df["symbol"].nunique() > 1:
        raise ValueError("Frame có nhiều mã — truyền ma= để chọn một.")

    cot_tg = "time" if "time" in df.columns else "date"
    tg = pd.to_datetime(df[cot_tg])
    if tg.dt.tz is not None:
        tg = tg.dt.tz_convert("Asia/Ho_Chi_Minh").dt.tz_localize(None)

    ra = pd.DataFrame(
        {c: df[c].to_numpy(dtype="float64") for c in (*_COT_GIA, "volume", *cot_phu)},
        index=pd.DatetimeIndex(tg.to_numpy(), name="datetime"),
    ).sort_index()
    ra = ra[~ra.index.duplicated(keep="last")]

    he_so = _HE_SO_VE_VND.get(don_vi_gia, 1.0)  # index_point giữ nguyên
    ra[list(_COT_GIA)] = ra[list(_COT_GIA)] * he_so
    for c, dv in don_vi_phu.items():
        if dv in _HE_SO_VE_VND:
            ra[c] = ra[c] * _HE_SO_VE_VND[dv]
    return ra


# ── Feed ────────────────────────────────────────────────────────────────────


def lop_feed(cot_phu: tuple[str, ...] = ()) -> type[bt.feeds.PandasData]:
    """Lớp ``PandasData`` có thêm line phụ — chỉ báo tính sẵn, dòng tiền, P/E…

    Mỗi tên cột thành một line đọc được bằng ``self.data.<ten>[0]`` trong
    strategy. ``openinterest`` tắt (``-1``) vì cổ phiếu không có.
    """
    if not cot_phu:
        return _FeedGoc
    params = tuple((c, -1) for c in cot_phu) + (("openinterest", None),)
    ten = "FeedFinlens_" + "_".join(cot_phu)
    return type(ten, (bt.feeds.PandasData,), {"lines": tuple(cot_phu), "params": params})


class _FeedGoc(bt.feeds.PandasData):
    params = (("openinterest", None),)


def feed_tu_finlens(
    df: pd.DataFrame,
    *,
    ma: str | None = None,
    don_vi_gia: str | None = None,
    cot_phu: tuple[str, ...] = (),
    don_vi_cot_phu: dict[str, str | None] | None = None,
    **kwargs: object,
) -> bt.feeds.PandasData:
    """Frame finlens → feed backtrader, đã quy giá (và line phụ đơn vị giá) về VND.

    ``ma`` chọn một mã từ frame nhiều mã — mỗi lần gọi lọc lại cả frame, nên
    với hàng trăm mã hãy ``groupby("symbol")`` một lần rồi truyền từng nhóm.
    ``cot_phu`` là các cột thêm vào thành line phụ. ``kwargs`` chuyển thẳng cho
    feed (``name=``, ``fromdate=``…); ``name`` mặc định là mã.
    """
    khung = chuan_bi_frame(
        df, ma=ma, don_vi_gia=don_vi_gia, cot_phu=cot_phu, don_vi_cot_phu=don_vi_cot_phu
    )
    if ma is None and "symbol" in df.columns and len(df):
        ma = str(df["symbol"].iloc[0])
    kwargs.setdefault("name", ma)
    return lop_feed(cot_phu)(dataname=khung, **kwargs)


# ── Phí và thuế ─────────────────────────────────────────────────────────────


class PhiCoPhieuVN(bt.CommInfoBase):
    """Phí môi giới hai chiều + thuế TNCN 0,1% **chỉ ở chiều bán**.

    backtrader mặc định một tỷ lệ cho cả hai chiều; thuế bán ở Việt Nam làm
    vòng mua-bán tốn ``2 × phi + thue_ban`` chứ không phải ``2 × phi``.
    Mức ``phi`` mặc định 0,15% là mức phổ biến của tài khoản bán lẻ — kiểm lại
    biểu phí công ty chứng khoán của bạn.
    """

    params = (
        ("phi", 0.0015),
        ("thue_ban", 0.001),
        ("stocklike", True),
        ("commtype", bt.CommInfoBase.COMM_PERC),
        ("percabs", True),
    )

    def _getcommission(self, size, price, pseudoexec):
        gia_tri = abs(size) * price
        return gia_tri * (self.p.phi + (self.p.thue_ban if size < 0 else 0.0))


class PhiPhaiSinhVN(bt.CommInfoBase):
    """Hợp đồng tương lai chỉ số VN30: hệ số nhân, ký quỹ theo tỷ lệ, phí/HĐ.

    ``mult=100_000`` VND cho mỗi điểm chỉ số. Ký quỹ tính bằng
    ``ty_le_ky_quy × giá × mult`` cho mỗi hợp đồng — tỷ lệ do VSDC công bố và
    thay đổi theo thời kỳ, nên là tham số. ``phi_hd`` là tổng phí mỗi chiều mỗi
    hợp đồng (môi giới + Sở + VSDC), VND — giá trị mặc định chỉ là xấp xỉ.

    ⚠️ Gắn bằng ``gan_phi_phai_sinh(cerebro, ...)`` chứ không bằng
    ``addcommissioninfo`` trần. Ký quỹ ở đây tỷ lệ với giá, nên broker phải
    định giá ký quỹ đang phong toả theo **giá vào lệnh** (``getvalue`` dưới
    đây) và chạy với ``shortcash=False`` — thiếu một trong hai thì giá trị tài
    khoản tính lãi/lỗ chưa chốt của vị thế long ×(1 + ty_le_ky_quy), short
    ×(1 − ty_le_ky_quy). Tiền cuối kỳ vẫn đúng nên lỗi chỉ lộ ở đường vốn,
    drawdown và Sharpe (notebook ``88``).
    """

    params = (
        ("mult", 100_000),
        ("ty_le_ky_quy", 0.20),
        ("phi_hd", 10_000.0),
        ("stocklike", False),
        ("commtype", bt.CommInfoBase.COMM_FIXED),
    )

    def get_margin(self, price):
        return price * self.p.mult * self.p.ty_le_ky_quy

    def getvalue(self, position, price):
        return abs(position.size) * self.get_margin(position.price)

    def _getcommission(self, size, price, pseudoexec):
        return abs(size) * self.p.phi_hd


def gan_phi_phai_sinh(cerebro: bt.Cerebro, **kwargs: object) -> PhiPhaiSinhVN:
    """Gắn ``PhiPhaiSinhVN(**kwargs)`` vào broker và tắt ``shortcash``."""
    phi = PhiPhaiSinhVN(**kwargs)
    cerebro.broker.addcommissioninfo(phi)
    cerebro.broker.set_shortcash(False)
    return phi


# ── Kích thước lệnh ─────────────────────────────────────────────────────────


class LoVN(bt.Sizer):
    """Mua bằng ``ty_le`` tiền mặt hiện có, làm tròn xuống lô 100; bán hết vị thế.

    Chừa ``1 - ty_le`` cho phí và khoảng nhảy giá giữa lúc đặt lệnh (giá đóng
    cửa hôm nay) và lúc khớp (giá mở cửa phiên sau) — không chừa thì lệnh bị
    broker từ chối ``Margin`` mỗi khi giá mở cửa cao hơn.

    Chiều bán: nếu strategy là ``ChienLuocVN`` thì chỉ bán phần đã về (T+2),
    nên ``self.sell()`` trần không lách được luật T+2.
    """

    params = (("ty_le", 0.95), ("lo", LO_CHAN))

    def _getsizing(self, comminfo, cash, data, isbuy):
        if not isbuy:
            vi_the = self.broker.getposition(data).size
            if isinstance(self.strategy, ChienLuocVN):
                return min(vi_the, self.strategy.ban_duoc(data))
            return vi_the
        return lam_tron_lo(cash * self.p.ty_le / data.close[0], self.p.lo)


# ── Khớp lệnh: trần/sàn trắng bên ───────────────────────────────────────────


class KhopTheoBienDo:
    """Filler cho broker: không khớp được ở phiên **trần/sàn trắng bên**.

    Phiên tăng trần mà ``high == low`` nghĩa là cả phiên chỉ có một mức giá và
    bên bán không có ai — lệnh mua không khớp. Đối xứng với lệnh bán ở phiên
    giảm sàn. Nhận diện bằng tỷ lệ so với giá đóng cửa phiên trước nên dùng
    được cả trên giá điều chỉnh (tỷ lệ được giữ, trừ phiên GDKHQ).

    Dùng: ``cerebro.broker.set_filler(KhopTheoBienDo("HOSE"))``.

    Lệnh bị chặn **không bị huỷ**: lệnh Market còn sống và khớp ở phiên mở
    được kế tiếp. ``so_lan_chan_mua``/``so_lan_chan_ban`` đếm số (lệnh, phiên)
    bị chặn — một lệnh nằm chờ qua ba phiên sàn được đếm ba lần.
    """

    def __init__(self, san: str = "HOSE", dung_sai: float = 0.003) -> None:
        self.bien_do = BIEN_DO[san]
        self.dung_sai = dung_sai
        self.so_lan_chan_mua = 0
        self.so_lan_chan_ban = 0

    @property
    def so_lan_chan(self) -> int:
        return self.so_lan_chan_mua + self.so_lan_chan_ban

    def __call__(self, order, price, ago):
        d = order.data
        con_lai = abs(order.executed.remsize)
        if len(d) < 2 or d.high[ago] != d.low[ago]:
            return con_lai
        thay_doi = d.close[ago] / d.close[ago - 1] - 1
        nguong = self.bien_do - self.dung_sai
        if order.isbuy() and thay_doi >= nguong:
            self.so_lan_chan_mua += 1
            return 0
        if order.issell() and thay_doi <= -nguong:
            self.so_lan_chan_ban += 1
            return 0
        return con_lai


# ── T+2 ─────────────────────────────────────────────────────────────────────


class ChienLuocVN(bt.Strategy):
    """Strategy nền có sổ theo dõi **T+2**: hàng mua phiên T bán được từ T+2.

    Lớp con gọi ``self.ban_duoc(data)`` để biết số cổ phiếu được phép bán, và
    dùng ``self.ban(data)`` thay cho ``self.close(data)``. Đếm theo **phiên có
    trong feed**, không theo ngày lịch — nghỉ lễ không làm hàng về sớm hơn.

    Lớp con override ``__init__`` hay ``notify_order`` thì phải gọi ``super()``
    — không gọi thì sổ T+2 rỗng và ``ban_duoc()`` luôn trả 0.
    """

    params = (("t_cong", 2),)

    def __init__(self) -> None:
        self._lo_mua: dict = defaultdict(deque)  # data -> deque[(phien_khop, so_cp)]

    def notify_order(self, order) -> None:
        if order.status == order.Completed and order.isbuy():
            self._lo_mua[order.data].append((len(order.data), order.executed.size))
        elif order.status == order.Completed and order.issell():
            can_tru = -order.executed.size
            lo = self._lo_mua[order.data]
            while can_tru > 0 and lo:
                phien, sl = lo[0]
                if sl <= can_tru:
                    can_tru -= sl
                    lo.popleft()
                else:
                    lo[0] = (phien, sl - can_tru)
                    can_tru = 0

    def ban_duoc(self, data=None) -> int:
        """Số cổ phiếu đã về và chưa nằm trong lệnh bán nào đang chờ khớp."""
        # `data or self.data` sai: bool(feed) là một phép so sánh line, không phải True/False.
        data = self.data if data is None else data
        # Lệnh đặt ở phiên hiện tại khớp ở phiên sau, nên tính theo phiên khớp.
        phien_khop = len(data) + 1
        da_ve = sum(sl for p, sl in self._lo_mua[data] if phien_khop - p >= self.p.t_cong)
        # Lệnh bán bị chặn ở phiên sàn vẫn sống — không trừ ra thì bán gấp đôi.
        dang_cho = sum(
            abs(o.executed.remsize) for o in self.broker.get_orders_open() if o.data is data and o.issell()
        )
        return int(max(0, da_ve - dang_cho))

    def ban(self, data=None, **kwargs):
        data = self.data if data is None else data
        sl = self.ban_duoc(data)
        if sl <= 0:
            return None
        return self.sell(data=data, size=sl, **kwargs)


# ── Analyzer → pandas ───────────────────────────────────────────────────────


def them_analyzer(cerebro: bt.Cerebro) -> None:
    """Gắn bộ analyzer chuẩn với tên cố định để ``ket_qua()`` đọc lại."""
    cerebro.addanalyzer(bt.analyzers.TimeReturn, _name="loi_suat", timeframe=bt.TimeFrame.Days)
    cerebro.addanalyzer(bt.analyzers.Transactions, _name="giao_dich")
    cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name="vong")


def chi_so_hieu_qua(
    loi_suat: pd.Series, *, rf_nam: float | pd.Series = 0.0, so_phien_nam: int = 252
) -> dict:
    """CAGR, MDD, Sharpe (năm hoá, trừ lãi suất phi rủi ro theo phiên), biến động.

    ``rf_nam`` là lãi suất phi rủi ro **theo năm, dạng phân số** (``0.0254`` =
    2,54%) — một số, hoặc một Series theo ngày (vd lợi suất TPCP 1 năm từ
    ``client.macro``, đã chia 100), được ffill lên lịch phiên. Quy về phiên bằng
    lãi kép ``(1 + rf)^(1/so_phien_nam) − 1``, cùng cách ``bt.analyzers.SharpeRatio``.

    ``mdd`` là số **âm, dạng phân số** (``-0.27``); ``bt.analyzers.DrawDown``
    báo cùng đại lượng nhưng **dương, dạng %** (``26.99``).
    """
    loi_suat = loi_suat.dropna()
    if loi_suat.empty:
        return {"cagr": np.nan, "mdd": np.nan, "sharpe": np.nan, "bien_dong": np.nan}
    duong_von = (1 + loi_suat).cumprod()
    so_nam = len(loi_suat) / so_phien_nam
    cagr = duong_von.iloc[-1] ** (1 / so_nam) - 1 if so_nam > 0 else np.nan
    mdd = (duong_von / duong_von.cummax() - 1).min()
    if isinstance(rf_nam, pd.Series):
        rf_nam = rf_nam.sort_index().reindex(loi_suat.index, method="ffill").bfill()
    vuot = loi_suat - ((1 + rf_nam) ** (1 / so_phien_nam) - 1)
    do_lech = vuot.std(ddof=1)
    sharpe = vuot.mean() / do_lech * math.sqrt(so_phien_nam) if do_lech > 0 else np.nan
    return {
        "cagr": float(cagr),
        "mdd": float(mdd),
        "sharpe": float(sharpe),
        "bien_dong": float(loi_suat.std(ddof=1) * math.sqrt(so_phien_nam)),
    }


def ket_qua(strat, *, rf_nam: float | pd.Series = 0.0) -> dict:
    """Đọc analyzer của ``them_analyzer()`` ra pandas.

    Trả về ``loi_suat`` (Series theo phiên), ``duong_von`` (chuẩn hoá về 1),
    ``giao_dich`` (một dòng mỗi lần khớp, giá VND), và ``tom_tat`` (dict chỉ số).
    """
    ls = pd.Series(strat.analyzers.loi_suat.get_analysis(), dtype="float64")
    ls.index = pd.DatetimeIndex(ls.index, name="date")

    dong = []
    for tg, ds in strat.analyzers.giao_dich.get_analysis().items():
        for amount, price, sid, symbol, value in ds:
            dong.append(
                {"date": pd.Timestamp(tg), "symbol": symbol, "so_cp": amount, "gia": price, "gia_tri": value}
            )
    giao_dich = pd.DataFrame(dong, columns=["date", "symbol", "so_cp", "gia", "gia_tri"])

    vong = strat.analyzers.vong.get_analysis()
    tong_vong = vong.get("total", {}).get("closed", 0) if vong else 0
    thang = vong.get("won", {}).get("total", 0) if tong_vong else 0

    tom_tat = chi_so_hieu_qua(ls, rf_nam=rf_nam)
    tom_tat.update(
        {
            "so_vong_dong": int(tong_vong),
            "ty_le_thang": thang / tong_vong if tong_vong else np.nan,
            "so_lenh_khop": len(giao_dich),
        }
    )
    return {"loi_suat": ls, "duong_von": (1 + ls).cumprod(), "giao_dich": giao_dich, "tom_tat": tom_tat}
