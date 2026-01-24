from app.services.evaluation_service import EvaluationService

class TestAddBaseMetricsDicts:

    BASE_METRICS = ['correct', 'fuzzy_correct', 'false_negative', 'false_positive']

    def assert_dict(self, result, expected):

        received_labels = list(result.keys())
        expected_labels = list(expected.keys())
        assert len(received_labels) == len(expected_labels)

        for label in expected_labels:
            received_metrics = list(result[label].keys())
            expected_metrics = list(expected[label].keys())
            assert len(received_metrics) == len(expected_metrics)

            for metric in self.BASE_METRICS:
                assert result[label][metric] == expected[label][metric]
    

    def test_standard_case(self):
        dict1 = {
            'Form': {
                'correct': 2,
                'fuzzy_correct': 0,
                'false_negative': 0,
                'false_positive': 0
                },
            'Frequency': {
                'correct': 1,
                'fuzzy_correct': 0,
                'false_negative': 0,
                'false_positive': 0
                }
            }
        
        dict2 = {
            'Form': {
                'correct': 2,
                'fuzzy_correct': 0,
                'false_negative': 0,
                'false_positive': 0
                },
            'Frequency': {
                'correct': 1,
                'fuzzy_correct': 0,
                'false_negative': 0,
                'false_positive': 0
                }
            }
        
        expected = {
            'Form': {
                'correct': 4,
                'fuzzy_correct': 0,
                'false_negative': 0,
                'false_positive': 0
                },
            'Frequency': {
                'correct': 2,
                'fuzzy_correct': 0,
                'false_negative': 0,
                'false_positive': 0
                }
            }
        
        result = EvaluationService.add_base_metrics_dicts(dict1, dict2)
        self.assert_dict(result, expected)