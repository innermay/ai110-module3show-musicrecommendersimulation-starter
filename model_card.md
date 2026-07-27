# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

**VibeMatch 1.0** — a transparent, content-based music recommender.

---

## 2. Intended Use (and Non-Intended Use)

**Goal / task.** VibeMatch predicts which songs a listener will like best. It takes a taste profile (favorite genre, mood, target energy, and whether the user likes acoustic, instrumental, or popular music) and returns a ranked, explained list of songs from a small catalog.

**Intended use.** It is a classroom tool for learning how data becomes a recommendation. It assumes the user can describe their taste up front. Every result is fully explainable.

**Non-intended use.** It should **not** be used as a real product or to make real choices for people. It should not be trusted to be fair, because the catalog is tiny and hand-made. It should not be used to judge artists, rank "good" vs. "bad" music, or personalize anything for real users. It has no real listening data, so it cannot actually learn what a person likes over time.

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

*(Draft — please edit into your own words.)*

**My biggest learning moment.** The "Conflicting" profile surprised me the most. I asked for high energy but a sad mood, and the system gave me a slow, quiet song. I realized the genre and mood rules were quietly overruling the energy request. That taught me that the *weights* I pick are really just my own opinions about what matters most.

**How AI tools helped, and when I double-checked them.** The AI assistant helped me write the CSV loader, the scoring function, and the ranking logic quickly, and it explained ideas like `.sort()` vs `sorted()`. But I had to double-check its work: it needed reminders to convert CSV numbers to floats, and when I added new features I had to make sure the tests still passed and the math still added up to a valid 0–1 score. I also checked that the recommendations actually made sense instead of just trusting the code ran.

**What surprised me about simple algorithms.** There is no machine learning here — just points and sorting. But the output still *feels* like a real recommendation. Adding up a few numbers and ranking them is enough to look "smart," which made me realize how much of a recommender is just clear rules plus good data.

**What I'd try next.** I'd add soft genre matching so related genres (like rock and metal) share credit, use a much bigger and more realistic dataset, and make the top results more diverse so I don't get five near-identical songs.
