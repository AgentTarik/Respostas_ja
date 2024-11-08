from django.shortcuts import render

# Create your views here.

def logindapag (request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        print (f'Usuario:{username}, Senha:{password}')
    return render (request,'login.html')
    