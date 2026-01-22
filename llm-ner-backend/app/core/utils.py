import re
from collections import defaultdict

# collection of serveral functions

def get_distinct_entity_classes(entries):
    entity_classes = set()
    for entry in entries:
        if 'label' in entry:
            for annotation in entry['label']:
                # annotation ist [start, end, label]
                if len(annotation) >= 3:
                    label = annotation[2]
                    entity_classes.add(label)
    return sorted(entity_classes)

def inline_ner_to_json(text: str):
        pattern = re.compile(r"<(?P<label>\w+)>(?P<value>.*?)</\1>")
        
        result = []
        current_pos = 0
        last_end = 0

        for match in pattern.finditer(text):
            # Text vor der Entität
            before = text[last_end:match.start()]
            current_pos += len(before)

            value = match.group("value")
            label = match.group("label")

            start = current_pos
            end = start + len(value)

            result.append({"start":start, "end":end, "label":label, "entity": value})

            current_pos = end
            last_end = match.end()

        return result

def restructure(data: list[dict]) -> dict:
    result = defaultdict(dict)

    for item in data:
        model = item["model"]
        identifier = item["identifier"]
        response = item["response"]

        result[model][identifier] = response

    return dict(result)
