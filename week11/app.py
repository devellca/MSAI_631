import streamlit as st
import pandas as pd
from sklearn.datasets import load_iris
from recommendation_engine import get_recommendations

iris = load_iris()
data = pd.DataFrame(iris.data, columns=iris.feature_names)
data['species'] = iris.target

data['name'] = ['Iris-' + str(i) for i in data.index]

st.title("Iris Data Recommendation Engine")

name_list = data['name'].tolist()
selected_name = st.selectbox("Select a record name:", name_list)

if st.button('Recommend'):
    recommendations = get_recommendations(selected_name)
    st.write("Top 5 similar records:")
    for name in recommendations:
        st.write(name)
    
    st.write("Details of similar records:")
    st.write(data[data['name'].isin(recommendations)])