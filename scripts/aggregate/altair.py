import altair as alt

# Prepare the data for visualization
df_visual = results_df.melt(
    id_vars=["package_manager"],
    value_vars=[
        "distinct_package_name_prod",
        "distinct_package_name_all",
        "distinct_package_name_version_prod",
        "distinct_package_name_version_all",
        "distinct_package_name_red_prod",
        "distinct_package_name_version_red_prod",
        "distinct_seal_id_red_prod",
    ],
    var_name="Metric",
    value_name="Count",
)

# Add a dropdown for classifications
classification_dropdown = alt.binding_select(
    options=["All", "Red", "Green", "Yellow"],
    name="Classification: ",
)
classification_selection = alt.selection_single(
    fields=["Metric"], bind=classification_dropdown, init={"Metric": "All"}
)

# Base chart
base = alt.Chart(df_visual).mark_bar().encode(
    x=alt.X("Metric:N", title="Metric"),
    y=alt.Y("Count:Q", title="Count"),
    color="package_manager:N",
    tooltip=["package_manager", "Metric", "Count"]
).transform_filter(
    classification_selection
)

# Add interactivity
interactive_chart = base.add_selection(classification_selection)

# Display the chart
interactive_chart.show()
