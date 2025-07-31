import pandas as pd
from scipy.spatial import cKDTree

def match_nearest_index(road_file, grids_file):
    """
    For each row in the road file, find the nearest real_index in the grids file based on lat/lon.
    Add new column 'nearest_area_index'.
    """
    road_df = pd.read_csv(road_file)
    grids_df = pd.read_excel(grids_file)

    # Build KD-tree for fast nearest neighbor search
    tree = cKDTree(grids_df[['latitude', 'longitude']].values)

    # Query nearest point
    distances, indices = tree.query(road_df[['latitude', 'longitude']].values, k=1)
    road_df['nearest_area_index'] = grids_df.iloc[indices]['real_index'].values

    return road_df
def merge_power_factors(road_df, range_file):
    """
    Merge power factors P_1 ~ P_8760 into road_df using 'nearest_area_index' <-> 'real_index'
    """
    range_df = pd.read_csv(range_file)
    merged_df = pd.merge(road_df, range_df, how='left', left_on='nearest_area_index', right_on='real_index')

    if 'real_index' in merged_df.columns:
        merged_df.drop(columns=['real_index'], inplace=True)

    return merged_df


def compute_hourly_power(merged_df):
    """
    Compute G_1 ~ G_8760 by multiplying each P_i with P_e_common_24
    """
    for i in range(1, 8761):
        merged_df[f'G_{i}'] = merged_df[f'P_{i}'] * merged_df['P_e_common_24']

    # Remove P_1 ~ P_8760 columns if desired
    merged_df.drop(columns=[f'P_{i}' for i in range(1, 8761)], inplace=True)

    return merged_df


def process_single_road_file(road_file, grids_file, range_file, output_file):
    """
    Complete processing pipeline:
    1. Match nearest_area_index
    2. Merge power coefficients
    3. Compute hourly power
    4. Output
    """
    print("Matching nearest grid index...")
    road_df = match_nearest_index(road_file, grids_file)

    print("Merging power coefficients...")
    merged_df = merge_power_factors(road_df, range_file)

    print("Calculating hourly power G_1 ~ G_8760...")
    final_df = compute_hourly_power(merged_df)

    print(f"Saving result to: {output_file}")
    final_df.to_csv(output_file, index=False, encoding='utf_8_sig')
    print("All done!")


# === Example Usage ===
road_file = 'input_rs_pg.csv'           # Road file: contains latitude, longitude, real_index, and P_e_common_24 (installed capacity)
grids_file = 'grids.xlsx'               # Grid reference file: includes real_index with corresponding latitude and longitude
range_file = 'P_fixed_0-100.csv'        # PV power coefficient file (includes real_index + P_1 ~ P_8760); here shown for grid points 1–100 as an example, but should include all
output_file = 'output_pg.csv'           # Output file: result file with added G_1 ~ G_8760 (hourly power values)


process_single_road_file(road_file, grids_file, range_file, output_file)



# ## Compute relative error for each road segment(if needed)

# import pandas as pd
# import numpy as np
#
# # === Input and Output Paths ===
# input_file = r"input_accuracy.xlsx"     # Input: road segment power generation calculated by different methods (e.g., railway in Beijing area)
# output_file = r"output_accuracy.xlsx"   # Output: road segment error using average method and centroid method
#
#
# try:
#     # Step 1: Read input Excel
#     df = pd.read_excel(input_file)
#
#     # Step 2: Compute relative errors (only where G_common_24 ≠ 0)
#     valid_mask = df['G_common_24'] != 0
#     df['R_aver'] = np.nan
#     df['R_cent'] = np.nan
#
#     df.loc[valid_mask, 'R_aver'] = (
#         (df.loc[valid_mask, 'G_aver'] - df.loc[valid_mask, 'G_common_24']) / df.loc[valid_mask, 'G_common_24']
#     )
#     df.loc[valid_mask, 'R_cent'] = (
#         (df.loc[valid_mask, 'G_cent'] - df.loc[valid_mask, 'G_common_24']) / df.loc[valid_mask, 'G_common_24']
#     )
#
#     # Step 3: Save result
#     df.to_excel(output_file, index=False)
#     print(f"Processed successfully. Output saved to: {output_file}")
#
# except Exception as e:
#     print(f"Error processing file: {e}")