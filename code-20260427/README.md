# Revealing infrastructure-coupled solar resources for transportation decarbonization: High-resolution assessment of roadside PV potential in China

## Project Overview

This repository provides three standalone Python scripts and corresponding demo datasets for assessing roadside photovoltaic (PV) potential in China. Each script serves a distinct purpose and can be used **independently** or **together** for full-chain assessment:

1. **Roadside Resource Assessment**: Calculate available roadside area and estimate installable capacity.
2. **Solar Resource Simulation**: Estimate POA irradiance and panel efficiency based on optimal tilt angle.
3. **Hourly Generation Calculation**: Combine installed capacity with hourly PV coefficients to compute power output for 8760 hours.

Each script is located in its own folder, with associated input data and individual usage instructions in a `README.md`.

## Project Structure

| Requirement            | Notes                                                   |
| ---------------------- | ------------------------------------------------------- |
| Standalone source code | Three separate, executable Python scripts               |
| Demo dataset           | Based on a section of the Daguang Expressway in Beijing |

```
project_root/
├── road_source/        # Roadside area and capacity estimation
├── solar_source/             # Optimal tilt and POA irradiance simulation
├── generation&accuracy/  # Hourly power output calculation
```

> Each folder contains: main script, demo input files, and its own README file

## System Requirements (tested)

- **Operating system**: Windows 10
- **Python version**: 3.9
- **Recommended environment**: Conda or venv virtual environment
- **Hardware**: No special hardware required (standard desktop/laptop is sufficient)

## Installation Guide

Install required packages using pip:

```
bash
pip install pandas numpy pvlib geopy scipy openpyxl
```

- Each code folder contains its own `README.md` explaining specific file structures and input formats.
- Estimated installation time: under 5–15 minutes on a standard internet connection.

## Demo

Each script is accompanied by a demo using real data from a section of the **Daguang Expressway in Beijing**, including:

- Road geometry data (`coordinates`)
- Meteorological inputs (irradiance, temperature, albedo)
- Grid reference files and tilt angle data

Run each script individually as described in its folder-level `README.md` to reproduce example results.