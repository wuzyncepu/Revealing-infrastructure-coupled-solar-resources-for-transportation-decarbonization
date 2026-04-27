# PV Potential Estimation and Error Evaluation

## Introduction
This code matches the installed PV capacity of road segments with hourly capacity factor data to estimate roadside PV output. It also performs statistical error analysis across three methods: matching-based, average-based, and centroid (single-point) methods.

## File Structure

| File / Directory       | Description                                                  |
| ---------------------- | ------------------------------------------------------------ |
| `input_rs_pg.csv`      | Input: Road segment data, including latitude, longitude, and installed capacity |
| `grids.xlsx`           | Input: Grid point reference with latitude, longitude, and corresponding `real_index` |
| `P_fixed_0-100.csv`    | Input: Hourly PV power coefficients (`P_1 ~ P_8760`) for each grid point (should include all `real_index` values) |
| `output_pg.csv`        | Output: Hourly power generation (`G_1 ~ G_8760`) for each road segment |
| `input_accuracy.xlsx`  | (Optional) Input file for error analysis between different calculation methods |
| `output_accuracy.xlsx` | (Optional) Output file containing relative error metrics     |

## Functional Overview

### 1. Nearest Grid Matching: `match_nearest_index`

- Inputs:
  - Road file with `latitude`, `longitude`
  - Grid file with `real_index`, `latitude`, `longitude`
- Output:
  - Adds a new column `nearest_area_index` to indicate the closest grid point for each road segment

### 2. Merge Power Coefficients: `merge_power_factors`

- Merges hourly PV coefficients (`P_1 ~ P_8760`) from grid data into the road data via `real_index`
- Essential for computing per-hour power generation

### 3. Compute Hourly Generation: `compute_hourly_power`

- For each hour `i`, calculates: G_i = P_i × P_e_common_24
- Deletes the original `P_1 ~ P_8760` columns after computation to save memory

## Dependencies
- pip install pandas scipy numpy openpyxl

## How to Use
1. Ensure all necessary columns are present: `latitude`, `longitude`, `real_index`, `P_e_common_24`

   The power coefficient file must cover all grid points referenced by the road data

   Processing large files (especially 8760 hours) may require higher memory

   Error analysis assumes non-zero values in `G_common_24`