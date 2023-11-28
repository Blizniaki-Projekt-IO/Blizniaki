import os

import cv2
import torch
import torch.nn.functional as F
from torchvision import transforms

from blizniaki_app import settings
from core.neurons.FaceNet import FaceNet

device = "cpu"

transforms_test = transforms.Compose([transforms.ToTensor(),
                                      transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])])

ANIMALS_MASK = {
    "pies": [2, 2, 0, 2, 2, 0],
    "kot": [2, 1, 1, 1, 1, 1],
    "lis": [0, 0, 2, 0, 1, 1],
    "niedzwiedz": [0, 1, 2, 1, 0, 2],
    "surykatka": [2, 2, 1, 2, 2, 1]
}


def predict(img, character):
    model = FaceNet()
    model.load_state_dict(torch.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'model_humanface_to_animal.pt'), map_location=torch.device('cpu')))
    model.eval()
    img_c = cv2.imread(os.path.join(settings.MEDIA_ROOT, img))
    img_c = cv2.resize(img_c, (178, 218))
    img_trans = transforms_test(img_c).to(device).unsqueeze(0)
    pred = model(img_trans)[0].detach()
    pred = (F.softmax(pred, dim=0)).numpy()
    zwierzeta = ["pies", "kot", "lis", "niedzwiedz", "surykatka"]

    result = dict(zip(zwierzeta, pred))

    for key in result.keys():
        result[key] = round(result.get(key) * 100)
    scores = add_points_by_character(character, result)
    return compute_final_results(scores)


MAX_POINTS = 2
MAX_PERCENT = 100


def add_points_by_character(character, scores):
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


def compute_final_results(scores):
    sum_points = sum(scores.values())
    if sum_points != 100:
        max_value_key = max(scores, key=scores.get)
        scores[max_value_key] += MAX_PERCENT - sum_points
    return scores
