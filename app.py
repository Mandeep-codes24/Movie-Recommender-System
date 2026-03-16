
import pickle
import streamlit as st
import requests
from concurrent.futures import ThreadPoolExecutor
import joblib


# -----------------------------
# TMDB API KEY
# -----------------------------
API_KEY = st.secrets["TMDB_API_KEY"] 

# -----------------------------
# Load data with caching
# -----------------------------
@st.cache_data
def load_data():
    movies = pickle.load(open('movies.pkl', 'rb'))
    similarity = joblib.load("similarity.joblib")
    return movies, similarity

movies, similarity = load_data()

# -----------------------------
# Fetch poster with title fallback
# -----------------------------
def fetch_poster(movie_id, title=""):
    try:
        # Step 1: Try by movie_id
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        poster_path = data.get('poster_path')  # ✅ .get() won't throw KeyError

        # Step 2: Fallback — search by title if no poster found
        if not poster_path and title:
            search_url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={title}"
            search_res = requests.get(search_url, timeout=5)
            search_data = search_res.json()
            results = search_data.get('results', [])
            if results:
                poster_path = results[0].get('poster_path')

        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
        else:
            return None

    except Exception:
        return None

# -----------------------------
# Recommendation function
# -----------------------------
def recommend(movie):
    try:
        index = movies[movies['title'] == movie].index[0]
    except IndexError:
        st.error("Movie not found.")
        return [], []

    distances = sorted(
        list(enumerate(similarity[index])),
        reverse=True,
        key=lambda x: x[1]
    )

    recommended_movie_names = []
    recommended_movie_ids = []

    for i in distances[1:6]:
        recommended_movie_names.append(movies.iloc[i[0]].title)
        recommended_movie_ids.append(movies.iloc[i[0]].movie_id)

    # Fetch all posters in parallel
    with ThreadPoolExecutor(max_workers=5) as executor:
        recommended_movie_posters = list(executor.map(
            lambda args: fetch_poster(*args),
            zip(recommended_movie_ids, recommended_movie_names)
        ))

    return recommended_movie_names, recommended_movie_posters

# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="wide")

st.markdown("""
    <style>
        h1 { color: #e50914; }
        .movie-title {
            color: #ffffff;
            font-size: 13px;
            font-weight: 600;
            margin-top: 8px;
            text-align: center;
        }
        .no-poster {
            height: 375px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: #1e1e1e;
            border-radius: 10px;
            color: #555;
            font-size: 14px;
            border: 1px dashed #333;
        }
    </style>
""", unsafe_allow_html=True)

st.title("🎬 Movie Recommender System")
st.markdown("Type or select a movie and click **Show Recommendation**.")

movie_list = movies['title'].values
selected_movie = st.selectbox("Type or select a movie from the dropdown", movie_list)

# -----------------------------
# Button
# -----------------------------
if st.button('Show Recommendation'):
    with st.spinner("Fetching recommendations..."):
        recommended_movie_names, recommended_movie_posters = recommend(selected_movie)

    if recommended_movie_names:
        st.subheader("Top 5 Recommendations")
        cols = st.columns(5)

        for col, name, poster in zip(cols, recommended_movie_names, recommended_movie_posters):
            with col:
                if poster:
                    st.image(poster, width=250)          
                else:
                    st.markdown(
                        '<div class="no-poster">No Poster Available</div>',
                        unsafe_allow_html=True
                    )
                st.markdown(f'<div class="movie-title">{name}</div>', unsafe_allow_html=True)


