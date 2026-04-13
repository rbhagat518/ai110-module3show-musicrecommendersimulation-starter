# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**VibeScorer 1.0** — A lightweight scoring-based music recommender that matches songs to user taste profiles using genre, mood, and audio feature similarity.  

---

## 2. Intended Use  

This recommender generates personalized song suggestions from a catalog of 20 songs based on a user's stated preferences for genre, mood, and energy level. It is designed for **classroom exploration only**, not for real-world deployment or production users. The system assumes users can articulate their preferences clearly and that their stated preferences are stable and meaningful.  

---

## 3. How the Model Works  

The recommender uses a **weighted scoring system** that evaluates each song across multiple dimensions:

**Categorical Matching:**
- If a song's genre matches the user's favorite genre → +1.0 points
- If a song's mood matches the user's preferred mood → +1.0 points

**Numeric Similarity:**
- Energy proximity: How close the song's energy is to the user's target energy (0–1 scale). A song with energy 0.9 when the user wants 0.8 scores close to 1.0; a song with 0.3 scores much lower.
- Acousticness preference: If the user likes acoustic sounds, songs with high acousticness get a bonus (up to ~0.75). If the user dislikes acoustic sounds, electric songs are preferred.

**The Final Score:**
Each song gets a total score combining genre match, mood match, energy closeness, and acousticness fit. The top 5 highest-scoring songs are returned as recommendations with explanation reasons.

**Changes from starter logic:**
The implementation maintains the original scoring structure but I've stress-tested it with adversarial profiles (conflicting preferences, extreme values, non-existent genres) to expose its strengths and weaknesses.

---

## 4. Data  

**Catalog Size:** 20 songs from `data/songs.csv`

**Genres Represented:** pop, lofi, rock, ambient, jazz, synthwave, indie pop, folk, hip-hop, classical, country, electronic, reggae, blues, metal

**Moods Included:** happy, chill, intense, moody, focused, energetic, relaxed, nostalgic, upbeat, adventurous, sad, melancholic, romantic, upbeat

**Audio Features:** Each song includes energy, tempo (BPM), valence, danceability, and acousticness on normalized scales.

**No modifications were made** to the original 20-song dataset.

**Missing Perspectives:** 
- Dataset skews toward English-language Western music genres; no diverse global music represented
- Underrepresented moods: introspective, contemplative, angry, ecstatic, confused
- Limited instrumentation/texture information (e.g., live vs. produced, vocal presence)
- No lyrical themes or semantic understanding
- No artist diversity metrics or representation counts  

---

## 5. Strengths  

✓ **Works well for clear, non-conflicting preferences:** Users with aligned preferences (e.g., "I like happy pop with high energy") get intuitive recommendations. Testing showed **Sunrise City** correctly ranked #1 for the High-Energy Pop profile.

✓ **Handles genre matching strongly:** When a user specifies a genre that exists in the dataset, the +1.0 genre bonus creates a powerful signal. Anti-Acoustic Rocker correctly surfaced **Steel Thunder** (metal genre match) as the top pick.

✓ **Gracefully degrades for missing genres:** When a user requests a non-existent genre like "experimental", the system falls back to mood and energy matching rather than crashing. It still produced sensible recommendations (e.g., **Focus Flow** for focused mood at energy 0.6).

✓ **Extreme preference handling:** Extreme cases (ultra-chill at energy 0.1 with acoustic preference, or max-energy 1.0 with anti-acoustic) are handled consistently and produce reasonable results.

✓ **Explainability:** Each recommendation includes reasoning ("matches your favorite genre", "energy is close to your target"), making it transparent why a song was suggested.  

---

## 6. Limitations and Bias  

✗ **Genre match dominates ratings:** A single genre match (+1.0) outweighs mood preferences entirely. The "Conflicting: Energetic Sadness" profile (wants high energy 0.9 but sad mood) recommended **Desert Dreams** at energy 0.55 because its country genre felt like a match. The user's conflicting signals were not resolved gracefully—energy won by default.

✗ **Mood mismatch has no penalty:** Unlike genre, mood mismatches do not reduce scores; they simply fail to add the +1.0 bonus. This means a very mismatched mood is treated the same as a neutral mood.

✗ **Acousticness preference is fragile:** It gets overridden easily by genre/mood/energy signals. The "Acoustic Paradox" profile (wants acoustic + high-energy pop) got **Sunrise City** (less acoustic, 0.18) instead of an equally energetic acoustic alternative, because genre+mood match trumped acousticness.

✗ **Limited feature set:** The system ignores:
  - Lyrical themes, sentiment, or language
  - Artist popularity or novelty
  - Collaboration and cross-artist patterns
  - Listening history or context (time of day, activity)
  - Diversity across recommendations (all top 5 might be very similar)

