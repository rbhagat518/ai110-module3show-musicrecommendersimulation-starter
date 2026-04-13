"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from .recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv") 
    print(f"✓ Loaded {len(songs)} songs from the dataset.\n")
    
    # Starter example profile
    user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}
    print(f"User Preferences: Genre={user_prefs['genre']}, Mood={user_prefs['mood']}, Target Energy={user_prefs['energy']}\n")

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("=" * 70)
    print("TOP 5 RECOMMENDATIONS")
    print("=" * 70)
    
    for idx, rec in enumerate(recommendations, 1):
        # You decide the structure of each returned item.
        # A common pattern is: (song, score, explanation)
        song, score, explanation = rec
        
        print(f"\n{idx}. {song['title'].upper()}")
        print(f"   Artist: {song['artist']} | Genre: {song['genre']} | Mood: {song['mood']}")
        print(f"   Score: {score:.3f}")
        print(f"   Reasons:")
        
        # Parse and display reasons with indentation
        if isinstance(explanation, str):
            reasons = explanation.split(" | ")
            for reason in reasons:
                print(f"     • {reason.strip()}")
        else:
            print(f"     • {explanation}")
    
    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()
