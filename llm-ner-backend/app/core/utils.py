import re

# collection of serveral functions

# Base Metrics ('correct', 'fuzzy_correct', 'false_negative', 'false_positive')
def compute_base_eval_metric(truth, prediction):
    # Gold-Standard Entitäten aufbereiten
    truth_entities = []
    for item in truth['label']:
        start, end, label = item
        truth_entities.append({'start': start, 'end': end, 'label': label})
    
    # Prediction Entitäten aufbereiten
    pred_entities = []
    for entity in prediction:
        pred_entities.append({
            'start': entity['start'],
            'end': entity['end'],
            'label': entity['label']
        })
    
    # Alle vorkommenden Entitätsklassen sammeln
    all_labels = set()
    for entity in truth_entities:
        all_labels.add(entity['label'])
    for entity in pred_entities:
        all_labels.add(entity['label'])
    
    # Ergebnis-Struktur initialisieren
    results = {}
    for label in all_labels:
        results[label] = {
            'correct': 0,
            'fuzzy_correct': 0,
            'false_negative': 0,
            'false_positive': 0
        }
    
    # Tracking welche Entitäten bereits gematched wurden
    matched_truth = set()
    matched_pred = set()
    
    # 1. Correct: Exakte Übereinstimmung (boundaries und label)
    for i, pred in enumerate(pred_entities):
        for j, truth_ent in enumerate(truth_entities):
            if (pred['start'] == truth_ent['start'] and 
                pred['end'] == truth_ent['end'] and 
                pred['label'] == truth_ent['label']):
                results[pred['label']]['correct'] += 1
                matched_truth.add(j)
                matched_pred.add(i)
                break
    
    # 2. Fuzzy Correct: Label stimmt überein, aber boundaries nicht
    for i, pred in enumerate(pred_entities):
        if i in matched_pred:
            continue
        for j, truth_ent in enumerate(truth_entities):
            if j in matched_truth:
                continue
            # Prüfen ob es eine Überlappung gibt
            if (pred['label'] == truth_ent['label'] and
                pred['start'] < truth_ent['end'] and 
                pred['end'] > truth_ent['start']):
                results[pred['label']]['fuzzy_correct'] += 1
                matched_truth.add(j)
                matched_pred.add(i)
                break
    
    # 3. False Negative: Entitäten im Gold-Standard, die nicht gematched wurden
    for j, truth_ent in enumerate(truth_entities):
        if j not in matched_truth:
            results[truth_ent['label']]['false_negative'] += 1
    
    # 4. False Positive: Entitäten in Prediction, die nicht gematched wurden
    for i, pred in enumerate(pred_entities):
        if i not in matched_pred:
            results[pred['label']]['false_positive'] += 1
    
    return results

def add_base_metrics_dicts(dict1, dict2):
    result = {}
    
    # Alle Entitätsklassen aus beiden Dicts sammeln
    all_labels = set(dict1.keys()) | set(dict2.keys())
    
    for label in all_labels:
        result[label] = {}
        
        # Alle Metriken aus beiden Dicts sammeln
        metrics1 = dict1.get(label, {})
        metrics2 = dict2.get(label, {})
        all_metrics = set(metrics1.keys()) | set(metrics2.keys())
        
        # Werte addieren
        for metric in all_metrics:
            value1 = metrics1.get(metric, 0)
            value2 = metrics2.get(metric, 0)
            result[label][metric] = value1 + value2
    
    return result


# Evaluation Metrics (precision, recall, f1-score)
def compute_precision(correct:int, fuzzy_correct:int, false_positive:int, strict:bool) -> float:
    if (strict):
        false_positive += fuzzy_correct
    else:
        correct += fuzzy_correct

    if (correct + false_positive > 0):
        return round(correct / (correct + false_positive), 4)
    else: return 0

def compute_recall(correct:int, fuzzy_correct:int, false_negative:int, strict:bool) -> float:
    if (strict):
        false_negative += fuzzy_correct
    else:
        correct += fuzzy_correct

    if (correct + false_negative > 0):
        return round(correct / (correct + false_negative), 4)
    else: return 0

def compute_f1_score(precision:float, recall:float) -> float:
    if (precision + recall) > 0:
        return round(2 * precision * recall / (precision + recall), 4)
    else: return 0

def compute_eval_metrics(base_metrics:dict) -> dict:
    result = {
        "overall": {},
        "entityClassLevel": {}
    }

    # Overall Evaluation
    agg_base_metrics = {
        "correct": 0,
        "fuzzy_correct": 0,
        "false_positive": 0,
        "false_negative": 0
    }
    for _, metrics in base_metrics.items():
        # Über alle Metriken der aktuellen Klasse iterieren
        for metric, value in metrics.items():
            agg_base_metrics[metric] += value

    overall_precision = compute_precision(agg_base_metrics["correct"], agg_base_metrics["fuzzy_correct"], agg_base_metrics["false_positive"], False)
    overall_recall = compute_precision(agg_base_metrics["correct"], agg_base_metrics["fuzzy_correct"], agg_base_metrics["false_negative"], False)
    overall_f1_score = compute_f1_score(overall_precision, overall_recall)

    result["overall"] = {
        "precision": overall_precision,
        "recall": overall_recall,
        "f1_score": overall_f1_score
    }

    # Entity Class Level Evaluation
    for label, metrics in base_metrics.items():
        precision = compute_precision(metrics["correct"], metrics["fuzzy_correct"], metrics["false_positive"], False)
        recall = compute_precision(metrics["correct"], metrics["fuzzy_correct"], metrics["false_negative"], False)
        f1_score = compute_f1_score(precision, recall)
        result["entityClassLevel"][label] = {
            "precision": precision,
            "recall": recall,
            "f1_score": f1_score
        }

    return result


# Misc
def get_distinct_entity_classes(entries):
    entity_classes = set()
    for entry in entries:
        if 'label' in entry:
            for annotation in entry['label']:
                # annotation ist [start, end, label]
                if len(annotation) >= 3:
                    label = annotation[2]
                    entity_classes.add(label)
    return entity_classes

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

