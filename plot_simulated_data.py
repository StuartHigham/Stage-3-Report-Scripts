import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# Find all original profile files (exclude _filtered and _integrated)
file_pattern = 'cpr_profile_*cmps2.csv'
file_list = sorted([f for f in glob.glob(file_pattern) if '_filtered' not in f and '_integrated' not in f])

# Set up 2-column subplot grid (original | integrated + filtered)
num_files = len(file_list)
fig, axes = plt.subplots(num_files, 2, figsize=(16, 3 * num_files), sharex='col')

# Handle single file case
if num_files == 1:
    axes = [axes]

# Plot each CPR profile row
for i, file_path in enumerate(file_list):
    base_name = os.path.basename(file_path).replace('.csv', '')
    label = base_name.split('_')[-1]

    # Left subplot: Original acceleration
    ax_left = axes[i][0]
    df = pd.read_csv(file_path)
    ax_left.plot(df['Time (s)'], df['Acceleration_g'], label='Original Accel', color='b')
    ax_left.set_ylabel('Acceleration (g)')
    ax_left.set_title(f'Original - Peak {label}')
    ax_left.grid(True)
    ax_left.legend()

    # Right subplot: Integrated + Filtered displacement
    ax_right = axes[i][1]

    plotted_any = False

    # Try plotting integrated
    integrated_path = file_path.replace('.csv', '_integrated.csv')
    if os.path.exists(integrated_path):
        df_integrated = pd.read_csv(integrated_path)
        ax_right.plot(df_integrated['Time (s)'], df_integrated['Displacement_mm'],
                      label='Integrated', color='r')
        plotted_any = True

    # Try plotting filtered
    filtered_path = file_path.replace('.csv', '_filtered.csv')
    if os.path.exists(filtered_path):
        df_filtered = pd.read_csv(filtered_path)
        ax_right.plot(df_filtered['Time (s)'], df_filtered['Displacement_mm'],
                      label='Filtered', color='g')
        plotted_any = True
    
    # Try plotting filtered
    filtered_path = file_path.replace('.csv', '_kalman.csv')
    if os.path.exists(filtered_path):
        df_filtered = pd.read_csv(filtered_path)
        ax_right.plot(df_filtered['Time (s)'], df_filtered['Displacement_mm'],
                      label='Kalman Filtered', color='black')
        plotted_any = True
    
    if not plotted_any:
        ax_right.text(0.5, 0.5, 'No integrated/filtered data', ha='center', va='center', transform=ax_right.transAxes)

    ax_right.set_ylabel('Displacement (mm)')
    ax_right.set_title(f'Displacement - Peak {label}')
    ax_right.grid(True)
    ax_right.legend()

# Label x-axis for the bottom row
axes[-1][0].set_xlabel('Time (s)')
axes[-1][1].set_xlabel('Time (s)')
plt.tight_layout()
plt.show()
