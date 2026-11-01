import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location('grade_usage_review', Path(__file__).parent/'agent_evals/grade_usage_review.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class UsageReviewTests(unittest.TestCase):
    def case(self):
        return {'task_id':'one','artifact_id':'v1','variant':'baseline',
                'rubric_ratings':dict.fromkeys(m.WEIGHTS,10),
                'critical_checks':[{'id':'core','status':'PASS','evidence':'Observed action/result'}]}

    def test_appearance_cannot_override_failed_critical_journey(self):
        r=self.case();r['critical_checks'][0]['status']='FAIL'
        result=m.grade(r)
        self.assertEqual(result['weighted_score'],10)
        self.assertEqual(result['readiness'],'BLOCKED')

    def test_unverified_behavior_is_not_a_pass(self):
        r=self.case();r['critical_checks'][0]['status']='UNVERIFIED'
        self.assertEqual(m.grade(r)['readiness'],'INCONCLUSIVE')

    def test_user_overall_is_preserved_not_recalculated_from_partial_scores(self):
        r=self.case();r['rubric_ratings']={'presentation':8};r['user_overall_rating']=4
        result=m.grade(r)
        self.assertIsNone(result['weighted_score'])
        self.assertEqual(result['user_overall_rating'],4)

    def test_repeats_are_clustered_by_task(self):
        before=[{'task_id':'one','repeat':i,'weighted_score':4}for i in range(10)]
        after=[{'task_id':'one','repeat':i,'weighted_score':6}for i in range(10)]
        result=m.compare(before,after)
        self.assertEqual(result['paired_runs'],10)
        self.assertEqual(result['distinct_scored_tasks'],1)
        self.assertEqual(result['mean_task_score_delta'],2)
        self.assertIsNone(result['two_sided_sign_test_p'])

    def test_exact_sign_test_uses_task_clusters_not_number_of_assertions(self):
        before=[{'task_id':str(i),'weighted_score':4}for i in range(5)]
        after=[{'task_id':str(i),'weighted_score':5}for i in range(5)]
        self.assertEqual(m.compare(before,after)['two_sided_sign_test_p'],.0625)

    def test_malformed_scores_and_duplicate_observations_are_rejected(self):
        for bad in (float('nan'),11,True):
            r=self.case();r['rubric_ratings']['presentation']=bad
            with self.assertRaises(ValueError):m.grade(r)
        with self.assertRaises(ValueError):m.compare([{'task_id':'one'},{'task_id':'one'}],[])
