import pandas as pd

ratings = pd.read_csv("prepared_data/FilteredMovie.csv")

# We create a movie-rating matrix using rating data.
user_movie_matrix = ratings.pivot(index="userId", columns="movieId", values="rating")

user_movie_matrix = user_movie_matrix.notnull().astype(int)

print(user_movie_matrix.head())
print(f"Matrix dimensions: {user_movie_matrix.shape}")

# Save the matrix to a CSV file
user_movie_matrix.to_csv("prepared_data/UserMovieMatrix.csv")
