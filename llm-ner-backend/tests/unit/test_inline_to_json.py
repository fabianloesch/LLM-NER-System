import pytest
from app.core.utils import inline_ner_to_json

class TestInlineToJson:

    @pytest.mark.parametrize("input, expected", [
        (
            "Lorem Ipsum <Drug>Ibuprofen</Drug>.", 
            [{"start": 12, "end": 21, "label": "Drug", "entity": "Ibuprofen"}]
        ),
        (
            "Lorem Ipsum <Strength>400mg</Strength> <Drug>Ibuprofen</Drug>.", 
            [{"start": 12, "end": 17, "label": "Strength", "entity": "400mg"}, 
             {"start": 18, "end": 27, "label": "Drug", "entity": "Ibuprofen"}]
        )
    ])
    def test_inline_ner_to_json_basic(self, input, expected):
        result = inline_ner_to_json(input)
        for idx, entity in enumerate(expected):
            assert result[idx]["start"] == entity["start"]
            assert result[idx]["end"] == entity["end"]
            assert result[idx]["label"] == entity["label"]
            assert result[idx]["entity"] == entity["entity"]

    def test_inline_ner_to_json_empty(self):
        result = inline_ner_to_json("Lorem Ipsum 400mg Ibuprofen.")
        assert result == []