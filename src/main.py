"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

It defines several user taste profiles (including a couple of deliberately
"adversarial" edge cases) and prints the top recommendations for each one.
"""

from src.recommender import load_songs, recommend_songs


# Each profile is a user-preference dictionary. The first three are ordinary
# taste profiles; the last two are edge cases designed to stress the scoring.
PROFILES = {
    "High-Energy Pop": {
        "genre": "pop", "mood": "happy", "energy": 0.9,
        "likes_acoustic": False, "likes_instrumental": False, "prefers_popular": True,
    },
    "Chill Lofi": {
        "genre": "lofi", "mood": "chill", "energy": 0.35,
        "likes_acoustic": True, "likes_instrumental": True, "prefers_popular": False,
    },
    "Deep Intense Rock": {
        "genre": "rock", "mood": "intense", "energy": 0.9,
        "likes_acoustic": False, "likes_instrumental": False, "prefers_popular": False,
    },
    # Edge case 1: conflicting preferences — wants very high energy but a
    # melancholy mood, which barely co-occur in the data.
    "Conflicting (high-energy + melancholy)": {
        "genre": "classical", "mood": "melancholy", "energy": 0.95,
        "likes_acoustic": True, "likes_instrumental": True, "prefers_popular": False,
    },
    # Edge case 2: almost no opinion — only an energy target is set, so every
    # other rule is skipped. Tests what surfaces with minimal information.
    "Minimal (energy only)": {
        "energy": 0.5,
    },
}


def print_recommendations(name: str, user_prefs: dict, songs: list, k: int = 5) -> None:
    """Print the top k recommendations for one named profile."""
    recommendations = recommend_songs(user_prefs, songs, k=k)
    print(f"\n=== {name} ===")
    print(f"profile: {user_prefs}\n")
    for rank, (song, score, reasons) in enumerate(recommendations, start=1):
        print(f"{rank}. {song['title']} — {song['artist']}  (score: {score:.2f})")
        for reason in reasons:
            print(f"     • {reason}")
        print()


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    for name, user_prefs in PROFILES.items():
        print_recommendations(name, user_prefs, songs, k=5)


if __name__ == "__main__":
    main()
