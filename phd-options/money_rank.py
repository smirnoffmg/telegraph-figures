import json
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from scipy.stats import spearmanr

plt.rcParams["font.family"] = "Arial"
SURFACE, TEXT, TEXT2, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#e4e3df"
BLUE = "#2a78d6"
MIN_C = "#9c9b97"
SPOUSE_C = {4: "#104281", 3: "#2a78d6", 2: "#86b6ef", 1: "#b7d3f6"}
SPOUSE_L = {4: "супруг получает ВНЖ и может работать", 3: "можно, но с условиями",
            1: "приезд супруга затруднён"}

# курсы ECB и Банка России на 02.10.2026
GBP, CHF, HUF, RUB, USD = 0.85033, 0.9279, 369.18, 94.5252, 1.1225

# --- выплаты, € в месяц (из money.json; ISTA и EPFL с 13-14 выплатами переведены как год/12)
STIPENDS = [  # (подпись, низ, верх, тип налога, минимум для ВНЖ € в месяц или None)
    ("ETH Zürich (брутто)", 53500 / CHF / 12, None, None),
    ("EPFL (брутто)", 55225 / CHF / 12, None, None),
    ("ISTA, Австрия (брутто)", 3053 * 14 / 12, 3673 * 14 / 12, 1308.39),
    ("Нидерланды, 1-й год (брутто)", 3059, None, 1635.90),
    ("Франция, contrat doctoral (брутто)", 2300, None, 877.50),
    ("Bocconi (брутто)", 27000 / 12, None, 10179.85 / 12),
    ("Бонн (на руки)", 2000, 2300, 992),
    ("Великобритания, UKRI", 21805 / GBP / 12, None, 1171 / GBP),
    ("Scuola Normale (брутто)", 18848 / 12, None, 10179.85 / 12),
    ("SISSA (брутто)", 16242.96 / 12, None, 10179.85 / 12),
    ("PGSM, магистратура M2", 1150, None, 877.50),
    ("Сколтех, лучшие (от)", 75000 / RUB, None, None),
    ("Stipendium Hungaricum", 140000 / HUF, 180000 / HUF, None),
    ("МФТИ", 25000 / RUB, None, None),
]
STIPENDS.sort(key=lambda r: (r[2] or r[1]))

fig, ax = plt.subplots(figsize=(9, 7.2), dpi=200)
fig.patch.set_facecolor(SURFACE); ax.set_facecolor(SURFACE)
for i, (label, lo, hi, mn) in enumerate(STIPENDS):
    if hi:
        ax.plot([lo, hi], [i, i], color=BLUE, linewidth=2, solid_capstyle="round", zorder=2)
        ax.scatter([lo, hi], [i, i], s=40, color=BLUE, edgecolor=SURFACE, linewidth=1.5, zorder=3)
    else:
        ax.scatter([lo], [i], s=48, color=BLUE, edgecolor=SURFACE, linewidth=1.5, zorder=3)
    if mn:
        ax.scatter([mn], [i], s=60, marker="|", color=MIN_C, linewidth=2.2, zorder=2)
    ax.text((hi or lo) + 90, i, f"{(lo + hi) / 2 if hi else lo:,.0f} €".replace(",", " "),
            va="center", fontsize=8, color=TEXT2)
ax.set_yticks(range(len(STIPENDS)), [r[0] for r in STIPENDS], fontsize=9, color=TEXT)
ax.set_xlim(0, 5600)
ax.set_xticks(range(0, 5001, 1000), [f"{x:,}".replace(",", " ") for x in range(0, 5001, 1000)],
              fontsize=8.5, color=TEXT2)
ax.set_xlabel("евро в месяц", fontsize=9, color=TEXT2)
ax.grid(axis="x", color=GRID, linewidth=0.8); ax.set_axisbelow(True)
for s in ax.spines.values(): s.set_visible(False)
ax.tick_params(length=0)
ax.legend(handles=[
    Line2D([], [], marker="o", color=BLUE, linestyle="", markersize=7, label="выплата аспиранту (точка) или диапазон"),
    Line2D([], [], marker="|", color=MIN_C, linestyle="", markersize=10, markeredgewidth=2.2,
           label="сколько страна требует иметь для ВНЖ\n(студента; в Нидерландах исследователя)"),
], loc="lower right", frameon=False, fontsize=8.5, labelcolor=TEXT2)
ax.set_title("Сколько платят аспиранту и сколько нужно на жизнь по меркам страны",
             loc="left", fontsize=13, color=TEXT, pad=12)
