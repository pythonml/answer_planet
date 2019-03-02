from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from .models import UserTotalScore, User, UserEvent, UserAnswer, UserTotalScore, Question, Option
import numpy as np
import hashlib
import uuid

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return redirect('menu')
    else:
        return redirect('login')

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
        msg = "用户名或密码不正确".format(username)
        return JsonResponse({"msg": msg, "success": False})

def register_html(request):
    return render(request, 'mainapp/register.html')

@login_required(login_url="/login/")
def menu_html(request):
    username = request.user.username
    return render(request, 'mainapp/menu.html', {"username": username})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required(login_url="/login/")
def questions(request):
    return render(request, 'mainapp/questions.html')

def answer_result(request):
    return render(request, 'mainapp/answer_result.html')

def prize(request):
    return render(request, 'mainapp/prize.html')

@login_required(login_url="/login/")
def leaderboard(request):
    me = request.user
    (my_score_row, _) = UserTotalScore.objects.get_or_create(user=me)
    my_score = my_score_row.total_score
    my_username = me.username

    NUM = 10
    leader_rows = UserTotalScore.objects.order_by('-total_score')[:10]
    leaders = []
    for user_score in leader_rows:
        username = user_score.user.username
        leaders.append({"username": username,
            "score": user_score.total_score
        })

    my_rank = UserTotalScore.objects.filter(total_score__gte=my_score).count()
    return render(request, 'mainapp/leaderboard.html', {
        "leaders": leaders,
        "my_score": my_score,
        "my_username": my_username,
        "my_rank": my_rank
    })

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
    name = request.POST.get("name", "")
    phone = request.POST.get("phone", "")
    address = request.POST.get("address", "")
    code = request.GET.get("member", "")

    user_exists = User.objects.filter(username=username).count() > 0
    if user_exists:
        msg = "用户{}已存在".format(username)
        return JsonResponse({"msg": msg, "success": False})

    found = User.objects.filter(invite_code=code).count() > 0
    invite_code = generate_invite_code(username)
    user = None
    if code and found:
        inviter = User.objects.get(invite_code=code)
        user = User.objects.create_user(username=username,
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
        (inviter_score_row, _) = UserTotalScore.objects.get_or_create(user=inviter_row)
        inviter_score_row.total_score = inviter_score_row.total_score + invite_bonus
        inviter_score_row.save()
    else:
        user = User.objects.create_user(username=username,
            password=password,
            name=name,
            phone=phone,
            address=address,
            invite_code=invite_code
        )
    login(request, user)
    return JsonResponse({"msg": "", "success": True})

@login_required(login_url="/login/")
def get_random_questions(request):
    num = 5
    question_ids = Question.objects.values_list('id', flat=True)
    sample_ids = np.random.choice(question_ids, num, replace=False)
    question_rows = Question.objects.filter(id__in=sample_ids)
    questions = []
    for question_row in question_rows:
        question_id = question_row.id
        question_text = question_row.question_text
        count_down = question_row.count_down
        score = question_row.score
        option_rows = question_row.options.order_by('label')
        options = []
        for option_row in option_rows:
            options.append({
                "option_id": option_row.id,
                "label": option_row.label,
                "option_text": option_row.option_text
            })

        questions.append({
            "question_id": question_id,
            "question_text": question_text,
            "count_down": count_down,
            "score": score,
            "options": options
        })
    (user_score_row, _) = UserTotalScore.objects.get_or_create(user=request.user)
    user_score = user_score_row.total_score
    result = {"questions": questions, "user_score": user_score}
    return JsonResponse({"msg": "", "success": True, "result": result})

@login_required(login_url="/login/")
def submit_answer(request):
    user = request.user
    option_id = int(request.POST["option_id"])
    option_row = Option.objects.get(pk=option_id)
    question_row = option_row.question
    user_answer_row = UserAnswer(user=user, question=question_row, answer=option_row)
    user_answer_row.save()

    if option_row.is_correct:
        user_event_row = UserEvent(user=user, event_type="answer",
            score=question_row.score, user_answer=user_answer_row)
        user_event_row.save()
        (user_score_row, _) = UserTotalScore.objects.get_or_create(user=user)
        user_score_row.total_score += question_row.score
        user_score_row.save()
    else:
        user_event_row = UserEvent(user=user, event_type="answer",
            score=0, user_answer=user_answer_row)
        user_event_row.save()
    correct_row = question_row.options.filter(is_correct=True)[0]
    result = {"is_correct": option_row.is_correct, "correct_option": correct_row.id}
    return JsonResponse({"msg": "", "success": True, "result": result})
