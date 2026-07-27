# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

**VibeMatch 1.0** — a transparent, content-based music recommender.

---

## 2. Intended Use

VibeMatch generates a ranked, *explained* list of song recommendations from a small catalog based on an explicit user "taste profile" (favorite genre, mood, target energy, and preferences for acoustic sound, instrumental music, and mainstream popularity). It assumes the user can describe their taste up front, and it treats every listener as a single fixed set of preferences. **This is a classroom exploration tool, not a production system** — the goal is to understand how data becomes a recommendation, with every result fully explainable.

---

## 3. How the Model Works

Each song is described by attributes like genre, mood, energy, how acoustic it is, whether it has vocals, and how popular it is. The user describes what they like. The model then acts like a judge: it looks at every song one at a time and awards points for each way the song matches the listener's taste — a chunk of points for a matching genre, a smaller chunk for a matching mood, and partial points for numeric traits (like energy) based on *how close* the song is to what the user wants. It adds up the points into a single score between 0 and 1, then sorts all the songs from best to worst and shows the top few, along with the exact reasons each one was picked. The main change from the starter logic was expanding it from a stub into a six-rule weighted recipe, adding two new features (instrumentalness and popularity), and making numeric traits score by *closeness* rather than raw size.

---

## 4. Data

The catalog has **18 songs** in `data/songs.csv`. It spans 15 genres (pop, lofi, rock, ambient, jazz, synthwave, indie pop, hip-hop, classical, edm, reggae, metal, r&b, country, folk) and 14 moods (happy, chill, intense, relaxed, moody, focused, energetic, melancholy, euphoric, laid-back, aggressive, romantic, nostalgic, dreamy). I expanded it from the original 10 songs by adding 8 with new genres/moods, and added two numeric columns (`instrumentalness`, `popularity`). **What's missing:** the data is tiny and hand-authored, most genres appear only once, and there is nothing about lyrics, language, era, or an artist's cultural context — so a big part of what actually defines musical taste is invisible to the model.

---

## 5. Strengths

- **Clear opposites are handled cleanly.** Profiles that differ on every axis (High-Energy Pop vs. Chill Lofi) get sharply different, sensible top picks.
- **Every recommendation is explainable.** The system reports the exact points each rule contributed, so a user can always see *why* a song was suggested.
- **Numeric closeness feels right.** Energy scoring rewards songs near the target from either direction, so it doesn't just pile up the loudest or quietest songs.
- **Graceful with partial input.** A user can leave preferences unset and still get reasonable, energy-driven results.

---

## 6. Limitations and Bias

The clearest weakness I found is that the **all-or-nothing genre and mood rules (a combined 0.45 of the weight) can silently override a user's numeric preferences.** In my "Conflicting" edge-case profile, the user asked for very high energy (`0.95`) but a `melancholy` mood — and the #1 result was *Winter Elegy*, a song with energy `0.30`. Because genre and mood matched, they contributed enough points to win even though the song is the *opposite* of the high energy the user requested (notice its explanation has no "energy close to target" line at all). In other words, the system quietly resolves conflicting preferences by ignoring the numeric one, without telling the user it did so. A second, related bias is a **filter-bubble / dataset-size problem**: with only 18 songs and most genres appearing just once, the content-based logic keeps recommending "more of the same" and can never surprise the user, while the over-represented genres (pop and lofi each appear 3×) have a structural advantage in showing up.

---

## 7. Evaluation

**Profiles tested.** I ran five profiles (see fenced output below): three ordinary ones — **High-Energy Pop**, **Chill Lofi**, **Deep Intense Rock** — and two adversarial edge cases — **Conflicting** (high energy + melancholy mood) and **Minimal** (only an energy target set). I looked for whether top picks matched intuition, whether the same song dominated every list, and how the system behaved under conflicting or missing input.

**What surprised me.** Two things. First, in the *Minimal* profile (energy `0.5` only) the scores jumped to `0.98` because the score is normalized by the weight of the rules that actually fired — with one rule active, a good energy match nearly maxes out. Second, *Gym Hero* (a pop song labeled "intense") shows up near the top for **both** the Pop and Rock profiles, which taught me that energy is a *shared* axis different profiles compete over.

**Why "Gym Hero" keeps showing up for a Happy Pop fan (plain language).** Imagine the recommender giving out gold stars. *Gym Hero* is pop, it's loud and high-energy, it's danceable, it has vocals, and it's popular — so it collects a gold star for almost every box a "happy pop" listener cares about. Its official mood tag is "intense" rather than "happy," so it misses *that one* star — but five out of six is still enough to land near the top. It's not a bug; it's the system correctly noticing that a high-energy pop hit is a pretty good match for someone who wants high-energy pop, even if the mood label isn't a perfect word-for-word match.

