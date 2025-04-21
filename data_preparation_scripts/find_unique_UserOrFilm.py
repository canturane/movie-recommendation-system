import pandas as pd

# Upload CSV file

ratings = pd.read_csv("prepared_data/FilteredMovie.csv")

movies = pd.read_csv("prepared_data/FilteredMovie.csv")

# Find the number of unique userIds

unique_user_count = ratings["userId"].nunique()
unique_movie_count = movies["movieId"].nunique()


print(f"Number of unique users: {unique_user_count}")
print(f"Number of unique movies: {unique_movie_count}")
