from student.utils.level_predictor import predict_level

def get_level_for_questions(questions, answers):
    total = len(questions)
    correct = 0

    for q in questions:
        if str(q.id) in answers and answers[str(q.id)] == q.correct_option:
            correct += 1

    return predict_level(correct, total)
