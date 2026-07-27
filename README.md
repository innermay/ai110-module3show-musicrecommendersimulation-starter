# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Real-world platforms like Spotify and YouTube predict what you'll love next by blending two ideas: **collaborative filtering**, which recommends music based on the behavior of users with similar taste ("people like you also liked this"), and **content-based filtering**, which recommends songs whose measurable attributes — tempo, energy, mood — resemble songs you already enjoy. At full scale they lean heavily on massive behavioral datasets (likes, skips, replays, watch time) fed into machine-learning models. My simulation is a **content-based** recommender: it has no crowd of other users to learn from, so instead of behavior it prioritizes the *attributes of the songs themselves* and how well they match an explicit user taste profile. The system scores every song against the user's preferences using a transparent, weighted rulebook, then ranks those scores to surface the best matches. I deliberately favor **explainability over accuracy** — every recommendation can state, in plain language, exactly why it was chosen — because the goal of this project is to understand how data becomes a prediction, not to compete with a real streaming service.

### Features used

**`Song`** describes each track's attributes:

- `id` — unique identifier
- `title` — song name
- `artist` — performer
- `genre` — category (pop, lofi, rock, …) *(used in scoring)*
- `mood` — vibe label (happy, chill, intense, …) *(used in scoring)*
- `energy` — intensity, 0–1 *(used in scoring)*
- `tempo_bpm` — speed in beats per minute
- `valence` — musical positivity (happy vs sad), 0–1
- `danceability` — rhythmic groove, 0–1
- `acousticness` — organic vs electronic texture, 0–1 *(used in scoring)*

**`UserProfile`** stores the listener's explicit taste:

- `favorite_genre` — the genre they prefer
- `favorite_mood` — the vibe they're after
- `target_energy` — how intense they want it, 0–1
- `likes_acoustic` — whether they prefer acoustic sound (True/False)

### How a score is computed

Each song earns a score in **[0.0, 1.0]** from four weighted rules, then all songs are sorted high-to-low and the top *k* are returned:

| Rule | Compares | Weight |
|------|----------|:------:|
| Genre match | `song.genre` vs `favorite_genre` | 0.30 |
| Mood match | `song.mood` vs `favorite_mood` | 0.25 |
| Energy fit (closeness: `1 − \|song.energy − target_energy\|`) | `song.energy` vs `target_energy` | 0.25 |
| Acoustic fit (direction depends on `likes_acoustic`) | `song.acousticness` vs `likes_acoustic` | 0.20 |

Genre is weighted highest because it is the most reliable "is this my kind of music?" signal; mood is close behind but coarser. Numeric features are scored by *closeness* to the target rather than by raw magnitude, so a song near the user's preferred energy scores well from either direction.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
# e.g.:
# User profile: genre=indie, mood=chill, energy=low
# Recommendations:
#   1. ...
#   2. ...
#   3. ...
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



