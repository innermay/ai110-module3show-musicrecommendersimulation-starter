````markdown
# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

**VibeMatch 1.0** — a transparent, content-based music recommender.

---

## 2. Intended Use and Non-Intended Use

### Goal and Task

VibeMatch predicts which songs a listener may like best. It takes a
taste profile containing the user's favorite genre, mood, target energy,
and preferences for acoustic, instrumental, or popular music.

It then returns a ranked list of songs from a small catalog. Each result
includes a score and an explanation of why the song was recommended.

### Intended Use

VibeMatch is intended as a classroom tool for learning how data becomes
a recommendation. It demonstrates how song attributes and user
preferences can be transformed into scores and ranked results.

The system assumes that the user can describe their musical preferences
before receiving recommendations. Its main benefit is explainability
because every recommendation includes the specific scoring reasons.

### Non-Intended Use

VibeMatch should not be used as a real commercial recommendation
product. It should not be trusted to make fair or complete decisions
about music because the catalog is small and hand-created.

The system should not be used to:

- Judge whether an artist or song is good or bad
- Rank artists based on their value
- Make important decisions for real users
- Represent the preferences of an entire population
- Replace real listening history or user feedback

VibeMatch does not learn over time, so it cannot automatically recognize
changes in a user's taste.

---

## 3. How the Model Works

Each song is described using attributes such as:

- Genre
- Mood
- Energy
- Acousticness
- Instrumentalness
- Popularity

The user creates a taste profile describing what kind of music they
want. The recommender examines every song in the catalog one at a time
and calculates how closely it matches the user's profile.

The model awards points for:

- Matching the user's preferred genre
- Matching the user's preferred mood
- Having energy close to the user's target
- Matching the user's acoustic or electronic preference
- Matching the user's instrumental or vocal preference
- Matching the user's popular or niche preference

Genre receives the highest weight because it is treated as the strongest
signal of musical preference. Mood receives the second-highest weight.
Energy is based on closeness rather than simply rewarding the highest
energy value.

The scoring weights are:

| Feature | Weight |
|---|---:|
| Genre | 0.25 |
| Mood | 0.20 |
| Energy | 0.20 |
| Acousticness | 0.15 |
| Instrumentalness | 0.10 |
| Popularity | 0.10 |

The energy closeness formula is:

```text
closeness = 1 - |song energy - target energy|
```

The recommender adds the points from all active rules and normalizes the
result to a score between `0.0` and `1.0`.

After scoring every song, the system sorts them from highest to lowest
score and returns the top recommendations. It also shows the exact
reasons that contributed strongly to each recommendation.

The main changes from the starter system were:

- Expanding the scoring function into six weighted rules
- Adding instrumentalness as a feature
- Adding popularity as a feature
- Scoring numeric traits by closeness
- Returning explanations with recommendation results
- Supporting optional user preferences
- Testing the system with several normal and adversarial profiles

---

## 4. Data Used

The catalog contains **18 songs** stored in `data/songs.csv`.

The original catalog contained 10 songs. I added 8 songs to increase
the variety of genres and moods represented in the system.

The catalog contains 15 genres:

- Pop
- Lofi
- Rock
- Ambient
- Jazz
- Synthwave
- Indie pop
- Hip-hop
- Classical
- EDM
- Reggae
- Metal
- R&B
- Country
- Folk

The catalog contains 14 moods:

- Happy
- Chill
- Intense
- Relaxed
- Moody
- Focused
- Energetic
- Melancholy
- Euphoric
- Laid-back
- Aggressive
- Romantic
- Nostalgic
- Dreamy

Each song contains the following attributes:

| Attribute | Description |
|---|---|
| `id` | Unique identifier |
| `title` | Song title |
| `artist` | Performer |
| `genre` | Musical category |
| `mood` | Overall vibe |
| `energy` | Intensity from 0.0 to 1.0 |
| `tempo_bpm` | Speed in beats per minute |
| `valence` | Positivity from 0.0 to 1.0 |
| `danceability` | Rhythmic movement from 0.0 to 1.0 |
| `acousticness` | Acoustic sound level from 0.0 to 1.0 |
| `instrumentalness` | Amount of instrumental content |
| `popularity` | How mainstream the song is |

