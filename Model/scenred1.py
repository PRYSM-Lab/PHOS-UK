import pandas as pd
import numpy as np
import os
import sys

num_scenarios = int(sys.argv[1])
#global num_scenarios
#num_scenarios = int(input("Press Input number of scenario: ")) 



def select_scenarios_with_refined_probabilities(data, num_scenarios):
    """
    Select scenarios dynamically and compute meaningful probabilities.
    :param data: Array of possible scenarios (columns represent scenarios, rows represent features).
    :param num_scenarios: Number of scenarios to reduce to.
    :return: Selected reduced scenarios and their probabilities.
    """
    selected_indices = []  # Indices of selected scenarios
    remaining_indices = list(range(data.shape[1]))  # All scenario indices

    # Select scenarios dynamically based on diversity
    for _ in range(num_scenarios):
        best_index = None
        best_score = float('-inf')

        for index in remaining_indices:
            scenario = data[:, index]  # Extract the column (scenario)
            # Compute the minimum distance to previously selected scenarios for diversity
            score = np.min([np.linalg.norm(scenario - data[:, i]) for i in selected_indices]) if selected_indices else np.linalg.norm(np.mean(data, axis=1) - scenario)

            if score > best_score:  # Maximize diversity
                best_index = index
                best_score = score

        selected_indices.append(best_index)
        remaining_indices.remove(best_index)  # Remove selected index

    # Compute distances for the selected scenarios relative to the mean
    target = np.mean(data, axis=1)  # Target scenario (mean of rows)
    distances = np.array([np.linalg.norm(data[:, index] - target) for index in selected_indices])

    # Compute probabilities directly proportional to inverse distances
    probabilities = 1 / (distances + 1e-6)  # Avoid division by zero
    probabilities /= probabilities.sum()  # Normalize probabilities to sum to 1

    # Retrieve the selected scenarios
    selected_scenarios = data[:, selected_indices]

    return selected_scenarios, probabilities

file_path = os.path.join(os.getcwd(), 'Step2_1.xlsx')
excel_data = pd.ExcelFile(file_path, engine='openpyxl')
df_renewable = excel_data.parse('renewables', header=None, usecols="D:UPP", skiprows=2, nrows=360)
df_renewable1 = excel_data.parse('renewables', header=None, usecols="A:UPP", skiprows=2, nrows=360)

data1 = df_renewable.to_numpy()

num_regions = 13
num_scenarios = num_scenarios 

total_scenarios = data1.shape[1] // num_regions  # =1125

region_data_list = []

for region in range(num_regions):
    region_columns = [i for i in range(region, data1.shape[1], num_regions)]
    region_matrix = data1[:, region_columns]  # shape = (288, 1125)
    region_data_list.append(region_matrix)

selected_scenarios_list = []
probabilities_list = []

for region_data in region_data_list:
    selected_scenarios, probabilities = select_scenarios_with_refined_probabilities(region_data, num_scenarios)
    selected_scenarios_list.append(selected_scenarios)
    probabilities_list.append(probabilities)

final_selected_scenarios = np.concatenate(selected_scenarios_list, axis=1)

first_two_columns = df_renewable1.iloc[:, :3]
first_two_columns_reduced = first_two_columns.iloc[:360, :]

reduced_scenarios_df = pd.DataFrame(
    final_selected_scenarios,
    columns=[f"Region{r+1}_Scenario{s+1}" for r in range(num_regions) for s in range(num_scenarios)]
)

final_df = pd.concat([first_two_columns_reduced, reduced_scenarios_df.reset_index(drop=True)], axis=1)

base_dir = os.path.dirname(file_path)
output_file_path = os.path.join(base_dir, 'Renewable.xlsx')

with pd.ExcelWriter(output_file_path, engine='openpyxl') as writer:
    final_df.to_excel(writer, index=False, sheet_name='renewable')

print("Reduced scenarios saved successfully to:", output_file_path)
#%%
import pandas as pd
import numpy as np
import os

def select_scenarios_with_refined_probabilities(data1, num_scenarios):
    """
    Select scenarios dynamically and compute meaningful probabilities.
    :param data: Array of possible scenarios (columns represent scenarios, rows represent features).
    :param num_scenarios: Number of scenarios to reduce to.
    :return: Selected reduced scenarios and their probabilities.
    """
    selected_indices = []  # Indices of selected scenarios
    remaining_indices = list(range(data1.shape[1]))  # All scenario indices

    # Select scenarios dynamically based on diversity
    for _ in range(num_scenarios):
        best_index = None
        best_score = float('-inf')

        for index in remaining_indices:
            scenario = data1[:, index]  # Extract the column (scenario)
            # Compute the minimum distance to previously selected scenarios for diversity
            score = np.min([np.linalg.norm(scenario - data1[:, i]) for i in selected_indices]) if selected_indices else np.linalg.norm(np.mean(data1, axis=1) - scenario)

            if score > best_score:  # Maximize diversity
                best_index = index
                best_score = score

        selected_indices.append(best_index)
        remaining_indices.remove(best_index)  # Remove selected index

    # Compute distances for the selected scenarios relative to the mean
    target = np.mean(data1, axis=1)  # Target scenario (mean of rows)
    distances = np.array([np.linalg.norm(data1[:, index] - target) for index in selected_indices])

    # Compute probabilities directly proportional to inverse distances
    probabilities = 1 / (distances + 1e-6)  # Avoid division by zero
    probabilities /= probabilities.sum()  # Normalize probabilities to sum to 1

    # Retrieve the selected scenarios
    selected_scenarios = data1[:, selected_indices]

    return selected_scenarios, probabilities


file_path = os.path.join(os.getcwd(), 'Step2_1.xlsx')
excel_data1 = pd.ExcelFile(file_path, engine='openpyxl')
df_dom = excel_data1.parse('domestic', header=None, usecols="D:UPO", skiprows=2, nrows=120)
df_dom1 = excel_data1.parse('domestic', header=None, usecols="A:UPO", skiprows=2, nrows=120)

