import pandas as pd

# -------------------------------------------------------------
# 1. PROCESS ABS HORTICULTURAL CROP DATA (ECONOMIC VALUES)
# -------------------------------------------------------------
filepath_abs = "data/AAHDC_Aust_Horticulture_202223.xlsx"

# Standard AgriFutures / Klein et al. pollination dependency benchmark ratios
pollination_dependency_map = {
    'Almonds': 1.00,       # 100% insect dependent
    'Apples': 1.00,        # 100%
    'Cherries': 1.00,      # 100%
    'Blueberries': 1.00,   # 100%
    'Macadamias': 0.90,    # 90%
    'Avocados': 0.65,      # 65%
    'Muskmelons': 0.65,    # 65%
    'Watermelons': 0.65,   # 65%
    'Plums': 0.65,         # 65%
    'Strawberries': 0.40,  # 40%
    'Rubus berries': 0.80, # 80%
    'Pears': 0.65,         # 65%
    'Oranges': 0.20,       # 20%
    'Mandarins': 0.20      # 20%
}

target_states = [
    'New South Wales', 'Victoria', 'Queensland', 
    'South Australia', 'Western Australia', 'Tasmania', 'Northern Territory'
]

crop_records = []
for sheet, category in [('Table 2', 'Fruit'), ('Table 4', 'Nut')]:
    df_raw = pd.read_excel(filepath_abs, sheet_name=sheet, header=5)
    for crop, dep in pollination_dependency_map.items():
        prod_col = f"{crop} - Production (t)"
        val_col = f"{crop} - Farm gate value ($m)"
        
        df_crop = df_raw[df_raw['Data item'].isin([prod_col, val_col])]
        for state in target_states:
            state_slice = df_crop[df_crop['Region'] == state]
            prod = state_slice[state_slice['Data item'] == prod_col]['2022-23'].values
            val = state_slice[state_slice['Data item'] == val_col]['2022-23'].values
            
            p_val = float(prod[0]) if len(prod) > 0 and pd.notna(prod[0]) and str(prod[0]).strip() not in ['-', 'np'] else 0.0
            v_val = float(val[0]) if len(val) > 0 and pd.notna(val[0]) and str(val[0]).strip() not in ['-', 'np'] else 0.0
            
            if v_val > 0 or p_val > 0:
                crop_records.append({
                    'state': state,
                    'crop': crop,
                    'category': category,
                    'production_tonnes': round(p_val, 2),
                    'farm_gate_value_m_aud': round(v_val, 2),
                    'pollination_dependency': dep,
                    'pollination_value_m_aud': round(v_val * dep, 2)
                })

df_crops = pd.DataFrame(crop_records)
df_crops.to_csv("data/crop_pollination_value.csv", index=False)
print(f"Saved crop_pollination_value.csv ({len(df_crops)} rows)")

# -------------------------------------------------------------
# 2. PROCESS ALA HONEY BEE OCCURRENCES
# -------------------------------------------------------------
filepath_ala = "data/records-2026-09-24.csv"
keep_cols = ['stateProvince', 'year', 'month', 'decimalLatitude', 'decimalLongitude']

df_bee = pd.read_csv(filepath_ala, usecols=keep_cols, low_memory=False)

# Filter: Clean records, modern decade (2015-2026), valid coordinates
df_bee = df_bee.dropna(subset=['decimalLatitude', 'decimalLongitude', 'year', 'stateProvince'])
df_bee = df_bee[df_bee['stateProvince'].isin(target_states + ['Australian Capital Territory'])]
df_bee['year'] = df_bee['year'].astype(int)
df_bee = df_bee[df_bee['year'] >= 2015].copy()

# Round coords to 3 decimals to reduce file size while maintaining street-level map precision
df_bee['latitude'] = df_bee['decimalLatitude'].round(3)
df_bee['longitude'] = df_bee['decimalLongitude'].round(3)
df_bee.rename(columns={'stateProvince': 'state'}, inplace=True)

# Export clean point records
df_bee_export = df_bee[['state', 'year', 'month', 'latitude', 'longitude']]
df_bee_export.to_csv("data/bee_observations_clean.csv", index=False)
print(f"Saved bee_observations_clean.csv ({len(df_bee_export)} rows, under 1 MB)")

# Export summary aggregation for high-speed time series & choropleths
df_summary = df_bee.groupby(['state', 'year']).size().reset_index(name='observation_count')
df_summary.to_csv("data/bee_state_yearly_counts.csv", index=False)
print("Saved bee_state_yearly_counts.csv")