The current scoring function uses genre, mood, energy, acousticness,
instrumentalness, and popularity.

Tempo, valence, and danceability are stored in the dataset but are not
currently included in the recommendation score.

### Data Limitations

The dataset is small and hand-authored. Most genres appear only once,
which means the system has limited choices for many user profiles.

The dataset also does not contain:

- Lyrics
- Language
- Release year
- Musical era
- Cultural context
- Real user likes
- Skips
- Replays
- Listening duration
- Playlist history

These missing features mean that a large part of real musical taste is
invisible to the recommender.

---

## 5. Strengths

### Explainable Recommendations

Every recommendation includes the reasons that contributed to the
song's score. A user can see whether a song matched based on genre,
mood, energy, sound, vocals, or popularity.

### Sensible Opposite Profiles

Profiles with very different preferences produce clearly different
results. For example, High-Energy Pop and Chill Lofi receive almost
opposite recommendations.

### Numeric Closeness

Energy scoring rewards songs near the target from either direction. The
system does not automatically assume that higher energy is always
better.

### Partial User Profiles

Optional preferences can be left unset. When a preference is missing,
that rule is skipped and the score is normalized using the remaining
active rules.

### Cross-Genre Matches

Songs can still rank well even when their genre does not match. A song
may compete through energy, mood, acousticness, instrumentalness, and
popularity.

---

## 6. Limitations and Biases

### Exact-Match Genre and Mood Rules

Genre and mood use all-or-nothing matching. A rock user receives no
genre credit for a metal song, even though those genres may be closely
related.

This can bury strong cross-genre recommendations that match the user's
other preferences.

### Conflicting Preferences

The clearest weakness I found is that the exact-match genre and mood
rules, which have a combined weight of `0.45`, can overpower a user's
numeric preferences.

In the Conflicting profile, the user requested:

- Classical music
- A melancholy mood
- Very high energy of `0.95`
- Acoustic sound
- Instrumental music
- Niche popularity

The top result was *Winter Elegy*, which has an energy level of only
`0.30`.

The song still received a small energy contribution:

```text
1 - |0.30 - 0.95| = 0.35

0.35 × 0.20 = 0.07 energy points
```

However, its matching genre and mood contributed enough points for it
to rank first despite the large energy mismatch.

The energy contribution was not shown as a recommendation reason
because the code only displays the phrase `energy close to target` when
the closeness value is at least `0.85`.

This means the system can return a technically high-scoring result that
does not satisfy one of the user's most noticeable preferences.

### Filter Bubbles

The system mainly recommends more of what the user already requested.
It does not intentionally introduce variety or unexpected genres.

This can create a filter bubble where users repeatedly receive similar
music instead of discovering something new.

### Dataset Imbalance

Pop and lofi each appear multiple times, while many genres appear only
once. Genres with more songs have more opportunities to appear in the
top results.

### Popularity Bias

The popularity rule can push already-mainstream songs higher in the
ranking. This creates a rich-get-richer effect that may make niche
artists less visible.

### Correlated Features

Mood and energy can describe similar characteristics. For example,
songs labeled intense are often also high-energy.

The recommender may partially count the same musical quality twice.

### Missing Lyrical and Cultural Context

The model only sees labels and numbers. It cannot understand the
meaning of lyrics, language, time period, cultural importance, or
personal memories associated with a song.

A bright-sounding song with sad lyrics might be treated as happy because
the system cannot interpret the lyrics.

---

## 7. Evaluation Process

I tested five user profiles:

1. High-Energy Pop
2. Chill Lofi
3. Deep Intense Rock
4. Conflicting high-energy and melancholy preferences
5. Minimal energy-only preferences

The first three represent ordinary music preferences. The final two are
adversarial edge cases designed to expose unusual behavior.

During evaluation, I checked:

- Whether the top recommendations matched musical intuition
- Whether different profiles produced meaningfully different results
- Whether the same song dominated every profile
- Whether explanations reflected the scoring rules
- How the system handled conflicting preferences
- How the system handled missing preferences

---

## 8. Evaluation Results

### High-Energy Pop

The High-Energy Pop profile requested:

```python
{
    "genre": "pop",
    "mood": "happy",
    "energy": 0.9,
    "likes_acoustic": False,
    "likes_instrumental": False,
    "prefers_popular": True,
}
```

