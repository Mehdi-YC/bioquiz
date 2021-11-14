from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse

from .models import Question,Image,Answer,UserDetails
from django.contrib.auth.models import User

from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import authenticate, login as l, logout

import random
import re

# since the categories are not stored in the database , 
# we need to get the distinct values from the category column in the question model
def get_categories(): 
    categories = Question.objects.values('category').distinct()
    categories = list(categories) if categories else []
    categories = [cat['category'] for cat in categories]
    return categories

#this function allows us to get the score of a user by it's username
def get_user_score(name):
    user = User.objects.values('id').filter(username=name)[0]
    score = UserDetails.objects.values('score').filter(user_id=1)[0]
    return dict(score)['score']


#this questin auto generates questions for the 2 question models : 
#1 - get a category 
#2 - get all the possible answers for this question
#3 - select a random answer
#4 - select n images from the database that have the same value of this catgory
#5 - serve this generated question
#5 - a category has 5 questions
def list_Question(request):
    q_id=int(request.GET['q_id'])-1
    questions = Question.objects.values().filter(category=request.GET['category'])
    question_answers=[]
    for question in questions:
        answers = Answer.objects.values().filter(question_id=question['id'])
        r_answer = random.choice(answers)
        images = Image.objects.raw("select *  from Bioquiz_image where "+question['category']+"='"+r_answer['answer']+"'")

        images = random.sample(list(images), question['n_image'])
        question_answers.append({'question':question,'r_answer':r_answer,'answers':answers,'images':[image.image_file for image in images]})

    if q_id <= 5:
        return render(request,'questions/question.html',{'qa':question_answers[0],'length':5,'q_id':q_id+1})
    return redirect('home')


def check_answer(request):
    category= request.GET['category']
    question_id = request.GET['question']
    img =request.GET['img']
    user_answer = request.GET['answer']
    img_answer = Image.objects.values().get(image_file=img)
    points = Question.objects.values('point').get(id=question_id)
    u = UserDetails.objects.get(user_id=request.user.id)

    # get the correct answer
    correct_answer = Answer.objects.values().filter(answer=img_answer[category])[0]

    # adding / removing points from the user
    if img_answer[category] == user_answer:
        print(request.user.id)
        u.score = u.score + int(points['point'])
        u.save()
        return JsonResponse({'val':True,'answer':dict(correct_answer)})

    u.score = u.score - int(points['point'])
    u.save()
    return JsonResponse({'val':False,'answer':dict(correct_answer)})






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