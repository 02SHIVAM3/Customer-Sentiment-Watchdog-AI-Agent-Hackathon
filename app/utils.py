from collections import Counter
from typing import List, Tuple

def summarize_negatives(results: List[Tuple[str,str,str]]):
    # results: [(message, sentiment, emotion)]
    negs = [r for r in results if r[1].upper().startswith("NEG")]
    total = len(results) or 1
    frac = len(negs)/total
    emotion_counts = Counter([r[2] for r in negs]) if negs else Counter()
    top_emotion = emotion_counts.most_common(1)[0][0] if emotion_counts else "N/A"
    return {
        "total": total,
        "negatives": len(negs),
        "negative_ratio": frac,
        "top_emotion": top_emotion,
        "emotion_counts": dict(emotion_counts)
    }