Top results:

```text
1. Sunrise City — Neon Echo  (score: 0.93)
2. Gym Hero — Max Pulse  (score: 0.77)
3. Rooftop Lights — Indigo Parade  (score: 0.63)
4. Storm Runner — Voltline  (score: 0.48)
5. Concrete Anthem — Kilo Verse  (score: 0.48)
```

*Sunrise City* ranked first because it matched the user's genre, mood,
energy target, electronic sound preference, vocal preference, and
popularity preference.

### Why Gym Hero Ranks Highly

*Gym Hero* is pop, has energy close to the user's target, has a produced
electronic sound, includes vocals, and is popular.

It earns points from five of the six active scoring rules. Its mood is
labeled intense instead of happy, so it does not receive mood points.
However, its other matches are strong enough for it to rank second.

This explanation reflects only features used by the scoring function.
Danceability is stored in the dataset but does not affect the current
score.

---

### Chill Lofi

The Chill Lofi profile requested:

```python
{
    "genre": "lofi",
    "mood": "chill",
    "energy": 0.35,
    "likes_acoustic": True,
    "likes_instrumental": True,
    "prefers_popular": False,
}
```

Top results:

```text
1. Library Rain — Paper Lanterns  (score: 0.92)
2. Midnight Coding — LoRoom  (score: 0.87)
3. Focus Flow — LoRoom  (score: 0.69)
4. Spacewalk Thoughts — Orbit Bloom  (score: 0.69)
5. Winter Elegy — Aria Solenne  (score: 0.49)
```

*Library Rain* ranked first because it matched the lofi genre, chill
mood, low-energy target, acoustic preference, instrumental preference,
and niche preference.

---

### Deep Intense Rock

The Deep Intense Rock profile requested:

```python
{
    "genre": "rock",
    "mood": "intense",
    "energy": 0.9,
    "likes_acoustic": False,
    "likes_instrumental": False,
    "prefers_popular": False,
}
```

Top results:

```text
1. Storm Runner — Voltline  (score: 0.91)
2. Gym Hero — Max Pulse  (score: 0.64)
3. Iron Verdict — Blacksteel Rise  (score: 0.47)
4. Concrete Anthem — Kilo Verse  (score: 0.43)
5. Sunrise City — Neon Echo  (score: 0.42)
```

*Storm Runner* ranked first because it matched the rock genre, intense
mood, high-energy target, electronic sound preference, and vocal
preference.

*Gym Hero* ranked second even though it is pop because it shares the
high-energy and intense characteristics requested by the profile. This
shows that energy and mood can act as bridges between genres.

---

### Conflicting Profile

The Conflicting profile requested:

```python
{
    "genre": "classical",
    "mood": "melancholy",
    "energy": 0.95,
    "likes_acoustic": True,
    "likes_instrumental": True,
    "prefers_popular": False,
}
```

Top results:

```text
1. Winter Elegy — Aria Solenne  (score: 0.82)
2. Spacewalk Thoughts — Orbit Bloom  (score: 0.37)
3. Library Rain — Paper Lanterns  (score: 0.35)
4. Focus Flow — LoRoom  (score: 0.35)
5. Coffee Shop Stories — Slow Stereo  (score: 0.34)
```

*Winter Elegy* has an energy value of only `0.30`, which is far below
the requested `0.95`.

It ranked first because its classical genre, melancholy mood, acoustic
sound, instrumentalness, and niche popularity matched the other parts
of the profile.

This result exposed a weakness: several categorical matches can
outweigh one major numeric mismatch.

---

### Minimal Profile

The Minimal profile only included an energy preference:

```python
{
    "energy": 0.5
}
```

Top results:

```text
1. Velvet Hours — Mara Sky  (score: 0.98)
2. Dust Road Home — Cedar & Pine  (score: 0.98)
3. Island Time — Sun Groove  (score: 0.95)
4. Midnight Coding — LoRoom  (score: 0.92)
5. Focus Flow — LoRoom  (score: 0.90)
```

The scores were very high because energy was the only active rule. The
final score was normalized using only the energy weight, so songs near
the target received scores close to `1.0`.

This confirmed that the optional rules switch off correctly when
preferences are missing.

---

## 9. Profile Comparisons

