import numpy as np
from scipy.integrate import solve_ivp

# Define the parameters
Vc = 3.1  # Volume of the central compartment
Vp = 2.23  # Volume of the peripheral compartment
Q = 4.67   # Flow rate between compartments
Cl = 0.841  # Clearance rate from the central compartment
Dosed = 25000.0  # Dose administered
td = 0  # Time of dosing

# Define the differential equations
def model(t, y):
    Cc, Cp = y
    input_t = Dosed / Vc if t == td else 0.0
    dCc_dt = input_t + Q * (Cp / Vp - Cc / Vc) - Cl / Vc * Cc
    dCp_dt = Q * (Cc / Vc - Cp / Vp)
    return [dCc_dt, dCp_dt]

# Initial conditions
initial_conditions = [Dosed / Vc, 0.0]

# Time span
t_span = (0.0, 10.0)  # Adjust the end time as needed

# Solve the differential equations
sol = solve_ivp(model, t_span, initial_conditions, t_eval=np.linspace(0.0, 10.0, 100))

# Extract the results
t = sol.t
Cc = sol.y[0]
Cp = sol.y[1]

# Plot the results (you can use matplotlib for this)
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))
plt.plot(t, Cc, label='Cc')
plt.plot(t, Cp, label='Cp')
plt.xlabel('Time')
plt.ylabel('Concentration')
plt.legend()
plt.grid()
plt.show()