✗ **Catalog bias:** With only 20 songs, some genres and moods are barely represented. Electronic music appears in 2 songs; country in 1. This creates artificial preference for well-represented genres.

✗ **User profile assumptions:** The system assumes users know their own preferences and that preferences are stable. It does not account for:
  - Mood drift (user's mood changes over time)
  - Discovery fatigue (always recommending similar songs)
  - Conflicting or evolving taste

✗ **Energy weighting bias:** Energy similarity uses a 1-to-1 penalty (max score ~1.0) while genre gets +1.0 as a categorical bonus. Energy-focused users may feel the system under-weights their priority.  

---

## 7. Evaluation  

**Testing Approach:** I created a test suite with 11 distinct user profiles spanning standard cases and adversarial edge cases. Each profile was evaluated for whether recommendations matched intuitive expectations.

**Profiles Tested:**

1. **Standard cases** (expected to work well):
   - High-Energy Pop (energy 0.9, happy mood, pop genre)
   - Chill Lofi (energy 0.3, chill mood, lofi genre)
   - Deep Intense Rock (energy 0.95, intense mood, rock genre)

2. **Adversarial cases** (designed to expose weaknesses):
   - Conflicting: Energetic Sadness (high energy + sad mood = contradictory)
   - Acoustic Paradox (wants acoustic + high-energy pop = conflicting)
   - Moody Acoustic Lover (unusual niche combo)
   - Anti-Acoustic Rocker (explicitly no acoustic)
   - Neutral Fence-Sitter (mid-range energy, fuzzy preferences)
   - Mystery Genre (non-existent genre)
   - Extreme Chill (energy 0.1 = test floor)
   - Extreme Energy (energy 1.0 = test ceiling)

**What I Looked For:**
- Did the top recommendation match the profile's primary preference?
- Were conflicting signals handled gracefully or did one preference blindside the others?
- Did mood and energy preferences interact logically?

**Key Surprises:**
- Genre match was far more powerful than I expected; it could override energy mismatches by 0.4+ on the score scale
- The system successfully ranked mood-matched songs even when genre didn't match, showing mood as a secondary but meaningful signal
- Extreme cases (energy boundaries) were handled surprisingly well, suggesting the energy formula scales gracefully

**Simple Tests:**
- Ran all 11 profiles and verified top-5 recommendations made intuitive sense
- Spot-checked score calculations to ensure genre/mood bonuses and energy proximity were computed as designed
- Checked that non-existent genres didn't crash the system

---

## 8. Future Work  

**Short-term improvements:**
- **Conflict resolution:** Detect when user preferences contradict (e.g., high energy + sad mood) and either warn the user or intelligently compromise (e.g., recommend energetic songs with melancholic lyrics).
- **Weighted preferences:** Let users specify importance weights ("energy matters 2x more than genre to me") so scoring respects priority ordering.
- **Diversity penalty:** After ranking by score, re-rank to ensure top-5 recommendations span different genres/moods rather than clustering around the best match.
- **Better mood explanation:** Include lyrical or thematic reasons for mood matches, not just categorical matching.

**Medium-term improvements:**
- **Collaborative filtering:** Track what songs similar users liked and cross-recommend ("Users who liked your top pick also enjoyed...").
- **Temporal context:** Adapt recommendations based on time of day (morning: upbeat; evening: chill) or user's listening history.
- **Expanded feature set:** Add instrumentation (acoustic guitar, synth, strings), tempo range preferences, and valence (positivity) as first-class features alongside energy.
- **Cold-start handling:** For new users with no history, offer guided preference elicitation ("On a scale of 1-10, how much do you like acoustic sounds?").

**Long-term research:**
- **Serendipity vs. precision:** Balance between giving users exactly what they ask for vs. recommending unexpected discoveries.
- **Fairness audits:** Measure whether the system recommends underrepresented artists/genres fairly or if it amplifies majority bias.
- **Interactive refinement:** Let users rate recommendations in real-time to re-rank remaining songs dynamically.  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Building VibeScorer taught me that recommender systems are far more nuanced than I initially realized. What appears to users as a simple "ranked list of songs" hides dozens of interconnected decisions: how to weight conflicting signals, whether genre should dominate mood, how to handle edge cases gracefully, and what to do when user preferences contradict themselves. The most surprising discovery was how much the scoring *weights* matter—a small shift in how much genre matching is worth relative to energy similarity completely reshapes what gets recommended. This realization deepened my appreciation for Spotify's engineering: their recommender doesn't just serve what you explicitly asked for, but strategically balances satisfying your current taste with introducing you to artists and moods you haven't discovered yet. That balance between precision and serendipity—between "giving the user what they want" and "surprising them with something great"—is the real art of recommendation systems.