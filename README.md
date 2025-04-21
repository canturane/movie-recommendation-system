# Movie Recommendation System

This project is an application designed to provide movie recommendations to users. The system offers two fundamental recommendation mechanisms: popular movie recommendations and personalized movie recommendations.

## About the Project

The Movie Recommendation System analyzes users' movie-watching habits using the Apriori algorithm and provides movie recommendations based on this data. The system was developed using the MovieLens 20M dataset and can offer personalized recommendations by considering users' movie-watching preferences.

## Features

- **Popular Movie Recommendations**: Popular movie recommendations based on all users' preferences and viewing data
  - Recommendations by movie genre
  - Recommendations by movie name

- **Personalized Movie Recommendations**: Customized recommendations for a specific user
  - Recommendations by movie genre (from movies the user hasn't watched)
  - Recommendations by movie name (similar movies to one the user has watched)

- **Fast Recommendation System**: Recommendation speed optimized using Hash Tree structure
  - Speed improvement of up to 33% compared to normal searches

- **User-Friendly Interface**: Simple and intuitive graphical interface developed with Tkinter

## Technical Details

### Technologies Used

- **Python**: Main programming language
- **Pandas**: Data processing and analysis
- **Tkinter**: Graphical User Interface (GUI)
- **PIL (Pillow)**: Image processing
- **Apriori Algorithm**: Extraction of movie association rules

### Dataset

The system uses the MovieLens 20M dataset:
- 138,493 users
- 27,278 unique movies
- 20,000,263 user ratings

For more effective recommendations, data cleaning was performed:
- Ratings between 3.5-4.5 were considered
- Users with 200-3000 ratings were included
- Movies with fewer than 50 ratings were excluded

### System Architecture

1. **Data Cleaning**: Preprocessing to filter out irrelevant data
2. **Matrix Creation**: User-movie matrix generation for Apriori algorithm
3. **Rule Extraction**: Using Apriori algorithm to find associations between movies
4. **Hash Tree Implementation**: Optimizing search operations for recommendations
5. **GUI Development**: Creating a user-friendly interface with Tkinter

## Installation and Usage

1. Clone the repository:
```
git clone https://github.com/yourusername/movie-recommendation-system.git
```

2. Install the required dependencies:
```
pip install pandas pillow
```

3. Make sure you have the required data files in the correct locations:
   - Main_Data/movie.csv
   - prepared_data/FilteredMovie.csv
   - prepared_data/rules.csv

4. Run the application:
```
python main.py
```

## System Screenshots

The system includes several screens:
- Main screen with two options: Popular and Personalized recommendations
- Genre selection screen
- Movie selection screen
- Recommendation display screen

## Future Improvements

- Implementation of additional recommendation algorithms
- Enhanced user interface with more features
- Support for user registration and profile creation
- Real-time data updates and learning
