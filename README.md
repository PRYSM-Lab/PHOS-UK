# PHOS-UK: Open-Source User Interface for Power-Hydrogen-Heat Optimisation for the United Kingdom




## 📌 Overview

PHOS-UK is a Graphical User Interface (GUI) developed for running integrated UK energy system optimisation models. It allows users to configure model settings, prepare input data, select optimisation approaches, and execute simulations for different decarbonisation pathways.

The spatial-temporal optimisation framework supports:

* Electricity system planning (Generation, Storage and Transmission)
* Hydrogen system integration (Generation, Storage and Trasportation) 
* Heating sector decarbonisation
* Carbon transport and storage

The optimisation model is formulated as a multi-period **Mixed-Integer Linear Programming (MILP)** problem.

---

## ⚙️ Supported Optimisation Approaches

PHOS-UK can be executed using three major optimisation approaches:

* Deterministic Optimisation (Support both hydrogen and hybrid models)
* Stochastic Optimisation (Only support hydrogen infrastructure optimisation model)
* Robust Optimisation (Only support hydrogen infrastructure optimisation model)
** In PHOS-UK, the hybrid model refers to the optimisation framework that simultaneously considers electricity, hydrogen, and heating infrastructures. 

---

# 1. Optimisation Methods

---

## 🔹 Deterministic Optimisation

In deterministic optimisation, all parameters are assumed to be known with certainty.


---

## 🔹 Stochastic Optimisation

In stochastic optimisation, model is formulated as two-stage optimisation framework under uncertainty associated with:

* Renewable energy availability
* Demand 
* Fuel price 
* Carbon price
* Technology efficiency
* Technology investment cost in upcoming year

The stochastic formulation is implemented using:

**Two-stage Stochastic Programming**

### Scenario Generation and Reduction

User can use pre-defined scenarios (more than 1,000) and then reduce by scenario reduction using:

```
SCENREDPY
```

The following reduction method is applied:

* Fast Forward Selection (FFS)

This reduces the number of scenarios while preserving the statistical properties of the original dataset.

---

## 🔹 Robust Optimisation

Robust optimisation handles demand uncertainty.

In this approach, uncertainty is represented using:

* Polyhedral uncertainty sets

Two robust approaches are supported:

* Static Robust Optimisation
* Adaptive Robust Optimisation

This approach ensures system feasibility under worst-case demand scenario.

---

# 2. Running PHOS-UK Using the GUI


---

🚨 **IMPORTANT NOTICE** 🚨

**Please make sure that all input files, Excel files, Python scripts, and required model files are placed in the same working directory (same folder) before running the model.**

**This is necessary to ensure that the optimisation framework can correctly read input data and execute without file path errors.**

---


## Step 0 — Install PHOS-UK

Install the PHOS-UK framework from the official repository.

Make sure all project files are correctly placed in the working directory.

---

<img width="680" height="254" alt="image" src="https://github.com/user-attachments/assets/94fa2c66-a78b-4e13-9ad4-63ac994858ff" />



## Step 1 — Install Required Python Packages

Before running the model, install all required dependencies.

The required packages are listed in:

```
Requirement.txt
```

Install packages using:

```
pip install -r Requirement.txt
```
PHOS does not require a complex installation process. The user only needs to unzip the package and run the main script to start using the platform.

## Step 2 — Run the Main PHOS-UK Script

Execute the main script:

```
python PHOS-UK.py
```

This launches the Graphical User Interface (GUI).

<img width="526" height="478" alt="image" src="https://github.com/user-attachments/assets/d9891c61-5e4d-4b22-a22a-46ee82735415" />

---

## Step 3 — Select Decarbonisation Pathway

After launching the GUI, the user must select the decarbonisation pathway:

Available options:

* Hydrogen-led decarbonisation
* Hybrid decarbonisation approach

This determines the structure of the optimisation model.

<img width="554" height="305" alt="image" src="https://github.com/user-attachments/assets/b2d79f64-1b37-4853-8fc3-c8520be6fbf7" />

---

## Step 4 — Select Optimisation Method

After selecting the decarbonisation pathway, choose the optimisation method:

Available options for hydrogen-led decarbonisation:

* Deterministic
* Stochastic
* Robust


<img width="479" height="328" alt="image" src="https://github.com/user-attachments/assets/369a53f7-891c-4bc4-bb48-7ec7308740cf" />  <img width="495" height="279" alt="image" src="https://github.com/user-attachments/assets/5754dfa3-e969-4ee3-ac11-46241f1e6588" />




