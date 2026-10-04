import json
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import to_rgb
from scipy.stats import rankdata

plt.rcParams["font.family"] = "Arial"
SURFACE, TEXT, TEXT2 = "#fcfcfb", "#0b0b0b", "#52514e"
DARK, LIGHT = "#104281", "#e8f1fc"

# курсы ECB и Банка России на 02.10.2026
GBP, CHF, HUF, RUB = 0.85033, 0.9279, 369.18, 94.5252
R = json.load(open("rankings.json"))
NOT_LISTED = {"arwu": 501, "qs": 604}  # вуза нет в опубликованном списке: место за его концом


def place(src, name):
    for r in R[src]["rows"]:
        if r["institution"].startswith(name):
            if not r["rank_low"]:
                return NOT_LISTED[src], "—"
            return (r["rank_low"] + r["rank_high"]) / 2, r["rank"]
    raise KeyError(name)


SPOUSE = {4: "ВНЖ и работа", 3: "с условиями", 2: "без права работы", 1: "затруднён"}
# (вариант, выплата € в месяц, подпись выплаты, супруг, виза нужна, язык страны свой или английский, вуз для рейтинга)
OPTIONS = [
    ("ISTA, Австрия", 3053 * 14 / 12, "3 562 € бр.", 4, True, False, "ISTA"),
    ("Бонн, Германия", 2150, "2 000–2 300 € нетто", 4, True, False, "Боннский"),
    ("ETH Zürich", 53500 / CHF / 12, "4 805 € бр.", 3, True, False, "ETH"),
    ("EPFL", 55225 / CHF / 12, "4 960 € бр.", 3, True, False, "EPFL"),
    ("Нидерланды (Амстердам)", 3059, "3 059 € бр.", 4, True, False, "Амстердам"),
    ("Франция, contrat doctoral (Сорбонна)", 2300, "2 300 € бр.", 4, True, False, "Sorbonne"),
    ("Франция, магистратура PGSM", 1150, "1 150 €", 2, True, False, "Sorbonne"),
    ("Великобритания, UKRI (Оксфорд)", 21805 / GBP / 12, "2 137 €", 4, True, True, "Oxford"),
    ("SISSA, Италия", 16242.96 / 12, "1 354 € бр.", 1, True, False, "SISSA"),
    ("Scuola Normale, Италия", 18848 / 12, "1 571 € бр.", 1, True, False, "Scuola Normale"),
    ("Bocconi, Италия", 27000 / 12, "2 250 € бр.", 1, True, False, "Bocconi"),
    ("Stipendium Hungaricum (ELTE)", 160000 / HUF, "380–490 €", 1, True, False, "ELTE"),
    ("Сколтех", 75000 / RUB, "от 793 €", 4, False, True, "Сколтех"),
    ("МФТИ", 25000 / RUB, "264 €", 4, False, True, "МФТИ"),
]

rows = []
for name, pay, pay_l, spouse, visa, lang, uni in OPTIONS:
    a, al = place("arwu", uni)
    q, ql = place("qs", uni)
    rows.append(dict(name=name, pay=pay, pay_l=pay_l, spouse=spouse, visa=visa, lang=lang,
                     rating=(a + q) / 2, rating_l=f"{al} / {ql}".replace("-", "–")))

CRIT = [  # (заголовок, ключ, больше = лучше, подпись ячейки)
    ("Выплата\nв месяц", "pay", True, lambda r: r["pay_l"]),
    ("Супруг", "spouse", True, lambda r: SPOUSE[r["spouse"]]),
    ("Виза", "visa", False, lambda r: "нужна" if r["visa"] else "не нужна"),
    ("Язык\nстраны", "lang", True, lambda r: "русский" if r["name"] in ("МФТИ", "Сколтех")
     else ("английский" if r["lang"] else "местный")),
    ("Рейтинг по математике\nARWU / QS", "rating", False, lambda r: r["rating_l"]),
]
ranks = np.array([rankdata([-r[k] if hi else r[k] for r in rows]) for _, k, hi, _ in CRIT]).T
mean = ranks.mean(axis=1)
total = rankdata(mean)
order = np.argsort(mean, kind="stable")

n = len(rows)


def shade(rank):
    t = (rank - 1) / (n - 1)
    a, b = np.array(to_rgb(DARK)), np.array(to_rgb(LIGHT))
    return a + (b - a) * t


fig, ax = plt.subplots(figsize=(11, 7.4), dpi=200)
fig.patch.set_facecolor(SURFACE); ax.set_facecolor(SURFACE)
W = [1.55, 1.25, 0.9, 0.95, 1.6, 0.9]
X = np.concatenate([[0], np.cumsum(W)])
for row_i, i in enumerate(order):
    y = row_i
    for j, (_, _, _, lab) in enumerate(CRIT):
        rk = ranks[i, j]
        c = shade(rk)
        ax.add_patch(plt.Rectangle((X[j] + 0.03, y + 0.06), W[j] - 0.06, 0.88, color=c, lw=0))
        ink = "#ffffff" if rk <= n * 0.55 else TEXT
        ax.text(X[j] + W[j] / 2, y + 0.5, lab(rows[i]), ha="center", va="center", fontsize=8, color=ink)
    j = len(CRIT)
    ax.add_patch(plt.Rectangle((X[j] + 0.03, y + 0.06), W[j] - 0.06, 0.88, color=shade(total[i]), lw=0))
    ink = "#ffffff" if total[i] <= n * 0.55 else TEXT
    ax.text(X[j] + W[j] / 2, y + 0.5, (f"{int(total[i])}" if total[i] == int(total[i]) else f"{int(total[i])}–{int(total[i]) + 1}") + f"  ({mean[i]:.1f})".replace(".", ","),
            ha="center", va="center", fontsize=8.5, color=ink, fontweight="bold")
    ax.text(-0.08, y + 0.5, rows[i]["name"], ha="right", va="center", fontsize=9, color=TEXT)
for j, (h, *_) in enumerate(CRIT + [("Итог: место\n(средний ранг)",)]):
    ax.text(X[j] + W[j] / 2, -0.25, h, ha="center", va="bottom", fontsize=8.5, color=TEXT2)
ax.set_xlim(-3.1, X[-1] + 0.05); ax.set_ylim(n + 0.1, -1.1)
ax.set_axis_off()
ax.set_title("Варианты аспирантуры по пяти критериям: чем темнее ячейка, тем выше ранг",
             loc="left", fontsize=13, color=TEXT, x=-0.0, pad=4)
fig.text(0.02, 0.015,
         "Ранги по каждому критерию от 1 (лучший) до 14, равные значения делят ранг. Итог: среднее пяти рангов с равными весами.\n"
         "Выплата брутто и нетто сравнивается приблизительно. Рейтинги 2026 года; вуз, которого нет в списке, ставится за его конец.\n"
         "Для страны в скобках указан вуз, чьё место взято. Курсы ЕЦБ и Банка России на 02.10.2026.",
         fontsize=7.5, color=TEXT2)
fig.subplots_adjust(left=0.01, right=0.99, top=0.93, bottom=0.1)
fig.savefig("Аспирантура — критерии и ранги.png", facecolor=SURFACE)

for i in order:
    print(f"{rows[i]['name']:40s} {ranks[i]} mean={mean[i]:.2f} total={total[i]}")
# устойчивость: итог без одного критерия
for j, (h, *_) in enumerate(CRIT):
    m = np.delete(ranks, j, axis=1).mean(axis=1)
    top = [rows[i]["name"] for i in np.argsort(m, kind="stable")[:4]]
    print("без", h.replace("\n", " "), "->", top)