data1 = df_dom.to_numpy()

num_regions = 13
num_scenarios = num_scenarios
total_scenarios = data1.shape[1] // num_regions  # =1125

region_data_list = []

for region in range(num_regions):
    region_columns = [i for i in range(region, data1.shape[1], num_regions)]
    region_matrix = data1[:, region_columns]  # shape = (288, 1125)
    region_data_list.append(region_matrix)

selected_scenarios_list = []
probabilities_list = []

for region_data in region_data_list:
    selected_scenarios, probabilities = select_scenarios_with_refined_probabilities(region_data, num_scenarios)
    selected_scenarios_list.append(selected_scenarios)
    probabilities_list.append(probabilities)

final_selected_scenarios = np.concatenate(selected_scenarios_list, axis=1)

first_two_columns = df_dom1.iloc[:, :2]
first_two_columns_reduced = first_two_columns.iloc[:120, :]

reduced_scenarios_df = pd.DataFrame(
    final_selected_scenarios,
    columns=[f"Region{r+1}_Scenario{s+1}" for r in range(num_regions) for s in range(num_scenarios)]
)

final_df = pd.concat([first_two_columns_reduced, reduced_scenarios_df.reset_index(drop=True)], axis=1)

base_dir = os.path.dirname(file_path)
output_file_path = os.path.join(base_dir, 'Domestic.xlsx')

with pd.ExcelWriter(output_file_path, engine='openpyxl') as writer:
    final_df.to_excel(writer, index=False, sheet_name='Domestic')

print("Reduced scenarios saved successfully to:", output_file_path)
#%%
import pandas as pd
import numpy as np
import os

def select_scenarios_with_refined_probabilities(data2, num_scenarios):
    """
    Select scenarios dynamically and compute meaningful probabilities.
    :param data: Array of possible scenarios (columns represent scenarios, rows represent features).
    :param num_scenarios: Number of scenarios to reduce to.
    :return: Selected reduced scenarios and their probabilities.
    """
    selected_indices = []  # Indices of selected scenarios
    remaining_indices = list(range(data2.shape[1]))  # All scenario indices

    # Select scenarios dynamically based on diversity
    for _ in range(num_scenarios):
        best_index = None
        best_score = float('-inf')

        for index in remaining_indices:
            scenario = data2[:, index]  # Extract the column (scenario)
            # Compute the minimum distance to previously selected scenarios for diversity
            score = np.min([np.linalg.norm(scenario - data2[:, i]) for i in selected_indices]) if selected_indices else np.linalg.norm(np.mean(data2, axis=1) - scenario)

            if score > best_score:  # Maximize diversity
                best_index = index
                best_score = score

        selected_indices.append(best_index)
        remaining_indices.remove(best_index)  # Remove selected index

    # Compute distances for the selected scenarios relative to the mean
    target = np.mean(data2, axis=1)  # Target scenario (mean of rows)
    distances = np.array([np.linalg.norm(data2[:, index] - target) for index in selected_indices])

    # Compute probabilities directly proportional to inverse distances
    probabilities = 1 / (distances + 1e-6)  # Avoid division by zero
    probabilities /= probabilities.sum()  # Normalize probabilities to sum to 1

    # Retrieve the selected scenarios
    selected_scenarios = data2[:, selected_indices]

    return selected_scenarios, probabilities


file_path = os.path.join(os.getcwd(), 'Step2_1.xlsx')
excel_data2 = pd.ExcelFile(file_path, engine='openpyxl')
df_ind = excel_data2.parse('industrial', header=None, usecols="D:UPO", skiprows=2, nrows=120)
df_ind1 = excel_data2.parse('industrial', header=None, usecols="A:UPO", skiprows=2, nrows=120)

data2 = df_ind.to_numpy()

num_regions = 13
num_scenarios = num_scenarios
total_scenarios = data2.shape[1] // num_regions  # =1125

region_data_list = []

for region in range(num_regions):
    region_columns = [i for i in range(region, data2.shape[1], num_regions)]
    region_matrix = data2[:, region_columns]  # shape = (288, 1125)
    region_data_list.append(region_matrix)

selected_scenarios_list = []
probabilities_list = []

for region_data in region_data_list:
    selected_scenarios, probabilities = select_scenarios_with_refined_probabilities(region_data, num_scenarios)
    selected_scenarios_list.append(selected_scenarios)
    probabilities_list.append(probabilities)

final_selected_scenarios = np.concatenate(selected_scenarios_list, axis=1)

first_two_columns = df_ind1.iloc[:, :2]
first_two_columns_reduced = first_two_columns.iloc[:120, :]

reduced_scenarios_df = pd.DataFrame(
    final_selected_scenarios,
    columns=[f"Region{r+1}_Scenario{s+1}" for r in range(num_regions) for s in range(num_scenarios)]
)

final_df = pd.concat([first_two_columns_reduced, reduced_scenarios_df.reset_index(drop=True)], axis=1)

base_dir = os.path.dirname(file_path)
output_file_path = os.path.join(base_dir, 'Industrial.xlsx')

with pd.ExcelWriter(output_file_path, engine='openpyxl') as writer:
    final_df.to_excel(writer, index=False, sheet_name='Industrial')

print("Reduced scenarios saved successfully to:", output_file_path)



#%%
import pandas as pd
import numpy as np
import os