fig.text(0.01, -0.06,
         "Суммы с официальных сайтов, 2026 год; пересчёт по курсам ECB и Банка России на 02.10.2026. Брутто, «на руки»\n"
         "и стипендии без налога сравнивать напрямую нельзя: тип указан в подписи. Минимум для ВНЖ: Австрия, Нидерланды\n"
         "(исследователь), Франция, Италия, Германия (памятка посольства, февраль 2025), Великобритания (вне Лондона).",
         fontsize=7.5, color=TEXT2)
fig.tight_layout()
fig.savefig("Аспирантура — выплаты и минимум для ВНЖ.png", bbox_inches="tight", facecolor=SURFACE)

# --- плата за обучение (только платные варианты), € в год
TUITION = [("Венский университет, MSc", 752.92 * 2), ("Белградский университет", 4500),
           ("ELTE, платное место", 8000), ("Nazarbayev University без стипендии", 23500 / USD)]
fig, ax = plt.subplots(figsize=(9, 2.6), dpi=200)
fig.patch.set_facecolor(SURFACE); ax.set_facecolor(SURFACE)
for i, (label, v) in enumerate(TUITION):
    ax.scatter([v], [i], s=48, color="#eb6834", edgecolor=SURFACE, linewidth=1.5, zorder=3)
    ax.text(v + 300, i, f"{v:,.0f} €".replace(",", " "), va="center", fontsize=8, color=TEXT2)
ax.set_yticks(range(len(TUITION)), [t[0] for t in TUITION], fontsize=9, color=TEXT)
ax.set_xlim(0, 24500)
ax.set_xticks(range(0, 20001, 5000), [f"{x:,}".replace(",", " ") for x in range(0, 20001, 5000)],
              fontsize=8.5, color=TEXT2)
ax.set_xlabel("евро в год", fontsize=9, color=TEXT2)
ax.grid(axis="x", color=GRID, linewidth=0.8); ax.set_axisbelow(True)
for s in ax.spines.values(): s.set_visible(False)
ax.tick_params(length=0)
ax.set_title("Плата за обучение там, где учатся за свой счёт", loc="left", fontsize=13, color=TEXT, pad=10)
fig.text(0.01, -0.08, "В финансируемых PhD (ISTA, IMPRS, Сколтех, Stipendium Hungaricum) обучение бесплатное. "
         "Курс ECB на 02.10.2026.", fontsize=7.5, color=TEXT2)
fig.tight_layout()
fig.savefig("Аспирантура — плата за обучение.png", bbox_inches="tight", facecolor=SURFACE)

# --- рейтинги против условий
R = json.load(open("rankings.json"))
def place(src, name):
    for r in R[src]["rows"]:
        if r["institution"].startswith(name) and r["rank_low"]:
            return (r["rank_low"] + r["rank_high"]) / 2, r["rank_low"], r["rank_high"]
    return None
FR, NL, UK, HU = 2300, 3059, 21805 / GBP / 12, 160000 / HUF
ROWS = [  # (название в rankings.json, подпись, выплата € в месяц, статус супруга)
    ("Боннский", "Бонн", 2150, 4), ("ETH", "ETH", 53500 / CHF / 12, 3), ("EPFL", "EPFL", 55225 / CHF / 12, 3),
    ("Утрехт", "Утрехт", NL, 4), ("Лейден", "Лейден", NL, 4), ("Амстердам", "Амстердам", NL, 4),
    ("TU Delft", "Делфт", NL, 4), ("TU Eindhoven", "Эйндховен", NL, 4),
    ("Sorbonne", "Сорбонна", FR, 4), ("Université Paris Cité", "Paris Cité", FR, 4), ("PSL", "PSL", FR, 4),
    ("Université Paris-Saclay", "Paris-Saclay", FR, 4), ("Institut Polytechnique", "IP Paris", FR, 4),
    ("SISSA", "SISSA", 16242.96 / 12, 1), ("Scuola Normale", "SNS", 18848 / 12, 1), ("Bocconi", "Bocconi", 2250, 1),
    ("ELTE", "ELTE", HU, 1), ("BME", "BME", HU, 1), ("Сегед", "Сегед", HU, 1), ("Дебрецен", "Дебрецен", HU, 1),
    ("Oxford", "Оксфорд", UK, 4), ("Cambridge", "Кембридж", UK, 4), ("Warwick", "Уорик", UK, 4),
    ("Imperial", "Imperial", UK, 4), ("МФТИ", "МФТИ", 25000 / RUB, 4),
]
money_rank = np.argsort(np.argsort([-r[2] for r in ROWS])) + 1
from scipy.stats import rankdata
m_rank = rankdata([-r[2] for r in ROWS]); s_rank = rankdata([-r[3] for r in ROWS])
composite = rankdata((m_rank + s_rank) / 2)  # 1 = лучшие условия

