import pandas as pd
import pandas as pd
import numpy as np
import os
import sys

file_path = os.path.join(os.getcwd(), 'clustering.xlsx')
excel_data = pd.ExcelFile(file_path, engine='openpyxl')

df_Sheet1 = excel_data.parse('Sheet1', header=None, usecols="A:CA", skiprows=25, nrows=96)
df_Sheet1 = df_Sheet1.round(3)

if len(sys.argv) > 1:
    n_slice = int(sys.argv[1])  
else:
    n_slice = int(input("Press Input number of time-slice: "))


from pyomo.environ import *

model = ConcreteModel()



#model.h = Set(initialize=["h" + str(i) for i in range(1, 25)])
#model.c = Set(initialize=["c" + str(i) for i in range(2, 6)])
#model.s = Set(initialize=["s" + str(i) for i in range(1, 78)])
#model.p = Set(initialize=["p" + str(i) for i in range(1, 7)])

model.h = RangeSet(1, 24)
model.c = RangeSet(2,5)
model.s = RangeSet(1,77)
model.p = RangeSet(1,n_slice)
model.h1 = Set(initialize=range(1, 25))


Hour_order = {hour: i+1 for i, hour in enumerate(model.h)}
model.ord_h = Param(model.h,initialize=Hour_order)

P_order = {hour: i+1 for i, hour in enumerate(model.p)}
model.ord_p = Param(model.p,initialize=P_order)


unique_c = sorted(df_Sheet1.iloc[:, 0].unique())  # Unique c values (e.g., 'c1', 'c2', ...)
unique_h = sorted(df_Sheet1.iloc[:, 1].unique())  # Unique h values (e.g., 'h1', 'h2', ...)

# Step 4: Create mappings for `c` and `h` to ensure numeric representation
c_mapping = {c: i+2 for i, c in enumerate(unique_c)}  # Ensure it starts from 2 (matching RangeSet(2,6))
h_mapping = {h: i+1 for i, h in enumerate(unique_h)}  # Ensure it starts from 1 (matching RangeSet(1,25))



# Step 5: Build `PP_data` Dictionary using numeric indices
PP_data = {}
for i, (c, h) in enumerate(zip(df_Sheet1.iloc[:, 0], df_Sheet1.iloc[:, 1])):
    for s_idx, s in enumerate(range(1, 78)):  # Ensure s is within RangeSet(1,77)
        # Ensure `c` and `h` exist in mappings before adding to PP_data
        if c in c_mapping and h in h_mapping:
            c_num = c_mapping[c]
            h_num = h_mapping[h]
            PP_data[(c_num, h_num, s)] = df_Sheet1.iloc[i, 2 + s_idx]

# Step 6: Define Pyomo Parameter using `PP_data`
model.PP = Param(model.c, model.h, model.s, initialize=PP_data, within=Reals)



'''
PP_data = {(c, h, s): df_Sheet1.iloc[i, 2 +  s_idx]
    for i, (c, h) in enumerate(zip(df_Sheet1.iloc[:, 0], df_Sheet1.iloc[:, 1]))   
    for s_idx, s in enumerate(model.s)}

model.PP = Param(model.c, model.h, model.s, initialize=PP_data)
'''
def Pmin_rule(model, c, s):
    return min(model.PP[c, h, s] for h in model.h)
def Pmax_rule(model, c, s):
    return max(model.PP[c, h, s] for h in model.h)

model.Pmin = Param(model.c, model.s, initialize=Pmin_rule)
model.Pmax = Param(model.c, model.s, initialize=Pmax_rule)

def NPP_rule(model, c, h, s):
    return (model.PP[c,h,s] - model.Pmin[c,s]) / (model.Pmax[c,s] - model.Pmin[c,s])

model.NPP = Param(model.c, model.h, model.s, initialize=NPP_rule)