def select_scenarios_with_refined_probabilities(data3, num_scenarios):
    """
    Select scenarios dynamically and compute meaningful probabilities.
    :param data: Array of possible scenarios (columns represent scenarios, rows represent features).
    :param num_scenarios: Number of scenarios to reduce to.
    :return: Selected reduced scenarios and their probabilities.
    """
    selected_indices = []  # Indices of selected scenarios
    remaining_indices = list(range(data3.shape[1]))  # All scenario indices

    # Select scenarios dynamically based on diversity
    for _ in range(num_scenarios):
        best_index = None
        best_score = float('-inf')

        for index in remaining_indices:
            scenario = data3[:, index]  # Extract the column (scenario)
            # Compute the minimum distance to previously selected scenarios for diversity
            score = np.min([np.linalg.norm(scenario - data3[:, i]) for i in selected_indices]) if selected_indices else np.linalg.norm(np.mean(data3, axis=1) - scenario)

            if score > best_score:  # Maximize diversity
                best_index = index
                best_score = score

        selected_indices.append(best_index)
        remaining_indices.remove(best_index)  # Remove selected index

    # Compute distances for the selected scenarios relative to the mean
    target = np.mean(data3, axis=1)  # Target scenario (mean of rows)
    distances = np.array([np.linalg.norm(data3[:, index] - target) for index in selected_indices])

    # Compute probabilities directly proportional to inverse distances
    probabilities = 1 / (distances + 1e-6)  # Avoid division by zero
    probabilities /= probabilities.sum()  # Normalize probabilities to sum to 1

    # Retrieve the selected scenarios
    selected_scenarios = data3[:, selected_indices]

    return selected_scenarios, probabilities


file_path = os.path.join(os.getcwd(), 'Step2_1.xlsx')
excel_data3 = pd.ExcelFile(file_path, engine='openpyxl')
df_serv = excel_data3.parse('services', header=None, usecols="D:UPO", skiprows=2, nrows=120)
df_serv1 = excel_data3.parse('services', header=None, usecols="A:UPO", skiprows=2, nrows=120)

data3 = df_serv.to_numpy()

num_regions = 13
num_scenarios = num_scenarios
total_scenarios = data3.shape[1] // num_regions  # =1125

region_data_list = []

for region in range(num_regions):
    region_columns = [i for i in range(region, data3.shape[1], num_regions)]
    region_matrix = data3[:, region_columns]  # shape = (288, 1125)
    region_data_list.append(region_matrix)

selected_scenarios_list = []
probabilities_list = []

for region_data in region_data_list:
    selected_scenarios, probabilities = select_scenarios_with_refined_probabilities(region_data, num_scenarios)
    selected_scenarios_list.append(selected_scenarios)
    probabilities_list.append(probabilities)

final_selected_scenarios = np.concatenate(selected_scenarios_list, axis=1)

first_two_columns = df_serv1.iloc[:, :2]
first_two_columns_reduced = first_two_columns.iloc[:120, :]

reduced_scenarios_df = pd.DataFrame(
    final_selected_scenarios,
    columns=[f"Region{r+1}_Scenario{s+1}" for r in range(num_regions) for s in range(num_scenarios)]
)

final_df = pd.concat([first_two_columns_reduced, reduced_scenarios_df.reset_index(drop=True)], axis=1)

base_dir = os.path.dirname(file_path)
output_file_path = os.path.join(base_dir, 'Commercial.xlsx')

with pd.ExcelWriter(output_file_path, engine='openpyxl') as writer:
    final_df.to_excel(writer, index=False, sheet_name='Commercial')

print("Reduced scenarios saved successfully to:", output_file_path)


#%%
import pandas as pd
import numpy as np
import os

def select_scenarios_with_refined_probabilities(data4, num_scenarios):
    """
    Select scenarios dynamically and compute meaningful probabilities.
    :param data: Array of possible scenarios (columns represent scenarios, rows represent features).
    :param num_scenarios: Number of scenarios to reduce to.
    :return: Selected reduced scenarios and their probabilities.
    """
    selected_indices = []  # Indices of selected scenarios
    remaining_indices = list(range(data4.shape[1]))  # All scenario indices

    # Select scenarios dynamically based on diversity
    for _ in range(num_scenarios):
        best_index = None
        best_score = float('-inf')

        for index in remaining_indices:
            scenario = data4[:, index]  # Extract the column (scenario)
            # Compute the minimum distance to previously selected scenarios for diversity
            score = np.min([np.linalg.norm(scenario - data4[:, i]) for i in selected_indices]) if selected_indices else np.linalg.norm(np.mean(data4, axis=1) - scenario)

            if score > best_score:  # Maximize diversity
                best_index = index
                best_score = score

        selected_indices.append(best_index)
        remaining_indices.remove(best_index)  # Remove selected index

    # Compute distances for the selected scenarios relative to the mean
    target = np.mean(data4, axis=1)  # Target scenario (mean of rows)
    distances = np.array([np.linalg.norm(data4[:, index] - target) for index in selected_indices])

    # Compute probabilities directly proportional to inverse distances
    probabilities = 1 / (distances )  # Avoid division by zero
    probabilities /= probabilities.sum()  # Normalize probabilities to sum to 1

    # Retrieve the selected scenarios
    selected_scenarios = data4[:, selected_indices]

    return selected_scenarios, probabilities


file_path = os.path.join(os.getcwd(), 'Step2_1.xlsx')
excel_data4 = pd.ExcelFile(file_path, engine='openpyxl')
df_dem = excel_data4.parse('dem', header=None, usecols="D:AQI", skiprows=1, nrows=12)
df_dem1 = excel_data4.parse('dem', header=None, usecols="A:AQI", skiprows=1, nrows=12)

data4 = df_dem.to_numpy()

num_scenarios = num_scenarios  # Number of reduced scenarios

# Compute selected scenarios and probabilities:
selected_scenarios, probabilities = select_scenarios_with_refined_probabilities(data4, num_scenarios)


first_two_columns = df_dem1.iloc[:, :2]

reduced_scenarios_df = pd.DataFrame(selected_scenarios, columns=[f"Scenario {i+1}" for i in range(selected_scenarios.shape[1])])

# Add the probabilities as a separate column corresponding to the reduced scenarios
#reduced_scenarios_df["Probability"] = probabilities

# Now, ensure the first two columns from the original DataFrame are properly aligned
# Note: We'll take only the first 'num_scenarios' rows from the first two columns
first_two_columns_reduced = first_two_columns.iloc[:12, :]

