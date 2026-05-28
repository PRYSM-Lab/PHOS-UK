# %%
import pandas as pd
import numpy as np
from numpy import unravel_index
from sklearn.cluster import KMeans
from collections import Counter, defaultdict
from scipy.stats import gaussian_kde
from scipy.interpolate import interp1d
from collections import Counter
import matplotlib.pyplot as plt

#%% Load the data
data = pd.read_csv('Clustering_Data_2017.csv') 
yeardays = 365
num_rows = len(data)

# Generate a datetime range that matches the number of rows in your data
date_range = pd.date_range(start='2017-01-01 00:00:00',  end='2017-12-31 23:00:00', freq='60min')


# Create a copy of the original data and add the datetime index
df = data.copy()
df['datetime'] = date_range
df = df.set_index('datetime')

#%%  Finding peak day
def find_peak_day(data, column):
    """
    Find the index of the peak day for a given column.
    """
    peak_day_index = df[column].idxmax()
    return peak_day_index

def find_peak_day_for_gas(data, gas_columns):
    """
    Find the index of the peak day for gas usage given a list of gas columns.
    """
    peak_day_index = df[gas_columns].sum(axis=1).idxmax()
    return peak_day_index

def find_peak_day_for_multiple_gas_types(data, gas_types):
    """
    Find the peak day index for multiple types of gas (Domestic, Services, Industrial).
    """
    peak_days = {}
    for gas_type, columns in gas_types.items():
        peak_days[gas_type] = find_peak_day_for_gas(df, columns)
    return peak_days

def remove_peak_day(data, peak_day_index):
    """
    Remove rows for the peak day from the DataFrame.
    """
    df_nopeak = df.copy()
    peak_date = peak_day_index.date()
    df_nopeak = df_nopeak.loc[df_nopeak.index.date != peak_date]
    return df_nopeak


# Define the columns for different gas types
gas_cols = ['EA', 'EM', 'NE', 'NO', 'NT', 
                     'NW', 'SC', 'SE', 'SO', 'SW', 
                     'WM', 'WN', 'WS']


# Find the peak day for electricity
electricity_peak_day = find_peak_day(data, 'Elec')
print('Electricity peak day index =', electricity_peak_day)

# Find the peak day for gas types
gas_types = {
    'gas': gas_cols,
}

peak_days = find_peak_day_for_multiple_gas_types(df, gas_types)
for gas_type, peak_day in peak_days.items():
    print(f'{gas_type} peak day index =', peak_day)

# Remove the peak day from the DataFrame
df_nopeak = remove_peak_day(data, electricity_peak_day)


# %% 
def find_peak_date(df, column):
    """
    Find the date of the peak value for a given column.
    """
    peak_datetime = pd.to_datetime(df[column].idxmax())
    peak_date = peak_datetime.date()
    return peak_date

# Assuming df is your DataFrame and 'Elec' is the column name
electricity_peak_date = find_peak_date(df, 'Elec')
print('Electricity peak date =', electricity_peak_date)
# %% Reshape each column of the DataFrame into a (yeardays, 24) array (days x 24 hours)
days = [data[col].values.reshape(yeardays, 24) for col in data]

# Find the index of the peak electricity day
peakELEC = unravel_index(data['Elec'].values.reshape(yeardays, 24).argmax(), 
                         data['Elec'].values.reshape(yeardays, 24).shape)[0]

# Remove the peak electricity day from the dataset
DaysNoPeak = np.delete(days, peakELEC, axis=1)

# Find the maximum non-peak day value for each attribute
DaysMax = [DaysNoPeak[i].max() for i in range(len(days))]

# Normalize the attributes for all remaining days (0, 1)
DaysNormalised = [DaysNoPeak[i] / DaysMax[i] for i in range(len(DaysNoPeak))]

# %% Array with rows each day and columns each hour of each attribute (yeardays, 24*70)

def concatenate_normalized_days(DaysNormalised):
    
    return np.concatenate(DaysNormalised, axis=1)

def concatenate_days(days):
    
    return np.concatenate(days, axis=1)

# Assuming 'days' and 'days_normalized' are already defined
# Concatenate normalized days
data_new = concatenate_normalized_days(DaysNormalised)

# Concatenate non-normalized days
days_new = concatenate_days(days)

# %% 
def run_kmeans_clustering(data, n_clusters, max_iter=2000, random_state=40):
    """
    Run KMeans clustering on the given data.
    """
    kmeans = KMeans(n_clusters=n_clusters, init='k-means++', max_iter=max_iter, random_state=random_state).fit(data)
    centroids = kmeans.cluster_centers_
    print('inertia=', kmeans.inertia_)  # Print inertia
    return kmeans, centroids

def count_days_in_clusters(kmeans):
    """
    Count the number of days in each cluster using KMeans labels.
    """
    nDays = Counter(kmeans.labels_)
    return sorted(nDays.items())  # Sort the days by cluster label

def get_days_per_cluster(kmeans):
    """
    Get the days (indices) that belong to each cluster.
    """
    return {i: np.where(kmeans.labels_ == i)[0] for i in range(kmeans.n_clusters)}

