import geopandas as gpd
import matplotlib.pyplot as plt
import ctypes
import numpy as np
plt.rcParams["font.family"] = "serif"


# Screen dimensions for window placement
user32 = ctypes.windll.user32
screen_width = user32.GetSystemMetrics(0)
screen_height = user32.GetSystemMetrics(1)
half_width = screen_width // 2

# Load shapefile
nuts1 = gpd.read_file("NUTS1_Jan_2018_SGCB_in_the_UK.shp")

# Map NUTS codes to LDZ
ldz_map = {
    'UKC': 'NO', 'UKD': 'NW', 'UKE': 'NE', 'UKF': 'EM', 'UKG': 'WM',
    'UKH': 'EA', 'UKI': 'NT', 'UKJ': 'SO & SE', 'UKK': 'SW',
    'UKL': 'WS & WN', 'UKM': 'SC',
}
nuts1['LDZ'] = nuts1['nuts118cd'].map(ldz_map)

# --- HEATMAP DATA ---
# Replace these values with your actual data
heatmap_data = {
    'NO': 500,
    'NW': 500,
    'NE': 500,
    'EM': 1000,
    'WM': 500,
    'EA': 1000,
    'NT': 0,
    'SO & SE': 1000,
    'SW': 1500,
    'WS & WN': 0,
    'SC': 1000
}

# Add the data to the dataframe
nuts1['Capacity'] = nuts1['LDZ'].map(heatmap_data)

# Create Figure
fig, ax = plt.subplots(figsize=(12, 14))

# Position the window on the right half of the screen


# Plot the Heatmap
# 'Greens' matches your reference image. Use 'edgecolor' for the borders.
ax=nuts1.plot(
    column='Capacity', 
    ax=ax, 
    cmap='Reds', 
    edgecolor='gray', 
    linewidth=0.8,
    legend=True,
    legend_kwds={'label': "Installed Capacity (MW)", 'orientation': "vertical"}
)
ax.figure.axes[1].set_ylabel("Installed Capacity (MW)", fontsize=15, weight='bold')

# 3. Optional: Change the tick label sizes (the numbers on the bar)
ax.figure.axes[1].tick_params(labelsize=12)
# Add numeric labels to each region
for idx, row in nuts1.iterrows():
    # Only label regions that have a valid geometry
    if row['geometry']:
        centroid = row['geometry'].centroid
        # Display the capacity value in the center of the region
        val = row['Capacity']
        ax.text(
            centroid.x, centroid.y, 
            f"{int(val) if not np.isnan(val) else 0}", 
            fontsize=11, 
            ha='center', 
            va='center',
            color='black'
        )

# Final Touches
ax.set_title("Installed BGCCS Capacity per Region (MW)", fontsize=18, color='red')
ax.axis('off')

plt.tight_layout()
plt.show()