import pandas as pd

# Example dataframe
data = {
    "package_manager": ["npm", "npm", "pip", "pip", "npm"],
    "package_name": ["pkg1", "pkg2", "pkg1", "pkg3", "pkg1"],
    "package_version": ["1.0", "2.0", "1.0", "1.0", "1.1"],
    "red_license_classification": [None, "yes", None, "yes", "yes"],
    "yellow_license_classification": ["yes", None, None, None, "yes"],
    "green_license_classification": ["yes", "yes", "yes", "yes", None],
    "target": ["prod", "Prod", "dev", "PROD", "test"],
    "seal_id": ["id1", "id2", "id3", "id4", "id5"],
}

df = pd.DataFrame(data)

# Define production filter
df['is_production'] = df['target'].str.contains("prod", case=False, na=False)

# Function to calculate aggregations
def calculate_aggregations(df):
    results = []

    for pm, group in df.groupby("package_manager"):
        # Filter for production
        prod_group = group[group['is_production']]
        # Filter for red_license_classification not null
        red_group = prod_group[prod_group['red_license_classification'].notnull()]

        # Aggregations
        row = {
            "package_manager": pm,
            "distinct_package_name_prod": prod_group["package_name"].nunique(),
            "distinct_package_name_all": group["package_name"].nunique(),
            "distinct_package_name_version_prod": prod_group[["package_name", "package_version"]].drop_duplicates().shape[0],
            "distinct_package_name_version_all": group[["package_name", "package_version"]].drop_duplicates().shape[0],
            "distinct_package_name_red_prod": red_group["package_name"].nunique(),
            "distinct_package_name_version_red_prod": red_group[["package_name", "package_version"]].drop_duplicates().shape[0],
            "distinct_seal_id_red_prod": red_group["seal_id"].nunique(),
        }
        results.append(row)

    # Convert to DataFrame
    return pd.DataFrame(results)

# Apply function
results_df = calculate_aggregations(df)

# Calculate percentages
results_df["percent_package_name_prod"] = (
    results_df["distinct_package_name_prod"] / results_df["distinct_package_name_all"] * 100
)
results_df["percent_package_name_version_prod"] = (
    results_df["distinct_package_name_version_prod"] / results_df["distinct_package_name_version_all"] * 100
)

# Display results
print(results_df)