### High-Energy Pop vs. Chill Lofi

These profiles produced almost opposite results.

The Pop profile favored:

- High energy
- Electronic production
- Vocals
- Popular songs

The Lofi profile favored:

- Lower energy
- Acoustic sound
- Instrumental music
- Niche songs

This shows that opposite user preferences produce different and
reasonable recommendations.

### High-Energy Pop vs. Deep Intense Rock

Both profiles requested high energy, so they shared some candidates.

The Pop profile was led by *Sunrise City*. The Rock profile was led by
*Storm Runner*. *Gym Hero* ranked highly in both because it matched the
energy and intensity traits shared by the two profiles.

This shows that energy can connect songs across genres.

### Deep Intense Rock vs. Conflicting

The Rock profile requested intense, high-energy music and correctly
received *Storm Runner*.

The Conflicting profile also requested high energy, but it received
*Winter Elegy*, a low-energy song, because the genre and mood matches
were more influential.

This comparison exposed how the system handles preferences that do not
naturally appear together in the dataset.

### Standard Profiles vs. Minimal

The standard profiles used genre, mood, energy, acousticness,
instrumentalness, and popularity.

The Minimal profile used only energy. As a result, genre and mood had no
effect, and songs near the target energy ranked first regardless of
style.

---

## 10. Weight Experiment

I tested the sensitivity of the system by changing two weights.

Original weights:

```text
Genre: 0.25
Energy: 0.20
```

Experimental weights:

```text
Genre: 0.125
Energy: 0.40
```

I doubled the importance of energy and cut the importance of genre in
half.

The number-one recommendation did not change for the Pop or Rock
profile because their top songs matched both genre and energy.

However, the score gap between the top song and the remaining songs
became smaller. High-energy songs from other genres also moved higher.

For example, *Storm Runner* increased from approximately `0.48` to
`0.63` in the Pop results.

The experiment made the recommendations more energy-driven, while genre
became closer to a tiebreaker.

The experiment did not make the recommender automatically more
accurate. It made the results different according to a different design
priority.

The scores remained between `0.0` and `1.0` because the scoring function
normalizes the total points by the sum of the active weights.

---

## 11. Full Terminal Output

The following output was produced by:

```bash
python -m src.main
```

```text
Loaded songs: 18

=== High-Energy Pop ===
profile: {'genre': 'pop', 'mood': 'happy', 'energy': 0.9, 'likes_acoustic': False, 'likes_instrumental': False, 'prefers_popular': True}

1. Sunrise City — Neon Echo  (score: 0.93)
     • genre match: pop (+0.25)
     • mood match: happy (+0.20)
     • energy close to target (+0.18)
     • produced/electronic match (+0.12)
     • vocal match (+0.10)
     • popular pick (+0.08)

2. Gym Hero — Max Pulse  (score: 0.77)
     • genre match: pop (+0.25)
     • energy close to target (+0.19)
     • produced/electronic match (+0.14)
     • vocal match (+0.10)
     • popular pick (+0.09)

3. Rooftop Lights — Indigo Parade  (score: 0.63)
     • mood match: happy (+0.20)
     • energy close to target (+0.17)
     • produced/electronic match (+0.10)
     • vocal match (+0.09)
     • popular pick (+0.07)

4. Storm Runner — Voltline  (score: 0.48)
5. Concrete Anthem — Kilo Verse  (score: 0.48)

=== Chill Lofi ===
profile: {'genre': 'lofi', 'mood': 'chill', 'energy': 0.35, 'likes_acoustic': True, 'likes_instrumental': True, 'prefers_popular': False}

1. Library Rain — Paper Lanterns  (score: 0.92)
     • genre match: lofi (+0.25)
     • mood match: chill (+0.20)
     • energy close to target (+0.20)
     • acoustic match (+0.13)
     • instrumental match (+0.09)

2. Midnight Coding — LoRoom  (score: 0.87)
3. Focus Flow — LoRoom  (score: 0.69)
4. Spacewalk Thoughts — Orbit Bloom  (score: 0.69)
5. Winter Elegy — Aria Solenne  (score: 0.49)

=== Deep Intense Rock ===
profile: {'genre': 'rock', 'mood': 'intense', 'energy': 0.9, 'likes_acoustic': False, 'likes_instrumental': False, 'prefers_popular': False}

1. Storm Runner — Voltline  (score: 0.91)
     • genre match: rock (+0.25)
     • mood match: intense (+0.20)
     • energy close to target (+0.20)
     • produced/electronic match (+0.14)
     • vocal match (+0.09)

2. Gym Hero — Max Pulse  (score: 0.64)
3. Iron Verdict — Blacksteel Rise  (score: 0.47)
4. Concrete Anthem — Kilo Verse  (score: 0.43)
5. Sunrise City — Neon Echo  (score: 0.42)

=== Conflicting (high-energy + melancholy) ===
profile: {'genre': 'classical', 'mood': 'melancholy', 'energy': 0.95, 'likes_acoustic': True, 'likes_instrumental': True, 'prefers_popular': False}

1. Winter Elegy — Aria Solenne  (score: 0.82)
     • genre match: classical (+0.25)
     • mood match: melancholy (+0.20)
     • acoustic match (+0.14)
     • instrumental match (+0.10)
     • niche pick (+0.07)

2. Spacewalk Thoughts — Orbit Bloom  (score: 0.37)
3. Library Rain — Paper Lanterns  (score: 0.35)
4. Focus Flow — LoRoom  (score: 0.35)
5. Coffee Shop Stories — Slow Stereo  (score: 0.34)

=== Minimal (energy only) ===
profile: {'energy': 0.5}

1. Velvet Hours — Mara Sky  (score: 0.98)
     • energy close to target (+0.20)

2. Dust Road Home — Cedar & Pine  (score: 0.98)
3. Island Time — Sun Groove  (score: 0.95)
4. Midnight Coding — LoRoom  (score: 0.92)
5. Focus Flow — LoRoom  (score: 0.90)
```

