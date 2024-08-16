from django.http import HttpResponse,HttpResponseNotFound
from django.shortcuts import render,redirect
from django.urls import reverse
from django.template import loader

# Create your views here.

def signUp(request):
    try:
        login_url = reverse('login')
        signUp_html = f'''<div class="container">
                <h2>Signup</h2>
                <form action="/submit-signup" method="post">
                    <div class="form-group">
                        <label for="name">Name:</label>
                        <input type="text" id="name" name="name" required>
                    </div>
                    <div class="form-group">
                        <label for="email">Email:</label>
                        <input type="email" id="email" name="email" required>
                    </div>
                    <div class="form-group">
                        <label for="password">Password:</label>
                        <input type="password" id="password" name="password" required>
                    </div>
                    <div class="form-group">
                        <input type="submit" value="Sign Up">
                    </div>
                    <div class="form-group">
                        <p>Already have a account? <a href={login_url}>Login</a></p>
                    </div>
                </form>
            </div>'''
        return HttpResponse(signUp_html)
    except:
        return HttpResponseNotFound("Error in signup.html")

def login(request):
    try:
        signUp_url = reverse('signUp')
        login_html = f'''
        <div class="container">
                <h2>Login</h2>
                <form action="/submit-login" method="post">
                    <div class="form-group">
                        <label for="email">Email:</label>
                        <input type="email" id="email" name="email" required>
                    </div>
                    <div class="form-group">
                        <label for="password">Password:</label>
                        <input type="password" id="password" name="password" required>
                    </div>
                    <div class="form-group">
                        <input type="submit" value="Login">
                    </div>
                    <div class="form-group">
                        <p>Don't have an account? <a href={signUp_url}>Sign up</a></p>
                    </div>
                </form>
            </div>
        '''
        return HttpResponse(login_html)
    except:
        return HttpResponseNotFound("Error in login.html")

def thankyou(request):
    try:
        home_url = reverse('login')

        thankyou_html = f'''
        <div class="container">
                <h2>Thank You!</h2>
                <p>Your submission has been received successfully.</p>
                <p>We appreciate your response and will get back to you shortly.</p>
                <a href={home_url}>Return to Homepage</a>
            </div>
        '''
        return HttpResponse(thankyou_html)
    except:
        return HttpResponseNotFound("Error in thankyou.html")