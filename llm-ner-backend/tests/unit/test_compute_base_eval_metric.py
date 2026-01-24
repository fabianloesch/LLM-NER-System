from app.services.evaluation_service import EvaluationService

class TestComputeBaseEvalMetric:

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
        truth = {
            "id": 1,
            "text": "Der Patient sollte bei Asthma bronchiale Formoterol/Beclometason 6/100 µg als Dosieraerosol morgens und abends inhalativ versuchen.",
            "label": [
            [78, 91, "Form"],
            [92, 110, "Frequency"],
            [111, 120, "Form"]
            ]
        }

        prediction = [
                    {
                        "entity": "Dosieraerosol",
                        "label": "Form",
                        "start": 78,
                        "end": 91
                    },
                    {
                        "entity": "morgens und abends",
                        "label": "Frequency",
                        "start": 92,
                        "end": 110
                    },
                    {
                        "entity": "inhalativ",
                        "label": "Form",
                        "start": 111,
                        "end": 120
                    }
            ]
        
        expected = {
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
        
        result = EvaluationService.compute_base_eval_metric(truth, prediction) 
        self.assert_dict(result, expected)

    def test_fuzzy_correct(self):
        truth = {
            "id": 1,
            "text": "Der Patient sollte bei Asthma bronchiale Formoterol/Beclometason 6/100 µg als Dosieraerosol morgens und abends inhalativ versuchen.",
            "label": [
            [78, 91, "Form"],
            [92, 110, "Frequency"],
            [111, 120, "Form"]
            ]
        }

        prediction = [
                    {
                        "entity": "Dosieraerosol",
                        "label": "Form",
                        "start": 79,
                        "end": 90
                    },
                    {
                        "entity": "morgens und abends",
                        "label": "Frequency",
                        "start": 93,
                        "end": 111
                    },
                    {
                        "entity": "inhalativ",
                        "label": "Form",
                        "start": 110,
                        "end": 120
                    }
            ]
        
        expected = {
            'Form': {
                'correct': 0,
                'fuzzy_correct': 2,
                'false_negative': 0,
                'false_positive': 0
                },
            'Frequency': {
                'correct': 0,
                'fuzzy_correct': 1,
                'false_negative': 0,
                'false_positive': 0
                }
            }
        
        result = EvaluationService.compute_base_eval_metric(truth, prediction) 
        self.assert_dict(result, expected)

    def test_false_negative(self):
        truth = {
            "id": 1,
            "text": "Der Patient sollte bei Asthma bronchiale Formoterol/Beclometason 6/100 µg als Dosieraerosol morgens und abends inhalativ versuchen.",
            "label": [
            [78, 91, "Form"],
            [92, 110, "Frequency"],
            [111, 120, "Form"]
            ]
        }

        prediction = [
                    {
                        "entity": "morgens und abends",
                        "label": "Frequency",
                        "start": 93,
                        "end": 111
                    },
                    {
                        "entity": "inhalativ",
                        "label": "Form",
                        "start": 110,
                        "end": 120
                    }
            ]
        
        expected = {
            'Form': {
                'correct': 0,
                'fuzzy_correct': 1,
                'false_negative': 1,
                'false_positive': 0
                },
            'Frequency': {
                'correct': 0,
                'fuzzy_correct': 1,
                'false_negative': 0,
                'false_positive': 0
                }
            }
        
        result = EvaluationService.compute_base_eval_metric(truth, prediction) 
        self.assert_dict(result, expected)

    def test_false_positive(self):
        truth = {
            "id": 1,
            "text": "Der Patient sollte bei Asthma bronchiale Formoterol/Beclometason 6/100 µg als Dosieraerosol morgens und abends inhalativ versuchen.",
            "label": [
            [78, 91, "Form"],
            [92, 110, "Frequency"],
            [111, 120, "Form"]
            ]
        }

        prediction = [
                    {
                        "entity": "Dosieraerosol",
                        "label": "Form",
                        "start": 78,
                        "end": 91
                    },
                    {
                        "entity": "morgens und abends",
                        "label": "Frequency",
                        "start": 92,
                        "end": 110
                    },
                    {
                        "entity": "inhalativ",
                        "label": "Form",
                        "start": 111,
                        "end": 120
                    },
                    {
                        "entity": "inhalativ",
                        "label": "Form",
                        "start": 121,
                        "end": 123
                    }
            ]
        
        expected = {
            'Form': {
                'correct': 2,
                'fuzzy_correct': 0,
                'false_negative': 0,
                'false_positive': 1
                },
            'Frequency': {
                'correct': 1,
                'fuzzy_correct': 0,
                'false_negative': 0,
                'false_positive': 0
                }
            }
        
        result = EvaluationService.compute_base_eval_metric(truth, prediction) 
        self.assert_dict(result, expected)

    def test_false_postive_combined_false_negative(self):
        truth = {
            "id": 1,
            "text": "Der Patient sollte bei Asthma bronchiale Formoterol/Beclometason 6/100 µg als Dosieraerosol morgens und abends inhalativ versuchen.",
            "label": [
            [78, 91, "Form"],
            [92, 110, "Frequency"],
            [111, 120, "Form"]
            ]
        }

        prediction = [
                    {
                        "entity": "Dosieraerosol",
                        "label": "Form",
                        "start": 78,
                        "end": 91
                    },
                    {
                        "entity": "morgens und abends",
                        "label": "Frequency",
                        "start": 92,
                        "end": 110
                    },
                    {
                        "entity": "inhalativ",
                        "label": "Frequency",
                        "start": 111,
                        "end": 120
                    }
            ]
        
        expected = {
            'Form': {
                'correct': 1,
                'fuzzy_correct': 0,
                'false_negative': 1,
                'false_positive': 0
                },
            'Frequency': {
                'correct': 1,
                'fuzzy_correct': 0,
                'false_negative': 0,
                'false_positive': 1
                }
            }
        
        result = EvaluationService.compute_base_eval_metric(truth, prediction) 
        self.assert_dict(result, expected)