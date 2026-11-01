"""Grade explicit review evidence; never infer usability or model improvement from screenshots."""
import argparse
import json
import math
from collections import defaultdict
from pathlib import Path

WEIGHTS = {'intent_alignment': 20, 'core_behavior': 30, 'workflow_usability': 25,
           'reliability_and_evidence': 15, 'presentation': 10}
STATUSES = {'PASS', 'FAIL', 'UNVERIFIED', 'NOT_APPLICABLE'}

def grade(review):
    """Ratings are assessor inputs, not results fabricated by this scorer."""
    ratings = review.get('rubric_ratings', {})
    if set(ratings) - set(WEIGHTS):
        raise ValueError('Unknown rubric dimension')
    for rating in ratings.values():
        if isinstance(rating, bool) or not isinstance(rating, (int, float)) or not math.isfinite(rating) or not 0 <= rating <= 10:
            raise ValueError('Ratings must be finite numbers from 0 to 10')
    checks = review.get('critical_checks', [])
    ids = []
    for check in checks:
        ids.append(check['id'])
        if check['status'] not in STATUSES or not check.get('evidence'):
            raise ValueError('Every check needs a valid status and evidence or a stated verification gap')
    if len(ids) != len(set(ids)):
        raise ValueError('Duplicate critical check')
    active = [c for c in checks if c['status'] != 'NOT_APPLICABLE']
    readiness = ('BLOCKED' if any(c['status'] == 'FAIL' for c in active) else
                 'INCONCLUSIVE' if not active or any(c['status'] == 'UNVERIFIED' for c in active) else
                 'ELIGIBLE_FOR_ACCEPTANCE')
    score = sum(ratings[k] * WEIGHTS[k] for k in WEIGHTS) / 100 if set(ratings) == set(WEIGHTS) else None
    return {'task_id': review['task_id'], 'artifact_id': review['artifact_id'],
            'variant': review['variant'], 'repeat': review.get('repeat', 1),
            'weighted_score': score, 'readiness': readiness,
            'passed_critical': sum(c['status'] == 'PASS' for c in active),
            'failed_critical': sum(c['status'] == 'FAIL' for c in active),
            'unverified_critical': sum(c['status'] == 'UNVERIFIED' for c in active),
            'critical_total': len(active),
            'user_overall_rating': review.get('user_overall_rating'),
            'missing_rubric_dimensions': sorted(set(WEIGHTS) - set(ratings))}

def compare(before, after):
    """Pair repeated runs, then give each task cluster one vote/weight."""
    def keyed(rows):
        output = {}
        for row in rows:
            key = (row['task_id'], row.get('repeat', 1))
            if key in output:
                raise ValueError('Duplicate task/repeat pair')
            output[key] = row
        return output
    left, right = keyed(before), keyed(after)
    by_task = defaultdict(list)
    pairs = set(left) & set(right)
    for key in pairs:
        a, b = left[key].get('weighted_score'), right[key].get('weighted_score')
        if a is not None and b is not None:
            by_task[key[0]].append(b-a)
    deltas = {k: sum(v)/len(v) for k,v in by_task.items()}
    positive, negative = sum(x>0 for x in deltas.values()), sum(x<0 for x in deltas.values())
    n = positive + negative
    # Only expose a test with enough distinct non-tied task clusters; independence
    # and preselection remain assumptions the caller must justify.
    p = min(1.0, 2*sum(math.comb(n,k) for k in range(min(positive,negative)+1))/(2**n)) if n >= 5 else None
    return {'paired_runs': len(pairs), 'distinct_scored_tasks': len(deltas),
            'mean_task_score_delta': sum(deltas.values())/len(deltas) if deltas else None,
            'task_deltas': deltas, 'two_sided_sign_test_p': p,
            'limitations': 'Repeated runs of one task are not independent tasks. A sign test assumes independent, preselected task clusters; it is not proof of generalization. User ratings, source coverage and behavior-test results are distinct evidence.'}

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('review', type=Path)
    args = p.parse_args()
    print(json.dumps(grade(json.loads(args.review.read_text())), indent=2))

if __name__ == '__main__':
    main()
