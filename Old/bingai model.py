# Import numpy and scipy libraries for numerical and scientific computing
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt


# Define the pharmacokinetic model as a system of ordinary differential equations
def pk_model(y, t, dose_i, dose_d, t_d, v_c, v_p, q, cl):
    # y is a vector of state variables: y = [c_c, c_p]
    # t is the time
    # dose_i is the initial bolus dose of heparin
    # dose_d is the multiple dose of heparin
    # t_d is the dosing interval
    # v_c, v_p, q, cl are the model parameters

    # Unpack the state variables
    c_c = y[0]  # anti-factor Xa activity in the central compartment
    c_p = y[1]  # anti-factor Xa activity in the peripheral compartment

    # Define the drug input function
    def input_t(t):
        if t == 0:  # initial bolus dose at time zero
            return dose_i / v_c
        elif t % t_d == 0:  # multiple doses at regular intervals
            return dose_d / v_c
        else:  # no drug input at other times
            return 0

    # Write the differential equations
    dc_c_dt = input_t(t) + q * (c_p / v_p - c_c / v_c) - (cl / v_c) * c_c  # mass balance equation for central compartment
    dc_p_dt = q * (c_c / v_c - c_p / v_p)  # mass balance equation for peripheral compartment

    # Return the derivatives
    return [dc_c_dt, dc_p_dt]


# Define the pharmacodynamic model as a function of anti-factor Xa activity and model parameters
def pd_model(c_c, act_0, e_max, c_50):
    # c_c is the anti-factor Xa activity in the central compartment
    # act_0, e_max, c_50 are the model parameters

    # Write the Emax model equation
    act = act_0 + (e_max * c_c) / (c_50 + c_c)  # activated clotting time as a function of anti-factor Xa activity

    # Return the pharmacodynamic response
    return act


# Define some example values for the model parameters and initial conditions
dose_i = 25000   # initial bolus dose of heparin in IU
dose_d = 5000  # multiple dose of heparin in IU
t_d = 1  # dosing interval in hours
v_c = 3.1  # volume of distribution of the central compartment in liters
v_p = 2.23  # volume of distribution of the peripheral compartment in liters
q = 4.67  # intercompartmental clearance in liters per hour
cl = 0.841  # elimination clearance in liters per hour
act_0 = 116  # baseline activated clotting time in seconds
e_max = 720  # maximal response value in seconds
c_50 = 3.49  # anti-factor Xa activity producing 50% of the maximal response value in IU per ml

y_0 = [dose_i / v_c, 0]  # initial conditions for anti-factor Xa activities

# Define the time grid for simulation
t = np.linspace(0, 100, 100)  # time points from 0 to 6 hours with 100 steps

# Solve the pharmacokinetic model using scipy.integrate.odeint function
y = odeint(pk_model, y_0, t, args=(
    dose_i, dose_d, t_d, v_c, v_p, q, cl))  # solve the ODE system and get the state variables at each time point

# Extract the anti-factor Xa activities from the solution
c_c = y[:, 0]  # anti-factor Xa activity in the central compartment
c_p = y[:, 1]  # anti-factor Xa activity in the peripheral compartment

# Calculate the activated clotting time using the pharmacodynamic model function
act = pd_model(c_c, act_0, e_max, c_50)  # activated clotting time at each time point

# Plot anti-factor Xa activity
plt.plot(t, c_c, label="Central")
plt.plot(t, c_p, label="Peripheral")
plt.xlabel("Time (hours)")
plt.ylabel("Anti-factor Xa activity (IU/ml)")
plt.title("Pharmacokinetic model of heparin")
plt.legend()
plt.show()

# Plot activated clotting time
plt.plot(t, act, label="ACT")
plt.xlabel("Time (hours)")
plt.ylabel("Activated clotting time (s)")
plt.title("Pharmacodynamic model of heparin")
plt.legend()
plt.show()
