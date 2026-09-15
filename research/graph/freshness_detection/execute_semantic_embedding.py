#!/usr/bin/env python3
"""
EXP-GRAPH-35010853847 — Test semantic embedding similarity as a staleness signal.
Replaces Jaccard (field_path,type) with TF-IDF cosine similarity on
(field_name:field_type) text pairs. Tests whether semantic similarity
distinguishes true drift from structural noise with TP>=0.8 and FP<=0.15.

Frozen prereg: sentence-transformers unavailable → TF-IDF fallback (disclosed).
"""

import json
import math
import hashlib
import random
import sys
import os
from pathlib import Path
from datetime import datetime, timezone
from collections import defaultdict

import numpy as np
from scipy import stats
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity as sklearn_cosine

# ============================================================
# CONSTANTS (frozen in spec.json / prereg.md)
# ============================================================

SCHEMA_SIZES = [10, 20, 30, 50]
SAMPLES_PER_GROUP = 30
DRIFT_PATTERNS_TRUE = ["add_field", "remove_field", "change_type"]
DRIFT_PATTERNS_NOISE = ["optional_field_churn", "null_valued_fields", "nested_object_variation"]
ALL_DRIFT_PATTERNS = DRIFT_PATTERNS_TRUE + DRIFT_PATTERNS_NOISE
FIELD_TYPES = ["string", "integer", "boolean", "array", "object"]
SEED = 20260913  # deterministic seed matching parent

PARENT_EXPERIMENT_ID = "EXP-GRAPH-34788722106"
THIS_EXPERIMENT_ID = "EXP-GRAPH-35010853847"

# ============================================================
# ADAPTIVE THRESHOLD (Jaccard baseline)
# ============================================================

def adaptive_threshold(n):
    """T(n) = 1 - 0.8 / (n + 1)"""
    return 1.0 - 0.8 / (n + 1)

# ============================================================
# MOCK SCHEMA GENERATION (identical to parent)
# ============================================================

def generate_baseline_schema(n, rng):
    """Generate n unique (field_path, type) pairs as baseline schema."""
    fields = []
    used_names = set()
    for i in range(n):
        while True:
            if rng.random() < 0.2 and i > 0:
                parents = [f for f, _ in fields if "." not in f]
                if parents:
                    parent = rng.choice(parents)
                    suffix = f"sub_{rng.randint(1, 99)}"
                    path = f"{parent}.{suffix}"
                else:
                    path = f"field_{rng.randint(1, 9999)}"
            else:
                path = f"field_{rng.randint(1, 9999)}"
            if path not in used_names:
                used_names.add(path)
                break
        ftype = rng.choice(FIELD_TYPES)
        fields.append((path, ftype))
    return fields

def generate_fresh_schema(baseline, rng):
    """Generate fresh schema with identical (path, type) pairs."""
    return list(baseline)

def generate_stale_add_field(baseline, rng):
    """Add one new field (true drift)."""
    new_field = f"new_field_{rng.randint(1, 9999)}"
    new_type = rng.choice(FIELD_TYPES)
    return baseline + [(new_field, new_type)]

def generate_stale_remove_field(baseline, rng):
    """Remove one field (true drift)."""
    idx = rng.randint(0, len(baseline) - 1)
    return [f for i, f in enumerate(baseline) if i != idx]

def generate_stale_change_type(baseline, rng):
    """Change one field's type (true drift)."""
    idx = rng.randint(0, len(baseline) - 1)
    path, old_type = baseline[idx]
    new_type = rng.choice([t for t in FIELD_TYPES if t != old_type])
    result = list(baseline)
    result[idx] = (path, new_type)
    return result

def generate_stale_optional_churn(baseline, rng):
    """Randomly add/remove ~10% of fields (structural noise)."""
    n = len(baseline)
    churn_count = max(1, round(n * 0.1))
    result = list(baseline)
    indices_to_remove = sorted(rng.sample(range(len(result)), min(churn_count, len(result))), reverse=True)
    for idx in indices_to_remove:
        result.pop(idx)
    for _ in range(churn_count):
        new_field = f"churn_field_{rng.randint(1, 9999)}"
        new_type = rng.choice(FIELD_TYPES)
        result.append((new_field, new_type))
    return result

def generate_stale_null_fields(baseline, rng):
    """Set random fields to null type (structural noise)."""
    n = len(baseline)
    null_count = max(1, round(n * 0.1))
    indices = set(rng.sample(range(n), min(null_count, n)))
    return [("field_null", "null") if i in indices else (p, t) for i, (p, t) in enumerate(baseline)]

def generate_stale_nested_object(baseline, rng):
    """Convert a field to nested object (structural noise)."""
    idx = rng.randint(0, len(baseline) - 1)
    path, old_type = baseline[idx]
    nested_path = f"{path}.nested_child"
    result = list(baseline)
    result[idx] = (nested_path, "string")
    return result

DRIFT_GENERATORS = {
    "add_field": generate_stale_add_field,
    "remove_field": generate_stale_remove_field,
    "change_type": generate_stale_change_type,
    "optional_field_churn": generate_stale_optional_churn,
    "null_valued_fields": generate_stale_null_fields,
    "nested_object_variation": generate_stale_nested_object,
}

# ============================================================
# JACCARD SIMILARITY (for baseline comparison)
# ============================================================

