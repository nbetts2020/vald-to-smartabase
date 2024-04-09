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

def process_csv(vald, metric_choice):
    test_type = vald["Test"][0]
    test_type_split = test_type.split(" ")

    l_mean_force1 = abbr_dict[vald["Test"][0]][0] + f" L {metric_choice} Force"
    r_mean_force1 = abbr_dict[vald["Test"][0]][0] + f" R {metric_choice} Force"
    l_mean_force2 = abbr_dict[vald["Test"][0]][1] + f" L {metric_choice} Force"
    r_mean_force2 = abbr_dict[vald["Test"][0]][1] + f" R {metric_choice} Force"
    ratio_col = False
    for col in vald.columns:
        if "Ratio" in col:
            ratio_col = True
            break
    if ratio_col:
        l_mean_force_ratio = test_type_split[0] + " L " + test_type_split[0] + f" {metric_choice} Force Ratio"
        r_mean_force_ratio = test_type_split[0] + " R " + test_type_split[0] + f" {metric_choice} Force Ratio"
        if test_type == "Shoulder IR/ER":
            movement_specific_columns = [r_mean_force2, l_mean_force2, r_mean_force1, l_mean_force1, r_mean_force_ratio, l_mean_force_ratio]
        else:
            movement_specific_columns = [l_mean_force1, r_mean_force1, l_mean_force2, r_mean_force2, l_mean_force_ratio, r_mean_force_ratio]
        new_vald = pd.DataFrame(columns = ['Date','About','by','Test Type', movement_specific_columns,'event-uuid','group-uuid'])
        new_vald = {
        "Date": [0] * int(len(vald["Date UTC"])/2),
        "About": [0] * int(len(vald["Date UTC"])/2),
        "by": ["Vald API"] * int(len(vald["Date UTC"])/2),
        "Test Type": [0] * int(len(vald["Date UTC"])/2),
        abbr_dict[vald["Test"][0]][0] + f" L {metric_choice} Force": [0] * int(len(vald["Date UTC"])/2),
        abbr_dict[vald["Test"][0]][0] + f" R {metric_choice} Force": [0] * int(len(vald["Date UTC"])/2),
        abbr_dict[vald["Test"][0]][1] + f" L {metric_choice} Force": [0] * int(len(vald["Date UTC"])/2),
        abbr_dict[vald["Test"][0]][1] + f" R {metric_choice} Force": [0] * int(len(vald["Date UTC"])/2),
        test_type_split[0] + " L " + test_type_split[0] + f" {metric_choice} Force Ratio": [0] * int(len(vald["Date UTC"])/2),
        test_type_split[0] + " R " + test_type_split[0] + f" {metric_choice} Force Ratio": [0] * int(len(vald["Date UTC"])/2),
        "event-uuid": ["n/a"] * int(len(vald["Date UTC"])/2),
        "group-uuid": ["n/a"] * int(len(vald["Date UTC"])/2)
    }
    else:
        if test_type == "Shoulder IR/ER":
            movement_specific_columns = [r_mean_force2, l_mean_force2, r_mean_force1, l_mean_force1]
        else:
            movement_specific_columns = [l_mean_force1, r_mean_force1, l_mean_force2, r_mean_force2]
        new_vald = pd.DataFrame(columns = ['Date','About','by','Test Type', movement_specific_columns,'event-uuid','group-uuid'])
        new_vald = {
        "Date": [0] * int(len(vald["Date UTC"])/2),
        "About": [0] * int(len(vald["Date UTC"])/2),
        "by": ["Vald API"] * int(len(vald["Date UTC"])/2),
        "Test Type": [0] * int(len(vald["Date UTC"])/2),
        abbr_dict[vald["Test"][0]][0] + f" L {metric_choice} Force": [0] * int(len(vald["Date UTC"])/2),
        abbr_dict[vald["Test"][0]][0] + f" R {metric_choice} Force": [0] * int(len(vald["Date UTC"])/2),
        abbr_dict[vald["Test"][0]][1] + f" L {metric_choice} Force": [0] * int(len(vald["Date UTC"])/2),
        abbr_dict[vald["Test"][0]][1] + f" R {metric_choice} Force": [0] * int(len(vald["Date UTC"])/2),
        "event-uuid": ["n/a"] * int(len(vald["Date UTC"])/2),
        "group-uuid": ["n/a"] * int(len(vald["Date UTC"])/2)
    }


    for i in range(len(vald)):
        if i % 2 == 0:
            new_vald["Date"][int(.5*i)] = vald["Date UTC"][i]
            new_vald["About"][int(.5*i)] = vald["Name"][i]
            new_vald["Test Type"][int(.5*i)] = vald["Test"][i]
            new_vald[abbr_dict[vald["Test"][0]][0] + f" L {metric_choice} Force"][int(.5*i)] = vald[f"L {metric_choice} Force (N)"][i]
            new_vald[abbr_dict[vald["Test"][0]][0] + f" R {metric_choice} Force"][int(.5*i)] = vald[f"R {metric_choice} Force (N)"][i]
            new_vald[abbr_dict[vald["Test"][0]][1] + f" L {metric_choice} Force"][int(.5*i)] = vald[f"L {metric_choice} Force (N)"][i+1]
            new_vald[abbr_dict[vald["Test"][0]][1] + f" R {metric_choice} Force"][int(.5*i)] = vald[f"R {metric_choice} Force (N)"][i+1]
            if ratio_col:
                metric_choice = metric_choice if metric_choice != "Mean" else "Avg"
                new_vald[test_type_split[0] + " L " + test_type_split[0] + f" {metric_choice} Force Ratio"][int(.5*i)] = vald[f"L {metric_choice} Ratio"][i]
                new_vald[test_type_split[0] + " R " + test_type_split[0] + f" {metric_choice} Force Ratio"][int(.5*i)] = vald[f"R {metric_choice} Ratio"][i]

    df = pd.DataFrame(new_vald)
    return df

st.title("Vald to Smartabase CSV Processor")
st.write("Upload your VALD CSV and select the metric to process.")

uploaded_file = st.file_uploader("", type="csv")
metric_choice = st.selectbox("Select the metric to process", ["Max", "Mean", "Min"])

if uploaded_file is not None:
    vald = load_vald(uploaded_file)
    if st.button("Process"):
        df = process_csv(vald, metric_choice)
        st.write(df)
        
        # Convert DataFrame to CSV for download
        csv = df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()  # Encode to Base64
        href = f'<a href="data:file/csv;base64,{b64}" download="processed_vald.csv">Download Processed CSV</a>'
        st.markdown(href, unsafe_allow_html=True)