def calculate_cluster_weights(nDays):
    """
    Calculate the weights for each cluster based on the number of days.
    """
    weights = [nDays[v][1] for v in range(len(nDays))]
    return weights

def extract_daily_centroids(centroids, days_no_peak_length):
    """
    Extract daily centroids from the full centroid array.
    """
    return [centroids[:, i*24:24*(1+i)] for i in range(days_no_peak_length)]


n_clusters = int(input("Press Input number of cluster: ")) 

kmeans, centroids = run_kmeans_clustering(data_new, n_clusters=n_clusters)

nDays = count_days_in_clusters(kmeans)

z = get_days_per_cluster(kmeans)

weights = calculate_cluster_weights(nDays)

DaysCentroids = extract_daily_centroids(centroids, len(DaysNoPeak))


# %% Calculate the centroids means and item means for non- peak days

def calculate_centroids_means(days_centroids, days_no_peak_length):
    
    return np.vstack([days_centroids[i].mean(axis=1) for i in range(days_no_peak_length)])

def calculate_items_mean(days_normalized, days_no_peak_length):
    
    return np.vstack([days_normalized[i].mean(axis=1) for i in range(days_no_peak_length)])


centroids_means = calculate_centroids_means(DaysCentroids, len(DaysNoPeak))
items_mean = calculate_items_mean(DaysNormalised, len(DaysNoPeak))

# %% 
df.columns[7:20]
#%% Find representative days and weights

def representative_day(centroid_means, items_mean, z, n_clusters):
    """
    Find the representative day for each cluster by comparing the centroid means with the actual daily data.
    """
    rep_days = []
    
    for clu in range(n_clusters):
        # Extract the mean centroid values for the current cluster (transpose to match day-wise comparison)
        centroid_cluster = centroid_means.transpose()[clu]
        
        # Select the actual days assigned to this cluster from the items_mean array
        cluster_days_data = items_mean.transpose()[z[clu]]
        
        # Focus on gas columns (7 to 20) and calculate the difference with centroid
        gas_diff = centroid_cluster[7:20] - cluster_days_data[:, 7:20]
        
        # Find the day with the smallest positive sum of differences
        # Use np.inf for negative values to ensure they're not selected
        positive_sum_diff = np.where(gas_diff.sum(axis=1) > 0, gas_diff.sum(axis=1), np.inf)
        
        # Find the index of the day with the smallest positive difference and append to the result list
        representative_day_idx = np.argmin(positive_sum_diff)
        rep_days.append(z[clu][representative_day_idx])
    
    return rep_days

rep_days = representative_day(centroids_means, items_mean, z, n_clusters)


# Output the representative days
print("Representative days for each cluster:", rep_days)
print("Weights for each cluster:", weights)


# %%
# Find cluster, representative days and weights
def add_peak_day(rep_days, weights, peak_elec, n_clusters):
    """
    Add the peak electricity day to the representative days and adjust weights.
    """
    # Insert peak electricity day at the beginning of representative days list
    rep_days.insert(0, peak_elec)
    
    # Insert a weight of 1 for the peak electricity day at the beginning of weights list
    weights.insert(0, 1)
    
    # Create a DataFrame with cluster IDs, representative days, and weights
    clusters_df = pd.DataFrame({
        "Cluster_iD": range(n_clusters + 1),  # Including peak electricity day
        "Repres_Days": rep_days,
        "Weights": pd.Series(weights)
    })
    
    return clusters_df

# Example usage based on your previous variables
clusters_df = add_peak_day(rep_days, weights, peakELEC, n_clusters)

# Output the resulting DataFrame
print(clusters_df)
# %%
clusters_df["Cluster_iD"]=range(n_clusters+1)
DaysFinal= [pd.DataFrame(days_new[rep_days,i*24:24*(1+i)], 
                         index=range(len(rep_days)),columns=range(24)) for i in range(0,len(DaysNormalised))]