model.Y = Var(model.h, model.p, domain=Binary)  
model.X = Var(model.c, model.s, model.p, domain=NonNegativeReals)
model.d = Var(model.c, model.s, model.h, model.p, domain=NonNegativeReals) 
#model.z = Var(domain=NonNegativeReals)  

def con1_rule(model, h):
    return sum(model.Y[h, p] for p in model.p) == 1
model.con1 = Constraint(model.h, rule=con1_rule)

def con2_rule(model, h, p):
    # Convert ord_h and ord_p to numeric indices
    if model.ord_h[h] < 24:
        
        return model.Y[h, p] <= model.Y[h+1, p] + (model.Y[h+1, p+1] if model.ord_p[p]<n_slice else 0)

    return Constraint.Skip

model.con2 = Constraint(model.h, model.p, rule=con2_rule)

'''
def con2_rule(model, h, p):
    h_index = list(model.h).index(h) + 1  # Get numeric position of h
    p_index = list(model.p).index(p) + 1  # Get numeric position of p

    if h_index < len(model.h) and p_index < len(model.p):  # Equivalent to ord(h) < card(h) and ord(p) < card(p)
        next_h = list(model.h)[h_index]  # h+1
        next_p = list(model.p)[p_index]  # p+1

        return model.Y[h, p] <= model.Y[next_h, p] + model.Y[next_h, next_p]
    return Constraint.Skip  # Skip constraint when conditions are not met

model.con2 = Constraint(model.h, model.p, rule=con2_rule)
'''


def con3a_rule(model, c, s, h, p):
    return model.d[c, s, h, p] >= model.NPP[c, h, s] - model.X[c, s, p] - (1 - model.Y[h, p])
model.con3a = Constraint(model.c, model.s, model.h, model.p, rule=con3a_rule)

def con3b_rule(model, c, s, h, p):
    return model.d[c, s, h, p] >= model.X[c, s, p] - model.NPP[c, h, s] - (1 - model.Y[h, p])
model.con3b = Constraint(model.c, model.s, model.h, model.p, rule=con3b_rule)

def obj_rule(model):
    return sum(model.d[c, s, h, p] for c in model.c for s in model.s for h in model.h for p in model.p)
model.z = Objective(rule=obj_rule, sense=minimize)

solver = SolverFactory('gurobi') 
solver.options['MIPGap']=0
solver.solve(model,tee=True)

for h in model.h:
    for p in model.p:
        if model.Y[h, p].value != 0:
            print(f"Y[{h}, {p}] = {model.Y[h, p].value}")
            

sum_Y = {}

for h in model.h:
    for p in model.p:
        if model.Y[h, p].value != 0:
            if p not in sum_Y:
                sum_Y[p] = 0
            sum_Y[p] += model.Y[h, p].value


slice_map = {p: [] for p in model.p}

for h1 in model.h1:
    for p in model.p:
        if model.Y[h1, p].value == 1:
            slice_map[p].append(h1)


Hsum_index_list = [
    (p, h1, c)
    for p in model.p
    for h1 in slice_map[p]
    for c in model.c
    if not (c == '1' and p != h1)
] + [
    (p, p, '1')
    for p in range(1, 25)
]

df_hsum_index = pd.DataFrame(Hsum_index_list, columns=["p", "h1", "c"])




num_intervals = len(sum_Y)
clusters = list(range(1, 6))  
hours = list(range(1, 25))  

data = []

for cluster in clusters:
    for hour in hours:
        if cluster == 1:
            value = 1  
        elif hour <= num_intervals:  
            value = list(sum_Y.values())[hour - 1]
        else:
            value = 0  
        data.append([cluster, hour, value])

df = pd.DataFrame(data)

file_path = 'Time Slice.xlsx'

with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
    df.to_excel(writer, sheet_name='theta', index=False)
    df_hsum_index.to_excel(writer, sheet_name='Hsum_index', index=False)



print("Data successfully written to the 'theta' sheet in Time Slice.xlsx")

