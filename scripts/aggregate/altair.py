import altair as alt
import numpy as np

# Add a classification column to the data for filtering
df["classification"] = np.where(
    df["red_license_classification"].notnull(),
    "Red",
    np.where(
        df["green_license_classification"].notnull(),
        "Green",
        np.where(df["yellow_license_classification"].notnull(), "Yellow", "None"),
    ),
)

# Prepare the data for visualization
df_filtered = df.groupby(["package_manager", "classification"]).agg(
    distinct_package_name=("package_name", "nunique"),
    distinct_package_name_version=(
        "package_name",
        lambda x: len(x.drop_duplicates()),
    ),
    distinct_seal_id=("seal_id", "nunique"),
).reset_index()

df_filtered = df_filtered.melt(
    id_vars=["package_manager", "classification"],
    var_name="Metric",
    value_name="Count",
)

# Add dropdown filter for classification
classification_dropdown = alt.binding_select(
    options=["All", "Red", "Green", "Yellow", "None"],
    name="Classification: ",
)
classification_selection = alt.selection_single(
    fields=["classification"],
    bind=classification_dropdown,
    init={"classification": "All"},
)

# Filter data based on selection
filtered_data = df_filtered.transform_filter(
    (alt.datum.classification == "All")
    | (alt.datum.classification == classification_selection.classification)
)

# Base chart
base_chart = alt.Chart(filtered_data).mark_bar().encode(
    x=alt.X("Metric:N", title="Metric"),
    y=alt.Y("Count:Q", title="Count"),
    color="package_manager:N",
    tooltip=["package_manager", "classification", "Metric", "Count"],
).properties(
    width=700,
    height=400,
    title="Interactive Dashboard for Package Metrics",
)

# Add interactivity
interactive_dashboard = base_chart.add_selection(classification_selection)

# Display the chart
interactive_dashboard.show()
