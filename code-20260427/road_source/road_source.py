import pandas as pd
import numpy as np
from geopy.distance import geodesic
from scipy.interpolate import interp1d


def process_excel(input_file_path):
    # === Step 0: Read the Excel file ===
    df = pd.read_excel(input_file_path)

    # === Step 1: Calculate distance from the 'coordinates' column ===
    def calculate_row_distance(row):
        coordinates = []
        for coord in str(row.get("coordinates", "")).split(","):
            try:
                coordinates.append(float(coord))
            except ValueError:
                continue
        if len(coordinates) % 2 != 0:
            coordinates = coordinates[:-1]
        points = [(coordinates[i + 1], coordinates[i]) for i in range(0, len(coordinates), 2)]
        total_distance = 0
        for i in range(len(points) - 1):
            total_distance += geodesic(points[i], points[i + 1]).meters
        return total_distance

    df["distance"] = df.apply(calculate_row_distance, axis=1)

    # === Step 2: Calculate available_distance, excluding bridge/tunnel segments ===
    df["available_distance"] = df.apply(
        lambda row: 0 if str(row.get("bridge")).upper() == "T" or str(row.get("tunnel")).upper() == "T" else row[
            "distance"],
        axis=1
    )

    # === Step 3: Interpolate unit land efficiency S_n based on latitude ===
    latitudes = np.array([18, 20, 25, 30, 35, 40, 45, 50])

    # You can switch to other scenarios below (currently using fixed-tilt system)
    # Fixed tilt
    efficiency_20 = np.array([8.536, 8.906, 10.046, 11.623, 13.912, 17.49, 23.789, 37.625])
    efficiency_24 = np.array([7.114, 7.422, 8.372, 9.686, 11.593, 14.575, 19.824, 31.354])
    efficiency_28 = np.array([6.097, 6.362, 7.176, 8.302, 9.937, 12.493, 16.992, 26.875])

    # # Single-axis tilt
    # efficiency_20 = np.array([13.009, 13.761,16.176,19.732,25.294,34.796,53.453,100])
    # efficiency_24 = np.array([10.841, 11.468,13.480,16.444,21.078,28.997,44.544,83.656])
    # efficiency_28 = np.array([9.292, 9.829,11.554,14.095,18.067,24.854,38.181,71.705])

    # # Dual-axis tracking
    # efficiency_20 = np.array([14.18, 15,17.633,21.509,27.571,37.929,58.265,100])
    # efficiency_24 = np.array([11.817, 12.5,14.694,17.924,22.976,31.607,48.554,91.187])
    # efficiency_28 = np.array([10.129, 10.714,12.595,15.363,19.693,27.092,41.618,78.161])

    interpolation_function_20 = interp1d(latitudes, efficiency_20, kind='linear', fill_value="extrapolate")
    interpolation_function_24 = interp1d(latitudes, efficiency_24, kind='linear', fill_value="extrapolate")
    interpolation_function_28 = interp1d(latitudes, efficiency_28, kind='linear', fill_value="extrapolate")

    df['S_n_20'] = interpolation_function_20(df['latitude'])
    df['S_n_24'] = interpolation_function_24(df['latitude'])
    df['S_n_28'] = interpolation_function_28(df['latitude'])

    # === Step 4: Estimate usable area under different assumptions ===
    def multiplier_conservative(row):
        return 1 if row['fclass'] == 'motorway' else (0.25 if 's' in str(row['ref']) else 0.5)

    def multiplier_common(row):
        return 1.5 if row['fclass'] == 'motorway' else (0.5 if 's' in str(row['ref']) else 0.75)

    def multiplier_positive(row):
        return 2 if row['fclass'] == 'motorway' else (0.75 if 's' in str(row['ref']) else 1)

    df['S_e_conservative'] = df['available_distance'] * df.apply(multiplier_conservative, axis=1)
    df['S_e_common'] = df['available_distance'] * df.apply(multiplier_common, axis=1)
    df['S_e_positive'] = df['available_distance'] * df.apply(multiplier_positive, axis=1)

    # # Railway scenario (if needed, uncomment below)
    # df['S_e_conservative'] = df['available_distance'] * 3
    # df['S_e_common'] = df['available_distance'] * 4
    # df['S_e_positive'] = df['available_distance'] * 5

    # === Step 5: Calculate installed capacity (9 combinations) ===
    for tilt in [20, 24, 28]:
        for scenario in ['conservative', 'common', 'positive']:
            df[f'P_e_{scenario}_{tilt}'] = df[f'S_e_{scenario}'] / (1000 * df[f'S_n_{tilt}'])

    # === Step 6: Write results to a new Excel file ===
    output_path = "output_rs.xlsx"
    df.to_excel(output_path, index=False)
    print(f"Processing complete. Output saved to: {output_path}")


# === Example call ===
# Please make sure the input Excel file contains a 'coordinates' column with comma-separated longitude and latitude values,
# and uses the first coordinate pair to determine the 'latitude' and 'longitude' values if needed.
input_excel_path = "input_rs.xlsx"
process_excel(input_excel_path)
