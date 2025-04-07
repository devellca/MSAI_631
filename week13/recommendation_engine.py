import pandas as pd
from sklearn.datasets import load_iris
from sklearn.metrics.pairwise import cosine_similarity

def load_data():
    iris = load_iris()
    df = pd.DataFrame(iris.data, columns=iris.feature_names)
    df['species'] = pd.Categorical.from_codes(iris.target, iris.target_names)
    return df

def compute_similarity(df):
    features = df.iloc[:, :-1]
    similarity_matrix = cosine_similarity(features)
    return similarity_matrix

def get_recommendations(index, similarity_matrix, df, top_n=5):
    similarity_scores = list(enumerate(similarity_matrix[index]))
    similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
    top_indices = [i for i, score in similarity_scores if i != index][:top_n]
    recommendations = df.iloc[top_indices].copy()
    recommendations['similarity_score'] = [similarity_matrix[index][i] for i in top_indices]
    return recommendations