"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    # Taste profile: a mainstream pop fan who wants upbeat, produced,
    # vocal-driven, popular tracks. Uses all six scoring preferences.
    user_prefs = {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.8,
        "likes_acoustic": False,     # prefers produced/electronic sound
        "likes_instrumental": False, # wants vocals
        "prefers_popular": True,     # wants mainstream hits
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print(f"\nTop {len(recommendations)} recommendations for profile: "
          f"{user_prefs['genre']} / {user_prefs['mood']} / energy {user_prefs['energy']}\n")
    for rank, (song, score, reasons) in enumerate(recommendations, start=1):
        print(f"{rank}. {song['title']} — {song['artist']}  (score: {score:.2f})")
        for reason in reasons:
            print(f"     • {reason}")
        print()


if __name__ == "__main__":
    main()