# %%  Build the cluster profile
# Build the cluster profile
'''
def select_representative_day(Cluster_iD, clusters_df, df, df_nopeak, peak_ids):
    """
    Select the representative day data based on cluster ID and whether it is a peak day or not.
    """
    rep_day = clusters_df.loc[clusters_df['Cluster_iD'] == Cluster_iD, 'Repres_Days'].values[0]
    if Cluster_iD in peak_ids:
        return df.iloc[rep_day * 24:(rep_day + 1) * 24]  # روز پیک را از df انتخاب کن
    else:
        return df_nopeak.iloc[rep_day * 24:(rep_day + 1) * 24]  # روزهای غیرپیک را از df_nopeak انتخاب کن

def create_clustered_profiles(clusters_df, df, df_nopeak, peak_ids, n_clusters):
    """
    Create a DataFrame with clustered profiles.
    """
    M_profiles = []
    
    for iD in clusters_df['Cluster_iD']:
        M_profiles.append(select_representative_day(iD, clusters_df, df, df_nopeak, peak_ids))
    
    
    index_tuples = list(zip(np.array([np.repeat(i+1, 24) for i in range(n_clusters)]).ravel(),
                        np.tile(np.arange(1, 25), n_clusters)))

    
    df_clustered_profiles = pd.DataFrame(
        index=index_tuples,
        columns=df.columns,
        data=pd.concat(M_profiles, axis=0).values
    )
    
    return df_clustered_profiles


def create_clusters_df(kmeans, n_clusters):
    """
    Create a DataFrame containing the cluster labels and representative days.
    """
    cluster_labels = kmeans.labels_
    clusters_df = pd.DataFrame({
        'Cluster_iD': range(n_clusters),
        'Repres_Days': [np.where(cluster_labels == i)[0][0] for i in range(n_clusters)]  # Assign the first day as the representative day
    })
    return clusters_df

# Now, create clusters_df
clusters_df = create_clusters_df(kmeans, n_clusters)
peak_ids = [0]  # Only one peak
df_clustered_profiles = create_clustered_profiles(clusters_df, df, df_nopeak, peak_ids, n_clusters)

# Output the resulting DataFrame
print(df_clustered_profiles)
'''
# Build the cluster profile
def select_representative_day(Cluster_iD, clusters_df, df, df_nopeak, peak_ids):
    """
    Select the representative day data based on cluster ID and whether it is a peak day or not.
    """
    rep_day = clusters_df.loc[clusters_df['Cluster_iD'] == Cluster_iD, 'Repres_Days'].values[0]
    if Cluster_iD in peak_ids:
        return df.iloc[rep_day * 24:(rep_day + 1) * 24]
    else:
        return df_nopeak.iloc[rep_day * 24:(rep_day + 1) * 24]

def create_clustered_profiles(clusters_df, df, df_nopeak, peak_ids, n_clusters):
    """
    Create a DataFrame with clustered profiles.
    
    """
    M_profiles = []
    
    for iD in clusters_df['Cluster_iD']:
        M_profiles.append(select_representative_day(iD, clusters_df, df, df_nopeak, peak_ids))
    
    index_tuples = list(zip(np.array([np.repeat(i, 24) for i in range(n_clusters + 1)]).ravel(),
                            np.tile(range(24), n_clusters + 1)))
    
    df_clustered_profiles = pd.DataFrame(
        index=index_tuples,
        columns=df.columns,
        data=pd.concat(M_profiles, axis=0).values
    )
    
    return df_clustered_profiles

peak_ids = [0]  # Only one peak
df_clustered_profiles = create_clustered_profiles(clusters_df, df, df_nopeak, peak_ids, n_clusters)

# Output the resulting DataFrame
print(df_clustered_profiles)
# %% 
def save_to_excel(clusters_df, weights, clustered_profiles_df, year_range, n_clusters):
    """
    Save the clusters and clustered profiles DataFrames to an Excel file.
    """
    clusters_df['Cluster_iD'] = range(1, len(clusters_df) + 1)
    
    # Convert weights from a list to a DataFrame
    weights_df = pd.DataFrame({'Cluster': range(1, len(weights) + 1), 'Weight': weights})

    # Adjust the index for the clustered_profiles_df
    min_i, min_j = min(clustered_profiles_df.index)[0], min(clustered_profiles_df.index)[1]
    clustered_profiles_df.index = [(i - min_i + 1, j - min_j + 1) for i, j in clustered_profiles_df.index.to_list()]

    file_name = f"{year_range}Cluster_{n_clusters}.xlsx"
    
    with pd.ExcelWriter(file_name) as writer:
        clusters_df.to_excel(writer, sheet_name='NDaysCluster', index=False)
        weights_df.to_excel(writer, sheet_name='NDaysCluster', index=False)  # Save weights to a separate sheet
        clustered_profiles_df.to_excel(writer, sheet_name='ClusteredProfiles', index=True)
        
    print(f"Data has been saved to {file_name}")

# Call the function with the correct arguments
save_to_excel(clusters_df, weights, df_clustered_profiles, '2017', n_clusters)

# %%

year_range = "2017" 
 

input_file = f"{year_range}Cluster_{n_clusters}.xlsx"
sheet_name = "ClusteredProfiles" 

df = pd.read_excel(input_file, sheet_name=sheet_name, header=1)

df_first_sheet = pd.read_excel(input_file, sheet_name=0)  

df_second_sheet = pd.read_excel(input_file, sheet_name=1) 


columns_second_sheet = [df_second_sheet.columns[0]] + ['EA', 'EM', 'NE', 'NO', 'NT', 'NW', 'SC', 'SE', 'SO', 'SW', 'WM', 'WN', 'WS']
df_second_sheet = df_second_sheet[columns_second_sheet]


df_second_sheet1 = pd.read_excel(input_file, sheet_name=1)    

columns_third_sheet_range = df_second_sheet1.iloc[:, [0] + list(range(21, 60))]


output_file = "Final_cluster.xlsx"  # فایل خروجی

with pd.ExcelWriter(output_file) as writer:
   
   df_first_sheet.to_excel(writer,sheet_name="Cluster and weights", index=False) 
   df_second_sheet.to_excel(writer, sheet_name="Demand", index=False)
   columns_third_sheet_range.to_excel(writer, sheet_name="Availability", index=False)






