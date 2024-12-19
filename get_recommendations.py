import pandas as pd

df = pd.read_csv('recommender/imdb_movies.csv')

df['text'] = df['names']+' '+df['overview']
df['text']

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

# list of english stop words to remove
tfidf = TfidfVectorizer(stop_words='english')
# creating tfidf matrix
tfidf_matrix = tfidf.fit_transform(df['text'])
# creating cosine similarity matrix
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

indices = pd.Series(df.index, index=df['names']).drop_duplicates()

def get_recommendations(title, cosine_sim=cosine_sim, count=10):
    title_match = df[df['names'].str.contains(title, case=False, na=False)]['names'].iloc[0]
    idx = indices[title_match]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:count+1]
    movie_indices = [i[0] for i in sim_scores]
    return df['names'].iloc[movie_indices]

print(get_recommendations('Croods', count=10))

if __name__ == '__main__':
    print(get_recommendations('Croods', count=10))