# Combine the reduced first two columns with the reduced scenarios and probabilities
final_df = pd.concat([first_two_columns_reduced, reduced_scenarios_df.reset_index(drop=True)], axis=1)


base_dir = os.path.dirname(file_path)
output_file_path = os.path.join(base_dir, 'Dem.xlsx')

with pd.ExcelWriter(output_file_path, engine='openpyxl') as writer:
    final_df.to_excel(writer, index=False, sheet_name='ِDem')

print("Reduced scenarios saved successfully to:", output_file_path)


#%%
import pandas as pd
import numpy as np
import os

def select_scenarios_with_refined_probabilities(data5, num_scenarios):
    """
    Select scenarios dynamically and compute meaningful probabilities.
    :param data: Array of possible scenarios (columns represent scenarios, rows represent features).
    :param num_scenarios: Number of scenarios to reduce to.
    :return: Selected reduced scenarios and their probabilities.
    """
    selected_indices = []  # Indices of selected scenarios
    remaining_indices = list(range(data5.shape[1]))  # All scenario indices

    # Select scenarios dynamically based on diversity
    for _ in range(num_scenarios):
        best_index = None
        best_score = float('-inf')

        for index in remaining_indices:
            scenario = data5[:, index]  # Extract the column (scenario)
            # Compute the minimum distance to previously selected scenarios for diversity
            score = np.min([np.linalg.norm(scenario - data5[:, i]) for i in selected_indices]) if selected_indices else np.linalg.norm(np.mean(data5, axis=1) - scenario)

            if score > best_score:  # Maximize diversity
                best_index = index
                best_score = score

        selected_indices.append(best_index)
        remaining_indices.remove(best_index)  # Remove selected index

    # Compute distances for the selected scenarios relative to the mean
    target = np.mean(data5, axis=1)  # Target scenario (mean of rows)
    distances = np.array([np.linalg.norm(data5[:, index] - target) for index in selected_indices])

    # Compute probabilities directly proportional to inverse distances
    probabilities = 1 / (distances + 1e-6)  # Avoid division by zero
    probabilities /= probabilities.sum()  # Normalize probabilities to sum to 1

    # Retrieve the selected scenarios
    selected_scenarios = data5[:, selected_indices]

    return selected_scenarios, probabilities


file_path = os.path.join(os.getcwd(), 'Step2_1.xlsx')
excel_data5 = pd.ExcelFile(file_path, engine='openpyxl')
df_cost = excel_data5.parse('costs', header=None, usecols="D:AQH", skiprows=1, nrows=4)
df_cost1 = excel_data5.parse('costs', header=None, usecols="A:AQH", skiprows=1, nrows=4)

data5 = df_cost.to_numpy()

num_scenarios = num_scenarios  # Number of reduced scenarios

# Compute selected scenarios and probabilities:
selected_scenarios, probabilities = select_scenarios_with_refined_probabilities(data5, num_scenarios)


first_two_columns = df_cost1.iloc[:, :1]

reduced_scenarios_df = pd.DataFrame(selected_scenarios, columns=[f"Scenario {i+1}" for i in range(selected_scenarios.shape[1])])

# Add the probabilities as a separate column corresponding to the reduced scenarios
#reduced_scenarios_df["Probability"] = probabilities

# Now, ensure the first two columns from the original DataFrame are properly aligned
# Note: We'll take only the first 'num_scenarios' rows from the first two columns
first_two_columns_reduced = first_two_columns.iloc[:4, :]

# Combine the reduced first two columns with the reduced scenarios and probabilities
final_df = pd.concat([first_two_columns_reduced, reduced_scenarios_df.reset_index(drop=True)], axis=1)


base_dir = os.path.dirname(file_path)
output_file_path = os.path.join(base_dir, 'Costs.xlsx')

with pd.ExcelWriter(output_file_path, engine='openpyxl') as writer:
    final_df.to_excel(writer, index=False, sheet_name='ِCosts')

print("Reduced scenarios saved successfully to:", output_file_path)


#%%

import pandas as pd
import numpy as np
import os

def select_scenarios_with_refined_probabilities(data6, num_scenarios):
    """
    Select scenarios dynamically and compute meaningful probabilities.
    :param data: Array of possible scenarios (columns represent scenarios, rows represent features).
    :param num_scenarios: Number of scenarios to reduce to.
    :return: Selected reduced scenarios and their probabilities.
    """
    selected_indices = []  # Indices of selected scenarios
    remaining_indices = list(range(data6.shape[1]))  # All scenario indices

    # Select scenarios dynamically based on diversity
    for _ in range(num_scenarios):
        best_index = None
        best_score = float('-inf')

        for index in remaining_indices:
            scenario = data6[:, index]  # Extract the column (scenario)
            # Compute the minimum distance to previously selected scenarios for diversity
            score = np.min([np.linalg.norm(scenario - data6[:, i]) for i in selected_indices]) if selected_indices else np.linalg.norm(np.mean(data6, axis=1) - scenario)

            if score > best_score:  # Maximize diversity
                best_index = index
                best_score = score

        selected_indices.append(best_index)
        remaining_indices.remove(best_index)  # Remove selected index

    # Compute distances for the selected scenarios relative to the mean
    target = np.mean(data6, axis=1)  # Target scenario (mean of rows)
    distances = np.array([np.linalg.norm(data6[:, index] - target) for index in selected_indices])

    # Compute probabilities directly proportional to inverse distances
    probabilities = 1 / (distances + 1e-6)  # Avoid division by zero
    probabilities /= probabilities.sum()  # Normalize probabilities to sum to 1

    # Retrieve the selected scenarios
    selected_scenarios = data6[:, selected_indices]

    return selected_scenarios, probabilities


file_path = os.path.join(os.getcwd(), 'Step2_1.xlsx')
excel_data6 = pd.ExcelFile(file_path, engine='openpyxl')
df_biomass = excel_data6.parse('biomass', header=None, usecols="D:AQH", skiprows=1, nrows=3)
df_biomass1= excel_data6.parse('biomass', header=None, usecols="A:AQH", skiprows=1, nrows=3)

