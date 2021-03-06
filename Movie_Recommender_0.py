import pandas as pd
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

"""Simple Recommendation System"""
data = pd.read_csv('/content/movies_metadata.csv', low_memory = False)
#data.head(5)
C = data['vote_average'].mean()
m = data['vote_count'].quantile(0.90)
top_movies = data.copy().loc[data['vote_count'] >= m]
#top_movies.shape
print(data.shape)

def score(df):
  v = df['vote_count']
  R = df['vote_average']
  #IMDB formula
  return (v/(v+m) * R) + (m/(m+v) * C)
top_movies['top'] = top_movies.apply(score, axis = 1)
top_movies = top_movies.sort_values('top', ascending = False)

"""Content-Based Recommendation System
NOTE: This part of the code needs a sufficient memory size due to the dataset size
(more than 12 GB)"""


#using TF_IDF to diminish the weight of the stop words in the overview
tfidf = TfidfVectorizer(stop_words= 'english')
data['overview'] = data['overview'].fillna('')
tfidf_matrix = tfidf.fit_transform(data['overview'])

#create a new series which contains the movie title as an index
indices = pd.Series(data.index, index = data['title']).drop_duplicates()

#using cosine similarity to compare the movies scores
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)


def recommend(title, cosine_sim = cosine_sim):
  
  id = indices[title]
  #list the compared socres
  sim_scores = list(enumerate(cosine_sim[id]))
  #sort the list of scores
  sim_scores = sorted(sim_scores, key = lambda x : x[1], reverse = True)
  #extract the top ten matches
  sim_scores = sim_scores[1:11]
    
  movie_indices = [i[0] for i in sim_scores]
#Return the top 10 most similar movies
  return data['title'].iloc[movie_indices]

recommend('The Dark Knight Rises')

