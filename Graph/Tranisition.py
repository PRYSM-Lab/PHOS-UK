import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.family'] = 'serif'

years = ['2030', '2035','2040','2045', '2050']
categories = ['Electricity', 'H2', 'Heating']

# ======================
# دیتای واقعی (ساختار درست)
# ======================
data = {
    '2030': {
        'Electricity': {
            'Solar': 39,
            'Wind Onshore': 15,
            'Wind Offshore': 35,
            'Battery': 30,
            'Nuclear': 15,
            'H2CCGT': 10,
            'FC': 0,
            'CCGT': 33,
            'CCGTCCS': 10,
            'BECCS': 0,
            'Biomass': 3.5,
        },
        'H2': {
            'WE': 0,
            'SMRCCS': 10,
            'ATRCCS': 10,
            'BGCCS': 3.5
        },
        'Heating': {
            'ASHP': 70,
            'HyBoiler': 24,
            'Gas Boiler': 83
        }
    },
    
    '2035': {
        'Electricity': {
            'Solar': 50,
            'Wind Onshore': 20,
            'Wind Offshore': 50,
            'Battery': 45,
            'Nuclear': 18,
            'H2CCGT': 20,
            'CCGT': 33,
            'CCGTCCS': 15,
            'FC': 0,
            'BECCS': 0,
            'Biomass': 3.5,
        },
        'H2': {
            'WE': 0,
            'SMRCCS': 20,
            'ATRCCS': 20,
            'BGCCS': 3.5
        },
        'Heating': {
            'ASHP': 150,
            'HyBoiler': 32,
            'Gas Boiler': 10
        }
    },
    
    
    

    '2040':{
        'Electricity': {
            'Solar': 50,
            'Wind Onshore': 26,
            'Wind Offshore': 60,
            'Battery': 60,
            'Nuclear': 19,
            'H2CCGT': 30,
            'FC': 0,
            'CCGT': 33,
            'CCGTCCS': 20,
            'BECCS': 0,
            'Biomass': 3.5,
        },
        'H2': {
            'WE': 1,
            'SMRCCS': 30,
            'ATRCCS': 30,
            'BGCCS': 4.5
        },
        'Heating': {
            'ASHP': 162,
            'HyBoiler': 52,
            'Gas Boiler': 0}
        },
    '2045': {
        'Electricity': {
            'Solar': 53,
            'Wind Onshore': 28,
            'Wind Offshore': 67,
            'Battery': 60,
            'Nuclear': 21,
            'H2CCGT': 40,
            'CCGT': 33,
            'CCGTCCS': 25,
            'FC': 5,
            'BECCS': 0,
            'Biomass': 3.5,
        },
        'H2': {
            'WE': 1,
            'SMRCCS': 38,
            'ATRCCS': 40,
            'BGCCS': 6
        },
        'Heating': {
            'ASHP': 177,
            'HyBoiler': 67,
            'Gas Boiler': 83
        }
    },


    '2050': {
        'Electricity': {
            'Solar': 68,
            'Wind Onshore': 35,
            'Wind Offshore': 75,
            'Battery': 60,
            'Nuclear': 24,
            'H2CCGT': 49,
            'FC': 15,
            'CCGT': 0,
            'CCGTCCS': 30,
           
            'BECCS': 0,
            'Biomass': 3.5,
        },
        'H2': {
            'WE': 1,
            'SMRCCS': 49,
            'ATRCCS': 50,
            'BGCCS': 7.5
        },
        'Heating': {
            'ASHP': 182,
            'HyBoiler': 99,
            'Gas Boiler': 0
        }
        }
}

# ======================
# colormap جدا برای هر سکتور
# ======================
# ======================
# تعریف رنگ‌های اختصاصی (اصلاح شده)
# ======================

