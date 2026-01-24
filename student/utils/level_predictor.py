def predict_level(correct, total):
    if total == 0:
        return "Beginner"

    accuracy = (correct / total) * 100

    if accuracy >= 80:
        return "Advanced"
    elif accuracy >= 50:
        return "Intermediate"
    else:
        return "Beginner"
