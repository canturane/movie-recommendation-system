import pandas as pd

# 1. movie.csv ve rating.csv files
movies = pd.read_csv("Main_Data/movie.csv")
ratings = pd.read_csv("Main_Data/rating.csv")

# 2. Upload popularfilms.csv file and get movie IDs
popularfilms = pd.read_csv("prepared_data/popularfilms.csv")

new2_movie_ids = popularfilms["movieId"].tolist()

# 3. Get only movies with the same IDs as new2_movie.csv from rating.csv
filtered_ratings = ratings[ratings["movieId"].isin(new2_movie_ids)]

# 4. Remove the timestamp column and only take scores 3.5 and above, 4.5 and below
filtered_ratings = filtered_ratings.drop(columns=["timestamp"])
filtered_ratings = filtered_ratings[
    (filtered_ratings["rating"] >= 3.5) & (filtered_ratings["rating"] <= 4.5)
]

# 5. Calculate the number of votes per user and filter active users
user_counts = filtered_ratings["userId"].value_counts()


active_users = user_counts[((user_counts > 200) & (user_counts < 3000))].index

# Apply filtered users to dataset
filtered_ratings = filtered_ratings[filtered_ratings["userId"].isin(active_users)]

# 6. Calculate the number of votes per movie and filter movies with at least 50 votes
movie_counts = filtered_ratings["movieId"].value_counts()
popular_movies = movie_counts[movie_counts >= 50].index
filtered_ratings = filtered_ratings[filtered_ratings["movieId"].isin(popular_movies)]

# 7. Save filtered data to filtered_rating.csv
filtered_ratings.to_csv(
    "prepared_data/FilteredMovie.csv",
    index=False,
)

print("filteredMovie.csv file has been created.")
