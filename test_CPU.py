import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import time
from filters import integrate_twice_live, integrate_twice_live_filtered

def main():
    # === Load the input file ===
    # List all CSV files in the current directory
    files = [f for f in os.listdir() if f.endswith('cmps2.csv')]
    print("Available CSV files:")
    for i, filename in enumerate(files):
        print(f"{i}: {filename}")
    choice = int(input("Enter the number of the file to use and click enter: "))
    file_path = f'cpr_profile_{choice}cmps2.csv'
    df = pd.read_csv(file_path)
    acc = df['Acceleration_mm_s2'].values
    time_array = df['Time (s)'].values
    dt = time_array[1] - time_array[0]  # assume constant step

    # === Prepare to store results ===
    velocities = []
    displacements = []

    # === Run integration live ===
    print("Index\tVelocity (mm/s)\tDisplacement (mm)")
    disp_points = []

    print("Choose your filter:\n\t- Basic Integration (1)\n\t- Integration with filter a (2)")

    match choice:
        case 1:
            returned = integrate_twice_live(acc, dt)
        case 2:
            returned = integrate_twice_live_filtered(acc, dt)
        case _:
            print("Error: Invalid input.")
            return

    for i, v, d in choice:
        velocities.append(v)
        displacements.append(d)
        print(f"{i}\t{v:.2f}\t\t{d:.2f}")
        disp_points.append(d)

    # === Save to new CSV ===
    output_df = pd.DataFrame({
        'Time (s)': time_array,
        'Acceleration_mm_s2': acc,
        'Velocity_mm_s': velocities,
        'Displacement_mm': displacements
    })

    output_filename = file_path.replace('.csv', '_integrated.csv')
    output_df.to_csv(output_filename, index=False)
    print(f"\nResults saved to {output_filename}")

if __name__ == "__main__":
    main()
