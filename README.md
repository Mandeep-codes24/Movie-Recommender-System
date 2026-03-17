🎬 Movie Recommendation System

An AI-powered content-based movie recommender system that suggests similar movies based on user selection using NLP and similarity techniques.

🚀 Live Demo

🔗 https://your-streamlit-app-link

📌 Project Overview

This project builds a movie recommendation engine using Natural Language Processing (NLP) and Machine Learning techniques.
It analyzes movie metadata such as genres, cast, crew, and keywords to recommend similar movies.

The system is deployed as an interactive web app using Streamlit.

⚙️ Features

🎯 Recommend Top 5 similar movies

🧠 Uses content-based filtering

🔍 NLP-based feature extraction (tags, cast, genres, keywords)

🎞 Fetches movie posters using TMDB API

⚡ Fast performance with caching & parallel API calls

🌐 Deployed on Streamlit Cloud

🛠 Tech Stack

Python

Pandas & NumPy

Scikit-learn

NLP (CountVectorizer)

Streamlit

TMDB API

Joblib

🧠 How It Works

Combine important features:

genres

cast

crew

keywords

Preprocess text:

lowercasing

stemming

removing spaces

Convert text → vectors using:

CountVectorizer (Bag of Words)

Compute similarity:

Cosine Similarity

Recommend top similar movies

📂 Dataset

Dataset used:
👉 https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata

The dataset contains:

tmdb_5000_movies.csv

tmdb_5000_credits.csv

movie titles

genres

cast & crew

keywords

overview



