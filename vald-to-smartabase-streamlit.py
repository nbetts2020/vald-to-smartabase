import streamlit as st
import pandas as pd
import base64

# Abbreviation Dictionary
abbr_dict = {
    "Hip AD/AB": ["Hip Abduction", "Hip Adduction"],
    "Shoulder IR/ER": ["Shoulder Internal Rotation", "Shoulder External Rotation"],
    "Hip IR/ER": ["Hip Internal Rotation", "Hip External Rotation"],
    "Ankle IN/EV": ["Ankle Inversion", "Ankle Eversion"],
    "Knee Flexion": ["Knee Flexion", "Knee Flexion"],
    "Knee Extension": ["Knee Extension", "Knee Extension"],
    "Hip Flexion": ["Hip Flexion", "Hip Flexion"]
}

def load_vald(file):
    vald = pd.read_csv(file)
    return vald

def process_csv(vald, metric):
    test_type = vald["Test"][0]
    test_type_split = test_type.split(" ")

    # Adjust column names based on selected metric
    l_metric_force1 = abbr_dict[vald["Test"][0]][0] + f" L {metric} Force"
    r_metric_force1 = abbr_dict[vald["Test"][0]][0] + f" R {metric} Force"
    l_metric_force2 = abbr_dict[vald["Test"][0]][1] + f" L {metric} Force"
    r_metric_force2 = abbr_dict[vald["Test"][0]][1] + f" R {metric} Force"
    l_metric_force_ratio = test_type_split[0] + f" L {test_type_split[1]} {metric} Force Ratio"
    r_metric_force_ratio = test_type_split[0] + f" R {test_type_split[1]} {metric} Force Ratio"

    movement_specific_columns = [l_metric_force1, r_metric_force1, l_metric_force2, r_metric_force2, l_metric_force_ratio, r_metric_force_ratio]
    
    # Setting up the new DataFrame structure with columns for the selected metric values
    new_vald = {"Date": [0] * int(len(vald["Date UTC"])/2),
                "About": [0] * int(len(vald["Date UTC"])/2),
                "by": ["Vald API"] * int(len(vald["Date UTC"])/2),
                "Test Type": [0] * int(len(vald["Date UTC"])/2)}
                
    for col in movement_specific_columns:
        new_vald[col] = [0] * int(len(vald["Date UTC"])/2)
    
    new_vald["event-uuid"] = ["n/a"] * int(len(vald["Date UTC"])/2)
    new_vald["group-uuid"] = ["n/a"] * int(len(vald["Date UTC"])/2)

    for i in range(len(vald)):
        if i % 2 == 0:
            index = int(.5*i)
            new_vald["Date"][index] = vald["Date UTC"][i]
            new_vald["About"][index] = vald["Name"][i]
            new_vald["Test Type"][index] = vald["Test"][i]
            # Adjusting for the selected metric force and ratios
            for col_name, vald_col_name in zip(movement_specific_columns, ["L Max Force (N)", "R Max Force (N)", "L Max Force (N)", "R Max Force (N)", "L Max Ratio", "R Max Ratio"]):
                new_vald[col_name][index] = vald[vald_col_name][i] if "Ratio" not in col_name else vald[vald_col_name][i]  # Adjust for actual data structure

    df = pd.DataFrame(new_vald)
    return df

st.title("Vald to Smartabase CSV Processor")
st.write("Upload your VALD CSV and select the metric to process.")

uploaded_file = st.file_uploader("", type="csv")
metric_choice = st.selectbox("Select the metric to process", ["Max", "Mean", "Min"])  # Example options

if uploaded_file is not None and metric_choice:
    vald = load_vald(uploaded_file)
    
    if st.button("Process"):
        df = process_csv(vald, metric_choice)
        st.write(df)
        
        csv = df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="processed_vald.csv">Download Processed CSV</a>'
        st.markdown(href, unsafe_allow_html=True)
