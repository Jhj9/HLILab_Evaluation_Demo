import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from rouge import Rouge
from datasets import load_metric

# Create your views here.


def index(request):
    return render(request, 'main/index.html')


i = 2


def demo(request):
    global i
    i = (i + 1) % 3
    return render(request, f'main/demo{i}.html')


rouge = Rouge()
bertscore_metric = load_metric('bertscore')

@csrf_exempt
def submit(request):
    jsonObject = json.loads(request.body)
    q1_reference = "Why don't you call back later this afternoon?"
    q2_reference = "I never trust those stupid doctors."
    q3_reference = "I was really sad too, but at least I can still listen to their Cds."
    q_reference = [q1_reference, q2_reference, q3_reference]
    rouge_scores = [[0.316, 0.0, 0.095], [0.333, 0, 0], [0.250, 0.095, 0.080]]
    bert_scores = [[0.919, 0.853, 0.847], [0.917, 0.882, 0.871], [0.918, 0.861, 0.861]]

    # Calculate score
    rouge_l_f1 = 0.0
    bertscore_f1 = 0.0
    quiz = jsonObject.get('quiz') -1
    op = int(jsonObject.get('op')) -1
    if op == 3:
        answer = jsonObject.get('answer')
        score = rouge.get_scores(answer, q_reference[quiz])
        rouge_l_f1 = score[0]["rouge-l"]["f"]
        bert_score = bertscore_metric.compute(predictions=[answer], references=[q_reference[quiz]], lang="en")
        bertscore_f1 = bert_score["f1"][0]
    else:
        rouge_l_f1 = rouge_scores[quiz][op]
        bertscore_f1 = bert_scores[quiz][op]

    response = {"rouge_score": round(rouge_l_f1*100), "bert_score": round(bertscore_f1*100)}
    return JsonResponse(response)