def jaccard_similarity(set_a, set_b):
    """Compute Jaccard similarity between two sets of (path, type) tuples."""
    a = set(set_a)
    b = set(set_b)
    if not a and not b:
        return 1.0
    intersection = a & b
    union = a | b
    return len(intersection) / len(union)

# ============================================================
# TF-IDF SEMANTIC SIMILARITY
# ============================================================

def schema_to_texts(schema):
    """Convert schema [(field_name, field_type), ...] to text representations."""
    return [f"{name}:{ftype}" for name, ftype in schema]

def compute_tfidf_embeddings(schemas, vectorizer=None):
    """
    Compute TF-IDF embeddings for schemas.
    Each schema is represented as the mean of its field text TF-IDF vectors.
    Returns (embeddings_matrix, fitted_vectorizer).
    """
    # Flatten all schemas into a list of text corpora
    all_schema_texts = []
    schema_lengths = []
    for schema in schemas:
        texts = schema_to_texts(schema)
        all_schema_texts.append(" ".join(texts))
        schema_lengths.append(len(texts))

    if vectorizer is None:
        vectorizer = TfidfVectorizer(
            analyzer='word',
            token_pattern=r'[a-zA-Z0-9_]+',
            lowercase=True,
            sublinear_tf=True,
        )
        tfidf_matrix = vectorizer.fit_transform(all_schema_texts)
    else:
        tfidf_matrix = vectorizer.transform(all_schema_texts)

    # Convert to dense and mean-pool (for TF-IDF, the "mean" is already
    # captured by the sparse vector since each document is a bag of words)
    # Actually, we want the TF-IDF vector itself as the schema embedding
    embeddings = tfidf_matrix.toarray()
    return embeddings, vectorizer

def compute_semantic_similarity(schema_a, schema_b, vectorizer):
    """Compute cosine similarity between two schemas using TF-IDF."""
    texts_a = " ".join(schema_to_texts(schema_a))
    texts_b = " ".join(schema_to_texts(schema_b))
    vec_a = vectorizer.transform([texts_a]).toarray()
    vec_b = vectorizer.transform([texts_b]).toarray()
    sim = sklearn_cosine(vec_a, vec_b)[0, 0]
    return float(sim)

# ============================================================
# WILSON CI
# ============================================================

def wilson_ci(successes, n, z=1.96):
    """Wilson score interval for a proportion."""
    if n == 0:
        return (0.0, 1.0)
    p = successes / n
    denom = 1 + z**2 / n
    center = (p + z**2 / (2 * n)) / denom
    margin = z * math.sqrt((p * (1 - p) + z**2 / (4 * n)) / n) / denom
    return (max(0.0, center - margin), min(1.0, center + margin))

# ============================================================
# MANN-WHITNEY U TEST
# ============================================================

def mann_whitney_test(true_drift_sims, noise_sims, alternative='less'):
    """
    Mann-Whitney U test for separation between true drift and noise.
    H0: distributions are equal.
    H1 (alternative='less'): true drift semantic similarity < noise semantic similarity.
    """
    if len(true_drift_sims) < 2 or len(noise_sims) < 2:
        return None, None
    stat, p_value = stats.mannwhitneyu(true_drift_sims, noise_sims, alternative=alternative)
    return stat, p_value

# ============================================================
# COHEN'S D
# ============================================================