Available option for hybrid (power-heat-hydrogen model):
* Deterministic

---

## Step 5 — Select Model Architecture (Deterministic Approach)

For deterministic optimisation, PHOS-UK supports multiple solution architectures designed to improve computational performance.

Available architectures:

* Monolithic
* Hierarchical 1
* Hierarchical 2

⚠️ Hyperlinks provided in the GUI panel redirect users to the corresponding published research papers.

<img width="535" height="385" alt="image" src="https://github.com/user-attachments/assets/11fc04ee-63a1-4a38-9a53-c64e2b2a6803" />


---

## Step 6 — Provide Input Data

The required Excel input files depend on the selected optimisation method.

Examples include:

* `InputDeterministic.xlsx`
* `InputStochastic.xlsx`
* `InputRobust.xlsx`
* `InputDataForHybrid.xlsx`

Users must ensure the correct file is selected before execution.


<img width="821" height="334" alt="image" src="https://github.com/user-attachments/assets/7b3afb2b-4752-4ad6-8c17-8ca71341fe65" />

---

## Step 7 — Configure Representative Days

Users can specify the number of representative days used in the model.

Representative days are generated using clustering techniques.

The clustering algorithm is implemented in:

```
kmedoid.py
```

This script performs:

* k-medoids clustering

Its purpose is to identify representative operational days while reducing computational burden.


<img width="800" height="277" alt="image" src="https://github.com/user-attachments/assets/999c0781-1222-4add-ad68-b952ecb48663" />


---

## Step 8 — Choose Solver

The optimisation problem can be solved using:

* Local Solver
* NEOS Optimisation Server


<img width="456" height="284" alt="image" src="https://github.com/user-attachments/assets/3b44612c-6c78-4a13-950a-f895d5bbe52c" />


---

## 🔸 Local Solver

If the local option is selected, the optimisation problem is solved using the optimisation solver installed on the user’s machine.

Examples:

* CPLEX
* Gurobi
* GLPK


<img width="612" height="319" alt="image" src="https://github.com/user-attachments/assets/080a0e60-ad8e-4ba3-bfe5-43cb77f70176" />


---

## 🔸 NEOS Server

If the NEOS option is selected:

* The model is submitted to the NEOS optimisation server
* The user selects the solver (e.g., CPLEX)
* The user provides an email address to receive results

This option is useful when a local solver is unavailable.


<img width="317" height="215" alt="image" src="https://github.com/user-attachments/assets/53244103-d3fd-449b-9e3d-17e54bad0f84" />


---

## Step 9 — Solver Configuration

The user may define:

* Optimality gap

This is used as the solver termination criterion and affects both:

* solution quality
* computational time

---

# 3. Special Procedure for Stochastic Optimisation

---

## Duration Slice Subproblem

When the stochastic method is selected, a MILP sub-problem is solved to determine duration slices.

The user can define:

* Number of slices between 0 and 24

### Important Note

Increasing the number of slices increases:

* Number of variables
* Computational complexity
* Total solution time

---

## Running the Fast Forward Selection (FFS) Algorithm

Initially, the stochastic model may generate:

* More than 1000 scenarios

Using the FFS algorithm, users can reduce this large scenario set into a smaller number of representative scenarios.

The algorithm:

* Selects the most representative scenarios
* Recalculates scenario probabilities
* Preserves statistical behaviour

The user must provide:

* Desired number of final scenarios

This significantly improves computational tractability.


<img width="432" height="360" alt="image" src="https://github.com/user-attachments/assets/96ba847f-0298-4f80-8b9f-1ec8dbeb758d" />



---

# 4. Output Results

After optimisation is completed:

* Results are generated automatically
* Output files are saved in the designated folders

The GUI allows users to:

* Visualise outputs
* Compare scenarios
* Analyse system performance
* Evaluate decarbonisation pathways

---

# 5. General Comments

All modelling approaches in PHOS-UK follow the same general workflow described above.

Users can:

* Run the complete framework using the main GUI
* Execute each model independently

It is not mandatory to use the general file.

Each individual model file contains:

* Objective function
* Mathematical constraints
* Optimisation formulation
* Model-specific assumptions

This allows advanced users to directly work with individual models.

---

## 📬 Support

The authors are available to provide guidance and technical support for users regarding:

* Model execution
* Input preparation
* Solver configuration
* Troubleshooting

For further assistance, please contact the project authors.

---

## 📜 Contact

Mohammad Hemmati m.hemmati@ucl.ac.uk; Vassilis M. Charitopoulos, v.charitopoulos@ucl.ac.uk

---
