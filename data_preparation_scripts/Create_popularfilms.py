# Import necessary libraries
import pandas as pd

# Load the data files
movies = pd.read_csv("Main_Data/movie.csv")
ratings = pd.read_csv("Main_Data/rating.csv")

# Define the genres to filter
target_genres = [
    "Drama",
    "Comedy",
    "Thriller",
    "Romance",
    "Action",
    "Crime",
    "Horror",
    "Documentary",
    "Adventure",
    "Sci-Fi",
]

# Create an empty DataFrame to store the top movies for each genre
top_movies_by_genre = pd.DataFrame()

# Loop through each genre to filter movies and find the top 150
for genre in target_genres:
    # Filter movies for the specific genre
    genre_movies = movies[movies["genres"].str.contains(genre)]

    # Merge with ratings to analyze based on ratings
    genre_ratings = pd.merge(
        genre_movies[["movieId", "title", "genres"]], ratings, on="movieId"
    )

    # Calculate rating count and average rating for each movie
    movie_stats = (
        genre_ratings.groupby(["movieId", "title", "genres"])
        .agg(rating_count=("rating", "size"), average_rating=("rating", "mean"))
        .reset_index()
    )

    # Sort by rating count and average rating, then pick the top 200
    top_200_movies = movie_stats.sort_values(
        ["rating_count", "average_rating"], ascending=[False, False]
    ).head(200)

    # Append the result to the overall DataFrame
    top_movies_by_genre = pd.concat([top_movies_by_genre, top_200_movies])

# Save the results to new2_movie.csv
top_movies_by_genre.to_csv(
    "prepared_data/popularfilms.csv",
    index=False,
    columns=["movieId", "title", "genres"],
)

print("popularmovie.csv files done")
