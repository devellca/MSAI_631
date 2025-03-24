import pandas as pd
from sklearn.datasets import load_iris
from sklearn.metrics.pairwise import cosine_similarity

iris = load_iris()
data = pd.DataFrame(iris.data, columns=iris.feature_names)
data['species'] = iris.target

data['name'] = ['Iris-' + str(i) for i in data.index]

cosine_sim = cosine_similarity(data.drop(['species', 'name'], axis=1))

cosine_sim_df = pd.DataFrame(cosine_sim, index=data['name'], columns=data['name'])

def get_recommendations(name, cosine_sim=cosine_sim_df):
    sim_scores = cosine_sim[name]

    sim_scores = pd.Series(sim_scores).sort_values(ascending=False)

    recommendations = sim_scores.iloc[1:6]
    return recommendations.index.tolist()