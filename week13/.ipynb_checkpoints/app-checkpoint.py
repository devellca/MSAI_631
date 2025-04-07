# app.py
import streamlit as st
from recommendation_engine import load_data, compute_similarity, get_recommendations

# Load and prepare data
df = load_data()
similarity_matrix = compute_similarity(df)

if "history" not in st.session_state:
    st.session_state.history = []

def sort_options(history, df):
    df['priority'] = df.index.map(lambda i: 1 if i in history else 0)
    return df.sort_values(by='priority', ascending=False).drop(columns='priority')

st.title("🌸 Adaptive Iris Recommendation Engine")

sorted_df = sort_options(st.session_state.history, df)
selected_index = st.selectbox(
    "Select a flower record to get similar recommendations:",
    options=sorted_df.index,
    format_func=lambda x: f"{x}: {df.iloc[x]['species']}"
)

if st.button("Recommend"):
    if selected_index not in st.session_state.history:
        st.session_state.history.append(selected_index)

    recommendations = get_recommendations(selected_index, similarity_matrix, df)

    if selected_index in st.session_state.history[:-1]:
        st.success("👋 Welcome back! You’ve selected this flower before. Here’s a fresh look at similar blooms:")
    else:
        st.info("🌱 Here are flowers that closely match your selection:")

    for i, row in recommendations.iterrows():
        intensity = int(row.similarity_score * 200)
        bg_color = f"rgba(144, 238, 144, {row.similarity_score:.2f})"  # lightgreen with opacity
        st.markdown(
            f"<div style='background-color:{bg_color}; padding: 10px; border-radius: 10px;'>"
            f"<b>Species:</b> {row['species']}<br>"
            f"<b>Sepal Length:</b> {row['sepal length (cm)']} cm<br>"
            f"<b>Sepal Width:</b> {row['sepal width (cm)']} cm<br>"
            f"<b>Petal Length:</b> {row['petal length (cm)']} cm<br>"
            f"<b>Petal Width:</b> {row['petal width (cm)']} cm<br>"
            f"<b>Similarity Score:</b> {row.similarity_score:.2f}"
            f"</div><br>",
            unsafe_allow_html=True
        )
