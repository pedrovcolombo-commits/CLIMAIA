"""
CLIMAIA – Event Comparison Engine
Computes comparative metrics between raw and treated extreme event masks.

Now counts DISTINCT EVENT EPISODES (consecutive extreme runs) rather than
individual extreme data points, which fixes the inflated event count problem.
"""

import pandas as pd
import numpy as np
from src.statistical.extreme_detection import count_event_episodes, label_event_episodes


def compare_event_masks(raw_mask: pd.Series, treated_mask: pd.Series,
                        min_gap: int = 1, min_duration: int = 1) -> dict:
    """
    Compare two boolean event masks to calculate overlap, creation, and
    suppression rates — counting DISTINCT EPISODES, not individual data points.
    
    An "episode" is a consecutive run of True values. For example, if a heat
    wave spans 72 consecutive hourly readings, that's 1 episode, not 72.

    Parameters:
        raw_mask: Boolean Series for raw data events.
        treated_mask: Boolean Series for treated data events.
        min_gap: Minimum gap (False values) to separate episodes.
        min_duration: Minimum duration (points) for an episode to count.
        
    Returns:
        A dictionary containing:
            total_raw: Total extreme DATA POINTS in raw (for reference)
            total_treated: Total extreme DATA POINTS in treated (for reference)
            total_raw_episodes: Distinct event episodes in raw data
            total_treated_episodes: Distinct event episodes in treated data
            coincident: Overlapping episodes between raw and treated
            created: Events that exist in treated but NOT in raw
            suppressed: Events that exist in raw but NOT in treated
            agreement_pct: Overlap agreement percentage
    """
    # Convert to boolean numpy arrays, handling type issues
    try:
        r_vals = np.asarray(raw_mask, dtype=bool)
        t_vals = np.asarray(treated_mask, dtype=bool)
    except (ValueError, TypeError):
        r_vals = np.asarray(raw_mask.fillna(False), dtype=bool)
        t_vals = np.asarray(treated_mask.fillna(False), dtype=bool)
    
    # Align to same length if different
    if len(r_vals) != len(t_vals):
        min_len = min(len(r_vals), len(t_vals))
        r_vals = r_vals[:min_len]
        t_vals = t_vals[:min_len]

    # Count raw data points (for reference info)
    total_raw_points = int(np.sum(r_vals))
    total_treated_points = int(np.sum(t_vals))

    # Count EPISODES (distinct consecutive runs of True)
    r_series = pd.Series(r_vals)
    t_series = pd.Series(t_vals)

    raw_episodes = count_event_episodes(r_series, min_gap=min_gap, min_duration=min_duration)
    treated_episodes = count_event_episodes(t_series, min_gap=min_gap, min_duration=min_duration)

    # The user requested a simplified definition:
    # Created is when treated > raw. Suppressed is when raw > treated.
    diff = treated_episodes - raw_episodes
    n_created = diff if diff > 0 else 0
    n_suppressed = -diff if diff < 0 else 0
    n_coincident = min(raw_episodes, treated_episodes)

    # Agreement percentage based on episodes
    union = raw_episodes + n_created  # total unique episodes across both
    agreement_pct = (n_coincident / union * 100.0) if union > 0 else 100.0

    return {
        "total_raw": total_raw_points,
        "total_treated": total_treated_points,
        "total_raw_episodes": raw_episodes,
        "total_treated_episodes": treated_episodes,
        "coincident": n_coincident,
        "created": n_created,
        "suppressed": n_suppressed,
        "agreement_pct": agreement_pct,
    }
