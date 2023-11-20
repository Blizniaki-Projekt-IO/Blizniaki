from core.recognition import scores

ANIMALS_MASK = {
    "pies": [5, 5, 1, 5, 5, 2],
    "kot": [4, 3, 3, 3, 2, 3],
    "niedźwiedź": [0, 2, 5, 2, 1, 5],
    "lis": [0, 1, 4, 1, 2, 3],
    "surykatka": [5, 4, 2, 4, 4, 2]
}

MAX_POINTS = 5
MAX_PERCENT = 100


def add_points_by_character(character):
    if character is not None:
        for key in scores:
            for i in range(6):
                if character[i] == 1:
                    scores[key] += ANIMALS_MASK[key][i]
                else:
                    scores[key] += MAX_POINTS - ANIMALS_MASK[key][i]
        return scores
    else:
        return {"error": "niepoprawny format odpowiedzi z quizu!"}


def compute_final_results(character):
    new_scores = add_points_by_character(character)
    sum_points = sum(new_scores.values())
    for key in new_scores.keys():
        new_scores[key] = round(new_scores.get(key) * 100 / sum_points)
    if sum(new_scores.values()) != 100:
        max_value_key = max(new_scores, key=new_scores.get)
        new_scores[max_value_key] += MAX_PERCENT - sum_points
    return new_scores
