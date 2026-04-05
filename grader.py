def grade_classification(pred, true):
    return 1.0 if pred == true else 0.0


def grade_priority(pred, true):
    return 1.0 if pred == true else 0.0


def grade_reply(pred, true):
    return 1.0 if pred.lower() == true.lower() else 0.0


def grade_all(pred, true):
    score = 0

    score += 0.4 * grade_classification(pred["category"], true["category"])
    score += 0.3 * grade_priority(pred["priority"], true["priority"])
    score += 0.3 * grade_reply(pred["reply"], true["reply"])

    return score