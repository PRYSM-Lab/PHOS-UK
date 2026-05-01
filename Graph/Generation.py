import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'serif'

# Years for the x-axis
years = [2030, 2035, 2040, 2045, 2050]

# Replace these lists with your actual data for each technology
data = {
    "CCGTCCS": [33, 39, 53, 60,60],
    "CCGT": [15, 16.5, 9, 5, 0],
    "H2CCGT": [0.5, 0.5, 1, 1,1],
    "LeadBat": [10, 17, 21, 24, 39],
    "Nuclear": [124, 130, 145, 160, 168],
    "Solar": [55, 70, 70, 73, 89],
    "WindOff": [130, 185, 225, 236, 241],
    "WindOn": [47, 63, 78, 93, 108],
    "Hydro": [5, 5, 5, 5, 5]
}

# Define colors to match your image as closely as possible
colors = [
    "#FF0000", # CCGTCCS - Grey
    "#8b0000", # CCGT - Black
    "#8000FF", # H2CCGT - Orange
    "#00FFFF", # LeadBat - Red/Coral
    "#0000FF", # Nuclear - Purple
    "#FFFF00", # Solar - Yellow
    "#228b22", # WindOff - SeaGreen
    "#00FF00", # WindOn - LightGreen
    "#1F77B4"  # Hydro - Blue
]

# Create the plot
fig, ax = plt.subplots(figsize=(10, 6))

# Stackplot generates the filled areas
ax.stackplot(years, data.values(), labels=data.keys(), colors=colors)

# Formatting the visual elements
#ax.set_title("Projected Energy Generation (TWh)")
ax.set_ylabel("Electricity Generation (TWh)", fontsize=16, fontweight='bold')
ax.set_xlabel("Year", fontsize=16, fontweight='bold')
ax.set_xlim(2030, 2050)
ax.set_xticks(years)
ax.grid(axis="y", linestyle="--", alpha=0.7)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
# Move the legend to the bottom and arrange in columns
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.1), ncol=5, frameon=False, fontsize=13)

plt.tight_layout()
plt.show()