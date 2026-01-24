from app.services.evaluation_service import EvaluationService

class TestComputeEvalMetrics:

    EVAL_METRICS = ['precision', 'recall', 'f1_score']

    def assert_dict(self, result, expected):

        received_levels = list(result.keys())
        expected_levels = list(expected.keys())
        assert len(received_levels) == len(expected_levels)

        assert result["overall"].keys() == expected["overall"].keys()

        for metric in self.EVAL_METRICS:
            assert result["overall"][metric] == expected["overall"][metric]
        
        result_entitylevel = result["entityClassLevel"]
        expected_entitylevel = expected["entityClassLevel"]
        assert result_entitylevel.keys() == expected_entitylevel.keys()
        for label in expected_entitylevel.keys():
            received_metrics = list(result_entitylevel[label].keys())
            expected_metrics = list(expected_entitylevel[label].keys())
            assert len(received_metrics) == len(expected_metrics)

            for metric in self.EVAL_METRICS:
                assert result_entitylevel[label][metric] == expected_entitylevel[label][metric]

    def test_standard_case(self):
        base_metrics = {
            'Form': {
                'correct': 50,
                'fuzzy_correct': 0,
                'false_negative': 0,
                'false_positive': 0
                },
            'Frequency': {
                'correct': 25,
                'fuzzy_correct': 0,
                'false_negative': 0,
                'false_positive': 0
                },
            'Drug': {
                'correct': 25,
                'fuzzy_correct': 0,
                'false_negative': 0,
                'false_positive': 0
                }
        }
        
        expected = {
            'overall': {
                'precision': 1.0, 
                'recall': 1.0, 
                'f1_score': 1.0
            },
            'entityClassLevel': {
                'Drug': {
                    'precision': 1.0,
                    'recall': 1.0,
                    'f1_score': 1.0
                },
                'Form': {
                    'precision': 1.0, 
                    'recall': 1.0, 
                    'f1_score': 1.0
                },
                'Frequency': {
                    'precision': 1.0,
                    'recall': 1.0, 
                    'f1_score': 1.0
                },
            }
        }

        result = EvaluationService.compute_eval_metrics(base_metrics)
        self.assert_dict(result, expected)

    def test_fuzzy_correct(self):
        base_metrics = {
            'Form': {
                'correct': 0,
                'fuzzy_correct': 50,
                'false_negative': 0,
                'false_positive': 0
                },
            'Frequency': {
                'correct': 25,
                'fuzzy_correct': 0,
                'false_negative': 0,
                'false_positive': 0
                },
            'Drug': {
                'correct': 20,
                'fuzzy_correct': 5,
                'false_negative': 0,
                'false_positive': 0
                }
        }
        
        expected = {
            'overall': {
                'precision': 1.0, 
                'recall': 1.0, 
                'f1_score': 1.0
            },
            'entityClassLevel': {
                'Drug': {
                    'precision': 1.0,
                    'recall': 1.0,
                    'f1_score': 1.0
                },
                'Form': {
                    'precision': 1.0, 
                    'recall': 1.0, 
                    'f1_score': 1.0
                },
                'Frequency': {
                    'precision': 1.0,
                    'recall': 1.0, 
                    'f1_score': 1.0
                },
            }
        }

        result = EvaluationService.compute_eval_metrics(base_metrics)
        self.assert_dict(result, expected)

    def test_false_positive(self):
            base_metrics = {
                'Form': {
                    'correct': 50,
                    'fuzzy_correct': 0,
                    'false_negative': 0,
                    'false_positive': 0
                    },
                'Frequency': {
                    'correct': 25,
                    'fuzzy_correct': 0,
                    'false_negative': 0,
                    'false_positive': 0
                    },
                'Drug': {
                    'correct': 25,
                    'fuzzy_correct': 0,
                    'false_negative': 0,
                    'false_positive': 5
                    }
            }
            
            expected = {
                'overall': {
                    'precision': 0.9524, 
                    'recall': 1.0, 
                    'f1_score': 0.9756
                },
                'entityClassLevel': {
                    'Drug': {
                        'precision': 0.8333,
                        'recall': 1.0,
                        'f1_score': 0.9091
                    },
                    'Form': {
                        'precision': 1.0, 
                        'recall': 1.0, 
                        'f1_score': 1.0
                    },
                    'Frequency': {
                        'precision': 1.0,
                        'recall': 1.0, 
                        'f1_score': 1.0
                    },
                }
            }

            result = EvaluationService.compute_eval_metrics(base_metrics)
            self.assert_dict(result, expected)
        
