"""
Adversarial Test Profiles for Music Recommender

This script tests the recommender with "edge case" user profiles designed to:
1. Expose weaknesses in the scoring logic
2. Test conflicting preferences
3. Challenge assumptions about what makes a good recommendation
"""

from src.recommender import load_songs, recommend_songs


# Define test profiles with descriptions
ADVERSARIAL_PROFILES = {
    # === Standard/Expected Cases ===
    "High-Energy Pop": {
        "prefs": {"genre": "pop", "mood": "happy", "energy": 0.9},
        "description": "Expects energetic, happy pop songs (e.g., Gym Hero, Sunrise City)",
        "expected_behavior": "Standard case - should work well"
    },
    
    "Chill Lofi": {
        "prefs": {"genre": "lofi", "mood": "chill", "energy": 0.3},
        "description": "Expects relaxed, low-energy lofi (e.g., Library Rain, Focus Flow)",
        "expected_behavior": "Standard case - should work well"
    },
    
    "Deep Intense Rock": {
        "prefs": {"genre": "rock", "mood": "intense", "energy": 0.95},
        "description": "Expects hard-hitting, intense rock (e.g., Storm Runner, Steel Thunder)",
        "expected_behavior": "Standard case - should work well"
    },

    # === Adversarial Cases ===
    "Conflicting: Energetic Sadness": {
        "prefs": {"genre": "country", "mood": "sad", "energy": 0.9, "likes_acoustic": False},
        "description": "ADVERSARIAL: Wants high-energy (0.9) but sad mood (contradictory signals)",
        "expected_behavior": "Should expose genre matching vs. mood mismatch tradeoff"
    },
    
    "Acoustic Paradox": {
        "prefs": {"genre": "pop", "mood": "happy", "energy": 0.9, "likes_acoustic": True},
        "description": "ADVERSARIAL: Wants acoustic (typically low-energy) but high-energy pop (contradictory)",
        "expected_behavior": "Should test conflict between acousticness preference and energy"
    },
    
    "Moody Acoustic Lover": {
        "prefs": {"genre": "jazz", "mood": "melancholic", "energy": 0.5, "likes_acoustic": True},
        "description": "ADVERSARIAL: Combining melancholic mood with acoustic preference (less common combo)",
        "expected_behavior": "Should test if acousticness can override genre/mood mismatches"
    },
    
    "Anti-Acoustic Rocker": {
        "prefs": {"genre": "metal", "mood": "intense", "energy": 0.95, "likes_acoustic": False},
        "description": "ADVERSARIAL: Wants maximum anti-acoustic (electric) with metal intensity",
        "expected_behavior": "Should boost non-acoustic songs and penalize acoustic ones"
    },

    "Neutral Fence-Sitter": {
        "prefs": {"genre": "pop", "mood": "happy", "energy": 0.5},
        "description": "NEUTRAL: Mid-range energy with no strong acoustic preference",
        "expected_behavior": "Should match many songs equally (test tiebreaker logic)"
    },
    
    "Mystery Genre": {
        "prefs": {"genre": "experimental", "mood": "focused", "energy": 0.6},
        "description": "ADVERSARIAL: Non-existent genre - should algorithmically degrade gracefully",
        "expected_behavior": "No genre match bonus; should rely on mood/energy"
    },

    "Extreme Chill": {
        "prefs": {"genre": "ambient", "mood": "chill", "energy": 0.1, "likes_acoustic": True},
        "description": "ADVERSARIAL: Ultra-low energy with acoustic preference (tests bottoming out)",
        "expected_behavior": "Should strongly prefer ambient/classical/lofi acoustic tracks"
    },

    "Extreme Energy": {
        "prefs": {"genre": "electronic", "mood": "energetic", "energy": 1.0, "likes_acoustic": False},
        "description": "ADVERSARIAL: Maximum energy with anti-acoustic (tests topping out)",
        "expected_behavior": "Should strongly prefer high-energy electronic/metal non-acoustic"
    },
}


def run_single_profile(profile_name: str, user_prefs: dict, songs: list) -> list:
    """Run recommender for a single profile and return results."""
    return recommend_songs(user_prefs, songs, k=5)


def print_profile_header(profile_name: str, profile_info: dict):
    """Print formatted header for a profile."""
    print("\n" + "=" * 90)
    print(f"PROFILE: {profile_name.upper()}")
    print("=" * 90)
    print(f"Description: {profile_info['description']}")
    print(f"Expected Behavior: {profile_info['expected_behavior']}")
    print(f"\nPreferences: {profile_info['prefs']}")
    print("\nTop 5 Recommendations:")
    print("-" * 90)


def print_recommendation(idx: int, song: dict, score: float, explanation: str):
    """Print a single recommendation in readable format."""
    print(f"\n{idx}. {song['title'].upper()}")
    print(f"   Artist: {song['artist']:20s} | Genre: {song['genre']:12s} | "
          f"Mood: {song['mood']:12s}")
    print(f"   Energy: {song['energy']:.2f} | Acousticness: {song['acousticness']:.2f}")
    print(f"   SCORE: {score:.3f}")
    print(f"   Why: {explanation}")


def main():
    """Run all adversarial profiles and display results."""
    songs = load_songs("data/songs.csv")
    print(f"✓ Loaded {len(songs)} songs from the dataset.\n")
    
    results_summary = []
    
    for profile_name, profile_info in ADVERSARIAL_PROFILES.items():
        print_profile_header(profile_name, profile_info)
        
        recommendations = run_single_profile(
            profile_name,
            profile_info["prefs"],
            songs
        )
        
        for idx, (song, score, explanation) in enumerate(recommendations, 1):
            print_recommendation(idx, song, score, explanation)
        
        results_summary.append({
            "profile": profile_name,
            "top_recommendation": recommendations[0][0]["title"] if recommendations else "N/A",
            "top_score": recommendations[0][1] if recommendations else 0.0
        })
    
    # Print summary table
    print("\n\n" + "=" * 90)
    print("SUMMARY: Top Recommendation for Each Profile")
    print("=" * 90)
    print(f"{'Profile':<35} {'Top Pick':<30} {'Score':>10}")
    print("-" * 90)
    for result in results_summary:
        print(f"{result['profile']:<35} {result['top_recommendation']:<30} {result['top_score']:>10.3f}")


if __name__ == "__main__":
    main()
