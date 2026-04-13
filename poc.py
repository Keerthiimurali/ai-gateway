import csv
from routing import routing_model
from sklearn.metrics import confusion_matrix, precision_score, recall_score, f1_score

def evaluate_routing(test_file="test_prompts.csv"):
    results = []
    correct = 0
    total = 0
    false_pos = 0  
    false_neg = 0  

    y_true = []
    y_pred = []

    with open(test_file, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            prompt = row["prompt"]
            label = row["label"]

            # ✅ FIX: routing_model now returns 4 values
            decision, reason, confidence, signals = routing_model(prompt)

            predicted = "fast" if decision == "fast" else "capable"

            # Convert to numeric for ML metrics
            pred_num = 1 if predicted == "capable" else 0
            actual_num = 1 if label == "complex" else 0

            y_pred.append(pred_num)
            y_true.append(actual_num)

            is_correct = (predicted == "fast" and label == "simple") or \
                         (predicted == "capable" and label == "complex")

            if is_correct:
                correct += 1
            else:
                if predicted == "fast" and label == "complex":
                    false_pos += 1
                elif predicted == "capable" and label == "simple":
                    false_neg += 1

            total += 1

            results.append({
                "prompt": prompt[:50],
                "label": label,
                "predicted": predicted,
                "confidence": confidence,
                "signals": signals,   # ✅ ADDED (important for explanation)
                "correct": is_correct
            })

    accuracy = correct / total * 100 if total > 0 else 0

    # -------------------------
    # ML METRICS
    # -------------------------
    cm = confusion_matrix(y_true, y_pred)
    precision = precision_score(y_true, y_pred, zero_division=0)
    recall = recall_score(y_true, y_pred, zero_division=0)
    f1 = f1_score(y_true, y_pred, zero_division=0)

    # -------------------------
    # PRINT SUMMARY
    # -------------------------
    print("\n ROUTING MODEL EVALUATION:\n")
    print(f"Total prompts: {total}")
    print(f"Accuracy: {accuracy:.2f}%")
    print(f"False Positives (complex → fast): {false_pos}")
    print(f"False Negatives (simple → capable): {false_neg}")

    print("\nConfusion Matrix:")
    print(cm)

    print(f"\nPrecision: {precision:.2f}")
    print(f"Recall: {recall:.2f}")
    print(f"F1 Score: {f1:.2f}")

    # -------------------------
    # PER-PROMPT OUTPUT
    # -------------------------
    print("\n-> Per-Prompt Results:\n")
    for idx, r in enumerate(results, start=1):
        status = "Correct" if r["correct"] else "Incorrect"
        print(f"{idx}. Prompt: {r['prompt']}")
        print(f"   Label: {r['label']} | Predicted: {r['predicted']} | Confidence: {r['confidence']:.2f}")
        print(f"   Signals: {', '.join(r['signals']) if r['signals'] else 'None'} | {status}\n")

    # -------------------------
    # FAILURE CASES (IMPORTANT)
    # -------------------------
    print("\n FAILURE CASES (Top 3):\n")

    count = 0
    for r in results:
        if not r["correct"]:
            print(f"Prompt: {r['prompt']}")
            print(f"Actual: {r['label']} | Predicted: {r['predicted']}")
            print(f"Confidence: {r['confidence']:.2f}")
            print(f"Signals: {', '.join(r['signals']) if r['signals'] else 'None'}")
            print("-" * 50)

            count += 1
            if count == 3:
                break


if __name__ == "__main__":
    evaluate_routing()