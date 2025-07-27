import pickle
import streamlit as st
import pandas as pd
import requests
import gdown

url = "https://drive.google.com/file/d/1PJ5UMjXEVoAt-L5qe4bmuCDaQ3vr9JCq/view?usp=drive_link"
gdown.download(url, "similarity.pkl", quiet=False)

# Fetch poster
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8"
    data = requests.get(url).json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

# Recommendation logic
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(enumerate(similarity[index]), key=lambda x: x[1], reverse=True)
    movie_names, posters = [], []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        movie_names.append(movies.iloc[i[0]].title)
        posters.append(fetch_poster(movie_id))
    return movie_names, posters

# Load data
movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# UI
st.title('Movie Recommender System')
selected_movie = st.selectbox("Type or select a movie", movies['title'].values)

if st.button('Show Recommendation'):
    names, posters = recommend(selected_movie)
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.text(names[i])
            st.image(posters[i])
