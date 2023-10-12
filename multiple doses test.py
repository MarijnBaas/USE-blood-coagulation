# import relevant libraries
from scipy.integrate import solve_ivp
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

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

method = 'RK45'

# solve the differential equations
sol = solve_ivp(pk_model, (t0, t1), initial_conditions, args=(dosed_i, dosed_d, td, v_c, v_p, q, c_l),
                dense_output=True, t_eval=t_eval)

# extract the solution vectors for c_c and c_p from the solution object
c_c = sol.y[0]
c_p = sol.y[1]

# plot the anti-factor Xa activity in the central and peripheral compartments over time
plt.plot(sol.t, c_c / 1000, label='c_c')
plt.plot(sol.t, c_p / 1000, label='c_p')
plt.xlabel('Time (h)')
plt.ylabel('Anti-factor Xa activity (IU/mL)')
plt.legend()
plt.show()

# calculate the ACT values using the defined function and the solution vector for c_c
ACT = ACT(ACT0, Emax, C50, c_c)

# plot the ACT values over time
plt.plot(sol.t, ACT, label='ACT', color='red')
plt.xlabel('Time (h)')
plt.ylabel('ACT (s)')
plt.legend()
plt.show()

# plot the relationship between ACT and anti-factor Xa activity and also scatter the data points from the Excel file
#plt.plot(c_c / 1000, ACT)
#plt.scatter(Anti_Xa, ACT_data, s=5, color='red')
#plt.yticks(np.arange(0, 1100, step=250))
#plt.xlabel('Anti-factor Xa activity (IU/mL)')
#plt.ylabel('ACT (s)')
#plt.title('ACT vs Xa activity')
#plt.show()
