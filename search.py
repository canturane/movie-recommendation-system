import pandas as pd


class Search:
    def __init__(self, movies, user_ratings, rules):
        self.movies = movies
        self.user_ratings = user_ratings
        self.rules = rules
        self.hash_tree = self.build_hash_tree(rules)

    def build_hash_tree(self, rules):
        hash_tree = {}

        for _, row in rules.iterrows():
            # Properly evaluate frozensets
            antecedents = eval(row["antecedents"])
            consequents = eval(row["consequents"])

            for antecedent in antecedents:
                # Add antecedent to hash tree if not present
                if antecedent not in hash_tree:
                    hash_tree[antecedent] = []
                # Store consequents along with confidence and antecedent support
                hash_tree[antecedent].append(
                    (consequents, row["confidence"], row["antecedent support"])
                )

        return hash_tree

    def get_movie_recommendations(self, input_movie_id):
        # Convert input_movie_id to string and fetch from hash tree
        input_movie_id_str = str(input_movie_id)
        similar_movies = self.hash_tree.get(input_movie_id_str, [])

        return self._extract_movie_confidences_from_hash_tree(similar_movies)

    def _extract_movie_confidences_from_hash_tree(self, similar_movies):
        movie_confidences = []
        seen_movies = set()

        for (
            consequents,
            confidence,
            antecedent_support,
        ) in similar_movies:  # Include the third value
            for movie_id in consequents:
                # Convert movie ID to string
                movie_id_str = str(movie_id)
                movie_info = self.movies[self.movies["movieId"] == int(movie_id_str)][
                    ["title", "genres"]
                ].values

                if movie_info.size > 0 and movie_id_str not in seen_movies:
                    title, genres = movie_info[0]
                    movie_confidences.append(
                        (int(movie_id_str), title, genres, confidence)
                    )
                    seen_movies.add(movie_id_str)

        # Sort by confidence value
        movie_confidences.sort(key=lambda x: x[3], reverse=True)
        return movie_confidences

    def get_genre_recommendations(self, selected_genre):
        # Filter movies that contain the selected genre
        genre_movies = self.movies[
            self.movies["genres"].str.contains(selected_genre, case=False)
        ]
        genre_movie_ids = set(genre_movies["movieId"].astype(str))

        # Collect genre-related movies from hash_tree, sorted by antecedent support
        sorted_rules = sorted(
            [
                (ant, consequents, conf, supp)
                for ant in genre_movie_ids
                if ant in self.hash_tree
                for consequents, conf, supp in self.hash_tree[ant]
            ],
            key=lambda x: x[3],  # Sort by antecedent support
            reverse=True,
        )

        # Generate recommendation list
        genre_recommendations = []
        seen_movies = set()

        for antecedent, consequents, _, antecedent_support in sorted_rules:
            # Get movie info from movie.csv
            movie_data = self.movies[self.movies["movieId"] == int(antecedent)][
                ["movieId", "title"]
            ].values

            # Add movie to list if not already added
            if movie_data.size > 0 and antecedent not in seen_movies:
                movie_id, title = movie_data[0]
                genre_recommendations.append((int(movie_id), title, antecedent_support))
                seen_movies.add(antecedent)

            # Return if we have collected 20 recommendations
            if len(genre_recommendations) >= 20:
                return genre_recommendations

        return genre_recommendations
