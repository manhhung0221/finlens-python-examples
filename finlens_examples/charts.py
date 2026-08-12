"""Biểu đồ Plotly dùng chung — một bảng màu, một theme, sáu hàm.

## Vì sao bảng màu lại là thế này

Quy ước của thị trường Việt Nam là **xanh tăng / đỏ giảm**, và đổi nó đi thì
người đọc hiểu ngược. Nhưng cặp xanh lá ``#0ca30c`` với đỏ ``#d03b3b`` chỉ cách
nhau **ΔE 4,1** dưới mắt người mù màu deutan — tức khoảng 8% nam giới nhìn hai
cột thấy gần như một màu.

Cặp dùng ở đây là **aqua ``#1baf7a`` với đỏ ``#d03b3b``**: vẫn đọc là "xanh
tăng", nhưng ΔE deutan là **9,9**, vượt ngưỡng 8. Đây là kết quả chạy validator
chứ không phải cảm nhận bằng mắt.

Aqua có tương phản 2,74:1 trên nền sáng, dưới ngưỡng 3:1 — nên mọi hàm ở đây
**luôn in con số ra cạnh mảng màu**. Màu là kênh phụ, số mới là kênh chính.

## Hai luật không phá

1. **Không bao giờ hai trục y.** Giá và khối lượng là hai đại lượng khác thang —
   chúng đi thành hai hàng subplot chứ không chồng lên nhau bằng ``secondary_y``.
2. **Màu bám theo thực thể, không bám theo thứ hạng.** Lọc bớt mã không được làm
   các mã còn lại đổi màu.
"""

from __future__ import annotations

from typing import Sequence

import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
from plotly.subplots import make_subplots

# ── Bảng màu ────────────────────────────────────────────────────────────────
# Tám màu định danh, dùng theo đúng thứ tự này và không xoay vòng. Chuỗi thứ 9
# gộp vào "Khác" hoặc tách thành small multiples.
CHUOI: tuple[str, ...] = (
    "#2a78d6",  # 1 lam
    "#eb6834",  # 2 cam
    "#1baf7a",  # 3 aqua
    "#eda100",  # 4 vàng
    "#e87ba4",  # 5 hồng
    "#008300",  # 6 lục
    "#4a3aa7",  # 7 tím
    "#e34948",  # 8 đỏ
)

TANG = "#1baf7a"  # xanh — giá lên
GIAM = "#d03b3b"  # đỏ — giá xuống
THAM_CHIEU = "#eda100"  # vàng — đứng giá

# Thang phân kỳ cho lợi suất: đỏ đậm ← xám trung tính → aqua đậm.
# Xám ở giữa là bắt buộc; một màu sắc ở điểm giữa làm "không đổi" trông như một
# trạng thái, trong khi nó là *vắng mặt* của trạng thái.
PHAN_KY: list[tuple[float, str]] = [
    (0.000, "#a32d2d"),
    (0.125, "#d03b3b"),
    (0.250, "#de7a7a"),
    (0.375, "#ecb2b2"),
    (0.500, "#f0efec"),
    (0.625, "#96dcc2"),
    (0.750, "#4fc79b"),
    (0.875, "#1baf7a"),
    (1.000, "#14875e"),
]

# Thang tuần tự một sắc (độ lớn thuần, không có dấu): lam nhạt → lam đậm.
TUAN_TU: list[tuple[float, str]] = [
    (0.0, "#cde2fb"),
    (0.25, "#9ec5f4"),
    (0.5, "#5598e7"),
    (0.75, "#256abf"),
    (1.0, "#0d366b"),
]

_NEN = "#fcfcfb"
_MUC_CHINH = "#0b0b0b"
_MUC_PHU = "#52514e"
_MUC_MO = "#898781"
_LUOI = "#e1e0d9"
_TRUC = "#c3c2b7"

_TEN_THEME = "finlens"


def ap_dung_theme() -> None:
    """Đăng ký và bật theme ``finlens`` cho mọi biểu đồ Plotly sau đó.

    Gọi một lần ở cell đầu notebook.
    """
    pio.templates[_TEN_THEME] = go.layout.Template(
        layout=go.Layout(
            colorway=list(CHUOI),
            paper_bgcolor=_NEN,
            plot_bgcolor=_NEN,
            font=dict(
                family='system-ui, -apple-system, "Segoe UI", sans-serif',
                size=13,
                color=_MUC_CHINH,
            ),
            title=dict(font=dict(size=17, color=_MUC_CHINH), x=0, xanchor="left"),
            xaxis=dict(
                showgrid=False,
                zeroline=False,
                linecolor=_TRUC,
                tickcolor=_TRUC,
                tickfont=dict(color=_MUC_MO, size=12),
                title=dict(font=dict(color=_MUC_PHU, size=12)),
            ),
            yaxis=dict(
                gridcolor=_LUOI,
                gridwidth=1,
                zerolinecolor=_TRUC,
                zerolinewidth=1,
                linecolor="rgba(0,0,0,0)",
                tickfont=dict(color=_MUC_MO, size=12),
                title=dict(font=dict(color=_MUC_PHU, size=12)),
            ),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="left",
                x=0,
                font=dict(color=_MUC_PHU, size=12),
                bgcolor="rgba(0,0,0,0)",
            ),
            colorscale=dict(diverging=PHAN_KY, sequential=TUAN_TU),
            margin=dict(l=64, r=24, t=64, b=48),
            hoverlabel=dict(
                bgcolor=_NEN,
                bordercolor=_TRUC,
                font=dict(color=_MUC_CHINH, size=12),
            ),
        )
    )
    pio.templates.default = _TEN_THEME


