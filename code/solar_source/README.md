# Solar Resource Assessment

## Introduction
This code processes hourly solar irradiance and meteorological data to perform tilt angle matching, compute solar positions and irradiance components, and estimate the irradiance received by PV panels as well as the resulting capacity factor.

## File Structure

| File / Directory    | Description                                                  |
| ------------------- | ------------------------------------------------------------ |
| `grids.xlsx`        | Grid index and corresponding latitude/longitude (`real_index`, `latitude`, `longitude`) |
| `optimal_tilt.xlsx` | Optimal tilt angles for Chinese cities/counties (columns: `纬度`, `经度`, `最佳安装倾角`) |
| `input_ss.csv`      | Input: Hourly weather data for one grid point (must include `SZA`, `ALLSKY_SFC_SW_DWN`, `T2M`, `ALLSKY_SRF_ALB`, `real_index`) |
| `output_ss.csv`     | Output: Contains optimal tilt `beta`, panel-incident irradiance `poa`, and capacity factor `P_eta` |

### Function Overview

#### 1. Match Optimal Tilt: `match_optimal_tilt`

- Finds the nearest city/county for each grid point using Euclidean distance on coordinates
- Matches the corresponding optimal PV tilt angle (`最佳安装倾角`)
- Returns an extended grid dataframe with `beta` info

#### 2. Solar and Efficiency Calculation: `process_single_file`

- For each hour:
  - Retrieves matched tilt angle
  - Computes solar position using `pvlib`
  - Estimates `DNI`, `DHI`, and POA irradiance
  - Calculates module temperature and power efficiency (`P_eta`)
- Outputs include:
  - `beta`: Optimal tilt angle
  - `poa_global_1`: Global irradiance received by PV panel
  - `P_eta`: Capacity factor (efficiency)

## Dependencies
- pip install pandas numpy pvlib scipy openpyxl

## How to Use
1. Prepare CSV files containing meteorological data (e.g., GHI, SZA, T2M, etc.).
2. Set file paths and run the corresponding code blocks step by step.
3. Outputs will include estimation fields such as `poa_global_1`, `P_eta`, and `T_t`.