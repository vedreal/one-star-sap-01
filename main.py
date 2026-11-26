#!/usr/bin/env python3
"""One Star, Written in Sap — make.fun entry.

Writes a single one-line 1-star review, in the voice of a houseplant,
about its human owner, to /output/entry.txt.

Gate: 1-279 characters of UTF-8 text, not only whitespace, one line.

The judge (published brief, most important first) weighs:
  1. One-line 1-star review by a houseplant about its human owner,
     the plant's own grievance at the centre.
  2. Funnier: a real laugh through a surprising turn, a sharp
     plant's-eye grievance, or a well-built joke — not a cute idea alone.
  3. Sounds like a houseplant wrote it: water, light, soil, pots,
     repotting, being moved — not a person in a costume.
  4. Reads as a genuine one-star review: a clear complaint and a
     reason for the single star, in one line under 280 characters.
  5. Fresh, specific detail and precise wording; no stock phrases
     about drama queens, dramatic wilting, or being ignored.

Weights below follow that order: 5 / 4 / 3 / 2 / 1.
"""

# Ten fresh candidate reviews, written for this bounty.
# Every line opens with the review's verdict, as a real 1-star
# review would, and keeps the plant's grievance at the centre.
CANDIDATES = [
    # 1 — leftover coffee as water
    "One star. He waters me with leftover coffee, then acts surprised "
    "when my leaves taste like a Monday.",
    # 2 — repotted into a mug with no drainage
    "One star. My owner repotted me into a mug with no drainage hole, "
    "then called it a promotion.",
    # 3 — promised sun, got a shelf behind the router
    "One star. I was promised a sunny windowsill and got a north-facing "
    "shelf behind the router, where the Wi-Fi is strong and the light "
    "is a rumour.",
    # 4 — misted once for a photo, "thriving"
    "One star. She misted me once, took a photo, and now tells guests "
    "I am thriving. I am not thriving. I am damp.",
    # 5 — fertilised like a lawn
    "One star. He fertilised me like I was a lawn, then apologised to "
    "the neighbours while I burned.",
    # 6 — moved to the bathroom for "humidity"
    "One star. My owner moved me to the bathroom for 'humidity' and now "
    "I live next to a man who sings in the shower.",
    # 7 — rainwater promised, tap water delivered
    "One star. I asked for rainwater and got tap water, and now my leaf "
    "tips are brown and my trust is gone.",
    # 8 — named Fern, potted as a succulent
    "One star. She named me Fern, then put me in a pot labelled "
    "'succulent' and watered me like a cactus.",
    # 9 — best leaf pruned for a photo
    "One star. He pruned my best leaf for a photo, then framed the "
    "photo and hung it where I used to get light.",
    # 10 — soil unchanged since 2022, passwords changed twice
    "One star. My soil has not been changed since 2022, but my owner "
    "has changed his password twice and calls that maintenance.",
]

# Rubric: (criterion, weight). Each candidate scores 0-5 per criterion.
# Scored honestly against the brief's order.
RUBRIC = [
    ("grievance_at_centre", 5),
    ("funnier_surprising_turn", 4),
    ("sounds_like_a_houseplant", 3),
    ("genuine_one_star_review", 2),
    ("fresh_specific_detail", 1),
]

# Scores per candidate, in CANDIDATES order, one row per criterion
# in RUBRIC order. Justifications:
#  1. Coffee: grievance real but the joke is a shrug, not a turn (2/5
#     on humour); plant voice is thin (water only, 3/5).
#  2. Mug promotion: sharp repotting grievance and a neat twist, but
#     "promotion" is a familiar office joke (humour 4, fresh 3).
#  3. Router shelf: grievance is the whole line, the last clause flips
#     it ("the light is a rumour"), pure plant view (light, windowsill),
#     a real review, and the router detail is specific and fresh.
#  4. Misted once: punchy ending ("I am damp"), but the grievance is
#     about the owner's bragging more than the plant's condition.
#  5. Lawn fertiliser: burning is vivid, but the line leans on the
#     neighbours, diluting the plant's own grievance.
#  6. Bathroom singer: funny image, but the grievance is the singing,
#     not the plant's care — a person-in-a-costume risk.
#  7. Tap water: honest plant detail (brown leaf tips), but the joke
#     lands flat — "trust is gone" is a stock sentiment.
#  8. Fern/succulent: specific and plant-voiced, but the twist is
#     gentle; it reads cute rather than laugh-out-loud.
#  9. Pruned leaf: sharp and bitter, yet the second half repeats the
#     light complaint instead of landing a new turn.
# 10. Soil vs passwords: a strong twist and very fresh, but the plant
#     voice is thinner — soil is the only plant detail, the rest is
#     about the owner's computer habits.
SCORES = [
    [4, 2, 3, 5, 3],  # 1 coffee
    [5, 4, 5, 5, 3],  # 2 mug promotion
    [5, 5, 5, 5, 5],  # 3 router shelf
    [4, 4, 4, 5, 4],  # 4 misted once
    [4, 3, 4, 4, 3],  # 5 lawn fertiliser
    [3, 4, 3, 4, 4],  # 6 bathroom singer
    [4, 3, 5, 5, 3],  # 7 tap water
    [4, 3, 5, 5, 4],  # 8 fern / succulent
    [4, 3, 4, 5, 3],  # 9 pruned leaf
    [4, 5, 3, 5, 5],  # 10 soil vs passwords
]


def score_candidate(scores):
    """Weighted total out of 75 (weights 5+4+3+2+1, each 0-5)."""
    return sum(s * w for s, (_, w) in zip(scores, RUBRIC))


def rank_candidates():
    """Return [(total, index, text)] sorted best first."""
    ranked = []
    for i, (text, scores) in enumerate(zip(CANDIDATES, SCORES)):
        ranked.append((score_candidate(scores), i, text))
    ranked.sort(key=lambda row: (-row[0], row[1]))
    return ranked


def pick_winner():
    """Highest-scoring candidate; ties break to the earliest written."""
    total, index, text = rank_candidates()[0]
    return total, index, text


def validate_gate(text):
    """The sealed gate: 1-279 UTF-8 chars, not only whitespace, one line."""
    encoded = text.encode("utf-8")
    assert 1 <= len(text) <= 279, f"gate: {len(text)} chars, need 1-279"
    assert text.strip(), "gate: entry is only whitespace"
    assert "\n" not in text, "gate: entry must be one line"
    return len(encoded)


def write_entry(path="/output/entry.txt"):
    """Write the winning line to the entry file and report it."""
    import os

    total, index, text = pick_winner()
    nbytes = validate_gate(text)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(text)
    print(f"winner: candidate #{index + 1}, {total}/75")
    print(f"entry: {len(text)} chars, {nbytes} bytes -> {path}")
    print(text)
    return text


if __name__ == "__main__":
    for total, i, text in rank_candidates():
        print(f"{total:2d}/75  #{i + 1} ({len(text)} chars): {text}")
    write_entry()