data6 = df_biomass.to_numpy()

num_scenarios = num_scenarios # Number of reduced scenarios

# Compute selected scenarios and probabilities:
selected_scenarios, probabilities = select_scenarios_with_refined_probabilities(data6, num_scenarios)


first_two_columns = df_biomass1.iloc[:, :1]

reduced_scenarios_df = pd.DataFrame(selected_scenarios, columns=[f"Scenario {i+1}" for i in range(selected_scenarios.shape[1])])

# Add the probabilities as a separate column corresponding to the reduced scenarios
#reduced_scenarios_df["Probability"] = probabilities

# Now, ensure the first two columns from the original DataFrame are properly aligned
# Note: We'll take only the first 'num_scenarios' rows from the first two columns
first_two_columns_reduced = first_two_columns.iloc[:4, :]

# Combine the reduced first two columns with the reduced scenarios and probabilities
final_df = pd.concat([first_two_columns_reduced, reduced_scenarios_df.reset_index(drop=True)], axis=1)


base_dir = os.path.dirname(file_path)
output_file_path = os.path.join(base_dir, 'biomass.xlsx')

with pd.ExcelWriter(output_file_path, engine='openpyxl') as writer:
    final_df.to_excel(writer, index=False, sheet_name='ِbiomass')

print("Reduced scenarios saved successfully to:", output_file_path)



#%%
import pandas as pd
import numpy as np
import os

def select_scenarios_with_refined_probabilities(data7, num_scenarios):
    """
    Select scenarios dynamically and compute meaningful probabilities.
    :param data: Array of possible scenarios (columns represent scenarios, rows represent features).
    :param num_scenarios: Number of scenarios to reduce to.
    :return: Selected reduced scenarios and their probabilities.
    """
    selected_indices = []  # Indices of selected scenarios
    remaining_indices = list(range(data7.shape[1]))  # All scenario indices

    # Select scenarios dynamically based on diversity
    for _ in range(num_scenarios):
        best_index = None
        best_score = float('-inf')

        for index in remaining_indices:
            scenario = data7[:, index]  # Extract the column (scenario)
            # Compute the minimum distance to previously selected scenarios for diversity
            score = np.min([np.linalg.norm(scenario - data7[:, i]) for i in selected_indices]) if selected_indices else np.linalg.norm(np.mean(data7, axis=1) - scenario)

            if score > best_score:  # Maximize diversity
                best_index = index
                best_score = score

        selected_indices.append(best_index)
        remaining_indices.remove(best_index)  # Remove selected index

    # Compute distances for the selected scenarios relative to the mean
    target = np.mean(data7, axis=1)  # Target scenario (mean of rows)
    distances = np.array([np.linalg.norm(data7[:, index] - target) for index in selected_indices])

    # Compute probabilities directly proportional to inverse distances
    probabilities = 1 / (distances + 1e-6)  # Avoid division by zero
    probabilities /= probabilities.sum()  # Normalize probabilities to sum to 1

    # Retrieve the selected scenarios
    selected_scenarios = data7[:, selected_indices]

    return selected_scenarios, probabilities


file_path = os.path.join(os.getcwd(), 'Step2_1.xlsx')
excel_data7 = pd.ExcelFile(file_path, engine='openpyxl')
df_price = excel_data7.parse('gasprice', header=None, usecols="D:AQH", skiprows=1, nrows=3)
df_price1 = excel_data7.parse('gasprice', header=None, usecols="A:AQH", skiprows=1, nrows=3)

data7 = df_price.to_numpy()

num_scenarios = num_scenarios  # Number of reduced scenarios

# Compute selected scenarios and probabilities:
selected_scenarios, probabilities = select_scenarios_with_refined_probabilities(data7, num_scenarios)


first_two_columns = df_price1.iloc[:, :1]

reduced_scenarios_df = pd.DataFrame(selected_scenarios, columns=[f"Scenario {i+1}" for i in range(selected_scenarios.shape[1])])

# Add the probabilities as a separate column corresponding to the reduced scenarios
#reduced_scenarios_df["Probability"] = probabilities

# Now, ensure the first two columns from the original DataFrame are properly aligned
# Note: We'll take only the first 'num_scenarios' rows from the first two columns
first_two_columns_reduced = first_two_columns.iloc[:4, :]

# Combine the reduced first two columns with the reduced scenarios and probabilities
final_df = pd.concat([first_two_columns_reduced, reduced_scenarios_df.reset_index(drop=True)], axis=1)


base_dir = os.path.dirname(file_path)
output_file_path = os.path.join(base_dir, 'Prices.xlsx')

with pd.ExcelWriter(output_file_path, engine='openpyxl') as writer:
    final_df.to_excel(writer, index=False, sheet_name='ِprice')

print("Reduced scenarios saved successfully to:", output_file_path)


#%%
probabilities_df = pd.DataFrame(
    probabilities, 
    columns=['Probability'], 
    index=[f"Scenario {i+1}" for i in range(len(probabilities))] 
)

base_dir = os.path.dirname(file_path)
output_file_path = os.path.join(base_dir, 'Probabilities.xlsx')

with pd.ExcelWriter(output_file_path, engine='openpyxl') as writer:
    probabilities_df.to_excel(writer, index=True, sheet_name='ِprobabilities')
#%%
import pandas as pd
import numpy as np
import os