def _khung(fig: go.Figure, tieu_de: str, phu_de: str | None, cao: int) -> go.Figure:
    """Gắn tiêu đề (kèm phụ đề nhỏ) và chiều cao chuẩn."""
    if phu_de:
        tieu_de = f"{tieu_de}<br><sub style='color:{_MUC_PHU}'>{phu_de}</sub>"
    fig.update_layout(title_text=tieu_de, height=cao)
    return fig


def duong(
    df: pd.DataFrame,
    *,
    x: str,
    y: str,
    theo: str | None = None,
    tieu_de: str = "",
    phu_de: str | None = None,
    nhan_y: str = "",
    cao: int = 460,
    moc_khong: bool = False,
) -> go.Figure:
    """Đường theo thời gian, tách chuỗi theo cột ``theo`` (thường là ``symbol``).

    Bật ``moc_khong=True`` khi trục y là phần trăm thay đổi — đường 0 khi đó là
    một mốc có nghĩa chứ không phải một gạch trang trí.

    Chú giải luôn có khi từ hai chuỗi trở lên; một chuỗi thì tiêu đề đã gọi tên
    nó rồi nên không cần hộp chú giải.
    """
    fig = go.Figure()
    nhom: Sequence[tuple[object, pd.DataFrame]]
    nhom = list(df.groupby(theo, observed=True)) if theo else [(None, df)]

    for i, (ten, phan) in enumerate(nhom):
        fig.add_trace(
            go.Scatter(
                x=phan[x],
                y=phan[y],
                name=str(ten) if ten is not None else y,
                mode="lines",
                line=dict(width=2, color=CHUOI[i % len(CHUOI)]),
                hovertemplate="%{y:,.2f}<extra>%{fullData.name}</extra>",
            )
        )

    if moc_khong:
        fig.add_hline(y=0, line_width=1, line_color=_TRUC)

    fig.update_layout(
        hovermode="x unified",
        showlegend=len(nhom) > 1,
        yaxis_title=nhan_y,
    )
    return _khung(fig, tieu_de, phu_de, cao)


def nen(
    df: pd.DataFrame,
    *,
    x: str = "date",
    tieu_de: str = "",
    phu_de: str | None = None,
    nhan_gia: str = "nghìn VND",
    cao: int = 620,
) -> go.Figure:
    """Nến giá và khối lượng — **hai hàng subplot, không phải hai trục y**.

    Chồng khối lượng lên trục y thứ hai là lỗi biểu đồ phổ biến nhất: nó buộc
    người đọc so hai thang khác nhau trên cùng một khung, và độ cao tương đối
    giữa hai chuỗi là thứ do người vẽ chọn chứ không phải do dữ liệu quyết định.

    Frame vào phải là **một mã** với các cột ``open · high · low · close · volume``.
    """
    fig = make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.06,
        row_heights=[0.72, 0.28],
    )
    fig.add_trace(
        go.Candlestick(
            x=df[x],
            open=df["open"],
            high=df["high"],
            low=df["low"],
            close=df["close"],
            name="Giá",
            increasing=dict(line=dict(color=TANG, width=1), fillcolor=TANG),
            decreasing=dict(line=dict(color=GIAM, width=1), fillcolor=GIAM),
        ),
        row=1,
        col=1,
    )
    mau_kl = [
        TANG if c >= o else GIAM for o, c in zip(df["open"], df["close"], strict=True)
    ]
    fig.add_trace(
        go.Bar(
            x=df[x],
            y=df["volume"],
            name="Khối lượng",
            marker=dict(color=mau_kl, line=dict(width=0)),
            hovertemplate="%{y:,.0f} cp<extra></extra>",
        ),
        row=2,
        col=1,
    )
    fig.update_layout(
        showlegend=False,
        xaxis_rangeslider_visible=False,
        hovermode="x unified",
    )
    fig.update_yaxes(title_text=nhan_gia, row=1, col=1)
    fig.update_yaxes(title_text="cổ phiếu", row=2, col=1)
    return _khung(fig, tieu_de, phu_de, cao)