fig, axes = plt.subplots(1, 2, figsize=(10, 5.4), dpi=200, sharey=True)
fig.patch.set_facecolor(SURFACE)
LABEL = {"ETH", "EPFL", "Бонн", "Сорбонна", "Оксфорд", "SISSA", "SNS", "МФТИ", "Bocconi"}
OFFSET = {"ETH": (-6, -3, "right"), "Бонн": (0, -13, "center")}
GROUPS = {"Нидерланды, 5 вузов": {"Утрехт", "Лейден", "Амстердам", "Делфт", "Эйндховен"},
          "Венгрия, Stipendium Hungaricum": {"ELTE", "BME", "Сегед", "Дебрецен"}}
stats = {}
for ax, src, title in [(axes[0], "arwu", "ShanghaiRanking (ARWU) 2026"), (axes[1], "qs", "QS 2026")]:
    ax.set_facecolor(SURFACE)
    xs, comp = [], []
    for row, c in zip(ROWS, composite):
        p = place(src, row[0])
        if not p:
            continue
        mid, lo, hi = p
        xs.append(mid); comp.append(c)
        col = SPOUSE_C[row[3]]
        if hi > lo:
            ax.plot([lo, hi], [row[2], row[2]], color=col, linewidth=1.6, alpha=0.8, zorder=2)
        ax.scatter([mid], [row[2]], s=46, color=col, edgecolor=SURFACE, linewidth=1.5, zorder=3)
        if row[1] in LABEL:
            dx, dy, ha = OFFSET.get(row[1], (4, 4, "left"))
            ax.annotate(row[1], (mid, row[2]), xytext=(dx, dy), textcoords="offset points",
                        fontsize=7.5, color=TEXT2, ha=ha)
    for gname, members in GROUPS.items():
        pts = [(place(src, r[0]), r[2]) for r in ROWS if r[1] in members and place(src, r[0])]
        if pts:
            ax.annotate(gname, (min(p[0][1] for p in pts), pts[0][1]), xytext=(0, 9),
                        textcoords="offset points", fontsize=7.5, color=TEXT2)
    rho, _ = spearmanr(comp, xs)
    stats[src] = (rho, len(xs))
    ax.set_xscale("log")
    ax.set_xlim(1.5, 800)
    ax.set_xticks([2, 5, 10, 20, 50, 100, 200, 500], ["2", "5", "10", "20", "50", "100", "200", "500"],
                  fontsize=8.5, color=TEXT2)
    ax.minorticks_off()
    ax.set_xlabel("место в рейтинге по математике (лог. шкала)", fontsize=9, color=TEXT2)
    ax.set_title(f"{title}: ρ = {rho:.2f}, n = {len(xs)}", loc="left", fontsize=10.5, color=TEXT)
    ax.grid(color=GRID, linewidth=0.8); ax.set_axisbelow(True)
    for s in ax.spines.values(): s.set_visible(False)
    ax.tick_params(length=0)
axes[0].set_ylabel("выплата аспиранту, € в месяц", fontsize=9, color=TEXT2)
axes[0].set_yticks(range(0, 5001, 1000), [f"{x:,}".replace(",", " ") for x in range(0, 5001, 1000)],
                   fontsize=8.5, color=TEXT2)
fig.legend(handles=[Line2D([], [], marker="o", linestyle="", color=SPOUSE_C[k], markersize=7, label=v)
                    for k, v in SPOUSE_L.items()],
           loc="lower left", bbox_to_anchor=(0.06, -0.06), ncol=3, frameon=False, fontsize=8.5, labelcolor=TEXT2)
fig.suptitle("Сильнее вуз в рейтинге, лучше ли условия для аспиранта?", x=0.06, ha="left",
             fontsize=13, color=TEXT)
fig.text(0.06, -0.14,
         "ρ: корреляция Спирмена между сводным рангом условий и местом в рейтинге; ρ > 0 значит, что у вузов выше в рейтинге\n"
         "условия лучше. Сводный ранг: среднее рангов по выплате и статусу супруга. Выплата во Франции, Нидерландах,\n"
         "Великобритании и Венгрии задана на уровне страны. Диапазон мест показан отрезком, точка в середине.",
         fontsize=7.5, color=TEXT2)
fig.tight_layout()
fig.savefig("Аспирантура — рейтинг вуза и условия.png", bbox_inches="tight", facecolor=SURFACE)
print(stats)