def select_scenarios_with_refined_probabilities(data8, num_scenarios):
    """
    Select scenarios dynamically and compute meaningful probabilities.
    :param data: Array of possible scenarios (columns represent scenarios, rows represent features).
    :param num_scenarios: Number of scenarios to reduce to.
    :return: Selected reduced scenarios and their probabilities.
    """
    selected_indices = []  # Indices of selected scenarios
    remaining_indices = list(range(data8.shape[1]))  # All scenario indices

    # Select scenarios dynamically based on diversity
    for _ in range(num_scenarios):
        best_index = None
        best_score = float('-inf')

        for index in remaining_indices:
            scenario = data8[:, index]  # Extract the column (scenario)
            # Compute the minimum distance to previously selected scenarios for diversity
            score = np.min([np.linalg.norm(scenario - data8[:, i]) for i in selected_indices]) if selected_indices else np.linalg.norm(np.mean(data8, axis=1) - scenario)

            if score > best_score:  # Maximize diversity
                best_index = index
                best_score = score

        selected_indices.append(best_index)
        remaining_indices.remove(best_index)  # Remove selected index

    # Compute distances for the selected scenarios relative to the mean
    target = np.mean(data8, axis=1)  # Target scenario (mean of rows)
    distances = np.array([np.linalg.norm(data8[:, index] - target) for index in selected_indices])

    # Compute probabilities directly proportional to inverse distances
    probabilities = 1 / (distances + 1e-6)  # Avoid division by zero
    probabilities /= probabilities.sum()  # Normalize probabilities to sum to 1

    # Retrieve the selected scenarios
    selected_scenarios = data8[:, selected_indices]

    return selected_scenarios, probabilities


file_path = os.path.join(os.getcwd(), 'Step2_1.xlsx')
excel_data8 = pd.ExcelFile(file_path, engine='openpyxl')
print(excel_data8.sheet_names)
df_rccost = excel_data8.parse('rccost', header=None, usecols="C:AQI", skiprows=1, nrows=9)
df_rccost1 = excel_data8.parse('rccost', header=None, usecols="A:AQI", skiprows=1, nrows=9)

data8 = df_rccost.to_numpy()

num_scenarios = num_scenarios  # Number of reduced scenarios

# Compute selected scenarios and probabilities:
selected_scenarios, probabilities = select_scenarios_with_refined_probabilities(data8, num_scenarios)


first_two_columns = df_rccost1.iloc[:, :2]

reduced_scenarios_df = pd.DataFrame(selected_scenarios, columns=[f"Scenario {i+1}" for i in range(selected_scenarios.shape[1])])

# Add the probabilities as a separate column corresponding to the reduced scenarios
#reduced_scenarios_df["Probability"] = probabilities

# Now, ensure the first two columns from the original DataFrame are properly aligned
# Note: We'll take only the first 'num_scenarios' rows from the first two columns
first_two_columns_reduced = first_two_columns.iloc[:9, :]

# Combine the reduced first two columns with the reduced scenarios and probabilities
final_df = pd.concat([first_two_columns_reduced, reduced_scenarios_df.reset_index(drop=True)], axis=1)


base_dir = os.path.dirname(file_path)
output_file_path = os.path.join(base_dir, 'rccost.xlsx')

with pd.ExcelWriter(output_file_path, engine='openpyxl') as writer:
    final_df.to_excel(writer, index=False, sheet_name='ِrccost')

print("Reduced scenarios saved successfully to:", output_file_path)


#%%
import pandas as pd
import numpy as np
import os

def select_scenarios_with_refined_probabilities(data9, num_scenarios):
    """
    Select scenarios dynamically and compute meaningful probabilities.
    :param data: Array of possible scenarios (columns represent scenarios, rows represent features).
    :param num_scenarios: Number of scenarios to reduce to.
    :return: Selected reduced scenarios and their probabilities.
    """
    selected_indices = []  # Indices of selected scenarios
    remaining_indices = list(range(data9.shape[1]))  # All scenario indices

    # Select scenarios dynamically based on diversity
    for _ in range(num_scenarios):
        best_index = None
        best_score = float('-inf')

        for index in remaining_indices:
            scenario = data9[:, index]  # Extract the column (scenario)
            # Compute the minimum distance to previously selected scenarios for diversity
            score = np.min([np.linalg.norm(scenario - data9[:, i]) for i in selected_indices]) if selected_indices else np.linalg.norm(np.mean(data9, axis=1) - scenario)

            if score > best_score:  # Maximize diversity
                best_index = index
                best_score = score

        selected_indices.append(best_index)
        remaining_indices.remove(best_index)  # Remove selected index

    # Compute distances for the selected scenarios relative to the mean
    target = np.mean(data9, axis=1)  # Target scenario (mean of rows)
    distances = np.array([np.linalg.norm(data9[:, index] - target) for index in selected_indices])

    # Compute probabilities directly proportional to inverse distances
    probabilities = 1 / (distances + 1e-6)  # Avoid division by zero
    probabilities /= probabilities.sum()  # Normalize probabilities to sum to 1

    # Retrieve the selected scenarios
    selected_scenarios = data9[:, selected_indices]

    return selected_scenarios, probabilities


file_path = os.path.join(os.getcwd(), 'Step2_1.xlsx')
excel_data9 = pd.ExcelFile(file_path, engine='openpyxl')
df_pocostV = excel_data9.parse('pocostV', header=None, usecols="B:AQH", skiprows=1, nrows=3)
df_pocostV1 = excel_data9.parse('pocostV', header=None, usecols="A:AQH", skiprows=1, nrows=3)

data9 = df_pocostV.to_numpy()

num_scenarios = num_scenarios  # Number of reduced scenarios

# Compute selected scenarios and probabilities:
selected_scenarios, probabilities = select_scenarios_with_refined_probabilities(data9, num_scenarios)


first_two_columns = df_pocostV1.iloc[:, :1]

reduced_scenarios_df = pd.DataFrame(selected_scenarios, columns=[f"Scenario {i+1}" for i in range(selected_scenarios.shape[1])])

# Add the probabilities as a separate column corresponding to the reduced scenarios
#reduced_scenarios_df["Probability"] = probabilities

# Now, ensure the first two columns from the original DataFrame are properly aligned
# Note: We'll take only the first 'num_scenarios' rows from the first two columns
first_two_columns_reduced = first_two_columns.iloc[:3, :]

# Combine the reduced first two columns with the reduced scenarios and probabilities
final_df = pd.concat([first_two_columns_reduced, reduced_scenarios_df.reset_index(drop=True)], axis=1)


