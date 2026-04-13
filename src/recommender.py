from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import csv

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    songs = []
    with open(csv_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Convert numeric fields to float, id to int
            song = {
                'id': int(row['id']),
                'title': row['title'],
                'artist': row['artist'],
                'genre': row['genre'],
                'mood': row['mood'],
                'energy': float(row['energy']),
                'tempo_bpm': float(row['tempo_bpm']),
                'valence': float(row['valence']),
                'danceability': float(row['danceability']),
                'acousticness': float(row['acousticness']),
            }
            songs.append(song)
    return songs

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    preferred_genre = str(user_prefs.get('genre', '')).strip().lower()
    preferred_mood = str(user_prefs.get('mood', '')).strip().lower()
    target_energy = float(user_prefs.get('energy', 0.5))
    likes_acoustic = user_prefs.get('likes_acoustic')

    recommendations = []
    append_recommendation = recommendations.append

    for song in songs:
        song_genre = str(song.get('genre', '')).strip().lower()
        song_mood = str(song.get('mood', '')).strip().lower()
        song_energy = float(song.get('energy', 0.0))
        song_acousticness = float(song.get('acousticness', 0.0))

        genre_match = song_genre == preferred_genre
        mood_match = song_mood == preferred_mood
        energy_score = max(0.0, 1.0 - abs(song_energy - target_energy))

        score = energy_score
        if genre_match:
            score += 1.0
        if mood_match:
            score += 1.0
        if likes_acoustic is True:
            score += song_acousticness
        elif likes_acoustic is False:
            score += 1.0 - song_acousticness

        explanation_parts = []
        if genre_match:
            explanation_parts.append(f"matches your favorite genre ({song.get('genre', '')})")
        if mood_match:
            explanation_parts.append(f"fits your preferred mood ({song.get('mood', '')})")
        explanation_parts.append(
            f"energy is close to your target ({song_energy:.2f} vs {target_energy:.2f})"
        )
        if likes_acoustic is True:
            explanation_parts.append("has an acoustic sound")
        elif likes_acoustic is False:
            explanation_parts.append("leans away from acoustic")

        append_recommendation((song, score, ", ".join(explanation_parts)))

    recommendations.sort(key=lambda item: item[1], reverse=True)
    return recommendations[:k]