---

## 12. Ideas for Improvement

### Soft Genre Matching

Related genres could receive partial credit instead of using exact
matching.

Examples include:

```text
rock ↔ metal
pop ↔ indie pop
ambient ↔ lofi
country ↔ folk
```

### Conflict Warnings

The system could detect when one user preference strongly disagrees
with another preference.

For example, it could show:

```text
Note: This song matches your genre and mood, but its energy is much
lower than your requested target.
```

### Multiple Taste Profiles

A user could create separate profiles for different activities:

- Studying
- Working out
- Driving
- Relaxing
- Sleeping

### More Diverse Top Results

A diversity rule could prevent the top recommendations from containing
too many songs with nearly identical attributes.

### Larger Real Dataset

A larger dataset would give less-represented genres more competition
and reduce the influence of individual hand-created songs.

### Real User Feedback

Future versions could use:

- Likes
- Skips
- Replays
- Playlist additions
- Listening duration

These behaviors could update the user's profile over time.

### Additional Features

Tempo, valence, and danceability could be incorporated into the scoring
function.

---

## 13. Personal Reflection

### Biggest Learning Moment

The Conflicting profile surprised me the most. I requested high energy
and a melancholy mood, but the system recommended a slow, quiet song.

After examining the score, I realized that genre and mood had enough
combined weight to overpower the energy preference. This taught me that
the weights in an algorithm are not automatically correct. They reflect
the developer's decisions about what should matter most.

### How AI Tools Helped

The AI assistant helped me understand and implement:

- CSV loading
- Numeric type conversion
- Weighted scoring
- Recommendation ranking
- `.sort()` compared with `sorted()`
- Human-readable explanation strings
- Edge-case profiles
- Possible filter bubbles and biases

However, I still needed to double-check the generated work. I verified
that numeric CSV values were converted to floats, that the scoring
weights matched my plan, and that scores stayed between `0.0` and `1.0`.

I also checked whether the recommendations made sense instead of
assuming the system was correct just because the code ran.

### What Surprised Me

The system does not use machine learning. It only uses points, formulas,
and sorting. However, the final results still feel similar to real
recommendations.

This taught me that recommendation systems can appear intelligent even
when their behavior comes from relatively simple rules. The quality of
the data and scoring decisions strongly affects how intelligent the
output feels.

### What I Would Try Next

I would add partial matching for related genres, use a larger and more
realistic dataset, and add diversity to the top results.

I would also allow the system to learn from likes, skips, and replays so
the user would not need to describe every preference manually.
````