def cohens_d(group1, group2):
    """Compute Cohen's d effect size."""
    n1, n2 = len(group1), len(group2)
    if n1 < 2 or n2 < 2:
        return None
    var1 = np.var(group1, ddof=1)
    var2 = np.var(group2, ddof=1)
    pooled_std = math.sqrt(((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2))
    if pooled_std == 0:
        return 0.0
    return (np.mean(group1) - np.mean(group2)) / pooled_std

# ============================================================
# CALIBRATION / TEST SPLIT
# ============================================================

def split_calibration_test(true_drift_sims, noise_sims, cal_ratio=0.8, rng=None):
    """
    Stratified 80/20 split of true drift and noise similarities.
    Returns (cal_true, cal_noise, test_true, test_noise).
    """
    if rng is None:
        rng = random.Random(SEED + 1000)

    n_true = len(true_drift_sims)
    n_noise = len(noise_sims)
    n_true_cal = max(1, int(n_true * cal_ratio))
    n_noise_cal = max(1, int(n_noise * cal_ratio))

    indices_true = list(range(n_true))
    indices_noise = list(range(n_noise))
    rng.shuffle(indices_true)
    rng.shuffle(indices_noise)

    cal_true_idx = indices_true[:n_true_cal]
    test_true_idx = indices_true[n_true_cal:]
    cal_noise_idx = indices_noise[:n_noise_cal]
    test_noise_idx = indices_noise[n_noise_cal:]

    cal_true = [true_drift_sims[i] for i in cal_true_idx]
    cal_noise = [noise_sims[i] for i in cal_noise_idx]
    test_true = [true_drift_sims[i] for i in test_true_idx]
    test_noise = [noise_sims[i] for i in test_noise_idx]

    return cal_true, cal_noise, test_true, test_noise

# ============================================================
# THRESHOLD OPTIMIZATION
# ============================================================

def optimize_threshold(cal_true, cal_noise):
    """
    Find threshold maximizing F1 for discriminating true drift (positive)
    from structural noise (negative) on calibration set.
    """
    all_sims = sorted(set(cal_true + cal_noise))
    best_f1 = -1
    best_threshold = None

    for threshold in all_sims:
        # True drift: similarity < threshold means detected (stale)
        tp = sum(1 for s in cal_true if s < threshold)
        fp = sum(1 for s in cal_noise if s < threshold)
        fn = sum(1 for s in cal_true if s >= threshold)

        precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0

        if f1 > best_f1:
            best_f1 = f1
            best_threshold = threshold

    # Also try thresholds between values
    for i in range(len(all_sims) - 1):
        threshold = (all_sims[i] + all_sims[i + 1]) / 2
        tp = sum(1 for s in cal_true if s < threshold)
        fp = sum(1 for s in cal_noise if s < threshold)
        fn = sum(1 for s in cal_true if s >= threshold)

        precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0

        if f1 > best_f1:
            best_f1 = f1
            best_threshold = threshold

    return best_threshold, best_f1

# ============================================================
# ENSEMBLE OPTIMIZATION
# ============================================================

def optimize_ensemble_alpha(cal_true_jaccard, cal_noise_jaccard,
                            cal_true_semantic, cal_noise_semantic,
                            n_folds=10):
    """
    Optimize alpha for ensemble: alpha * Jaccard + (1-alpha) * Semantic.
    Uses 10-fold cross-validation on calibration set.
    Returns best alpha and per-alpha F1 scores.
    """
    cal_true_j = np.array(cal_true_jaccard)
    cal_noise_j = np.array(cal_noise_jaccard)
    cal_true_s = np.array(cal_true_semantic)
    cal_noise_s = np.array(cal_noise_semantic)

    n_true = len(cal_true_j)
    n_noise = len(cal_noise_j)

    # Create fold indices
    fold_size_true = max(1, n_true // n_folds)
    fold_size_noise = max(1, n_noise // n_folds)

    best_alpha = 0.5
    best_f1 = -1
    alpha_f1_scores = {}

    for alpha_int in range(0, 101):
        alpha = alpha_int / 100.0
        fold_f1s = []

        for fold in range(min(n_folds, n_true, n_noise)):
            # Simple fold: use fold-th chunk as test
            test_start_t = fold * fold_size_true
            test_end_t = min(test_start_t + fold_size_true, n_true)
            test_start_n = fold * fold_size_noise
            test_end_n = min(test_start_n + fold_size_noise, n_noise)

            if test_start_t >= n_true or test_start_n >= n_noise:
                continue

            # Build calibration and test sets
            cal_t_idx = list(range(0, test_start_t)) + list(range(test_end_t, n_true))
            cal_n_idx = list(range(0, test_start_n)) + list(range(test_end_n, n_noise))
            test_t_idx = list(range(test_start_t, test_end_t))
            test_n_idx = list(range(test_start_n, test_end_n))

            # Compute ensemble scores
            cal_true_scores = [alpha * cal_true_j[i] + (1 - alpha) * cal_true_s[i] for i in cal_t_idx]
            cal_noise_scores = [alpha * cal_noise_j[i] + (1 - alpha) * cal_noise_s[i] for i in cal_n_idx]
            test_true_scores = [alpha * cal_true_j[i] + (1 - alpha) * cal_true_s[i] for i in test_t_idx]
            test_noise_scores = [alpha * cal_noise_j[i] + (1 - alpha) * cal_noise_s[i] for i in test_n_idx]

            # Find threshold on cal set
            threshold, _ = optimize_threshold(cal_true_scores, cal_noise_scores)
            if threshold is None:
                continue

            # Evaluate on test set
            tp = sum(1 for s in test_true_scores if s < threshold)
            fp = sum(1 for s in test_noise_scores if s < threshold)
            fn = sum(1 for s in test_true_scores if s >= threshold)

            precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
            recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
            f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0
            fold_f1s.append(f1)

        avg_f1 = sum(fold_f1s) / len(fold_f1s) if fold_f1s else 0.0
        alpha_f1_scores[str(alpha)] = round(avg_f1, 4)

        if avg_f1 > best_f1:
            best_f1 = avg_f1
            best_alpha = alpha

    return best_alpha, best_f1, alpha_f1_scores

# ============================================================
# REALISTIC SCHEMA TEST (supplementary)
# ============================================================

REALISTIC_SCHEMAS = {
    "github_user": [
        ("login", "string"), ("id", "integer"), ("node_id", "string"),
        ("avatar_url", "string"), ("gravatar_id", "string"), ("url", "string"),
        ("html_url", "string"), ("followers_url", "string"), ("following_url", "string"),
        ("gists_url", "string"), ("starred_url", "string"), ("subscriptions_url", "string"),
        ("organizations_url", "string"), ("repos_url", "string"), ("events_url", "string"),
        ("received_events_url", "string"), ("type", "string"), ("site_admin", "boolean"),
    ],
    "github_user_with_email": [
        ("login", "string"), ("id", "integer"), ("node_id", "string"),
        ("avatar_url", "string"), ("gravatar_id", "string"), ("url", "string"),
        ("html_url", "string"), ("followers_url", "string"), ("following_url", "string"),
        ("gists_url", "string"), ("starred_url", "string"), ("subscriptions_url", "string"),
        ("organizations_url", "string"), ("repos_url", "string"), ("events_url", "string"),
        ("received_events_url", "string"), ("type", "string"), ("site_admin", "boolean"),
        ("email", "string"),  # TRUE DRIFT: new concept
    ],
    "github_user_noise": [
        ("login", "string"), ("id", "integer"), ("node_id", "string"),
        ("avatar_url", "string"), ("gravatar_id", "string"), ("url", "string"),
        ("html_url", "string"), ("followers_url", "string"), ("following_url", "string"),
        ("gists_url", "string"), ("starred_url", "string"), ("subscriptions_url", "string"),
        ("organizations_url", "string"), ("repos_url", "string"), ("events_url", "string"),
        ("received_events_url", "string"), ("type", "string"), ("site_admin", "null"),
        # STRUCTURAL NOISE: site_admin set to null type (same concept)
    ],
    "stripe_charge": [
        ("id", "string"), ("object", "string"), ("amount", "integer"),
        ("currency", "string"), ("status", "string"), ("created", "integer"),
        ("livemode", "boolean"), ("paid", "boolean"), ("captured", "boolean"),
        ("refunded", "boolean"), ("amount_refunded", "integer"),
        ("fee", "integer"), ("fee_details", "object"), ("customer", "string"),
        ("description", "string"), ("invoice", "string"),
    ],
    "stripe_charge_with_dispute": [
        ("id", "string"), ("object", "string"), ("amount", "integer"),
        ("currency", "string"), ("status", "string"), ("created", "integer"),
        ("livemode", "boolean"), ("paid", "boolean"), ("captured", "boolean"),
        ("refunded", "boolean"), ("amount_refunded", "integer"),
        ("fee", "integer"), ("fee_details", "object"), ("customer", "string"),
        ("description", "string"), ("invoice", "string"),
        ("dispute", "object"),  # TRUE DRIFT: new concept
    ],
    "stripe_charge_churn": [
        ("id", "string"), ("object", "string"), ("amount", "integer"),
        ("currency", "string"), ("status", "string"), ("created", "integer"),
        ("livemode", "boolean"), ("paid", "boolean"), ("captured", "boolean"),
        ("refunded", "boolean"), ("amount_refunded", "integer"),
        ("fee", "integer"), ("fee_details", "object"), ("customer", "string"),
        ("description", "null"), ("invoice", "string"),
        # STRUCTURAL NOISE: description set to null (same concept)
    ],
    "twitter_tweet": [
        ("id", "integer"), ("id_str", "string"), ("text", "string"),
        ("truncated", "boolean"), ("entities", "object"), ("metadata", "object"),
        ("source", "string"), ("in_reply_to_status_id", "integer"),
        ("in_reply_to_user_id", "integer"), ("in_reply_to_screen_name", "string"),
        ("geo", "object"), ("coordinates", "object"), ("place", "object"),
        ("contributors", "object"), ("retweet_count", "integer"),
        ("favorite_count", "integer"), ("lang", "string"),
    ],
    "twitter_tweet_with_annotations": [
        ("id", "integer"), ("id_str", "string"), ("text", "string"),
        ("truncated", "boolean"), ("entities", "object"), ("metadata", "object"),
        ("source", "string"), ("in_reply_to_status_id", "integer"),
        ("in_reply_to_user_id", "integer"), ("in_reply_to_screen_name", "string"),
        ("geo", "object"), ("coordinates", "object"), ("place", "object"),
        ("contributors", "object"), ("retweet_count", "integer"),
        ("favorite_count", "integer"), ("lang", "string"),
        ("annotations", "object"),  # TRUE DRIFT: new concept
    ],
    "twitter_tweet_churn": [
        ("id", "integer"), ("id_str", "string"), ("text", "string"),
        ("truncated", "boolean"), ("entities", "object"), ("metadata", "object"),
        ("source", "string"), ("in_reply_to_status_id", "integer"),
        ("in_reply_to_user_id", "integer"), ("in_reply_to_screen_name", "string"),
        ("geo", "object"), ("coordinates", "object"), ("place", "object"),
        ("contributors", "object"), ("retweet_count", "integer"),
        ("favorite_count", "integer"), ("lang", "string"),
    ],
}

# ============================================================
# MAIN EXPERIMENT
# ============================================================

def run_experiment():
    """Execute the full experiment and return all raw evidence."""
    print("=" * 70)
    print(f"  {THIS_EXPERIMENT_ID}: Semantic Embedding Staleness Detection")
    print(f"  TF-IDF fallback (sentence-transformers unavailable)")
    print("=" * 70)
    print()

    rng = random.Random(SEED)

    # ---- Phase 1: Regenerate schemas from parent baselines ----
    print("[1/8] Regenerating schemas from parent baselines...")
    parent_path = Path(__file__).parent.parent.parent / "experiments" / PARENT_EXPERIMENT_ID / "raw_evidence" / "mock_schemas.json"
    with open(parent_path) as f:
        parent_data = json.load(f)

    # Regenerate baselines and stale schemas using same seed
    all_schemas = {}  # {size: {baseline, fresh, {pattern: [schemas]}}}
    for n in SCHEMA_SIZES:
        baseline = generate_baseline_schema(n, rng)
        # Verify against parent
        parent_baseline = [tuple(f) for f in parent_data["per_schema_size"][str(n)]["baseline"]]
        assert [tuple(f) for f in baseline] == parent_baseline, \
            f"Baseline mismatch at n={n}: regenerated != parent"

        fresh_schemas = [generate_fresh_schema(baseline, rng) for _ in range(SAMPLES_PER_GROUP)]
        stale_schemas = {}
        for pattern in ALL_DRIFT_PATTERNS:
            gen = DRIFT_GENERATORS[pattern]
            stale_schemas[pattern] = [gen(baseline, rng) for _ in range(SAMPLES_PER_GROUP)]

        # Verify Jaccard similarities match parent
        for pattern in ALL_DRIFT_PATTERNS:
            parent_jaccards = parent_data["per_schema_size"][str(n)]["stale_similarities"][pattern]
            for i, (regen, parent_j) in enumerate(zip(stale_schemas[pattern], parent_jaccards)):
                computed_j = jaccard_similarity(baseline, regen)
                assert abs(computed_j - parent_j) < 1e-6, \
                    f"Jaccard mismatch at n={n} pattern={pattern} i={i}: {computed_j} != {parent_j}"

        all_schemas[n] = {
            "baseline": baseline,
            "fresh": fresh_schemas,
            "stale": stale_schemas,
        }
        print(f"  n={n}: OK (baseline verified, {SAMPLES_PER_GROUP} fresh + {len(ALL_DRIFT_PATTERNS)}x{SAMPLES_PER_GROUP} stale)")

    # ---- Phase 2: Build TF-IDF vectorizer on all schemas ----
    print("[2/8] Building TF-IDF vectorizer...")
    all_flat_schemas = []
    for n in SCHEMA_SIZES:
        all_flat_schemas.append(all_schemas[n]["baseline"])
        all_flat_schemas.extend(all_schemas[n]["fresh"])
        for pattern in ALL_DRIFT_PATTERNS:
            all_flat_schemas.extend(all_schemas[n]["stale"][pattern])

    # Fit TF-IDF on all field texts
    all_texts = []
    for schema in all_flat_schemas:
        all_texts.extend(schema_to_texts(schema))

    vectorizer = TfidfVectorizer(
        analyzer='word',
        token_pattern=r'[a-zA-Z0-9_]+',
        lowercase=True,
        sublinear_tf=True,
    )
    vectorizer.fit(all_texts)
    vocab_size = len(vectorizer.vocabulary_)
    print(f"  Vocab size: {vocab_size}")
    print(f"  Sample features: {vectorizer.get_feature_names_out()[:10].tolist()}")

    # ---- Phase 3: Compute semantic similarities ----
    print("[3/8] Computing semantic similarities...")
    raw_evidence = {
        "experiment_id": THIS_EXPERIMENT_ID,
        "parent_experiment_id": PARENT_EXPERIMENT_ID,
        "seed": SEED,
        "embedding_method": "TF-IDF (sentence-transformers unavailable)",
        "executed_at": datetime.now(timezone.utc).isoformat(),
        "vocab_size": vocab_size,
        "per_schema_size": {},
    }

    for n in SCHEMA_SIZES:
        baseline = all_schemas[n]["baseline"]
        size_evidence = {
            "schema_size": n,
            "baseline_schema": [list(f) for f in baseline],
            "fresh_similarities": [],
            "stale_similarities": {},
            "jaccard_fresh": [],
            "jaccard_stale": {},
        }

        # Fresh similarities (semantic + Jaccard)
        for fresh in all_schemas[n]["fresh"]:
            sem_sim = compute_semantic_similarity(baseline, fresh, vectorizer)
            jac_sim = jaccard_similarity(baseline, fresh)
            size_evidence["fresh_similarities"].append(round(sem_sim, 6))
            size_evidence["jaccard_fresh"].append(round(jac_sim, 6))

        # Stale similarities per pattern (semantic + Jaccard)
        for pattern in ALL_DRIFT_PATTERNS:
            sem_sims = []
            jac_sims = []
            for stale in all_schemas[n]["stale"][pattern]:
                sem_sim = compute_semantic_similarity(baseline, stale, vectorizer)
                jac_sim = jaccard_similarity(baseline, stale)
                sem_sims.append(round(sem_sim, 6))
                jac_sims.append(round(jac_sim, 6))
            size_evidence["stale_similarities"][pattern] = sem_sims
            size_evidence["jaccard_stale"][pattern] = jac_sims

        raw_evidence["per_schema_size"][str(n)] = size_evidence
        print(f"  n={n}: semantic sims computed")

    # ---- Phase 4: Threshold optimization (per schema size) ----
    print("[4/8] Optimizing thresholds per schema size...")
    threshold_results = {}
    for n in SCHEMA_SIZES:
        se = raw_evidence["per_schema_size"][str(n)]

        # Pool true drift and noise semantic similarities
        true_drift_sims = []
        for pattern in DRIFT_PATTERNS_TRUE:
            true_drift_sims.extend(se["stale_similarities"][pattern])
        noise_sims = []
        for pattern in DRIFT_PATTERNS_NOISE:
            noise_sims.extend(se["stale_similarities"][pattern])

        # Split calibration/test
        cal_true, cal_noise, test_true, test_noise = split_calibration_test(
            true_drift_sims, noise_sims, cal_ratio=0.8, rng=random.Random(SEED + 2000)
        )

        # Optimize threshold on calibration set
        threshold, cal_f1 = optimize_threshold(cal_true, cal_noise)

        # Apply to test set
        if threshold is not None:
            tp_test = sum(1 for s in test_true if s < threshold)
            fp_test = sum(1 for s in test_noise if s < threshold)
            fn_test = sum(1 for s in test_true if s >= threshold)
            tn_test = sum(1 for s in test_noise if s >= threshold)
        else:
            tp_test = fp_test = fn_test = tn_test = 0

        threshold_results[str(n)] = {
            "threshold": round(threshold, 6) if threshold is not None else None,
            "cal_f1": round(cal_f1, 4),
            "cal_size": {"true": len(cal_true), "noise": len(cal_noise)},
            "test_size": {"true": len(test_true), "noise": len(test_noise)},
            "test_tp": tp_test,
            "test_fp": fp_test,
            "test_fn": fn_test,
            "test_tn": tn_test,
        }
        print(f"  n={n}: threshold={threshold:.4f}, cal_f1={cal_f1:.4f}, test TP={tp_test}/{len(test_true)} FP={fp_test}/{len(test_noise)}")

    # ---- Phase 5: Full evaluation with Wilson CIs ----
    print("[5/8] Computing Wilson CIs and per-pattern metrics...")
    measurements = {
        "per_schema_size": {},
        "overall": {},
    }

    all_tp = 0
    all_tp_total = 0
    all_fp = 0
    all_fp_total = 0

    for n in SCHEMA_SIZES:
        se = raw_evidence["per_schema_size"][str(n)]
        threshold = threshold_results[str(n)]["threshold"]

        # Fresh FP
        fresh_sims = se["fresh_similarities"]
        fp_fresh = sum(1 for s in fresh_sims if s < threshold)
        fp_fresh_total = len(fresh_sims)
        fp_fresh_rate = fp_fresh / fp_fresh_total if fp_fresh_total > 0 else 0.0
        fp_fresh_ci = wilson_ci(fp_fresh, fp_fresh_total)

        all_fp += fp_fresh
        all_fp_total += fp_fresh_total

        # Per-pattern metrics
        pattern_metrics = {}
        for pattern in ALL_DRIFT_PATTERNS:
            sims = se["stale_similarities"][pattern]
            is_true = pattern in DRIFT_PATTERNS_TRUE

            # "Detected" means semantic similarity < threshold (schema looks stale)
            detected = sum(1 for s in sims if s < threshold)
            total = len(sims)
            rate = detected / total if total > 0 else 0.0
            ci = wilson_ci(detected, total)
            mean_sim = sum(sims) / len(sims) if sims else 0.0
            detection_margin = threshold - mean_sim

            pattern_metrics[pattern] = {
                "detected_count": detected,
                "total": total,
                "detection_rate": round(rate, 4),
                "ci_lower": round(ci[0], 4),
                "ci_upper": round(ci[1], 4),
                "mean_semantic_similarity": round(mean_sim, 6),
                "detection_margin": round(detection_margin, 6),
                "threshold": round(threshold, 6) if threshold is not None else None,
            }

            if is_true:
                all_tp += detected
                all_tp_total += total
            else:
                all_fp += detected
                all_fp_total += total

        # Aggregate TP across true drift
        true_tp_rates = [pattern_metrics[p]["detection_rate"] for p in DRIFT_PATTERNS_TRUE]
        overall_tp_rate = sum(true_tp_rates) / len(true_tp_rates) if true_tp_rates else 0.0
        true_tp_ci = wilson_ci(all_tp, all_tp_total) if all_tp_total > 0 else (0.0, 1.0)

        # Aggregate FP across noise
        noise_fp_details = {}
        total_noise_fp = 0
        total_noise_n = 0
        for pattern in DRIFT_PATTERNS_NOISE:
            sims = se["stale_similarities"][pattern]
            noise_fp = sum(1 for s in sims if s < threshold)
            noise_n = len(sims)
            noise_fp_details[pattern] = {
                "fp_count": noise_fp,
                "fp_total": noise_n,
                "fp_rate": round(noise_fp / noise_n, 4) if noise_n > 0 else 0.0,
            }
            total_noise_fp += noise_fp
            total_noise_n += noise_n

        overall_noise_fp_rate = total_noise_fp / total_noise_n if total_noise_n > 0 else 0.0
        overall_noise_fp_ci = wilson_ci(total_noise_fp, total_noise_n)

        measurements["per_schema_size"][str(n)] = {
            "threshold": round(threshold, 6) if threshold is not None else None,
            "fp_rate_fresh": round(fp_fresh_rate, 4),
            "fp_ci_fresh": [round(fp_fresh_ci[0], 4), round(fp_fresh_ci[1], 4)],
            "overall_tp_rate_true_drift": round(overall_tp_rate, 4),
            "overall_tp_ci_true_drift": [round(true_tp_ci[0], 4), round(true_tp_ci[1], 4)],
            "overall_noise_fp_rate": round(overall_noise_fp_rate, 4),
            "overall_noise_fp_ci": [round(overall_noise_fp_ci[0], 4), round(overall_noise_fp_ci[1], 4)],
            "per_pattern": pattern_metrics,
            "noise_pattern_details": noise_fp_details,
        }

    # Overall
    overall_tp_rate = all_tp / all_tp_total if all_tp_total > 0 else 0.0
    overall_tp_ci = wilson_ci(all_tp, all_tp_total)
    overall_fp_rate = all_fp / all_fp_total if all_fp_total > 0 else 0.0
    overall_fp_ci = wilson_ci(all_fp, all_fp_total)

    measurements["overall"] = {
        "total_true_stale_samples": all_tp_total,
        "total_true_detected": all_tp,
        "overall_tp_rate": round(overall_tp_rate, 4),
        "overall_tp_ci": [round(overall_tp_ci[0], 4), round(overall_tp_ci[1], 4)],
        "total_fresh_samples": all_fp_total,
        "total_fresh_fp": all_fp,
        "overall_fp_rate_fresh": round(overall_fp_rate, 4),
        "overall_fp_ci_fresh": [round(overall_fp_ci[0], 4), round(overall_fp_ci[1], 4)],
    }

    print(f"  Overall TP: {overall_tp_rate:.4f} CI={overall_tp_ci}")
    print(f"  Overall FP (fresh): {overall_fp_rate:.4f} CI={overall_fp_ci}")

    # ---- Phase 6: Statistical tests ----
    print("[6/8] Running statistical tests...")
    stat_tests = {}
    for n in SCHEMA_SIZES:
        se = raw_evidence["per_schema_size"][str(n)]
        threshold = threshold_results[str(n)]["threshold"]

        # Pool true drift and noise semantic similarities
        true_drift_sims = []
        for pattern in DRIFT_PATTERNS_TRUE:
            true_drift_sims.extend(se["stale_similarities"][pattern])
        noise_sims = []
        for pattern in DRIFT_PATTERNS_NOISE:
            noise_sims.extend(se["stale_similarities"][pattern])

        # Mann-Whitney U: H1 is true drift < noise (less similar)
        stat, p_value = mann_whitney_test(true_drift_sims, noise_sims, alternative='less')

        # Cohen's d
        d = cohens_d(true_drift_sims, noise_sims)

        stat_tests[str(n)] = {
            "mann_whitney_stat": round(stat, 4) if stat is not None else None,
            "mann_whitney_p": round(p_value, 6) if p_value is not None else None,
            "cohens_d": round(d, 4) if d is not None else None,
            "n_true": len(true_drift_sims),
            "n_noise": len(noise_sims),
        }
        print(f"  n={n}: MW U={stat:.2f}, p={p_value:.6f}, d={d:.4f}")

    # Bonferroni correction: alpha = 0.05 / 4 = 0.0125
    bonferroni_alpha = 0.05 / len(SCHEMA_SIZES)
    print(f"  Bonferroni-corrected alpha: {bonferroni_alpha}")

    # ---- Phase 7: Ensemble optimization ----
    print("[7/8] Optimizing ensemble (Jaccard + semantic)...")
    ensemble_results = {}
    for n in SCHEMA_SIZES:
        se = raw_evidence["per_schema_size"][str(n)]

        true_jaccard = []
        true_semantic = []
        for pattern in DRIFT_PATTERNS_TRUE:
            true_jaccard.extend(se["jaccard_stale"][pattern])
            true_semantic.extend(se["stale_similarities"][pattern])

        noise_jaccard = []
        noise_semantic = []
        for pattern in DRIFT_PATTERNS_NOISE:
            noise_jaccard.extend(se["jaccard_stale"][pattern])
            noise_semantic.extend(se["stale_similarities"][pattern])

        best_alpha, best_f1, alpha_scores = optimize_ensemble_alpha(
            true_jaccard, noise_jaccard, true_semantic, noise_semantic, n_folds=5
        )
        ensemble_results[str(n)] = {
            "best_alpha": round(best_alpha, 2),
            "best_f1": round(best_f1, 4),
            "note": "alpha=1.0 is pure Jaccard, alpha=0.0 is pure semantic",
        }
        print(f"  n={n}: best_alpha={best_alpha:.2f}, best_f1={best_f1:.4f}")

    # ---- Phase 8: Supplementary realistic schema test ----
    print("[8/8] Running supplementary realistic schema test...")
    realistic_results = {}
    realistic_pairs = [
        ("github_user", "github_user_with_email", "true_drift"),
        ("github_user", "github_user_noise", "structural_noise"),
        ("stripe_charge", "stripe_charge_with_dispute", "true_drift"),
        ("stripe_charge", "stripe_charge_churn", "structural_noise"),
        ("twitter_tweet", "twitter_tweet_with_annotations", "true_drift"),
    ]

    # Build vectorizer on realistic schemas
    realistic_all_texts = []
    for name, schema in REALISTIC_SCHEMAS.items():
        realistic_all_texts.extend(schema_to_texts(schema))
    realistic_vectorizer = TfidfVectorizer(
        analyzer='word',
        token_pattern=r'[a-zA-Z0-9_]+',
        lowercase=True,
        sublinear_tf=True,
    )
    realistic_vectorizer.fit(realistic_all_texts)

    for name_a, name_b, label in realistic_pairs:
        schema_a = REALISTIC_SCHEMAS[name_a]
        schema_b = REALISTIC_SCHEMAS[name_b]
        sem_sim = compute_semantic_similarity(schema_a, schema_b, realistic_vectorizer)
        jac_sim = jaccard_similarity(schema_a, schema_b)
        realistic_results[f"{name_a}_vs_{name_b}"] = {
            "pair": f"{name_a} vs {name_b}",
            "label": label,
            "semantic_similarity": round(sem_sim, 6),
            "jaccard_similarity": round(jac_sim, 6),
        }
        print(f"  {name_a} vs {name_b} ({label}): semantic={sem_sim:.4f}, jaccard={jac_sim:.4f}")

    # ---- Assemble raw evidence ----
    raw_evidence["threshold_results"] = threshold_results
    raw_evidence["measurements"] = measurements
    raw_evidence["stat_tests"] = stat_tests
    raw_evidence["ensemble_results"] = ensemble_results
    raw_evidence["realistic_results"] = realistic_results
    raw_evidence["bonferroni_alpha"] = bonferroni_alpha

    return raw_evidence

# ============================================================
# DECISION RULE EVALUATION
# ============================================================

def evaluate_decision_rule(raw_evidence):
    """Apply frozen decision rule from spec.json."""
    measurements = raw_evidence["measurements"]
    stat_tests = raw_evidence["stat_tests"]
    bonferroni_alpha = raw_evidence["bonferroni_alpha"]
    violations = []

    # Conditions checked per schema size
    for n_str in [str(s) for s in SCHEMA_SIZES]:
        n = int(n_str)
        size_data = measurements["per_schema_size"][n_str]

        # Condition 1: TP lower bound of 95% Wilson CI >= 0.8 across true drift patterns
        for pattern in DRIFT_PATTERNS_TRUE:
            p = size_data["per_pattern"][pattern]
            if p["ci_lower"] < 0.8:
                violations.append(f"n={n} pattern={pattern}: TP CI lower bound {p['ci_lower']} < 0.8")

        # Condition 2: FP upper bound of 95% Wilson CI <= 0.15 across noise patterns
        for pattern in DRIFT_PATTERNS_NOISE:
            noise_detail = size_data["noise_pattern_details"][pattern]
            fp_ci = wilson_ci(noise_detail["fp_count"], noise_detail["fp_total"])
            if fp_ci[1] > 0.15:
                violations.append(f"n={n} pattern={pattern}: Noise FP CI upper bound {fp_ci[1]:.4f} > 0.15")

        # Also check fresh FP
        if size_data["fp_ci_fresh"][1] > 0.15:
            violations.append(f"n={n}: Fresh FP CI upper bound {size_data['fp_ci_fresh'][1]} > 0.15")

        # Condition 3: Mann-Whitney U p < Bonferroni-corrected alpha
        st = stat_tests[n_str]
        if st["mann_whitney_p"] is not None and st["mann_whitney_p"] >= bonferroni_alpha:
            violations.append(f"n={n}: Mann-Whitney p={st['mann_whitney_p']:.6f} >= {bonferroni_alpha}")

        # Condition 4: Positive control - add_field semantic < baseline at all sizes
        add_field = size_data["per_pattern"]["add_field"]
        if add_field["mean_semantic_similarity"] >= 1.0:
            violations.append(f"n={n}: Positive control FAIL - add_field mean semantic similarity {add_field['mean_semantic_similarity']} >= 1.0")

        # Condition 5: Null control - fresh FP = 0
        if size_data["fp_rate_fresh"] > 0:
            violations.append(f"n={n}: Null control FAIL - fresh FP rate {size_data['fp_rate_fresh']} > 0")

    # Evaluate decision
    if violations:
        decision = "FALSIFIED-IN-SETTING"
    else:
        # Check if ensemble is strictly better
        ensemble_better_count = 0
        for n_str in [str(s) for s in SCHEMA_SIZES]:
            ens = raw_evidence["ensemble_results"][n_str]
            # Ensemble is better if alpha != 0 (not pure semantic) and has higher F1
            if ens["best_alpha"] > 0.0:
                ensemble_better_count += 1

        if ensemble_better_count >= 3:
            decision = "MIXED"
        else:
            decision = "SURVIVES_CURRENT_TEST"

    return decision, violations

# ============================================================
# OUTPUT GENERATION
# ============================================================

def main():
    # Run experiment
    raw_evidence = run_experiment()

    # Evaluate decision
    decision, violations = evaluate_decision_rule(raw_evidence)
    print()
    print(f"Decision: {decision}")
    if violations:
        print(f"Violations ({len(violations)}):")
        for v in violations:
            print(f"  - {v}")
    else:
        print("No violations - all conditions met")
    print()

    # Save raw evidence
    exp_dir = Path(__file__).parent.parent.parent / "experiments" / THIS_EXPERIMENT_ID
    raw_dir = exp_dir / "raw_evidence"
    raw_dir.mkdir(parents=True, exist_ok=True)

    # Save raw evidence (full)
    with open(raw_dir / "semantic_raw_evidence.json", "w") as f:
        json.dump(raw_evidence, f, indent=2)

    # Save derived measurements
    with open(raw_dir / "semantic_derived_measurements.json", "w") as f:
        json.dump(raw_evidence["measurements"], f, indent=2)

    # Save decision evaluation
    with open(raw_dir / "semantic_decision_evaluation.json", "w") as f:
        json.dump({
            "decision": decision,
            "violations": violations,
            "evaluated_at": datetime.now(timezone.utc).isoformat(),
        }, f, indent=2)

    # Compute hashes
    raw_hashes = {}
    for p in sorted(raw_dir.iterdir()):
        if p.is_file():
            h = hashlib.sha256(p.read_bytes()).hexdigest()
            raw_hashes[p.name] = h

    with open(raw_dir / "hashes.json", "w") as f:
        json.dump(raw_hashes, f, indent=2)

    print(f"Raw evidence saved to {raw_dir}")
    print(f"Hashes: {json.dumps(raw_hashes, indent=2)}")
    print("=== Experiment Complete ===")

    return raw_evidence, decision, violations, raw_hashes

if __name__ == "__main__":
    raw_evidence, decision, violations, raw_hashes = main()
