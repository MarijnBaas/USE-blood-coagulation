# import relevant libraries
from scipy.integrate import solve_ivp
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import tkinter as tk

# read the data from an Excel file
data = pd.read_excel('Dataset Xa vs ACT goed.xlsx')
# extract the anti-factor Xa and ACT columns as lists
Anti_Xa = list(data['Antifactor Xa (IU/mL)'])
ACT_data = list(data['ACT (s)'])

# define a function to calculate patient specific central volume through bodyweight
def patient_vci(v_c_baseline, b_vc_bw, bw_i, wi_vc):
    # use the formula given in the problem description
    v_ci = v_c_baseline + b_vc_bw * np.log10(bw_i / 70.0) + wi_vc
    # return the calculated value
    return v_ci

# define a function to calculate patient specific peripheral volume through bodyweight
def patient_vpi(v_p_baseline, b_vp_bw, bw_i, wi_vp):
    # use the formula given in the problem description
    v_pi = v_p_baseline + b_vp_bw * np.log10(bw_i / 70.0) + wi_vp
    # return the calculated value
    return v_pi

# define a function to solve the differential equations through solve_ivp
def pk_model(t, y, dose_i, dose_d, t_d, v_c, v_p, q, cl):
    # unpack the state variables from the input vector y
    c_c, c_p = y
    # check if the current time is a multiple of the dosing interval
    if t % t_d == 0:
        # if yes, then add the dose amount to the input term
        input_t = dose_d / v_c
        print(input_t)
    else:
        # if no, then set the input term to zero
        input_t = 0.0
    # calculate the rate of change of c_c using the given equation
    dc_c_dt = input_t + q * (c_p / v_p - c_c / v_c) - (cl / v_c) * c_c
    # calculate the rate of change of c_p using the given equation
    dc_p_dt = q * (c_c / v_c - c_p / v_p)
    # return the vector of derivatives as output
    return [dc_c_dt, dc_p_dt]

# define a function to calculate the ACT values using the given equation
def ACT(ACT0, Emax, C50, c_c):
    ACT = ACT0 + (Emax * c_c) / (C50 + c_c)
    return ACT

# define the parameters for the model as given in the problem description
v_c_baseline = 3.1
v_p_baseline = 2.23
b_vc_bw = 1.02
b_vp_bw = 1.02
bw_i = 77.5
wi_vc = 0
wi_vp = 0

# calculate the patient-specific volumes using the defined functions and print them
v_ci = patient_vci(v_c_baseline, b_vc_bw, bw_i, wi_vc)
v_pi = patient_vpi(v_p_baseline, b_vp_bw, bw_i, wi_vp)
print(v_ci)
print(v_pi)

# assign the volumes to shorter names for convenience
v_c = v_ci
v_p = v_pi

# define the other parameters for the model as given in the problem description
q = 4.67
c_l = 0.841
dosed_i = 30000.0
dosed_d = 50000.0
td = 2

# define the parameters for the ACT equation as given in the problem description
ACT0 = 116.0
Emax = 600.0
C50 = 3490

# define the initial conditions for the state variables as given in the problem description
initial_conditions = [dosed_i / v_c, 0.0]

# define the initial and final time points for the simulation
t0 = 0
t1 = 10

# define a vector of time points where the solution is computed with a fixed step size of 0.01
t_eval = np.linspace(t0, t1, int((t1 - t0) / 0.01) + 1)

# solve the differential equations
sol = solve_ivp(pk_model, (t0, t1), initial_conditions, args=(dosed_i, dosed_d, td, v_c, v_p, q, c_l),
                dense_output=True, t_eval=t_eval)

# extract the solution vectors for c_c and c_p from the solution object
c_c = sol.y[0]
c_p = sol.y[1]

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import tkinter as tk

# Define the functions for anti-factor Xa activity and ACT
def plot_antifactor_xa():
    # Extract solution vectors for c_c and c_p from the solution object
    c_c = sol.y[0]
    c_p = sol.y[1]

    # Create a Matplotlib figure for anti-factor Xa activity
    fig = Figure(figsize=(5, 4))
    ax = fig.add_subplot(1, 1, 1)

    # Plot the anti-factor Xa activity in the central and peripheral compartments over time
    ax.plot(sol.t, c_c / 1000, label='c_c')
    ax.plot(sol.t, c_p / 1000, label='c_p')

    # Add labels and title
    ax.set_xlabel('Time (h)')
    ax.set_ylabel('Anti-factor Xa activity (IU/mL)')
    ax.set_title('Anti-Factor Xa Activity')
    ax.legend()

    # Return the FigureCanvasTkAgg object
    return FigureCanvasTkAgg(fig, master=root)

def plot_act():
    # Calculate the ACT values using the ACT function and the solution vector for c_c
    ACT_plot = ACT(ACT0, Emax, C50, c_c)

    # Create a Matplotlib figure for ACT
    fig = Figure(figsize=(5, 4))
    ax = fig.add_subplot(1, 1, 1)

    # Plot the ACT values over time
    ax.plot(sol.t, ACT_plot, label='ACT', color='red')

    # Add labels and title
    ax.set_xlabel('Time (h)')
    ax.set_ylabel('ACT (s)')
    ax.set_title('Activating Factor Xa Inhibitor (AFX) Anti-Clotting Time (ACT)')
    ax.legend()

    # Return the FigureCanvasTkAgg object
    return FigureCanvasTkAgg(fig, master=root)

# Initialize the Tkinter application
root = tk.Tk()
root.title('Anti-factor Xa and ACT Simulation')
root.geometry("1920x1080")

# Create a frame to hold the plots
plot_frame = tk.Frame(root)
plot_frame.pack()

# Create buttons for the anti-factor Xa plot and ACT plot
antifactor_xa_button = tk.Button(plot_frame, text='Anti-factor Xa Activity', command=lambda: plot_antifactor_xa().get_tk_widget().pack(side='left'))
act_button = tk.Button(plot_frame, text='ACT', command=lambda: plot_act().get_tk_widget().pack(side='left'))

# Pack the buttons
antifactor_xa_button.pack()
act_button.pack()

# Run the Tkinter main loop
root.mainloop()
