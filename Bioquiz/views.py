from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse

from .models import Question,Image,Answer,UserDetails
from django.contrib.auth.models import User

from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import authenticate, login as l, logout

import re


def get_categories(): 
    categories = Question.objects.values('category').distinct()
    categories = list(categories) if categories else []
    categories = [cat['category'] for cat in categories]
    return categories

def get_user_score(name):
    user = User.objects.values('id').filter(username=name)[0]
    score = UserDetails.objects.values('score').filter(user_id=1)[0]
    return dict(score)['score']



def list_Question(request):
    q_id=int(request.GET['q_id'])-1
    questions = Question.objects.values().filter(category=request.GET['category'])
    answers = Answer.objects.values().filter(question_id=2)
    question_answers=[]
    for question in questions:
        answers = Answer.objects.values().filter(question_id=question['id'])
        images = Image.objects.values().filter(id__in=[int(img) for img in question['id_images'].split(',')])
        question_answers.append({'question':question,'answers':answers,'images':[image['image_file'] for image in images]})

    if q_id < len(question_answers):
        return render(request,'questions/question.html',{'qa':question_answers[int(q_id)],'length':len(question_answers),'q_id':q_id+1})
    return redirect('home')


def check_answer(request):
    question_id = request.GET['question']
    answer_id = int(request.GET['answer'])
    points = Question.objects.values('point').get(id=question_id)
    correct_answer_id = Question.objects.values('Correct_answer').get(id=question_id)
    correct_anwer = Answer.objects.values().get(id=correct_answer_id['Correct_answer'])
    u = UserDetails.objects.get(user_id=request.user.id)

    print(correct_answer_id,answer_id)
    if answer_id == correct_answer_id['Correct_answer']:
        print(request.user.id)
        u.score = u.score + int(points['point'])
        u.save()
        return JsonResponse({'val':True,'answer':dict(correct_anwer)})
    u.score = u.score - int(points['point'])
    u.save()
    return JsonResponse({'val':False,'answer':dict(correct_anwer)})






def get_images(request): 
    try:
        images = Image.objects.all().values().filter(image_name__in=re.findall(r'\d+', request.GET['images']))
        return render(request,'images/images.html',{'images':images})
    except:
        pass
    images = Image.objects.all().values()
    return render(request,'images/images.html',{'images':images})
#Routes
def index(request):
    if request.user.is_authenticated:
        categories,score = get_categories(),get_user_score(request.user)
        print("categories",categories)
        print("here im authenticated as",request.user)
        return render(request,'index.html',{'user':request.user,'categories':categories,'score':score,'connected':True})
    categories = get_categories()
    return render(request,'index.html',{'categories':categories})

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        r_form = UserCreationForm()
        print(r_form)
        if form.is_valid():
            user = authenticate(username=request.POST['username'], password=request.POST['password'])
            l(request,user)
            categories,score = get_categories(),get_user_score(request.POST['username'])
            return  redirect('home')
    else:
        form = AuthenticationForm()
        r_form = UserCreationForm()
    return render(request,'login.html',{'form':form,'r_form':r_form})

def register(request):
    if request.method == 'POST':
        r_form = UserCreationForm(data=request.POST)
        form = AuthenticationForm()
        print((form.base_fields))
        if r_form.is_valid():
            r_form.save()
            user = authenticate(username=request.POST['username'], password=request.POST['password1'])
            l(request,user)
            categories,score = get_categories(),get_user_score(request.POST['username']) 
            return  render(request,'index.html',{'user':request.POST['username'],'categories':categories,'score':score,'connected':True})
        else:
            return render(request,'login.html',{'form':form,'r_form':r_form})

def logout_user(request):
    logout(request)
    categories = get_categories()
    return  render(request,'index.html',{'categories':categories})