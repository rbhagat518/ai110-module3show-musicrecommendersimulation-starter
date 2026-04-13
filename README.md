# 🎵 Music Recommender Simulation

## Project Summary

**VibeScorer 1.0** is a lightweight music recommender that matches songs to user taste profiles using a weighted scoring system. Given a user's preferences (genre, mood, energy level, acoustic preference), the system scores each song in a 20-song catalog based on categorical matches (genre, mood) and numeric similarity (energy proximity, acousticness alignment). The top 5 highest-scoring songs are returned with explanations—making the recommendation logic transparent and inspectable.

This project demonstrates how simple scoring rules can create surprisingly sophisticated recommendations, while also exposing fundamental limitations: conflicting preferences, dominant signals that suppress others, and biases baked into scoring weights. By testing the system with adversarial user profiles, I identified where the recommender excels and where it fails gracefully.

---

## How The System Works

### Song Features
Each song in the catalog is represented by:
- **Categorical:** genre, mood
- **Numeric (0–1 scale):** energy, tempo (BPM), valence, danceability, acousticness

### User Profile
Users specify:
- `genre` — their favorite music genre (e.g., "pop", "lofi")
- `mood` — preferred emotional context (e.g., "happy", "chill")
- `energy` — target energy level on a 0–1 scale (0 = ultra-calm, 1 = maximum intensity)
- `likes_acoustic` (optional) — whether they prefer acoustic or electric sounds

### Scoring Logic

For each song, the recommender computes a score combining:

1. **Genre Match:** If the song's genre exactly matches the user's favorite → **+1.0 points**
2. **Mood Match:** If the song's mood exactly matches the user's preferred mood → **+1.0 points**
3. **Energy Proximity:** How close the song's energy is to the user's target.
   - Formula: `1.0 - |song_energy - target_energy|`
   - Example: User wants 0.8 energy; a song at 0.82 scores ~0.98; a song at 0.3 scores 0.5
4. **Acousticness Alignment:**
   - If `likes_acoustic=True`: add the song's acousticness value (0–1) as a bonus
   - If `likes_acoustic=False`: add `1 - acousticness` (boost non-acoustic songs)

**Final Score = genre_match + mood_match + energy_proximity + acousticness_bonus**

### Recommendation Process
1. Score all 20 songs using the above formula
2. Sort by score (highest first)
3. Return top 5 songs with their scores and explanations

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

## Experiments You Tried

I designed and tested **11 user profiles**— (see test_adversarial_profiles.py) to evaluate how well the scoring logic handles conflicting preferences and extreme scenarios.

![Recommendations Overview](recommendations.png)

#### Standard Profiles

**High-Energy Pop**
![High-Energy Pop Profile](high-energy-pop-profile.png)

**Chill Lofi**
![Chill Lofi Profile](chill-lofi-profile.png)

**Deep Intense Rock**
![Deep Intense Rock Profile](deep-intense-rock-profile.png)

**Energetic + Intense Sadness** (High energy 0.9 but sad mood)
![Energetic Sadness Profile](energetic-intense-sadness.png)

**Neutral Fence-Sitter** (Mid-range energy, no strong acoustic preference)
![Neutral Profile](neutral-profile.png)

#### Key Findings

- Genre matching heavily outweighs mood preferences (±1.0 bonus dominates)
- Acoustic preference is fragile and easily overridden by genre/energy factors
- System degrades gracefully for non-existent genres (falls back to mood/energy)
- Extreme cases (energy 0.1 or 1.0) are handled well with acoustic preference acting as a strong modifier

---

## Limitations and Risks

- **Tiny catalog:** With only 20 songs, recommendations are heavily constrained. Some genres appear only once or twice, skewing results.
- **Genre match dominates:** A single genre match worth +1.0 can overwhelm other signals. Users asking for "energetic + sad" get energetic songs regardless of mood match.
- **No contextual understanding:** The system doesn't know listening context, mood drift, or history. All recommendations are stateless.
- **Rigid categorical matching:** Genres and moods must match exactly—no fuzzy or partial credit for related categories.
- **Acousticness bias:** Acoustic preference (0–0.75 range) is weaker than genre/mood bonuses (±1.0), making it easy to override.
- **No diversity enforcement:** Top 5 recommendations might cluster around very similar songs instead of providing variety.

See [**Model Card**](model_card.md) for deeper analysis.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

