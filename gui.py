import tkinter as tk
from tkinter import messagebox, Listbox, Toplevel
import pandas as pd
from search import Search  # Search sınıfını import ettik
from PIL import Image, ImageTk


class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Film Öneri Sistemi")
        self.root.geometry("800x600")

        self.root.configure(bg="#ADD8E6")

        self.movies = self.load_movies()
        self.user_ratings = self.load_user_ratings()
        self.rules = self.load_rules()

        self.search = Search(self.movies, self.user_ratings, self.rules)

        self.create_main_screen()

    def load_movies(self):
        return pd.read_csv("Main_Data/movie.csv")

    def load_user_ratings(self):
        return pd.read_csv("prepared_data/FilteredMovie.csv")

    def load_rules(self):
        return pd.read_csv("prepared_data/rules.csv")

    def create_main_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.configure(bg="#ADD8E6")

        self.popular_btn = tk.Button(
            self.root,
            text="Popüler Film Önerileri",
            command=self.open_popular_recommendations,
            bg="#6B8E23",
            fg="white",
            font=("Arial", 14, "bold"),
            relief="raised",
            bd=3,
            padx=10,
            pady=5,
        )
        self.popular_btn.pack(pady=10)

        self.personalized_btn = tk.Button(
            self.root,
            text="Kişiselleştirilmiş Film Önerileri",
            command=self.open_personalized_recommendations,
            bg="#8D6E63",
            fg="white",
            font=("Arial", 14, "bold"),
            relief="raised",
            bd=3,
            padx=10,
            pady=5,
        )
        self.personalized_btn.pack(pady=10)

        self.add_image()

    def add_image(self):

        image_path = "images.jpeg"
        img = Image.open(image_path)
        img = img.resize((400, 300), Image.Resampling.LANCZOS)

        self.photo = ImageTk.PhotoImage(img)

        self.image_label = tk.Label(self.root, image=self.photo)
        self.image_label.pack(pady=70)

    def open_popular_recommendations(self):
        self.create_popular_recommendation_screen()

    def create_popular_recommendation_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.option_listbox = Listbox(
            self.root,
            selectmode="single",
            bg="#F0F8FF",
            fg="#333",
            font=("Arial", 12),
            width=50,
            height=15,
            bd=2,
            relief="solid",
            selectbackground="#4CAF50",
            selectforeground="white",
        )

        self.option_listbox.insert(1, "Film Türüne Göre Öneri")
        self.option_listbox.insert(2, "Film İsmiyle Öneri")
        self.option_listbox.pack(pady=(70, 40))

        self.suggest_btn = tk.Button(
            self.root,
            text="Öner",
            command=self.direction1,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 12, "bold"),
            relief="raised",
            bd=3,
            padx=10,
            pady=5,
        )
        self.suggest_btn.pack(side=tk.LEFT, padx=10, pady=20)

        self.back_btn = tk.Button(
            self.root,
            text="Geri Gel",
            command=self.create_main_screen,
            bg="#8D6E63",
            fg="white",
            font=("Arial", 12, "bold"),
            relief="raised",
            bd=3,
            padx=10,
            pady=5,
        )
        self.back_btn.pack(side=tk.RIGHT, padx=10, pady=20)

    def direction1(self):
        selection = self.option_listbox.curselection()

        if selection:
            selected_option = self.option_listbox.get(selection[0])
            if selected_option == "Film Türüne Göre Öneri":
                self.create_pop_genre()
            elif selected_option == "Film İsmiyle Öneri":
                self.create_pop_name()

    ####################################
    def create_pop_genre(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.genre_listbox = Listbox(
            self.root,
            selectmode="single",
            bg="#F0F8FF",
            fg="#333",
            font=("Arial", 12),
            width=50,
            height=15,
            bd=2,
            relief="solid",
            selectbackground="#4CAF50",
            selectforeground="white",
        )
        genres = [
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
        for genre in genres:
            self.genre_listbox.insert(tk.END, genre)
        self.genre_listbox.pack(pady=(70, 40))

        self.suggest_genre_btn = tk.Button(
            self.root,
            text="Öner",
            command=self.display_pop_genre_recommendations,
            bg="#6B8E23",
            fg="white",
            font=("Arial", 14, "bold"),
            relief="raised",
            bd=3,
            padx=10,
            pady=5,
        )
        self.suggest_genre_btn.pack(side=tk.LEFT, padx=5, pady=10)

        self.back_genre_btn = tk.Button(
            self.root,
            text="Geri Gel",
            command=self.create_popular_recommendation_screen,
            bg="#8D6E63",
            fg="white",
            font=("Arial", 12, "bold"),
            relief="raised",
            bd=3,
            padx=10,
            pady=5,
        )
        self.back_genre_btn.pack(side=tk.RIGHT, padx=5, pady=10)

    def display_pop_genre_recommendations(self):
        genre_selection = self.genre_listbox.curselection()
        if genre_selection:
            selected_genre = self.genre_listbox.get(genre_selection[0])
            recommendations_list = self.search.get_genre_recommendations(selected_genre)

            if recommendations_list:
                self.show_pop_genre_window(recommendations_list, selected_genre)
            else:
                messagebox.showinfo("Film Önerileri", "Bu türde film bulunamadı.")
        else:
            messagebox.showwarning("Uyarı", "Lütfen bir tür seçin.")

    def show_pop_genre_window(self, recommendations_list, selected_genre):
        self.recommendation_window = Toplevel(self.root)
        self.recommendation_window.title("Film Önerisi")

        self.current_recommendations = recommendations_list
        first_recommendation = self.current_recommendations[0]
        self.recommended_movie_label = tk.Label(
            self.recommendation_window,
            text=f"{selected_genre} türü için önerilen film: {first_recommendation[0]} - Tür: {first_recommendation[1]}",
        )
        self.recommended_movie_label.pack(pady=10)

        self.another_btn = tk.Button(
            self.recommendation_window,
            text="Başka Öner",
            command=self.show_pop_genre_another,
            bg="#6B8E23",
            fg="white",
            font=("Arial", 14, "bold"),
            relief="raised",
            bd=3,
            padx=10,
            pady=5,
        )
        self.another_btn.pack(side=tk.RIGHT, padx=5, pady=10)

        self.ok_btn = tk.Button(
            self.recommendation_window,
            text="Tamam",
            command=self.recommendation_window.destroy,
            bg="#8D6E63",
            fg="white",
            font=("Arial", 12, "bold"),
            relief="raised",
            bd=3,
            padx=10,
            pady=5,
        )
        self.ok_btn.pack(side=tk.RIGHT, padx=5, pady=10)

        self.current_recommendation_index = 0

    def show_pop_genre_another(self):
        self.current_recommendation_index += 1
        if self.current_recommendation_index >= len(self.current_recommendations):
            self.current_recommendation_index = 0

        next_recommendation = self.current_recommendations[
            self.current_recommendation_index
        ]
        self.recommended_movie_label.config(
            text=f"Başka öneri: {next_recommendation[0]} - Tür: {next_recommendation[1]}"
        )

    ########################
    def create_pop_name(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        unique_movie_ids = self.user_ratings["movieId"].unique()
        movie_titles = self.movies[self.movies["movieId"].isin(unique_movie_ids)]

        movie_count_label = tk.Label(
            self.root, text=f"Toplam Film Sayısı: {len(movie_titles)}"
        )
        movie_count_label.pack(pady=10)

        self.movie_listbox = Listbox(
            self.root,
            selectmode="single",
            bg="#F0F8FF",
            fg="#333",
            font=("Arial", 12),
            width=50,
            height=15,
            bd=2,
            relief="solid",
            selectbackground="#4CAF50",
            selectforeground="white",
        )
        for _, row in movie_titles.iterrows():
            self.movie_listbox.insert(tk.END, f"{row['movieId']} - {row['title']}")

        self.movie_listbox.pack(pady=(70, 40))

        self.suggest_btn = tk.Button(
            self.root,
            text="Öner",
            command=self.suggest_pop_name_movie,
            bg="#6B8E23",
            fg="white",
            font=("Arial", 14, "bold"),
            relief="raised",
            bd=3,
            padx=10,
            pady=5,
        )
        self.suggest_btn.pack(side=tk.LEFT, padx=5, pady=10)

        self.back_btn = tk.Button(
            self.root,
            text="Geri Gel",
            command=self.create_popular_recommendation_screen,
            bg="#8D6E63",
            fg="white",
            font=("Arial", 12, "bold"),
            relief="raised",
            bd=3,
            padx=10,
            pady=5,
        )
        self.back_btn.pack(side=tk.RIGHT, padx=5, pady=10)

    def suggest_pop_name_movie(self):
        selected = self.movie_listbox.curselection()
        if selected:
            selected_movie = self.movie_listbox.get(selected[0])
            movie_id = selected_movie.split(" - ")[0]
            recommendations = self.search.get_movie_recommendations(int(movie_id))

            if recommendations:
                self.show_pop_name_movies(recommendations)
            else:
                messagebox.showwarning("Uyarı", "Bu film için öneri bulunamadı.")
        else:
            messagebox.showwarning("Uyarı", "Lütfen bir film seçin.")

    def show_pop_name_movies(self, movie_confidences):

        self.current_movie_recommendations = movie_confidences
        self.current_recommendation_index = 0

        for widget in self.root.winfo_children():
            widget.destroy()

        title_label = tk.Label(self.root, text="Önerilen Filmler:")
        title_label.pack(pady=10)

        self.movie_label = tk.Label(self.root, text="")
        self.movie_label.pack(pady=5)
        self.update_movie_display()

        another_btn = tk.Button(
            self.root,
            text="Başka Öner",
            command=self.show_next_movie,
            bg="#6B8E23",
            fg="white",
            font=("Arial", 14, "bold"),
            relief="raised",
            bd=3,
            padx=10,
            pady=5,
        )
        another_btn.pack(side=tk.LEFT, padx=5, pady=10)

        ok_btn = tk.Button(
            self.root,
            text="Tamam",
            command=self.create_pop_name,
            bg="#8D6E63",
            fg="white",
            font=("Arial", 12, "bold"),
            relief="raised",
            bd=3,
            padx=10,
            pady=5,
        )
        ok_btn.pack(side=tk.RIGHT, padx=5, pady=10)

    def update_movie_display(self):

        movie_id, title, genres, confidence = self.current_movie_recommendations[
            self.current_recommendation_index
        ]
        self.movie_label.config(
            text=f"Film ID: {movie_id}\nBaşlık: {title}\nTür: {genres}\nConfidence: {confidence:.2f}"
        )

    def show_next_movie(self):

        self.current_recommendation_index += 1
        if self.current_recommendation_index >= len(self.current_movie_recommendations):
            self.current_recommendation_index = 0
        self.update_movie_display()

    ##########################################
    def open_personalized_recommendations(self):
        self.create_personalized_recommendation_screen()

    def create_personalized_recommendation_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.user_listbox = Listbox(
            self.root,
            selectmode="single",
            bg="#F0F8FF",
            fg="#333",
            font=("Arial", 12),
            width=50,
            height=15,
            bd=2,
            relief="solid",
            selectbackground="#4CAF50",
            selectforeground="white",
        )
        users = self.user_ratings["userId"].unique()
        for user in users:
            self.user_listbox.insert(tk.END, user)
        self.user_listbox.pack(pady=(70, 40))

        self.confirm_btn = tk.Button(
            self.root,
            text="Onayla",
            command=self.display_user_recommendations,
            bg="#6B8E23",
            fg="white",
            font=("Arial", 14, "bold"),
            relief="raised",
            bd=3,
            padx=10,
            pady=5,
        )
        self.confirm_btn.pack(side=tk.LEFT, padx=5, pady=10)

        self.back_user_btn = tk.Button(
            self.root,
            text="Geri Gel",
            command=self.create_main_screen,
            bg="#8D6E63",
            fg="white",
            font=("Arial", 12, "bold"),
            relief="raised",
            bd=3,
            padx=10,
            pady=5,
        )
        self.back_user_btn.pack(side=tk.RIGHT, padx=5, pady=10)

    def display_user_recommendations(self):

        user_selection = self.user_listbox.curselection()
        if user_selection:
            selected_user_id = self.user_listbox.get(user_selection[0])
            self.create_option_selection_screen(selected_user_id)
        else:
            messagebox.showwarning("Uyarı", "Lütfen bir kullanıcı seçin.")

    def create_option_selection_screen(self, user_id):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.option_listbox = Listbox(
            self.root,
            selectmode="single",
            bg="#F0F8FF",
            fg="#333",
            font=("Arial", 12),
            width=50,
            height=15,
            bd=2,
            relief="solid",
            selectbackground="#4CAF50",
            selectforeground="white",
        )
        self.option_listbox.insert(1, "Film Türüne Göre Öneri")
        self.option_listbox.insert(2, "Film İsmiyle Öneri")
        self.option_listbox.pack(pady=(70, 40))

        self.suggest_btn = tk.Button(
            self.root,
            text="Onay",
            command=lambda: self.direction2(user_id),
            bg="#6B8E23",
            fg="white",
            font=("Arial", 14, "bold"),
            relief="raised",
            bd=3,
            padx=10,
            pady=5,
        )
        self.suggest_btn.pack(side=tk.LEFT, padx=5, pady=10)

        self.back_btn = tk.Button(
            self.root,
            text="Geri Gel",
            command=self.create_personalized_recommendation_screen,
            bg="#8D6E63",
            fg="white",
            font=("Arial", 12, "bold"),
            relief="raised",
            bd=3,
            padx=10,
            pady=5,
        )
        self.back_btn.pack(side=tk.RIGHT, padx=5, pady=10)

    def direction2(self, user_id):
        selection = self.option_listbox.curselection()
        if selection:
            selected_option = self.option_listbox.get(selection[0])
            if selected_option == "Film Türüne Göre Öneri":
                self.create_person_genre(user_id)
            elif selected_option == "Film İsmiyle Öneri":
                self.create_person_name(user_id)

    def create_person_name(self, user_id):
        for widget in self.root.winfo_children():
            widget.destroy()

        user_movies = self.user_ratings[self.user_ratings["userId"] == int(user_id)]
        movie_titles = self.movies[self.movies["movieId"].isin(user_movies["movieId"])]

        self.movie_listbox = Listbox(
            self.root,
            selectmode="single",
            bg="#F0F8FF",
            fg="#333",
            font=("Arial", 12),
            width=50,
            height=15,
            bd=2,
            relief="solid",
            selectbackground="#4CAF50",
            selectforeground="white",
        )
        for _, row in movie_titles.iterrows():
            self.movie_listbox.insert(tk.END, f"{row['movieId']} - {row['title']}")
        self.movie_listbox.pack(pady=(70, 40))

        self.suggest_movie_btn = tk.Button(
            self.root,
            text="Öner",
            command=lambda: self.display_selected_movie_id_forperson(user_id),
            bg="#6B8E23",
            fg="white",
            font=("Arial", 14, "bold"),
            relief="raised",
            bd=3,
            padx=10,
            pady=5,
        )
        self.suggest_movie_btn.pack(side=tk.LEFT, padx=5, pady=10)

        self.back_movie_btn = tk.Button(
            self.root,
            text="Geri Gel",
            command=self.open_personalized_recommendations,
            bg="#8D6E63",
            fg="white",
            font=("Arial", 12, "bold"),
            relief="raised",
            bd=3,
            padx=10,
            pady=5,
        )
        self.back_movie_btn.pack(side=tk.RIGHT, padx=5, pady=10)

    def display_selected_movie_id_forperson(self, user_id):

        movie_selection = self.movie_listbox.curselection()
        if movie_selection:
            selected_movie = self.movie_listbox.get(movie_selection[0])
            movie_id = selected_movie.split(" - ")[0]

            self.suggest_similar_movies_forperson_name(int(movie_id), int(user_id))
        else:
            messagebox.showwarning("Uyarı", "Lütfen bir film seçin.")

    def suggest_similar_movies_forperson_name(self, input_movie_id, user_id):

        similar_movies = self.search.get_movie_recommendations(input_movie_id)

        user_movies = set(
            self.user_ratings[self.user_ratings["userId"] == int(user_id)]["movieId"]
        )

        similar_movies = [
            movie for movie in similar_movies if movie[0] not in user_movies
        ]

        if similar_movies:

            self.show_single_movie_forperson_name(similar_movies)
        else:
            messagebox.showinfo(
                "Sonuç",
                f"{input_movie_id} ID'li film ile ilişkili benzer film bulunamadı.",
            )

    def show_single_movie_forperson_name(self, movie_confidences):

        for widget in self.root.winfo_children():
            widget.destroy()

        movie_id, title, genres, confidence = movie_confidences[0]
        self.current_movie_index = 0
        self.displayed_movies = movie_confidences

        self.movie_label = tk.Label(
            self.root,
            text=f"Film ID: {movie_id}\nBaşlık: {title}\nTür: {genres}\nConfidence: {confidence:.2f}",
        )
        self.movie_label.pack(pady=10)

        self.another_suggest_btn = tk.Button(
            self.root,
            text="Başka Öner",
            command=self.suggest_another_movie_forperson_name,
            bg="#6B8E23",
            fg="white",
            font=("Arial", 14, "bold"),
            relief="raised",
            bd=3,
            padx=10,
            pady=5,
        )
        self.another_suggest_btn.pack(side=tk.LEFT, padx=5, pady=10)

        self.ok_btn = tk.Button(
            self.root,
            text="Tamam",
            command=self.create_personalized_recommendation_screen,
            bg="#8D6E63",
            fg="white",
            font=("Arial", 12, "bold"),
            relief="raised",
            bd=3,
            padx=10,
            pady=5,
        )
        self.ok_btn.pack(side=tk.RIGHT, padx=5, pady=10)

    def suggest_another_movie_forperson_name(self):
        self.current_movie_index += 1
        if self.current_movie_index < len(self.displayed_movies):
            movie_id, title, genres, confidence = self.displayed_movies[
                self.current_movie_index
            ]
            self.movie_label.config(
                text=f"Film ID: {movie_id}\nBaşlık: {title}\nTür: {genres}\nConfidence: {confidence:.2f}"
            )
        else:
            messagebox.showinfo("Sonuç", "Daha fazla öneri yok.")

    ####################################################
    def create_person_genre(self, user_id):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.genre_listbox = Listbox(
            self.root,
            selectmode="single",
            bg="#F0F8FF",
            fg="#333",
            font=("Arial", 12),
            width=50,
            height=15,
            bd=2,
            relief="solid",
            selectbackground="#4CAF50",
            selectforeground="white",
        )

        genres = [
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

        for genre in genres:
            self.genre_listbox.insert(tk.END, genre)
        self.genre_listbox.pack(pady=(70, 40))

        self.suggest_genre_btn = tk.Button(
            self.root,
            text="Öner",
            command=lambda: self.display_person_genre_recommendations(user_id),
            bg="#6B8E23",
            fg="white",
            font=("Arial", 14, "bold"),
            relief="raised",
            bd=3,
            padx=10,
            pady=5,
        )
        self.suggest_genre_btn.pack(side=tk.LEFT, padx=5, pady=10)

        self.back_genre_btn = tk.Button(
            self.root,
            text="Geri Gel",
            command=self.create_personalized_recommendation_screen,
            bg="#8D6E63",
            fg="white",
            font=("Arial", 12, "bold"),
            relief="raised",
            bd=3,
            padx=10,
            pady=5,
        )
        self.back_genre_btn.pack(side=tk.RIGHT, padx=5, pady=10)

    def display_person_genre_recommendations(self, user_id):
        genre_selection = self.genre_listbox.curselection()
        if genre_selection:
            selected_genre = self.genre_listbox.get(genre_selection[0])
            recommendations_list = self.search.get_genre_recommendations(selected_genre)

            user_movies = set(
                self.user_ratings[self.user_ratings["userId"] == int(user_id)][
                    "movieId"
                ]
            )

            recommendations_list = [
                movie for movie in recommendations_list if movie[0] not in user_movies
            ]

            if recommendations_list:
                self.show_person_genre_window(recommendations_list, selected_genre)
            else:
                messagebox.showinfo("Film Önerileri", "Bu türde film bulunamadı.")
        else:
            messagebox.showwarning("Uyarı", "Lütfen bir tür seçin.")

    def show_person_genre_window(self, recommendations_list, selected_genre):
        self.recommendation_window = Toplevel(self.root)
        self.recommendation_window.title("Film Önerisi")

        self.current_recommendations = recommendations_list
        first_recommendation = self.current_recommendations[0]
        self.recommended_movie_label = tk.Label(
            self.recommendation_window,
            text=f"{selected_genre} türü için önerilen film: {first_recommendation[0]} - Tür: {first_recommendation[1]}",
        )
        self.recommended_movie_label.pack(pady=10)

        self.another_btn = tk.Button(
            self.recommendation_window,
            text="Başka Öner",
            command=self.show_person_genre_another,
            bg="#6B8E23",
            fg="white",
            font=("Arial", 14, "bold"),
            relief="raised",
            bd=3,
            padx=10,
            pady=5,
        )
        self.another_btn.pack(side=tk.RIGHT, padx=5, pady=10)

        self.ok_btn = tk.Button(
            self.recommendation_window,
            text="Tamam",
            command=self.recommendation_window.destroy,
            bg="#8D6E63",
            fg="white",
            font=("Arial", 12, "bold"),
            relief="raised",
            bd=3,
            padx=10,
            pady=5,
        )
        self.ok_btn.pack(side=tk.RIGHT, padx=5, pady=10)

        self.current_recommendation_index = 0

    def show_person_genre_another(self):
        self.current_recommendation_index += 1
        if self.current_recommendation_index >= len(self.current_recommendations):
            self.current_recommendation_index = 0

        next_recommendation = self.current_recommendations[
            self.current_recommendation_index
        ]
        self.recommended_movie_label.config(
            text=f"Başka öneri: {next_recommendation[0]} - Tür: {next_recommendation[1]}"
        )


if __name__ == "__main__":
    root = tk.Tk()
    gui = GUI(root)
    root.mainloop()
