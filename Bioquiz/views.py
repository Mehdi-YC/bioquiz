from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from django import forms

from .models import Question,Image,Answer,UserDetails
from django.contrib.auth.models import User

from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import authenticate, login as l, logout

import random
import re #regular expression




# since the categories are not stored in the database , 
# we need to get the distinct values from the category column in the question model
def get_categories(): 
    categories = Question.objects.values('category').distinct()
    categories = list(categories) if categories else []
    categories = [cat['category'] for cat in categories]
    return categories

#this function allows us to get the score of a user by it's username
def get_user_score(name):
    print("name : ",name)
    user = User.objects.values('id').filter(username=name)[0]
    score = UserDetails.objects.values('score').filter(user_id=user["id"])[0]
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


#this is accessed vie jquery post request to send data about the answer (valid or no) and send it
# after this , managing the user score 
#for the lvl it is automatically calculated with a trigger
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





#getting all the images data and rendering it in images page    
def get_images(request): 
    try:
        #when more infos clicked , we ge the images links , we extract the id from it and filter the images
        #to get only the images from the specific question
        images = Image.objects.all().values().filter(image_name__in=re.findall(r'\d+', request.GET['images']))
        return render(request,'images/images.html',{'images':images})
    except:
        pass
    #ense send all the images when the user clicks on gallery
    images = Image.objects.all().values()
    return render(request,'images/images.html',{'images':images})



def index(request):
    if request.user.is_authenticated:
        categories,score = get_categories(),get_user_score(request.user)
        print("categories",categories)
        print("here im authenticated as",request.user)
        return render(request,'index.html',{'user':request.user,'categories':categories,'score':score,'connected':True})
    categories = get_categories()
    return render(request,'index.html',{'categories':categories})



#manage the login register and logout
def login(request):
    if request.method == 'POST':
        #create the login and sign in forms
        form = AuthenticationForm(data=request.POST)
        r_form = UserCreationForm()
        print(r_form)
        if form.is_valid():#log the user
            #get the data from the post request form
            user = authenticate(username=request.POST['username'], password=request.POST['password'])
            l(request,user)
            #get the categories (distinct values of question's categories )
            categories,score = get_categories(),get_user_score(request.POST['username'])
            return  redirect('home')
    else:#resend the login screen wht the error
        form = AuthenticationForm()
        r_form = UserCreationForm()
    return render(request,'login.html',{'form':form,'r_form':r_form})

def register(request):
    if request.method == 'POST':
        r_form = UserCreationForm(data=request.POST)
        print(request.POST)
        form = AuthenticationForm()

        if r_form.is_valid():
            new_user = r_form.save(commit=False)
            new_user.email = request.POST["email"] 
            new_user.save()#save the user if the form is valid
            user = authenticate(username=request.POST['username'], password=request.POST['password1'])
            l(request,user)
            categories,score = get_categories(),get_user_score(request.POST['username']) 
            return  render(request,'index.html',{'user':request.POST['username'],'categories':categories,'score':score,'connected':True})
        else:
            return render(request,'login.html',{'form':form,'r_form':r_form})

def logout_user(request):#logout the user and resend it to home screen
    logout(request)
    categories = get_categories()
    return  render(request,'index.html',{'categories':categories})