base_dir = os.path.dirname(file_path)
output_file_path = os.path.join(base_dir, 'pocostV.xlsx')

with pd.ExcelWriter(output_file_path, engine='openpyxl') as writer:
    final_df.to_excel(writer, index=False, sheet_name='ِpocostV')

print("Reduced scenarios saved successfully to:", output_file_path)



#%%
import pandas as pd
import numpy as np
import os

def select_scenarios_with_refined_probabilities(data10, num_scenarios):
    """
    Select scenarios dynamically and compute meaningful probabilities.
    :param data: Array of possible scenarios (columns represent scenarios, rows represent features).
    :param num_scenarios: Number of scenarios to reduce to.
    :return: Selected reduced scenarios and their probabilities.
    """
    selected_indices = []  # Indices of selected scenarios
    remaining_indices = list(range(data10.shape[1]))  # All scenario indices

    # Select scenarios dynamically based on diversity
    for _ in range(num_scenarios):
        best_index = None
        best_score = float('-inf')

        for index in remaining_indices:
            scenario = data10[:, index]  # Extract the column (scenario)
            # Compute the minimum distance to previously selected scenarios for diversity
            score = np.min([np.linalg.norm(scenario - data10[:, i]) for i in selected_indices]) if selected_indices else np.linalg.norm(np.mean(data10, axis=1) - scenario)

            if score > best_score:  # Maximize diversity
                best_index = index
                best_score = score

        selected_indices.append(best_index)
        remaining_indices.remove(best_index)  # Remove selected index

    # Compute distances for the selected scenarios relative to the mean
    target = np.mean(data10, axis=1)  # Target scenario (mean of rows)
    distances = np.array([np.linalg.norm(data10[:, index] - target) for index in selected_indices])

    # Compute probabilities directly proportional to inverse distances
    probabilities = 1 / (distances + 1e-6)  # Avoid division by zero
    probabilities /= probabilities.sum()  # Normalize probabilities to sum to 1

    # Retrieve the selected scenarios
    selected_scenarios = data10[:, selected_indices]

    return selected_scenarios, probabilities


file_path = os.path.join(os.getcwd(), 'Step2_1.xlsx')
excel_data10 = pd.ExcelFile(file_path, engine='openpyxl')
df_pccostF = excel_data10.parse('pccostF', header=None, usecols="B:AQH", skiprows=1, nrows=3)
df_pccostF1 = excel_data10.parse('pccostF', header=None, usecols="A:AQH", skiprows=1, nrows=3)

data10 = df_pccostF.to_numpy()

num_scenarios = num_scenarios  # Number of reduced scenarios

# Compute selected scenarios and probabilities:
selected_scenarios, probabilities = select_scenarios_with_refined_probabilities(data10, num_scenarios)


first_two_columns = df_pccostF1.iloc[:, :1]

reduced_scenarios_df = pd.DataFrame(selected_scenarios, columns=[f"Scenario {i+1}" for i in range(selected_scenarios.shape[1])])

# Add the probabilities as a separate column corresponding to the reduced scenarios
#reduced_scenarios_df["Probability"] = probabilities

# Now, ensure the first two columns from the original DataFrame are properly aligned
# Note: We'll take only the first 'num_scenarios' rows from the first two columns
first_two_columns_reduced = first_two_columns.iloc[:3, :]

# Combine the reduced first two columns with the reduced scenarios and probabilities
final_df = pd.concat([first_two_columns_reduced, reduced_scenarios_df.reset_index(drop=True)], axis=1)


base_dir = os.path.dirname(file_path)
output_file_path = os.path.join(base_dir, 'pccostF.xlsx')

with pd.ExcelWriter(output_file_path, engine='openpyxl') as writer:
    final_df.to_excel(writer, index=False, sheet_name='ِpccostF')

print("Reduced scenarios saved successfully to:", output_file_path)


#%%
import pandas as pd
import numpy as np
import os

def select_scenarios_with_refined_probabilities(data11, num_scenarios):
    """
    Select scenarios dynamically and compute meaningful probabilities.
    :param data: Array of possible scenarios (columns represent scenarios, rows represent features).
    :param num_scenarios: Number of scenarios to reduce to.
    :return: Selected reduced scenarios and their probabilities.
    """
    selected_indices = []  # Indices of selected scenarios
    remaining_indices = list(range(data11.shape[1]))  # All scenario indices

    # Select scenarios dynamically based on diversity
    for _ in range(num_scenarios):
        best_index = None
        best_score = float('-inf')

        for index in remaining_indices:
            scenario = data11[:, index]  # Extract the column (scenario)
            # Compute the minimum distance to previously selected scenarios for diversity
            score = np.min([np.linalg.norm(scenario - data11[:, i]) for i in selected_indices]) if selected_indices else np.linalg.norm(np.mean(data11, axis=1) - scenario)

            if score > best_score:  # Maximize diversity
                best_index = index
                best_score = score

        selected_indices.append(best_index)
        remaining_indices.remove(best_index)  # Remove selected index

    # Compute distances for the selected scenarios relative to the mean
    target = np.mean(data11, axis=1)  # Target scenario (mean of rows)
    distances = np.array([np.linalg.norm(data11[:, index] - target) for index in selected_indices])

    # Compute probabilities directly proportional to inverse distances
    probabilities = 1 / (distances + 1e-6)  # Avoid division by zero
    probabilities /= probabilities.sum()  # Normalize probabilities to sum to 1

    # Retrieve the selected scenarios
    selected_scenarios = data11[:, selected_indices]

    return selected_scenarios, probabilities


file_path = os.path.join(os.getcwd(), 'Step2_1.xlsx')
excel_data11 = pd.ExcelFile(file_path, engine='openpyxl')
df_pccost = excel_data11.parse('pccost', header=None, usecols="B:AQH", skiprows=1, nrows=3)
df_pccost1 = excel_data11.parse('pccost', header=None, usecols="A:AQH", skiprows=1, nrows=3)

