import pandas as pd

# Load the CSV file into a DataFrame
data_file = "data.csv"  # Replace with your uploaded file path
df = pd.read_csv(data_file)

# Add Copyleft column combining strong_copyleft and weak_copyleft
def add_copyleft_column(row):
    if row['strong_copyleft']:
        return "Strong Copyleft"
    elif row['weak_copyleft']:
        return "Weak Copyleft"
    return ""

df['copyleft'] = df.apply(add_copyleft_column, axis=1)

# Remove rows where copyleft is empty
df = df[df['copyleft'] != ""]

# Group data by license family, lob, and copyleft
def group_by_license_family(df):
    grouped = df.groupby(['copyleft', 'license_family', 'lob']).agg({
        'total_seals_lob': 'first',
        'threshold': 'mean'
    }).reset_index()
    return grouped

# Generate report as a DataFrame
def generate_report_dataframe():
    grouped_df = group_by_license_family(df)
    sorted_lobs = grouped_df.groupby('lob')['total_seals_lob'].mean().sort_values(ascending=False).index
    
    data = []
    columns = ["License Family"] + list(sorted_lobs)
    
    # Top Row: Total SEALs
    total_seals = ["Total SEALs"] + [
        f"{grouped_df[grouped_df['lob'] == lob]['total_seals_lob'].mean():.0f}" 
        if not grouped_df[grouped_df['lob'] == lob].empty else "0%"
        for lob in sorted_lobs
    ]
    data.append(total_seals)

    # Add Rows for Copyleft and License Families
    for copyleft in grouped_df['copyleft'].unique():
        data.append([copyleft] + [""] * len(sorted_lobs))  # Copyleft Header remains empty
        copyleft_data = grouped_df[grouped_df['copyleft'] == copyleft]
        for license_family in copyleft_data['license_family'].unique():
            family_data = copyleft_data[copyleft_data['license_family'] == license_family]
            row = [license_family]
            for lob in sorted_lobs:
                lob_data = family_data[family_data['lob'] == lob]
                value = f"{lob_data['threshold'].iloc[0]:.1f}%" if not lob_data.empty else "0%"
                row.append(value)
            data.append(row)
    
    report_df = pd.DataFrame(data, columns=columns)
    return report_df

# Conditional formatting function
def highlight_threshold(val):
    if isinstance(val, str) and "%" in val:
        percentage = float(val.strip('%'))
        if percentage > 20:
            return 'background-color: red; color: white;'
        elif percentage > 10:
            return 'background-color: yellow; color: black;'
        else:
            return 'background-color: green; color: white;'
    return ''  # No formatting for other cells

# Apply special formatting for Total SEALs and Title Rows
def highlight_special_rows(row):
    if row.name == 0:  # Total SEALs Row
        return ['background-color: #6fa8dc; font-weight: bold; color: white; text-align: center;'] * len(row)
    elif "Copyleft" in row[0]:  # Title Rows
        return ['background-color: #d9d9d9; font-weight: bold; color: black; text-align: center;'] * len(row)
    else:
        return ['text-align: center;'] * len(row)

# Generate the report DataFrame
report_df = generate_report_dataframe()

# Apply conditional formatting
# Updated Table Styles
styled_df = (report_df.style
             .applymap(highlight_threshold)  # Color cells based on thresholds
             .apply(highlight_special_rows, axis=1)  # Add special row formatting
             .set_table_styles([
                 {'selector': 'th', 'props': [('font-weight', 'bold'), 
                                              ('background-color', '#4f81bd'), 
                                              ('color', 'white'),
                                              ('text-align', 'center')]},
                 {'selector': 'th.col0', 'props': [('color', 'transparent')]},  # Hide "License Family"
                 {'selector': 'thead th.index_name', 'props': [('color', 'transparent')]},  # Hide index header
                 {'selector': 'tbody th', 'props': [('color', 'transparent')]}  # Hide index values
             ])
             .set_properties(**{'border': '1px solid lightgray', 'padding': '4px'})  # Add cell borders and padding
            )

# Display the styled DataFrame
styled_df
