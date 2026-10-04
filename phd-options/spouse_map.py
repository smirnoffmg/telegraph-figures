import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from shapely.geometry import box

plt.rcParams["font.family"] = "Arial"

SURFACE = "#fcfcfb"
TEXT = "#0b0b0b"
TEXT2 = "#52514e"
# последовательная шкала синего (палитра по умолчанию dataviz): темнее — проще супругу
C_WORK = "#104281"      # ВНЖ и право работать
C_COND = "#2a78d6"      # с условиями
C_NOWORK = "#86b6ef"    # приедет без права работы
C_HARD = "#b7d3f6"      # приезд затруднён
C_BLOCK = "#9c9b97"     # визы почти не выдают (со штриховкой)
C_NONE = "#ecebe8"      # в статье не разбирались

STATUS = {
    "Austria": ("work", "Австрия"), "Germany": ("work", "Германия"),
    "Netherlands": ("work", "Нидерланды"), "France": ("work", "Франция"),
    "United Kingdom": ("work", "Великобритания"),
    "Switzerland": ("cond", "Швейцария"), "Turkey": ("cond", "Турция"),
    "Israel": ("nowork", "Израиль"),
    "Hungary": ("hard", "Венгрия"), "Italy": ("hard", "Италия"),
    "Czechia": ("block", None), "Poland": ("block", "Польша"),
    "Estonia": ("block", None), "Latvia": ("block", None),
    "Lithuania": ("block", None), "Finland": ("block", "Финляндия"),
}
COLOR = {"work": C_WORK, "cond": C_COND, "nowork": C_NOWORK, "hard": C_HARD, "block": C_BLOCK}

w = gpd.read_file("ne_50m_admin_0_countries.shp")
w["key"] = w["NAME_EN"].replace({"Czech Republic": "Czechia"})
w = w.to_crs(3035)
VIEW = gpd.GeoSeries([box(-10, 29.5, 44, 70.5)], crs=4326).to_crs(3035).total_bounds
xmin, ymin, xmax, ymax = VIEW[0] + 3.5e5, VIEW[1] + 2.5e5, VIEW[2] - 3e5, VIEW[3] - 2e5
w = w.clip(box(xmin, ymin, xmax, ymax))

fig, ax = plt.subplots(figsize=(9, 8.6), dpi=200)
fig.patch.set_facecolor(SURFACE)
ax.set_facecolor(SURFACE)

for _, r in w.iterrows():
    st = STATUS.get(r["key"], (None, None))[0]
    color = COLOR.get(st, C_NONE)
    hatch = "////" if st == "block" else None
    gpd.GeoSeries([r.geometry], crs=w.crs).plot(
        ax=ax, color=color, edgecolor=SURFACE, linewidth=0.8, hatch=hatch)

# подписи: внутри страны или в море с выносной линией (точки подобраны вручную)
INSIDE = {
    "Austria": (14.3, 47.5), "Germany": (10.2, 51.0), "France": (2.3, 46.6),
    "Turkey": (34.5, 39.0), "Hungary": (19.4, 47.1),
    "Italy": (12.8, 42.8), "Poland": (19.2, 52.1), "Finland": (26.0, 63.0),
}
OUTSIDE = {  # якорь в стране -> место подписи
    "United Kingdom": ((-4.2, 57.4), (-4.5, 61.6)),
    "Netherlands": ((5.5, 52.4), (3.0, 55.6)),
    "Switzerland": ((8.1, 46.8), (5.5, 41.2)),
    "Israel": ((34.9, 31.6), (31.0, 33.6)),
}
def proj(lon, lat):
    pt = gpd.GeoSeries(gpd.points_from_xy([lon], [lat]), crs=4326).to_crs(3035).iloc[0]
    return pt.x, pt.y
for key, (lon, lat) in INSIDE.items():
    st, name = STATUS[key]
    light = st in ("nowork", "hard", "block")
    ax.annotate(name, proj(lon, lat), ha="center", va="center", fontsize=8.5,
                color=TEXT if light else "#ffffff", fontweight="normal" if light else "bold")
for key, (anchor, at) in OUTSIDE.items():
    ax.annotate(STATUS[key][1], xy=proj(*anchor), xytext=proj(*at), ha="center", va="center",
                fontsize=8.5, color=TEXT,
                arrowprops=dict(arrowstyle="-", color=TEXT2, linewidth=0.6, shrinkA=2, shrinkB=0))

ax.set_xlim(xmin, xmax)
ax.set_ylim(ymin, ymax)
ax.set_axis_off()

handles = [
    Patch(facecolor=C_WORK, label="супруг получает ВНЖ и может работать"),
    Patch(facecolor=C_COND, label="можно, но с условиями (жильё, язык, срок)"),
    Patch(facecolor=C_NOWORK, label="супруг приедет без права работы"),
    Patch(facecolor=C_HARD, label="приезд супруга затруднён"),
    Patch(facecolor=C_BLOCK, hatch="////", edgecolor=SURFACE, label="визы гражданам России почти не выдают"),
    Patch(facecolor=C_NONE, label="в статье не разбирались (Россия: виза не нужна)"),
]
leg = fig.legend(handles=handles, loc="upper left", bbox_to_anchor=(0.06, 0.08), ncol=2,
                 frameon=False, fontsize=9, labelcolor=TEXT2, handlelength=1.6, handleheight=1.1,
                 columnspacing=1.5)
ax.set_title("Если аспирант едет с семьёй: что будет с супругом",
             loc="left", fontsize=14, color=TEXT, pad=12)
fig.text(0.07, -0.06,
         "Статус указан для аспиранта по трудовому договору там, где такие позиции есть. Италия: закон 2024 года\n"
         "требует для воссоединения двух лет пребывания. Венгрия: запрет при учебном ВНЖ. Данные на октябрь 2026 года.",
         fontsize=7.5, color=TEXT2)
fig.subplots_adjust(left=0.02, right=0.98, top=0.93, bottom=0.1)
fig.savefig("Аспирантура — супруг на карте Европы.png", bbox_inches="tight", facecolor=SURFACE)