Building VibeScorer taught me that recommender systems are far more nuanced than I initially realized. What appears to users as a simple "ranked list of songs" hides dozens of interconnected decisions: how to weight conflicting signals, whether genre should dominate mood, how to handle edge cases gracefully, and what to do when user preferences contradict themselves. The most surprising discovery was how much the scoring *weights* matter—a small shift in how much genre matching is worth relative to energy similarity completely reshapes what gets recommended. This realization deepened my appreciation for Spotify's engineering: their recommender doesn't just serve what you explicitly asked for, but strategically balances satisfying your current taste with introducing you to artists and moods you haven't discovered yet. That balance between precision and serendipity—between "giving the user what they want" and "surprising them with something great"—is the real art of recommendation systems.

Bias or unfairness could show up in the form of a lack of exploration due to the lack of weight of other 

---

## 7. `model_card_template.md`

Combines reflection and model card framing from the Module 3 guidance. :contentReference[oaicite:2]{index=2}  

```markdown
# 🎧 Model Card - Music Recommender Simulation

## 1. Model Name

Give your recommender a name, for example:

> VibeFinder 1.0

---

## 2. Intended Use

- What is this system trying to do
- Who is it for

Example:

> This model suggests 3 to 5 songs from a small catalog based on a user's preferred genre, mood, and energy level. It is for classroom exploration only, not for real users.

---

## 3. How It Works (Short Explanation)

Describe your scoring logic in plain language.

- What features of each song does it consider
- What information about the user does it use
- How does it turn those into a number

Try to avoid code in this section, treat it like an explanation to a non programmer.

The scoring logic is a multi angle mechanism looking at categorical matching as well as audio feature similarity.
More specifically 

Total Score = (0.4 × genre_match) + (0.3 × mood_match) + 
              (0.2 × energy_similarity) + (0.15 × tempo_similarity) + 
              (0.15 × valence_similarity) + (0.1 × danceability_similarity) + 
              (0.1 × acousticness_similarity)

I think this system is weighing too much on audio attributes and not enough on user to user taste.

---

## 4. Data

**Catalog Size:** The dataset contains **20 songs** from `data/songs.csv`. No songs were added or removed—this is the original starter dataset.

**Genres Represented:** pop, lofi, rock, ambient, jazz, synthwave, indie pop, folk, hip-hop, classical, country, electronic, reggae, blues, metal (15 unique genres total).

**Moods Included:** happy, chill, intense, moody, focused, energetic, relaxed, nostalgic, upbeat, adventurous, sad, melancholic, romantic (13 unique moods total).

**Audio Features:** Each song includes energy, tempo (BPM), valence (positivity), danceability, and acousticness on normalized scales (0–1).

**Whose Taste This Reflects:** The dataset skews toward Western pop, indie, and electronic music with a contemporary vibe. It reflects a taste profile that enjoys both high-energy party tracks (Gym Hero, Urban Pulse) and low-energy focus music (lofi, ambient). Moods range from energetic to melancholic, suggesting diversity, but the catalog underrepresents some genres (only 1 country song, 2 electronic) and emotional states (no explicit anger, confusion, or ecstasy). Overall, this feels like a curated "study and chill" playlist balanced with upbeat alternatives—leaning toward younger, Western audiences familiar with Spotify/music streaming culture.

---

## 5. Strengths

✓ **Clear, non-conflicting preferences:** When users have aligned preferences (e.g., "I like happy pop with high energy"), the system produces intuitive recommendations. The High-Energy Pop profile correctly ranked **Sunrise City** as the top pick with a strong genre + mood match.

✓ **Strong genre signal:** Genre matching creates a powerful +1.0 bonus that surfaces highly relevant results. The Anti-Acoustic Rocker profile immediately surfaced **Steel Thunder** (metal genre match) as the top recommendation, demonstrating the strength of categorical matching.

✓ **Graceful degradation:** When users request non-existent genres (e.g., "experimental"), the system doesn't crash—it falls back to mood and energy matching. The Mystery Genre profile still produced sensible recommendations like **Focus Flow** for the "focused" mood.

✓ **Handles extremes well:** Extreme preference scenarios (energy 0.1 ultra-chill or 1.0 max-intensity) are handled consistently and logically. The Extreme Chill profile correctly preferred ambient and acoustic tracks; Extreme Energy preferred high-tempo electric songs.

✓ **Transparency:** Every recommendation includes a plain-language explanation ("matches your favorite genre", "energy is close to your target"), making the reasoning inspectable and trustworthy.

---

## 6. Limitations and Bias

✗ **Genre match dominates:** A single +1.0 genre bonus can outweigh all other signals. The "Conflicting: Energetic Sadness" profile (high energy 0.9 but sad mood) recommended **Desert Dreams** (energy 0.55) simply because it's in the country genre—energy target was compromised.

✗ **Mood has no penalty:** Unlike genre mismatches, mood mismatches don't reduce scores. A very wrong mood is treated identically to a neutral mood, making the recommendation less precise for mood-sensitive users.

✗ **Acousticness preference is weak:** Acousticness scoring (0–0.75 range) is easily overridden by genre/mood/energy signals worth ±1.0. The "Acoustic Paradox" profile got an electric Sunrise City instead of acoustic alternatives.

✗ **Limited feature coverage:** The system ignores lyrical themes, artist novelty, listening context (time of day, activity), and user history. All recommendations are stateless and contextless.

✗ **Catalog bias:** With only 20 songs, some genres are barely represented (country: 1 song, electronic: 2 songs). This creates artificial preference amplification for well-represented genres.

✗ **No diversity enforcement:** Top 5 recommendations can cluster around very similar songs with no penalty for sameness. A user could get 5 high-energy pop songs when they might benefit from variety.

✗ **Treats all users identically:** There's no learning or personalization. Two users with the same stated preferences get identical results, even if their underlying tastes diverge after a few recommendations.

---

## 7. Evaluation

**Testing Approach:** I created a comprehensive test suite (`test_adversarial_profiles.py`) with 11 distinct user profiles spanning standard cases and adversarial edge cases. Each profile was run through the recommender, and I evaluated whether the top recommendation matched intuitive expectations.

**Profiles Tested:**
- **Standard cases** (3): High-Energy Pop, Chill Lofi, Deep Intense Rock
- **Adversarial cases** (8): Conflicting Sadness, Acoustic Paradox, Moody Acoustic Lover, Anti-Acoustic Rocker, Neutral Fence-Sitter, Mystery Genre (non-existent), Extreme Chill (0.1), Extreme Energy (1.0)

**What I Looked For:**
- Did the top-ranked song match the user's primary preference?
- Were conflicting signals handled gracefully or did one preference blindside others?
- Did the recommendations degrade gracefully for edge cases?
- Were scores calculated consistently?

**Key Validation Checks:**
- Spot-checked score calculations to verify genre/mood bonuses and energy proximity formulas
- Verified that non-existent genres didn't crash the system and fell back to mood/energy matching
- Confirmed that extreme energy values (0.1, 1.0) produced sensible results
- Tested all 11 profiles and verified results matched my intuitions for standard cases and exposed weaknesses for adversarial cases

**Results:** Standard profiles produced expected results; adversarial profiles revealed that genre dominance, mood insensitivity, and weak acousticness preference are the system's key limitations.

---

## 8. Future Work

**Short-term improvements:**
- **Conflict resolution:** Detect when user preferences contradict (e.g., high energy + sad mood) and either warn the user or intelligently compromise with a hybrid strategy.
- **Weighted preferences:** Allow users to specify importance weights ("energy matters 2x more than genre to me") so scoring adapts to individual priority hierarchies.
- **Diversity enforcement:** After ranking by score, re-rank to ensure top-5 span different genres/moods instead of clustering around the single best match.
- **Mood penalty system:** Penalize mood mismatches (not just fail to add bonus) to make mood-sensitive matching more precise.

**Medium-term improvements:**
- **Collaborative filtering:** Track what songs similar users liked and recommend based on user clusters ("Users like you also enjoyed...").
- **Temporal context:** Adapt recommendations based on time of day, user listening history, or seasonal patterns (morning upbeat, evening chill).
- **Expanded features:** Add instrumentation (acoustic guitar, synth, strings), lyrical themes, artist novelty/popularity, and valence (positivity) as first-class features.
- **Cold-start handling:** For new users, guide preference elicitation with a questionnaire ("Rate your acoustic preference 1-10").

**Long-term research:**
- **Serendipity vs. precision:** Balance giving users exactly what they ask for vs. surprising them with undiscovered artists/genres they'll love.
- **Fairness audits:** Measure whether the system recommends underrepresented artists/genres fairly or amplifies majority bias.
- **Interactive refinement:** Let users rate recommendations in real-time to dynamically re-rank remaining songs without retraining.

---

## 9. Personal Reflection

Building VibeScorer taught me that recommender systems are far more nuanced than I initially realized. What appears to users as a simple "ranked list of songs" hides dozens of interconnected decisions: how to weight conflicting signals, whether genre should dominate mood, how to handle edge cases gracefully, and what to do when user preferences contradict themselves. The most surprising discovery was how much the scoring *weights* matter—a small shift in how much genre matching is worth relative to energy similarity completely reshapes what gets recommended. This realization deepened my appreciation for Spotify's engineering: their recommender doesn't just serve what you explicitly asked for, but strategically balances satisfying your current taste with introducing you to artists and moods you haven't discovered yet. That balance between precision and serendipity—between "giving the user what they want" and "surprising them with something great"—is the real art of recommendation systems.