**Profile-to-profile comparisons:**

- **High-Energy Pop vs. Chill Lofi:** Complete opposites, as expected. Pop surfaces *Sunrise City* (loud, produced, vocal, popular); Lofi surfaces *Library Rain* (quiet, acoustic, instrumental, niche). This is the system working exactly as intended — opposite tastes, opposite results.
- **High-Energy Pop vs. Deep Intense Rock:** Both want high energy, so they *share* candidates. Pop is led by *Sunrise City* and Rock by *Storm Runner*, but *Gym Hero* ranks highly in both because it matches the energy/intensity axis they have in common. This shows energy is a cross-genre bridge.
- **Deep Intense Rock vs. Conflicting:** Rock (intense + energy 0.9) correctly gets the high-energy *Storm Runner*; the Conflicting profile (melancholy + energy 0.95) gets the *low-energy* *Winter Elegy*. The difference makes sense and exposes the bias above — genre + mood beat the energy request, so a "high-energy" user was handed a slow song.
- **Any profile vs. Minimal:** With only energy set, genre/mood/sound stop mattering and mid-energy songs like *Velvet Hours* win regardless of style. This confirms the rules switch off cleanly when a preference is absent.

**Weight experiment (data sensitivity).** I doubled the energy weight (0.20 → 0.40) and halved genre (0.25 → 0.125), then re-ran. The **#1 pick did not change** for either Pop or Rock (those songs match on both energy *and* genre), but the gap between #1 and the rest **compressed sharply** and high-energy off-genre songs climbed (e.g. *Storm Runner* rose from 0.48 to 0.63 in the Pop list). Conclusion: the change made recommendations *different* (more energy-driven, genre reduced to a tiebreaker) rather than obviously *more accurate* — a good reminder that weight choices are value judgments, not correctness fixes. The scoring math stayed valid: scores remained in [0, 1] because the total is normalized by the sum of active weights.

### Full terminal output (`python -m src.main`)

```
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
4. Storm Runner — Voltline  (score: 0.48)  [rock — surfaces on energy/sound, not genre]
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
2. Gym Hero — Max Pulse  (score: 0.64)  [pop — shares the energy/intensity axis]
3. Iron Verdict — Blacksteel Rise  (score: 0.47)
4. Concrete Anthem — Kilo Verse  (score: 0.43)
5. Sunrise City — Neon Echo  (score: 0.42)

=== Conflicting (high-energy + melancholy) ===
profile: {'genre': 'classical', 'mood': 'melancholy', 'energy': 0.95, 'likes_acoustic': True, 'likes_instrumental': True, 'prefers_popular': False}

1. Winter Elegy — Aria Solenne  (score: 0.82)  [energy 0.30 — NO energy-match line: request ignored]
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

1. Velvet Hours — Mara Sky  (score: 0.98)   • energy close to target (+0.20)
2. Dust Road Home — Cedar & Pine  (score: 0.98)
3. Island Time — Sun Groove  (score: 0.95)
4. Midnight Coding — LoRoom  (score: 0.92)
5. Focus Flow — LoRoom  (score: 0.90)
```

---

## 8. Future Work

- **Soft genre matching** — give partial credit to related genres (rock ↔ metal ↔ punk) instead of all-or-nothing, so great cross-genre songs aren't buried.
- **Warn on conflicts** — detect when genre/mood overrides a numeric request and flag it in the explanation ("note: energy was much higher than this song").
- **Multi-mood profiles** — let one user hold several taste profiles (gym / study / commute) and recommend against the closest.
- **Diversity in the top-K** — penalize near-duplicates so the list isn't five variations of the same song.
- **A much larger, real dataset** — to reduce the filter-bubble effect and give single-song genres real competition.

---

## 9. Personal Reflection

*(Draft — personalize this.)* Building VibeMatch made recommender systems feel much less magical and much more like a transparent set of point rules. The most interesting discovery was the "Conflicting" profile: I assumed asking for high energy would guarantee an energetic song, but the genre and mood rules quietly overruled it — which showed me how much a system's *weights* silently encode someone's assumptions about what matters. It changed how I think about apps like Spotify: when a recommendation feels "off," it's often not broken, it's just optimizing for a different balance of signals than I expected.
