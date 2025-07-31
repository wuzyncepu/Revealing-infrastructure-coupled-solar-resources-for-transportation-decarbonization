import pandas as pd
import pvlib
import numpy as np
from scipy.spatial.distance import cdist
from pvlib import irradiance

def match_optimal_tilt(grids_file, optimal_tilt_file):
    """Match each point in grids.xlsx with nearest tilt angle from optimal_tilt.xlsx."""
    df1 = pd.read_excel(grids_file)
    df2 = pd.read_excel(optimal_tilt_file)

    coords1 = df1[['latitude', 'longitude']].values
    coords2 = df2[['纬度', '经度']].values
    distances = cdist(coords1, coords2)
    nearest_indices = np.argmin(distances, axis=1)
    df1['最佳安装倾角'] = df2.iloc[nearest_indices]['最佳安装倾角'].values

    return df1  # returns matched DataFrame with tilt info


def process_single_file(input_csv, output_csv, grids_df_with_tilt):
    """Process a single CSV file with solar and power calculations."""
    df = pd.read_csv(input_csv)
    real_index_value = df.at[0, 'real_index']

    # Match tilt angle
    match_row = grids_df_with_tilt[grids_df_with_tilt['real_index'] == real_index_value]
    if match_row.empty:
        print(f"No matching tilt angle for real_index = {real_index_value}")
        return

    latitude = match_row.iloc[0]['latitude']
    longitude = match_row.iloc[0]['longitude']

    tilt_str = str(match_row.iloc[0]['最佳安装倾角']).replace('°', '')
    try:
        beta = float(tilt_str)
    except ValueError:
        beta = 30.0  # default
    df['beta'] = beta

    # Generate hourly time index for 2022
    start_time = pd.Timestamp('2022-01-01 08:00', tz='Asia/Shanghai')
    times = pd.date_range(start=start_time, periods=8760, freq='H')
    df.index = times[:len(df)]

    # Solar position
    solpos = pvlib.solarposition.get_solarposition(times, latitude, longitude)
    df['azimuth'] = solpos['azimuth'].values

    # DNI / DHI calculation
    ghi = df['ALLSKY_SFC_SW_DWN']
    sza = df['SZA']
    dni = irradiance.dirint(ghi, solar_zenith=sza, times=times)
    dni[ghi == 0] = 0
    cos_zenith = np.cos(np.radians(sza))
    dhi = ghi - dni * cos_zenith
    df['DNI'] = dni.values
    df['DHI'] = dhi.values

    # POA irradiance
    poa = irradiance.get_total_irradiance(
        surface_tilt=beta,
        surface_azimuth=180,# Fixed: 180; single-axis/dual: azimuth
        solar_zenith=df['SZA'],
        solar_azimuth=df['azimuth'],
        dni=df['DNI'],
        ghi=ghi,
        dhi=dhi,
        albedo=df['ALLSKY_SRF_ALB'],
        model='klucher'
    )
    df['poa_global_1'] = poa['poa_global']

    # Temperature + power efficiency
    I_0 = 1000
    T_0 = 25
    DE = 0.7
    df['T_t'] = df['T2M'] + df['poa_global_1'] / 1000 * ((T_0 - 20) / 0.8)
    df['P_eta'] = DE * (df['poa_global_1'] / I_0) * (1 - 0.0046 * (df['T_t'] - T_0))

    # Save to output file
    df.to_csv(output_csv, index=False, encoding='utf_8_sig')
    print(f"File processed and saved to: {output_csv}")


# === Example usage ===
grids_file = 'grids.xlsx'  # Grid index and corresponding latitude/longitude for all locations
optimal_tilt_file = 'optimal_tilt.xlsx'  # Latitude, longitude, and optimal tilt angle for each county/city in China
input_csv = 'input_ss.csv'  # Input: hourly meteorological data for a single grid point, must include irradiance, temperature, surface albedo, solar zenith angle, and grid index
output_csv = 'output_ss.csv'  # Output: includes optimal tilt angle (beta) for the PV panel (example uses fixed PV), actual irradiance received by the panel surface(poa), and capacity factor(P_eta)


grids_with_tilt_df = match_optimal_tilt(grids_file, optimal_tilt_file)
process_single_file(input_csv, output_csv, grids_with_tilt_df)