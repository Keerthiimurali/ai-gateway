import csv
from routing import routing_model

def evaluate_routing(test_file="test_prompts.csv"):
    results = []
    correct = 0
    total = 0
    false_pos = 0  
    false_neg = 0  

    with open(test_file, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            prompt = row["prompt"]
            label = row["label"]

            decision, reason, confidence = routing_model(prompt)
            predicted = "fast" if decision == "fast" else "capable"

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
                "correct": is_correct
            })

    accuracy = correct / total * 100 if total > 0 else 0

    # Print summary
    print("\n->ROUTING MODEL EVALUATION:\n")
    print(f"\tTotal prompts: {total}")
    print(f"\tAccuracy: {accuracy:.2f}%")
    print(f"\tFalse Positives (complex → fast): {false_pos}")
    print(f"\tFalse Negatives (simple → capable): {false_neg}")

    
    print("\n->Per-Prompt Results:\n")
    for idx, r in enumerate(results, start=1):
        status = "Correct" if r["correct"] else "Incorrect"
        print(f"{idx}. Prompt: {r['prompt']}")
        print(f"   Label: {r['label']} | Predicted: {r['predicted']} | Confidence: {r['confidence']:.2f} | {status}\n")

if __name__ == "__main__":
    evaluate_routing()