data11 = df_pccost.to_numpy()

num_scenarios = num_scenarios  # Number of reduced scenarios

# Compute selected scenarios and probabilities:
selected_scenarios, probabilities = select_scenarios_with_refined_probabilities(data11, num_scenarios)


first_two_columns = df_pccost1.iloc[:, :1]

reduced_scenarios_df = pd.DataFrame(selected_scenarios, columns=[f"Scenario {i+1}" for i in range(selected_scenarios.shape[1])])

# Add the probabilities as a separate column corresponding to the reduced scenarios
#reduced_scenarios_df["Probability"] = probabilities

# Now, ensure the first two columns from the original DataFrame are properly aligned
# Note: We'll take only the first 'num_scenarios' rows from the first two columns
first_two_columns_reduced = first_two_columns.iloc[:3, :]

# Combine the reduced first two columns with the reduced scenarios and probabilities
final_df = pd.concat([first_two_columns_reduced, reduced_scenarios_df.reset_index(drop=True)], axis=1)


base_dir = os.path.dirname(file_path)
output_file_path = os.path.join(base_dir, 'pccost.xlsx')

with pd.ExcelWriter(output_file_path, engine='openpyxl') as writer:
    final_df.to_excel(writer, index=False, sheet_name='ِpccost')

print("Reduced scenarios saved successfully to:", output_file_path)


#%%
import pandas as pd
import numpy as np
import os

def select_scenarios_with_refined_probabilities(data12, num_scenarios):
    """
    Select scenarios dynamically and compute meaningful probabilities.
    :param data: Array of possible scenarios (columns represent scenarios, rows represent features).
    :param num_scenarios: Number of scenarios to reduce to.
    :return: Selected reduced scenarios and their probabilities.
    """
    selected_indices = []  # Indices of selected scenarios
    remaining_indices = list(range(data12.shape[1]))  # All scenario indices

    # Select scenarios dynamically based on diversity
    for _ in range(num_scenarios):
        best_index = None
        best_score = float('-inf')

        for index in remaining_indices:
            scenario = data12[:, index]  # Extract the column (scenario)
            # Compute the minimum distance to previously selected scenarios for diversity
            score = np.min([np.linalg.norm(scenario - data12[:, i]) for i in selected_indices]) if selected_indices else np.linalg.norm(np.mean(data12, axis=1) - scenario)

            if score > best_score:  # Maximize diversity
                best_index = index
                best_score = score

        selected_indices.append(best_index)
        remaining_indices.remove(best_index)  # Remove selected index

    # Compute distances for the selected scenarios relative to the mean
    target = np.mean(data12, axis=1)  # Target scenario (mean of rows)
    distances = np.array([np.linalg.norm(data12[:, index] - target) for index in selected_indices])

    # Compute probabilities directly proportional to inverse distances
    probabilities = 1 / (distances + 1e-6)  # Avoid division by zero
    probabilities /= probabilities.sum()  # Normalize probabilities to sum to 1

    # Retrieve the selected scenarios
    selected_scenarios = data12[:, selected_indices]

    return selected_scenarios, probabilities


file_path = os.path.join(os.getcwd(), 'Step2_1.xlsx')
excel_data12 = pd.ExcelFile(file_path, engine='openpyxl')
df_eta = excel_data12.parse('eta', header=None, usecols="B:AQH", skiprows=1, nrows=3)
df_eta1 = excel_data12.parse('eta', header=None, usecols="A:AQH", skiprows=1, nrows=3)

data12 = df_eta.to_numpy()

num_scenarios = num_scenarios  # Number of reduced scenarios

# Compute selected scenarios and probabilities:
selected_scenarios, probabilities = select_scenarios_with_refined_probabilities(data12, num_scenarios)


first_two_columns = df_eta1.iloc[:, :1]

reduced_scenarios_df = pd.DataFrame(selected_scenarios, columns=[f"Scenario {i+1}" for i in range(selected_scenarios.shape[1])])

# Add the probabilities as a separate column corresponding to the reduced scenarios
#reduced_scenarios_df["Probability"] = probabilities

# Now, ensure the first two columns from the original DataFrame are properly aligned
# Note: We'll take only the first 'num_scenarios' rows from the first two columns
first_two_columns_reduced = first_two_columns.iloc[:3, :]

# Combine the reduced first two columns with the reduced scenarios and probabilities
final_df = pd.concat([first_two_columns_reduced, reduced_scenarios_df.reset_index(drop=True)], axis=1)


base_dir = os.path.dirname(file_path)
output_file_path = os.path.join(base_dir, 'eta.xlsx')

with pd.ExcelWriter(output_file_path, engine='openpyxl') as writer:
    final_df.to_excel(writer, index=False, sheet_name='ِeta')

print("Reduced scenarios saved successfully to:", output_file_path)

#%%
import pandas as pd
import os

input_dir = os.getcwd() 

file_names = [
    'Renewable.xlsx',
    'Domestic.xlsx',
    'Industrial.xlsx',
    'Commercial.xlsx',
    'Dem.xlsx',
    'Costs.xlsx',
    'biomass.xlsx',
    'Prices.xlsx',
    'eta.xlsx',
    'pccost.xlsx',
    'pocostV.xlsx',
    'pccostF.xlsx',
    'rccost.xlsx',
    'Probabilities.xlsx'
]

file_paths = [os.path.join(input_dir, name) for name in file_names]

output_file_path = os.path.join(input_dir, 'ReducedScenarios.xlsx')

with pd.ExcelWriter(output_file_path, engine='openpyxl') as writer:
    for path in file_paths:
        sheet_name = os.path.splitext(os.path.basename(path))[0][:31]  # شیت نباید بیشتر از 31 کاراکتر باشه
        try:
            df = pd.read_excel(path, engine='openpyxl')
            df.to_excel(writer, index=False, sheet_name=sheet_name)
            
        except Exception as e:
            print(f"❌ Error reading {sheet_name}: {e}")





