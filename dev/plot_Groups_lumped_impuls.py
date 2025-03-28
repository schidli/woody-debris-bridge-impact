# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 17:05:56 2025

@author: cscheidl/cfriedl
"""

import os
from scipy import fftpack
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import pickle
from scipy import signal
import numpy as np
import winsound
import pandas as pd
import math

# Helper function to round numbers to the nearest multiple of 10
def next_integer_from_decimal(n):
    if isinstance(n, list):
        return [next_integer_from_decimal(x) for x in n]
    elif n > 0:
        return math.ceil(n / 10) * 10
    elif n < 0:
        return math.floor(n / 10) * 10
    else:
        return 0  # Falls die Zahl 0 ist, bleibt sie 0

# Der Pfad des aktuellen Skripts
current_dir = os.getcwd()
# Relativer Pfad zu den anderen Verzeichnissen
dat_dir = os.path.join(current_dir, 'dat')
plt_dir = os.path.join(current_dir, 'fig/main/figures_5to8')
doc_dir= os.path.join(current_dir, 'fig')
# Normalisieren der Pfade
dat_dir = os.path.normpath(dat_dir)
plt_dir = os.path.normpath(plt_dir)
doc_dir=os.path.normpath(doc_dir)
# Set directory of data
#os.chdir(r'\dat\interim')
os.chdir(os.path.join(dat_dir, 'raw'))
n_exp = 40
fs = 2400

# Load horizontal impact force data
file_to_read = open("impact_force", "rb")
impact_force = pickle.load(file_to_read)

# Load time data
file_to_read = open("time", "rb")
time = pickle.load(file_to_read)

del file_to_read
#%%
df = pd.read_excel('241017_Butter_30Hz.xlsx')

u=1

os.chdir(plt_dir)
date = "240219_"
tmin = 8000
tmax = 14400
fs = 2400
# Start line in 241017_Butter_30Hz.xlsx for the search for sign change of Fz
# Indices to process
#indices = [1, 2, 3, 4, 5]
#image_path = os.path.join(doc_dir, 'symbols', 'Full_slab_nowood.png') #Setup AF
#indices = [6, 7, 8, 9, 10] 
image_path = os.path.join(doc_dir, 'symbols', 'Full_slab_wood10.png') #Setup BF
indices = [11, 12, 13, 14, 15] 
#image_path = os.path.join(doc_dir, 'symbols', 'Full_slab_wood15.png') #Setup CF
#indices = [16, 17, 18, 19, 20] 
#image_path = os.path.join(doc_dir, 'symbols', 'Full_slab_wood20.png') #Setup DF
#indices = [21, 22, 23, 24, 25] 
#image_path = os.path.join(doc_dir, 'symbols', 'Trough_nowood.png') #Setup AT
#indices = [26, 27, 28, 29, 30] 
#image_path = os.path.join(doc_dir, 'symbols', 'Trough_wood10.png') #Setup BT
#indices = [31, 32, 33, 34, 35] 
#image_path = os.path.join(doc_dir, 'symbols', 'Trough_wood15.png') #Setup CT
#indices = [36, 37, 38, 39, 40] 
#image_path = os.path.join(doc_dir, 'symbols', 'Trough_wood20.png') #Setup DT
# Initialize lists to store data
Fy_data = []
Fz_data = []
time_data = []

# Collect data for the specified indices
for i in indices:
    Fy_data.append(impact_force[i][:,1] + impact_force[i][:,4])
    Fz_data.append(impact_force[i][:,2] + impact_force[i][:,5])
    ##########!!!!!!!ATTENTION!!!!!!!!!!!!################################
    ## There is an issue with the start time for the runs 16 -25
    ######################################################################
    ## For all othe runs use:
    time_data.append(time[i])
    # only for indices 16 - 25 use:
    #time_data.append(time[i]+3)
    ##########!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!##############################
    ######################################################################    
# Find the time shift for each index to align the forces
time_shifts = []
for i in range(len(indices)):
    # Find the first time point where Fy or Fz is greater than zero
    Fy_nonzero_index = np.argmax(Fy_data[i] > 0.5)
    Fz_nonzero_index = np.argmax(Fz_data[i] > 0.5)
    first_nonzero_index = min(Fy_nonzero_index, Fz_nonzero_index)
    time_shifts.append(time_data[i][first_nonzero_index])

# Use the minimum time shift to align all data
min_time_shift = min(time_shifts)

# Adjust time data to align all forces
aligned_time_data = []
aligned_Fy_data = []
aligned_Fz_data = []
for i in range(len(indices)):
    shift = time_shifts[i] - min_time_shift
    aligned_time = time_data[i] - shift
    nonzero_start_index = np.argmax(aligned_time >= 0)
    aligned_time_data.append(aligned_time[nonzero_start_index:])
    aligned_Fy_data.append(Fy_data[i][nonzero_start_index:])
    aligned_Fz_data.append(Fz_data[i][nonzero_start_index:])

# Find the minimum length of the aligned data to ensure uniformity
min_length = min(len(data) for data in aligned_time_data)

# Truncate all data to the minimum length
aligned_time_data = [data[:min_length] for data in aligned_time_data]
aligned_Fy_data = [data[:min_length] for data in aligned_Fy_data]
aligned_Fz_data = [data[:min_length] for data in aligned_Fz_data]
# Normalize the time data between 0 and 1
#normalized_time_data = [(data - data.min()) / (data.max() - data.min()) for data in aligned_time_data]
# Convert aligned data to numpy arrays for easier manipulation
aligned_time_data = np.array(aligned_time_data)
aligned_Fy_data = np.array(aligned_Fy_data)
aligned_Fz_data = np.array(aligned_Fz_data)

# Calculate mean and standard deviation for the aligned data
Fy_mean = np.mean(aligned_Fy_data, axis=0)
Fy_std = np.std(aligned_Fy_data, axis=0)
Fz_mean = np.mean(aligned_Fz_data, axis=0)
Fz_std = np.std(aligned_Fz_data, axis=0)

# Use the time data from the first index (assuming all time arrays are the same)
#time_mean = normalized_time_data[0]
time_mean = aligned_time_data[0]
####################################################################################
# Plotting mean and standard deviation for each experimental setup
####################################################################################
fig, ax = plt.subplots(1, figsize=(25, 15), dpi=600)

# Plot mean and standard deviation for Fy
ax.plot(time_mean, Fy_mean, color='green', linewidth=5, label='$\it{F_{Y}}$ Mean')
ax.fill_between(time_mean, Fy_mean - Fy_std, Fy_mean + Fy_std, color='green', alpha=0.3, label='$\it{F_{Y}}$ Std Dev')

# Plot mean and standard deviation for Fz
ax.plot(time_mean, Fz_mean, color='blue', linewidth=5, label='$\it{F_{Z}}$ Mean')
ax.fill_between(time_mean, Fz_mean - Fz_std, Fz_mean + Fz_std, color='blue', alpha=0.3, label='$\it{F_{Z}}$ Std Dev')
line8=plt.axhline(xmin=0,xmax=1,y=0, color = 'grey', linewidth = 1, linestyle = 'dashed')
# Define the min and max values for the Y-axis
min_ax = [min(Fy_mean - Fy_std), min(Fz_mean - Fz_std)]
max_ax = [max(Fy_mean + Fy_std), max(Fz_mean + Fz_std)]
F_array = [max_ax, min_ax]
axes = next_integer_from_decimal(F_array)
max_ax = max(axes)
min_ax = min(axes)
# Set Y-axis ticks
yticks = np.arange(int(-90), int(90) + 1, step=20)
#yticks = np.arange(int(min(min_ax)), int(max(max_ax)) + 1, step=10)
plt.yticks(yticks)
for ytick in yticks:
    plt.axhline(y=ytick, color='grey', linewidth=0.5, linestyle='dashed')
#plt.yticks(np.linspace(min(min_ax), max(max_ax), num=int((max(max_ax) - min(min_ax)) / 10) + 1))
plt.ylim(-100, 100)
#plt.ylim(min(min_ax), max(max_ax))
plt.xlabel('$\it{t}$ [s]', fontsize=50)
plt.ylabel('$\it{F}$ [N]', fontsize=50)
plt.tick_params(axis="both", which='both', labelsize=45)

plt.legend(loc='upper right', labelspacing=0.25, frameon=True, fontsize=45)
plt.xlim(3, 6)
arr_img = plt.imread(image_path)
im = OffsetImage(arr_img, zoom=1.8)
ab = AnnotationBbox(im, (0.60, 0.85), xycoords='axes fraction', bboxprops=dict(facecolor='white', edgecolor='lightgrey', boxstyle='round,pad=0.5', alpha=0.8))
ax.add_artist(ab)
fig.tight_layout()
plt.show

# Generate the filename based on the first index
filename = f"impact_forces_mean_std_aligned_index_{indices[0]}.png"
plt.savefig(filename)
x=0
####################################################################################
#Plotting individual plots for each replicate
####################################################################################
for x in range(len(indices)):
    i = indices[x]
    IF_Z_ganz = (aligned_Fz_data[x])
    data_exp = pd.DataFrame({'IF_Z': IF_Z_ganz})
    filename = f'231025_IFZ_{i}.xlsx'
    data_exp.to_excel(filename, index=False)
    time_y = aligned_time_data[x][np.argmax(aligned_Fy_data[x])]
    time_z = aligned_time_data[x][np.argmin(aligned_Fz_data[x])]
    time_zm = aligned_time_data[x][np.argmax(aligned_Fz_data[x])]
    
    match i:
        case 1:
            start_row = 8400
            image_path = os.path.join(doc_dir, 'symbols', 'Full_slab_nowood.png')
        case 2:
            start_row = 8400
            image_path = os.path.join(doc_dir, 'symbols', 'Full_slab_nowood.png')
        case 3:
            start_row = 8700
            image_path = os.path.join(doc_dir, 'symbols', 'Full_slab_nowood.png')
        case 4:
            start_row = 8640
            image_path = os.path.join(doc_dir, 'symbols', 'Full_slab_nowood.png')
        case 5:
            start_row = 8500
            image_path = os.path.join(doc_dir, 'symbols', 'Full_slab_nowood.png')
        case 6:
            start_row = 9699
            image_path = os.path.join(doc_dir, 'symbols', 'Full_slab_wood10.png')
        case 7:
            start_row = 9000
            image_path = os.path.join(doc_dir, 'symbols', 'Full_slab_wood10.png')
        case 8:
            start_row = 9400
            image_path = os.path.join(doc_dir, 'symbols', 'Full_slab_wood10.png')
        case 9:
            start_row = 9500
            image_path = os.path.join(doc_dir, 'symbols', 'Full_slab_wood10.png')
        case 10:
            start_row = 9600
            image_path = os.path.join(doc_dir, 'symbols', 'Full_slab_wood10.png')
        case 11:
            start_row = 9600
            image_path = os.path.join(doc_dir, 'symbols', 'Full_slab_wood15.png')
        case 12:
            start_row = 9800
            image_path = os.path.join(doc_dir, 'symbols', 'Full_slab_wood15.png')
        case 13:
            start_row = 9600
            image_path = os.path.join(doc_dir, 'symbols', 'Full_slab_wood15.png')
        case 14:
            start_row = 9600
            image_path = os.path.join(doc_dir, 'symbols', 'Full_slab_wood15.png')
        case 15:
            start_row = 9600
            image_path = os.path.join(doc_dir, 'symbols', 'Full_slab_wood15.png')
        case 16:
            start_row = 9600
            image_path = os.path.join(doc_dir, 'symbols', 'Full_slab_wood20.png')
        case 17:
            start_row = 9600
            image_path = os.path.join(doc_dir, 'symbols', 'Full_slab_wood20.png')
        case 18:
            start_row = 9800
            image_path = os.path.join(doc_dir, 'symbols', 'Full_slab_wood20.png')
        case 19:
            start_row = 10600
            image_path = os.path.join(doc_dir, 'symbols', 'Full_slab_wood20.png')
        case 20:
            start_row = 9800
            image_path = os.path.join(doc_dir, 'symbols', 'Full_slab_wood20.png')
        case 21:
            start_row = 9150
            image_path = os.path.join(doc_dir, 'symbols', 'Trough_nowood.png')
        case 22:
            start_row = 9800
            image_path = os.path.join(doc_dir, 'symbols', 'Trough_nowood.png')
        case 23:
            start_row = 9250
            image_path = os.path.join(doc_dir, 'symbols', 'Trough_nowood.png')
        case 24:
            start_row = 9300
            image_path = os.path.join(doc_dir, 'symbols', 'Trough_nowood.png')
        case 25:
            start_row = 9200
            image_path = os.path.join(doc_dir, 'symbols', 'Trough_nowood.png')
        case 26:
            start_row = 9800
            image_path = os.path.join(doc_dir, 'symbols', 'Trough_wood10.png')
        case 27:
            start_row = 9800
            image_path = os.path.join(doc_dir, 'symbols', 'Trough_wood10.png')
        case 28:
            start_row = 9700
            image_path = os.path.join(doc_dir, 'symbols', 'Trough_wood10.png')
        case 29:
            start_row = 10000
            image_path = os.path.join(doc_dir, 'symbols', 'Trough_wood10.png')
        case 30:
            start_row = 9800
            image_path = os.path.join(doc_dir, 'symbols', 'Trough_wood10.png')
        case 31:
            start_row = 8800
            image_path = os.path.join(doc_dir, 'symbols', 'Trough_wood15.png')
        case 32:
            start_row = 8950
            image_path = os.path.join(doc_dir, 'symbols', 'Trough_wood15.png')
        case 33:
            start_row = 9200
            image_path = os.path.join(doc_dir, 'symbols', 'Trough_wood15.png')
        case 34:
            start_row = 9150
            image_path = os.path.join(doc_dir, 'symbols', 'Trough_wood15.png')
        case 35:
            start_row = 9000
            image_path = os.path.join(doc_dir, 'symbols', 'Trough_wood15.png')
        case 36:
            start_row = 9800
            image_path = os.path.join(doc_dir, 'symbols', 'Trough_wood20.png')
        case 37:
            start_row = 9600
            image_path = os.path.join(doc_dir, 'symbols', 'Trough_wood20.png')
        case 38:
            start_row = 9800
            image_path = os.path.join(doc_dir, 'symbols', 'Trough_wood20.png')
        case 39:
            start_row = 9800
            image_path = os.path.join(doc_dir, 'symbols', 'Trough_wood20.png')
        case 40:
            start_row = 9900
            image_path = os.path.join(doc_dir, 'symbols', 'Trough_wood20.png')
        case _:
            start_row = 5000

    # List to store row numbers with sign changes
    sign_change_rows = []

    # Iterate over the IF_Z column starting from the start row
    for u in range(start_row, len(data_exp) - 1):
        current_value = data_exp.loc[u, 'IF_Z']
        next_value = data_exp.loc[u + 1, 'IF_Z']
        
        # Check if the sign is different
        if (current_value > 0 and next_value < 0) or (current_value < 0 and next_value > 0):
            sign_change_rows.append(u)

    # Ensure there is at least one sign change
    if not sign_change_rows:
        continue

    to_ = sign_change_rows[0]
    from_ = sign_change_rows[0] + 1
    max1 = impact_force[i][:, 1].max()
    min1 = impact_force[i][:, 1].min()
    maxFy = [max1 + impact_force[i][:, 4].max()]
    minFy = [min1 + impact_force[i][:, 4].min()]
    # Fz
    max1 = impact_force[i][:, 2].max()
    min1 = impact_force[i][:, 2].min()
    maxFz = [max1 + impact_force[i][:, 5].max()]
    minFz = [min1 + impact_force[i][:, 5].min()]
    F_array = [maxFy, minFy , maxFz, minFz]
    axes = next_integer_from_decimal(F_array)
    max_ax = max(axes)
    min_ax = min(axes)
    exp_name = str(i)
    fig, ax = plt.subplots(1, figsize=(25, 15), dpi=600)
    if i == 22:
        aligned_time_data[x] = aligned_time_data[x] - 3
        time_y = time_y - 3
        time_z = time_z - 3
        time_zm = time_zm - 3

    # Plot Fy and Fz for the current index
    line2, = plt.plot(aligned_time_data[x], aligned_Fy_data[x], color='green', linewidth=5)
    
    # Ensure the lengths of the data arrays match before plotting
    if len(aligned_time_data[x][:to_]) == len(aligned_Fz_data[x][:to_]):
        line3, = plt.plot(aligned_time_data[x][:to_], aligned_Fz_data[x][:to_], color='red', linewidth=5)
    if len(aligned_time_data[x][from_:]) == len(aligned_Fz_data[x][from_:]):
        line4, = plt.plot(aligned_time_data[x][from_:], aligned_Fz_data[x][from_:], color='blue', linewidth=5)

    ymin_normalized = (0 - min_ax[0]) / (max_ax[0] - min_ax[0])
    Fmax_normalized = (maxFy[0] - min_ax[0]) / (max_ax[0] - min_ax[0])
    Zmax_normalized = (maxFz[0] - min_ax[0]) / (max_ax[0] - min_ax[0])
    Zmin_normalized = (minFz[0] - min_ax[0]) / (max_ax[0] - min_ax[0])

    line5 = plt.axvline(x=time_zm, ymin=ymin_normalized, ymax=Zmax_normalized, color='red', linewidth=2, linestyle='dashdot')
    line6 = plt.axvline(x=time_y, ymin=ymin_normalized, ymax=Fmax_normalized, color='green', linewidth=2, linestyle="dashdot")
    line7 = plt.axvline(x=time_z, ymin=ymin_normalized, ymax=Zmin_normalized, color='blue', linewidth=2, linestyle='dashdot')
    line8 = plt.axhline(xmin=0, xmax=1, y=0, color='grey', linewidth=1, linestyle='dashed')
    yticks = np.arange(int(min(min_ax)), int(max(max_ax)) + 1, step=10)
    plt.yticks(yticks)
    plt.ylim(min_ax[0], max_ax[0])
    plt.xlim(3, 6)
    plt.tick_params(axis="both", which='both', labelsize=45)
    for ytick in yticks:
        plt.axhline(y=ytick, color='grey', linewidth=0.5, linestyle='dashed')
    line2.set_label('$\mathit{\;\;\;F_{Y}}$')
    if 'line3' in locals():
        line3.set_label('$\mathit{+F_{Z}}$')
    if 'line4' in locals():
        line4.set_label('$\mathit{-F_{Z}}$')
    plt.text(time_zm - 0.2, min_ax[0] / 7, '$\it{t_{F_{Z,max}}}$', fontsize=45, color='red')
    plt.text(time_y + 0.06, 8, '$\it{t_{F_{Y,max}}}$', fontsize=45, color='green')
    plt.text(time_z, 2, '$\it{t_{F_{Z,min}}}$', fontsize=45, color='blue')

    plt.xlabel('$\it{t}$ [s]', fontsize=50)
    plt.ylabel('$\it{F}$ [N]', fontsize=50)
    plt.tick_params(axis="both", which='both', labelsize=45)
    plt.legend(loc='upper right', labelspacing=0.25, frameon=True, fontsize=45)
    arr_img = plt.imread(image_path)
    im = OffsetImage(arr_img)
    im = OffsetImage(arr_img, zoom=1.8)
    ab = AnnotationBbox(im, (0.70, 0.88), xycoords='axes fraction', bboxprops=dict(facecolor='white', edgecolor='lightgrey', boxstyle='round,pad=0.5', alpha=0.8))
    ax.add_artist(ab)
    fig.tight_layout()
    plt.show
    # Generate the filename based on the current index
    filenameplot = f"impact_forces_index_{indices[x]}.png"
    plt.savefig(filenameplot)

    # ####################################################################################
    # #Plotting individual impuls plots for each replicate
    # ####################################################################################
    # # Calculate the impulse (integral of force over time) for Fy and Fz
    # impulse_Fy = np.cumsum(aligned_Fy_data[x]) * (aligned_time_data[x][1] - aligned_time_data[x][0])
    # impulse_Fz = np.cumsum(aligned_Fz_data[x]) * (aligned_time_data[x][1] - aligned_time_data[x][0])

    # # Plot the impulse for Fy and Fz
    # fig, ax = plt.subplots(1, figsize=(25, 15), dpi=600)
    # ax.plot(aligned_time_data[x], impulse_Fy, color='green', linewidth=5, label='$\mathit{Impulse\;\;\;\;\;\;F_{Y}}$')

    # # Plot positive and negative impulse values for Fz separately
    # positive_impulse_Fz = np.where(impulse_Fz > 0, impulse_Fz, np.nan)
    # negative_impulse_Fz = np.where(impulse_Fz < 0, impulse_Fz, np.nan)
    # max_positive_impulse_Fy = np.max(impulse_Fy)+10
    # max_negative_impulse_Fy = -max_positive_impulse_Fy
    # ax.plot(aligned_time_data[x], positive_impulse_Fz, color='red', linewidth=5, label='$\mathit{Impulse\;+F_{Z}}$')
    # ax.plot(aligned_time_data[x], negative_impulse_Fz, color='blue', linewidth=5, label='$\mathit{Impulse\;-F_{Z}}$')
    # plt.ylim(max_negative_impulse_Fy, max_positive_impulse_Fy)
    # # Add horizontal lines at y-axis ticks
    # yticks = np.arange(math.floor(max_negative_impulse_Fy / 20) * 20, math.ceil(max_positive_impulse_Fy / 20) * 20 + 1, step=20)
    # plt.yticks(yticks)
    # for ytick in yticks:
    #     plt.axhline(y=ytick, color='grey', linewidth=0.5, linestyle='dashed')
    # plt.xlabel('$\it{t}$ [s]', fontsize=50)
    # plt.ylabel('$\it{Impulse}$ [Ns]', fontsize=50)
    # plt.tick_params(axis="both", which='both', labelsize=45)
    # plt.legend(loc='upper left', labelspacing=0.25, frameon=True, fontsize=45)
    # arr_img = plt.imread(image_path)
    # im = OffsetImage(arr_img)
    # im = OffsetImage(arr_img, zoom=1.8)
    # ab = AnnotationBbox(im, (0.45, 0.88), xycoords='axes fraction', bboxprops=dict(facecolor='white', edgecolor='lightgrey', boxstyle='round,pad=0.5', alpha=0.8))
    # ax.add_artist(ab)
    # fig.tight_layout()
    # plt.show

    # # Generate the filename for the impulse plot based on the current index
    # filename_impulse_plot = f"impulse_index_{indices[x]}.png"
    # plt.savefig(filename_impulse_plot)