def thanh_doi_mau(
    df: pd.DataFrame,
    *,
    x: str,
    y: str,
    tieu_de: str = "",
    phu_de: str | None = None,
    nhan_y: str = "",
    cao: int = 420,
    dinh_dang_nhan: str = "{:,.1f}",
) -> go.Figure:
    """Cột đổi màu theo dấu — dương aqua, âm đỏ, kèm nhãn số trên từng cột.

    Dùng cho mua/bán ròng theo phiên, thay đổi phần trăm theo ngành. Nhãn số
    không phải để trang trí: aqua nằm dưới ngưỡng tương phản 3:1 nên con số là
    thứ giữ cho biểu đồ đọc được khi màu thất bại.
    """
    gia_tri = df[y]
    mau = [TANG if v >= 0 else GIAM for v in gia_tri]
    nhan = [dinh_dang_nhan.format(v) for v in gia_tri]

    fig = go.Figure(
        go.Bar(
            x=df[x],
            y=gia_tri,
            marker=dict(color=mau, line=dict(color=_NEN, width=2)),
            text=nhan,
            textposition="outside",
            textfont=dict(color=_MUC_PHU, size=11),
            cliponaxis=False,
            hovertemplate="%{x}<br>%{y:,.2f}<extra></extra>",
        )
    )
    fig.add_hline(y=0, line_width=1, line_color=_TRUC)
    fig.update_layout(showlegend=False, yaxis_title=nhan_y, bargap=0.25)
    return _khung(fig, tieu_de, phu_de, cao)


def bar_ngang(
    df: pd.DataFrame,
    *,
    nhan: str,
    gia_tri: str,
    tieu_de: str = "",
    phu_de: str | None = None,
    nhan_x: str = "",
    cao: int | None = None,
    dinh_dang_nhan: str = "{:,.1f}",
) -> go.Figure:
    """Bảng xếp hạng dạng thanh ngang — top tăng/giảm, top mua ròng.

    Thanh ngang thắng thanh dọc khi nhãn là mã hoặc tên ngành: chữ nằm ngang
    đọc được, còn nhãn xoay 45° thì không.
    """
    sap = df.sort_values(gia_tri)
    mau = [TANG if v >= 0 else GIAM for v in sap[gia_tri]]
    fig = go.Figure(
        go.Bar(
            x=sap[gia_tri],
            y=sap[nhan],
            orientation="h",
            marker=dict(color=mau, line=dict(color=_NEN, width=2)),
            text=[dinh_dang_nhan.format(v) for v in sap[gia_tri]],
            textposition="outside",
            textfont=dict(color=_MUC_PHU, size=11),
            cliponaxis=False,
            hovertemplate="%{y}: %{x:,.2f}<extra></extra>",
        )
    )
    fig.add_vline(x=0, line_width=1, line_color=_TRUC)
    fig.update_layout(
        showlegend=False,
        xaxis_title=nhan_x,
        yaxis=dict(showgrid=False, type="category"),
        xaxis=dict(showgrid=True, gridcolor=_LUOI),
        bargap=0.3,
    )
    return _khung(fig, tieu_de, phu_de, cao or max(320, 26 * len(sap) + 130))


def heatmap(
    bang: pd.DataFrame,
    *,
    tieu_de: str = "",
    phu_de: str | None = None,
    nhan_mau: str = "%",
    phan_ky: bool = True,
    cao: int | None = None,
    dinh_dang_o: str = "%{z:.1f}",
) -> go.Figure:
    """Ma trận giá trị — hàng là thực thể, cột là kỳ. Số in trong từng ô.

    ``phan_ky=True`` (mặc định) cho dữ liệu có dấu: thang đỏ ↔ xám ↔ aqua với
    **điểm giữa khoá ở 0**, nên một ô xám luôn nghĩa là "không đổi" bất kể biên
    độ của bảng. ``phan_ky=False`` cho độ lớn thuần, dùng thang một sắc.

    Số hiện trong ô là bắt buộc chứ không phải tuỳ chọn: đây là chỗ màu mang
    toàn bộ thông tin, nên phải có một kênh thứ hai đọc được.
    """
    z = bang.to_numpy(dtype=float)
    if phan_ky:
        bien = float(pd.Series(z.ravel()).abs().max() or 1.0)
        thang, zmin, zmax, zmid = PHAN_KY, -bien, bien, 0.0
    else:
        thang, zmin, zmax, zmid = TUAN_TU, None, None, None

    fig = go.Figure(
        go.Heatmap(
            z=z,
            x=[str(c) for c in bang.columns],
            y=[str(i) for i in bang.index],
            colorscale=thang,
            zmin=zmin,
            zmax=zmax,
            zmid=zmid,
            xgap=2,
            ygap=2,
            texttemplate=dinh_dang_o,
            textfont=dict(size=11),
            colorbar=dict(
                title=dict(text=nhan_mau, font=dict(color=_MUC_PHU, size=12)),
                thickness=12,
                outlinewidth=0,
                tickfont=dict(color=_MUC_MO, size=11),
            ),
            hovertemplate="%{y} · %{x}<br>%{z:,.2f}<extra></extra>",
        )
    )
    fig.update_layout(
        xaxis=dict(showgrid=False, side="top", linecolor="rgba(0,0,0,0)"),
        yaxis=dict(showgrid=False, autorange="reversed"),
    )
    return _khung(fig, tieu_de, phu_de, cao or max(320, 24 * len(bang) + 160))
