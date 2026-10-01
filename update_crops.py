import pandas as pd

file_path = "data/crop_pollination_value.csv"

# Load the existing CSV
df = pd.read_csv(file_path)

# Proportional values for Almonds based on ABS state production shares:
# Victoria (54,792 t): $277.40M | SA (28,947 t): $146.55M | NSW (18,609 t): $94.21M | WA (1,034 t): $5.23M
almond_records = [
    {
        "state": "Victoria",
        "crop": "Almonds",
        "category": "Nut",
        "production_tonnes": 54791.93,
        "farm_gate_value_m_aud": 277.40,
        "pollination_dependency": 1.0,
        "pollination_value_m_aud": 277.40,
    },
    {
        "state": "South Australia",
        "crop": "Almonds",
        "category": "Nut",
        "production_tonnes": 28946.68,
        "farm_gate_value_m_aud": 146.55,
        "pollination_dependency": 1.0,
        "pollination_value_m_aud": 146.55,
    },
    {
        "state": "New South Wales",
        "crop": "Almonds",
        "category": "Nut",
        "production_tonnes": 18608.58,
        "farm_gate_value_m_aud": 94.21,
        "pollination_dependency": 1.0,
        "pollination_value_m_aud": 94.21,
    },
    {
        "state": "Western Australia",
        "crop": "Almonds",
        "category": "Nut",
        "production_tonnes": 1033.81,
        "farm_gate_value_m_aud": 5.23,
        "pollination_dependency": 1.0,
        "pollination_value_m_aud": 5.23,
    },
]

# Drop any existing Almond entries to avoid duplicates
df = df[df["crop"] != "Almonds"]

# Append complete almond records
df = pd.concat([df, pd.DataFrame(almond_records)], ignore_index=True)

# Save back to CSV
df.to_csv(file_path, index=False)
print("Updated data/crop_pollination_value.csv successfully.")