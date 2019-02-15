from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from .models import UserTotalScore, User, UserEvent, UserTotalScore
import numpy as np
import hashlib
import uuid

# Create your views here.
def index(request):
    return render(request, 'mainapp/index.html')

def login_html(request):
    return render(request, 'mainapp/login.html')

def auth_user(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return JsonResponse({"msg": "", "success": True})
    else:
        msg = "cannot login user {}".format(username)
        return JsonResponse({"msg": msg, "success": False})

def register_html(request):
    return render(request, 'mainapp/register.html')

def menu_html(request):
    return render(request, 'mainapp/menu.html')

def logout_view(request):
    logout(request)

def questions(request):
    return render(request, 'mainapp/questions.html')

def answer_result(request):
    return render(request, 'mainapp/answer_result.html')

def prize(request):
    return render(request, 'mainapp/prize.html')

def leaderboard(request):
    return render(request, 'mainapp/leaderboard.html')

def generate_invite_code(text):
    text = text.encode("utf-8")
    m = hashlib.sha256()
    m.update(text)
    result = m.hexdigest()
    code = result[:5]
    count = User.objects.filter(invite_code=code).count()
    if count == 0:
        return code
    else:
        new_text = text + "_"
        return generate_invite_code(new_text)

def create_user(request):
    username = request.POST["username"]
    password = request.POST["password"]
    name = request.POST["name"]
    phone = request.POST["phone"]
    address = request.POST["address"]
    code = request.GET.get("member", "")
    found = User.objects.filter(invite_code=code).count() > 0
    invite_code = generate_invite_code(username)
    if code and found:
        inviter = User.objects.get(invite_code=code)
        user = User.objects.create(username=username,
            password=password,
            name=name,
            phone=phone,
            address=address,
            invited_by=inviter,
            invite_code=invite_code
        )
        invite_bonus = 100
        inviter_row = User.objects.get(invite_code=code)
        inviter_event_row = UserEvent.objects.create(user=inviter_row, event_type="invite",
            score=invite_bonus)
        inviter_score_row = UserTotalScore.objects.get_or_create(user=inviter_row)
        inviter_score_row.total_score = inviter_score_row.total_score + invite_bonus
        inviter_score_row.save()
    else:
        user = User.objects.create(username=username,
            password=password,
            name=name,
            phone=phone,
            address=address,
            invite_code=invite_code
        )
    return JsonResponse({"msg": "", "success": True})

@login_required(login_url="/mainapp/login/")
def get_random_questions(request):
    num = 5
    question_ids = Question.objects.values_list('id', flat=True)
    sample_ids = np.random.choice(question_ids, num, replace=False)
    question_rows = Question.objects.filter(id__in=sample_ids)
    result = []
    for question_row in question_rows:
        question_id = question_row.id
        question_text = question_row.question_text
        count_down = question_row.count_down
        score = question_row.score
        option_rows = question_row.options.all()
        options = []
        for option_row in option_rows:
            options.append({
                "label": option_row.label,
                "option_text": option_row.option_text
            })

        result.append({
            "question_id": question_id,
            "question_text": question_text,
            "count_down": count_down,
            "score": score,
            "options": options
        })
    return JsonResponse({"msg": "", "success": True, "result": result})

@login_required(login_url="/mainapp/login/")
def submit_answer(request):
    user = request.user
    question_id = request.POST["question_id"]
    answer_label = request.POST["answer_label"]
    question_row = Question.objects.get(pk=question_id)
    correct_label = question_row.options.get(is_correct=True).label
    option_row = question_row.options.get(label=answer_label)
    user_answer_row = UserAnswer(user=user, answer=option_row)
    user_answer_row.save()
    if correct_label == answer_label:
        user_event_row = UserEvent(user=user, event_type="answer",
            score=question_row.score, user_answer=user_answer_row)
        user_event_row.save()
        user_score_row = UserScore.objects.get_or_create(user=user)
        user_score_row.total_score = user_score_row.total_score + question_row.score
        user_score_row.save()
    else:
        user_event_row = UserEvent(user=user, event_type="answer",
            score=0, user_answer=user_answer_row)
        user_event_row.save()
    return JsonResponse({"msg": "", "success": True})

@login_required(login_url="/mainapp/login/")
def get_top_players(request):
    NUM = 10
    leader_rows = UserTotalScore.objects.order_by('-total_score')[:10]
    result = []
    for row in leader_rows:
        username = user.username
        result.append({"username": username,
            "score": user.total_score
        })
    return JsonResponse({"msg": "", "success": True, "result": result})