# ۱. رنگ‌های بخش الکتریسیته
labels_e = ["Solar","Wind Onshore","Wind Offshore","Battery","CCGT","Nuclear","H2CCGT","FC","BECCS","CCGTCCS","Biomass"]
colors_e = ["#FFFF00","#00FF00","#228b22","#00FFFF","#8b0000","#0000FF","#8000FF","#FF00FF","#FF0080","#FF0000","#ffa54f"]

# ۲. رنگ‌های بخش هیدروژن
labels_h2 = ["SMRCCS","ATRCCS","BGCCS","WE"]
colors_h2 = ["#6c7b8b", "#9fb6cd", "#96cdcd","#afeeee"]

# ۳. رنگ‌های بخش گرمایش
labels_ht = ["HyBoiler", "ASHP", "Gas Boiler"]
colors_ht = ["#8b5a00", "#cd8500", "#5d4037"] # رنگ سوم برای Gas Boiler اصلاح شد

# ایجاد دیکشنری نهایی رنگ‌ها
colors = {}
colors.update(dict(zip(labels_e, colors_e)))
colors.update(dict(zip(labels_h2, colors_h2)))
colors.update(dict(zip(labels_ht, colors_ht)))

# ======================
# ادامه کد رسم (بدون تغییر نسبت به قبل)
# ======================
# ======================
# موقعیت
# ======================
x = np.arange(len(years)) * 2.5
width = 0.4

fig, ax = plt.subplots(figsize=(10,9))

# برای legend جدا
legend_e = {}
legend_h2 = {}
legend_ht = {}

# ======================
# رسم
# ======================
for i, year in enumerate(years):
    for j, cat in enumerate(categories):
        xpos = x[i] + (j - 1) * width * 1.2

        bottom = 0
        for tech, value in data[year][cat].items():
            bar = ax.bar(
                xpos,
                value,
                width,
                bottom=bottom,
                color=colors[tech],
                edgecolor='black',
                linewidth=0.3
            )

            # ذخیره برای legend جدا
            if cat == 'Electricity' and tech not in legend_e:
                legend_e[tech] = bar
            elif cat == 'H2' and tech not in legend_h2:
                legend_h2[tech] = bar
            elif cat == 'Heating' and tech not in legend_ht:
                legend_ht[tech] = bar

            bottom += value

# ======================
# محور x
# ======================
all_positions = []
all_labels = []

for i, year in enumerate(years):
    for j, cat in enumerate(categories):
        xpos = x[i] + (j - 1) * width * 1.3
        all_positions.append(xpos)
        all_labels.append(cat)

ax.set_xticks(all_positions)
ax.set_xticklabels(all_labels, rotation=90,  fontsize=14)

# سال‌ها
for i, year in enumerate(years):
    ax.text(
        x[i],
        -0.2 * ax.get_ylim()[1],
        
        year,
        ha='center',
        va='top',
        fontsize=16,
        fontweight='bold'
    )

# ======================
# legend های جدا (حرفه‌ای)
# ======================
leg1 = ax.legend(
    [legend_e[k][0] for k in legend_e],
    legend_e.keys(),
    title='Electricity',
    loc='upper right',
    bbox_to_anchor=(1.28, 0.8),
    fontsize=11,
    frameon=False
)
leg1.get_title().set_fontweight('bold')
leg2 = ax.legend(
    [legend_h2[k][0] for k in legend_h2],
    legend_h2.keys(),
    title='H2', 
    loc='upper right',
    bbox_to_anchor=(1.24, 0.35),
    fontsize=11,
    frameon=False
)
leg2.get_title().set_fontweight('bold')
leg3 = ax.legend(
    [legend_ht[k][0] for k in legend_ht],
    legend_ht.keys(),
    title='Heating',
    loc='upper right',
    bbox_to_anchor=(1.25, 0.15),
    fontsize=11,
    frameon=False
)
leg3.get_title().set_fontweight('bold')
ax.add_artist(leg1)
ax.add_artist(leg2)

# ======================
# استایل
# ======================
ax.set_ylabel('Installed capacity (GW)', fontsize=18,fontweight='bold')

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.show()