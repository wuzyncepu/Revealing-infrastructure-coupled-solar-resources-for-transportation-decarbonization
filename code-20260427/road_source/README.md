# Road Resource Assessment

## Introduction
This code parses coordinate data to calculate path distances and estimates the available roadside land area and corresponding installable PV capacity, considering different categories of PV tracking systems.

### Input/Output Description

| File Name        | Description                                                  |
| ---------------- | ------------------------------------------------------------ |
| `input_rs.xlsx`  | Input Excel file containing road coordinates, bridge/tunnel flags, road type (`fclass`), and reference ID |
| `output_rs.xlsx` | Output Excel file with calculated distance, interpolated efficiency, available area, and 9 capacity estimates |

## Functional Overview
1. **Distance Calculation**: Computes the actual path distance based on coordinate columns.
2. **Land Efficiency Matching**: Uses interpolation to estimate land-use standards based on latitude.
3. **Usable Area Estimation**: Calculates available land area for highways and railways under three scenarios.
4. **Capacity Estimation**: Combines area and efficiency to calculate PV capacity under nine scenario combinations.

## Dependencies
- pip install pandas numpy geopy scipy openpyxl

## How to Use
1. Set the input and output folder paths.
2. Ensure the input files contain necessary columns such as `coordinates` and `latitude`.
3. Run the script to automatically batch process all files and output the results with newly added columns.