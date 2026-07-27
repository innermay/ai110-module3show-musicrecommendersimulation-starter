import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

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
    instrumentalness: float = 0.0
    popularity: float = 0.0

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
    # New optional preferences (default to None = "no opinion", rule is skipped).
    likes_instrumental: Optional[bool] = None
    prefers_popular: Optional[bool] = None


# --- Algorithm Recipe -------------------------------------------------------
# Each rule contributes up to WEIGHTS[rule] points. Genre is the strongest
# "is this my kind of music?" signal, so it carries the most weight. The final
# score is normalized to 0-1 by the total weight of the rules that actually
# fired, so scores stay comparable even if a user leaves some preferences unset.
WEIGHTS = {
    "genre": 0.25,
    "mood": 0.20,
    "energy": 0.20,
    "acoustic": 0.15,
    "instrumental": 0.10,
    "popularity": 0.10,
}


def _compute_score(
    *,
    song_genre: str,
    song_mood: str,
    song_energy: float,
    song_acousticness: float,
    song_instrumentalness: float,
    song_popularity: float,
    pref_genre: Optional[str],
    pref_mood: Optional[str],
    pref_energy: Optional[float],
    likes_acoustic: Optional[bool],
    likes_instrumental: Optional[bool],
    prefers_popular: Optional[bool],
) -> Tuple[float, List[str]]:
    """
    Shared scoring core used by both the OOP and functional paths.
    Returns (normalized_score in [0, 1], list of human-readable reasons).
    """
    points = 0.0
    total_weight = 0.0
    reasons: List[str] = []

    # Rule 1: genre match (categorical, all-or-nothing)
    if pref_genre is not None:
        w = WEIGHTS["genre"]
        total_weight += w
        if song_genre == pref_genre:
            points += w
            reasons.append(f"genre match: {song_genre} (+{w:.2f})")

    # Rule 2: mood match (categorical, all-or-nothing)
    if pref_mood is not None:
        w = WEIGHTS["mood"]
        total_weight += w
        if song_mood == pref_mood:
            points += w
            reasons.append(f"mood match: {song_mood} (+{w:.2f})")

    # Rule 3: energy fit (numeric, rewards *closeness* to the target)
    if pref_energy is not None:
        w = WEIGHTS["energy"]
        total_weight += w
        closeness = 1.0 - abs(song_energy - pref_energy)
        earned = closeness * w
        points += earned
        if closeness >= 0.85:
            reasons.append(f"energy close to target (+{earned:.2f})")

    # Rule 4: acoustic fit (boolean flips which end of the scale is "good")
    if likes_acoustic is not None:
        w = WEIGHTS["acoustic"]
        total_weight += w
        alignment = song_acousticness if likes_acoustic else (1.0 - song_acousticness)
        earned = alignment * w
        points += earned
        if alignment >= 0.6:
            label = "acoustic match" if likes_acoustic else "produced/electronic match"
            reasons.append(f"{label} (+{earned:.2f})")

    # Rule 5: instrumentalness fit
    if likes_instrumental is not None:
        w = WEIGHTS["instrumental"]
        total_weight += w
        alignment = song_instrumentalness if likes_instrumental else (1.0 - song_instrumentalness)
        earned = alignment * w
        points += earned
        if alignment >= 0.6:
            label = "instrumental match" if likes_instrumental else "vocal match"
            reasons.append(f"{label} (+{earned:.2f})")

    # Rule 6: popularity fit
    if prefers_popular is not None:
        w = WEIGHTS["popularity"]
        total_weight += w
        alignment = song_popularity if prefers_popular else (1.0 - song_popularity)
        earned = alignment * w
        points += earned
        if alignment >= 0.6:
            label = "popular pick" if prefers_popular else "niche pick"
            reasons.append(f"{label} (+{earned:.2f})")

    score = points / total_weight if total_weight > 0 else 0.0
    return score, reasons


def _reasons_to_sentence(reasons: List[str]) -> str:
    """Join reason fragments into one readable string."""
    if not reasons:
        return "no strong matches; closest available option"
    return "; ".join(reasons)


class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def _score(self, user: UserProfile, song: Song) -> Tuple[float, List[str]]:
        return _compute_score(
            song_genre=song.genre,
            song_mood=song.mood,
            song_energy=song.energy,
            song_acousticness=song.acousticness,
            song_instrumentalness=song.instrumentalness,
            song_popularity=song.popularity,
            pref_genre=user.favorite_genre,
            pref_mood=user.favorite_mood,
            pref_energy=user.target_energy,
            likes_acoustic=user.likes_acoustic,
            likes_instrumental=user.likes_instrumental,
            prefers_popular=user.prefers_popular,
        )

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # SCORE every song, then RANK (sort high -> low) and CUT to top k.
        scored = [(song, self._score(user, song)[0]) for song in self.songs]
        scored.sort(key=lambda pair: pair[1], reverse=True)
        return [song for song, _ in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a one-line, human-readable justification for a song's score."""
        score, reasons = self._score(user, song)
        return f"Recommended (score {score:.2f}) — {_reasons_to_sentence(reasons)}"


NUMERIC_FIELDS = (
    "energy", "tempo_bpm", "valence", "danceability",
    "acousticness", "instrumentalness", "popularity",
)


def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file into a list of dicts, converting numeric
    columns to floats. Required by src/main.py
    """
    songs: List[Dict] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            for field in NUMERIC_FIELDS:
                if field in row and row[field] != "":
                    row[field] = float(row[field])
            songs.append(row)
    return songs


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song (dict) against user preferences (dict).
    Accepts both key styles: "genre"/"favorite_genre", "energy"/"target_energy".
    Returns (score, reasons).
    """
    return _compute_score(
        song_genre=song.get("genre", ""),
        song_mood=song.get("mood", ""),
        song_energy=float(song.get("energy", 0.0)),
        song_acousticness=float(song.get("acousticness", 0.0)),
        song_instrumentalness=float(song.get("instrumentalness", 0.0)),
        song_popularity=float(song.get("popularity", 0.0)),
        pref_genre=user_prefs.get("genre", user_prefs.get("favorite_genre")),
        pref_mood=user_prefs.get("mood", user_prefs.get("favorite_mood")),
        pref_energy=user_prefs.get("energy", user_prefs.get("target_energy")),
        likes_acoustic=user_prefs.get("likes_acoustic"),
        likes_instrumental=user_prefs.get("likes_instrumental"),
        prefers_popular=user_prefs.get("prefers_popular"),
    )


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, List[str]]]:
    """Score every song, rank high->low, and return the top k as (song, score, reasons)."""
    scored = [(song, *score_song(user_prefs, song)) for song in songs]
    scored.sort(key=lambda item: item[1], reverse=True)
    return scored[:k]
