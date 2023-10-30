import streamlit as st
import pandas as pd
import base64

# Abbreviation Dictionary
abbr_dict = {
    "Hip AD/AB": ["Hip Abduction", "Hip Adduction"],
    "Shoulder IR/ER": ["Shoulder Internal Rotation", "Shoulder External Rotation"],
    "Hip IR/ER": ["Hip Internal Rotation", "Hip External Rotation"],
    "Ankle IN/EV": ["Ankle Inversion", "Ankle Eversion"]
}

def load_vald(file):
    vald = pd.read_csv(file)
    return vald

def process_csv(vald):
    test_type = vald["Test"][0]
    test_type_split = test_type.split(" ")

    l_mean_force1 = abbr_dict[vald["Test"][0]][0] + " L Mean Force"
    r_mean_force1 = abbr_dict[vald["Test"][0]][0] + " R Mean Force"
    l_mean_force2 = abbr_dict[vald["Test"][0]][1] + " L Mean Force"
    r_mean_force2 = abbr_dict[vald["Test"][0]][1] + " R Mean Force"
    l_mean_force_ratio = test_type_split[0] + " L " + test_type_split[0] + " Mean Force Ratio"
    r_mean_force_ratio = test_type_split[0] + " R " + test_type_split[0] + " Mean Force Ratio"
    movement_specific_columns = [l_mean_force1, r_mean_force1, l_mean_force2, r_mean_force2, l_mean_force_ratio, r_mean_force_ratio]
    new_vald = pd.DataFrame(columns = ['Date','About','by','Test Type', movement_specific_columns,'event-uuid','group-uuid'])

    new_vald = {
        "Date": [0] * int(len(vald["Date UTC"])/2),
        "About": [0] * int(len(vald["Date UTC"])/2),
        "by": ["Vald API"] * int(len(vald["Date UTC"])/2),
        "Test Type": [0] * int(len(vald["Date UTC"])/2),
        abbr_dict[vald["Test"][0]][0] + " L Mean Force": [0] * int(len(vald["Date UTC"])/2),
        abbr_dict[vald["Test"][0]][0] + " R Mean Force": [0] * int(len(vald["Date UTC"])/2),
        abbr_dict[vald["Test"][0]][1] + " L Mean Force": [0] * int(len(vald["Date UTC"])/2),
        abbr_dict[vald["Test"][0]][1] + " R Mean Force": [0] * int(len(vald["Date UTC"])/2),
        test_type_split[0] + " L " + test_type_split[0] + " Mean Force Ratio": [0] * int(len(vald["Date UTC"])/2),
        test_type_split[0] + " R " + test_type_split[0] + " Mean Force Ratio": [0] * int(len(vald["Date UTC"])/2),
        "event-uuid": ["n/a"] * int(len(vald["Date UTC"])/2),
        "group-uuid": ["n/a"] * int(len(vald["Date UTC"])/2)
    }


    for i in range(len(vald)):
        if i % 2 == 0:
            new_vald["Date"][int(.5*i)] = vald["Date UTC"][i]
            new_vald["About"][int(.5*i)] = vald["Name"][i]
            new_vald["Test Type"][int(.5*i)] = vald["Test"][i]
            new_vald[abbr_dict[vald["Test"][0]][0] + " L Mean Force"][int(.5*i)] = vald["L Avg Force (N)"][i]
            new_vald[abbr_dict[vald["Test"][0]][0] + " R Mean Force"][int(.5*i)] = vald["R Avg Force (N)"][i]
            new_vald[abbr_dict[vald["Test"][0]][1] + " L Mean Force"][int(.5*i)] = vald["L Avg Force (N)"][i+1]
            new_vald[abbr_dict[vald["Test"][0]][1] + " R Mean Force"][int(.5*i)] = vald["R Avg Force (N)"][i+1]
            new_vald[test_type_split[0] + " L " + test_type_split[0] + " Mean Force Ratio"][int(.5*i)] = vald["L Avg Ratio"][i]
            new_vald[test_type_split[0] + " R " + test_type_split[0] + " Mean Force Ratio"][int(.5*i)] = vald["R Avg Ratio"][i]

    df = pd.DataFrame(new_vald)
    return df

st.title("CSV Processor")
st.write("Upload your VALD CSV")

uploaded_file = st.file_uploader("", type="csv")

if uploaded_file is not None:
    vald = load_vald(uploaded_file)
    
    if st.button("Process"):
        df = process_csv(vald)
        st.write(df)
        
        csv = df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
        href = f'<a href="data:file/csv;base64,{b64}" download="processed_vald.csv">Download Processed CSV</a>'
        st.markdown(href, unsafe_allow_html=True)




