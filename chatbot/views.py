from django.shortcuts import render, redirect      # 12.4) Importing redirect
from django.http import JsonResponse            # 9)
import openai

from django.contrib import auth                 # 12.1) for logout
from django.contrib.auth.models import User      # 12.3) will give us access to Django User module

from .models import Chat                       # 18)
from django.utils import timezone

# Create your views here.

#10) OpenAI API key
openai_api_key = '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'
openai.api_key = openai_api_key


# 11) A function which will sends a request to openAI API and will get response from that API
def ask_openai(message):
    response = openai.Completion.create(
        model = "text-davinci-003",
        prompt = message,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.7,
    )
    # 11) We are returning the response of the chatbot, now it is interactive.
    # print(response)
    answer = response.choices[0].text.strip()       
    return answer                                  

    

# 4) Creating our first view function
def chatbot(request):

    # 19) Chat history
    chats = Chat.objects.filter(user=request.user)  # returns all the chat data from db and store it in the variable named 'chats'
     # Now we will pass it in the end of this function in 'return render....'

    # 9)
    if request.method == 'POST':
        message = request.POST.get('message')
        response = ask_openai(message)               # 11.1)
        
        chat = Chat(user=request.user, message=message, response=response, created_at=timezone.now())        # 18
        chat.save()            # 18
        return JsonResponse({'message': message, 'response': response})
    return render(request, 'chatbot.html', {'chats': chats})         # we added 'templates' in 'DIRS' in settings.py so now Django knows where to find the html files


# 12) Creating a 'login', 'register', 'logout' function
def login(request):

    # 14) 
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:           # If the user is not an invalid user
            auth.login(request,user)
            return redirect('chatbot')
        else:
            error_message = 'Invalid username or password'
            return render(request, 'login.html',{'error_message':error_message})
    
    else:
        return render(request,'login.html')

def register(request):
    # 12.2)
    if request.method == 'POST':
        username = request.POST['username']      # Initialising the variable 'username' with the value we entered while registering in our register.html 
        email = request.POST['email']
        password1 = request.POST['password1'] 
        password2 = request.POST['password2'] 
        
        # 12.3) Matching both the passwords
        if password1 == password2:
            try:
                user = User.objects.create_user(username, email, password1)  # Creating new user
                user.save()                                                  # Saves the user object in db
                auth.login(request,user)                                     # login the user
                return redirect('chatbot')                                   # redirect to chatbot
            except:
                error_message = 'Error creating account'
                return render(request,'register.html',{'error_message':error_message})               
        else:
            error_message = 'Password dont match'
            return render(request, 'register.html',{'error_message': error_message})
    return render(request,'register.html')

def logout(request):
    auth.logout(request)      # This allows us to logout
                              # Now to use it, we will import auth above
    
    return redirect('login')                          