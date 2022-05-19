from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
import random
from datasearch.models import Userreg
from .utils import sendcode

# Create your views here.
def register(request):
    request.session.save()
    sess_id = request.session.session_key
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid(): 
            user = form.save()           
            usern=form.cleaned_data['username']
            print (usern)
            obj = Userreg(sess_id=sess_id)
            obj.username = usern
            obj.save()
            return redirect('login')
            # ins = Userreg(sess_id=sess_id)
            # ins.usernm=request.POST['username']
            # ins.save()
            
        else:
            form = UserCreationForm()

    print(sess_id)
    form = UserCreationForm()
    if not Userreg.objects.filter(sess_id=sess_id).exists():
        obj = Userreg(sess_id=sess_id)
        obj.save() 
        context = {
            "form":form,
            "error":""
        }
        return render(request, "registration/registration.html", context)    
    ins = Userreg.objects.get(sess_id=sess_id)    
    context = {
        "form":form,
        "domain": ins.domain,
        "email":ins.email,
        "passres":ins.passres,
        "error":ins.errormsg,
    }
    if ins.domain=='morgan.edu':
        sendcode(ins.email, ins.passcode)
        context["error"]=""
    return render(request, "registration/registration.html", context)
    

def regemail(request):
    if request.method == 'POST': 
        sess_id = request.session.session_key
        passcode = random.randint(100000,999999)
        ins = Userreg.objects.get(sess_id=sess_id)        
        print(sess_id)       
        ins.email = request.POST['useremail']
        ins.domain = ins.email.split('@')[1]
        ins.passcode = passcode
        ins.errormsg = ins.domain+"domain is not authorized to access this application at the moment. Please check back later..."
        ins.save()
        print(ins.email.split('@'))
        
        print (str(passcode))
        return redirect('register')


def codecheck(request):
    if request.method == 'POST': 
        sess_id = request.session.session_key
        ins = Userreg.objects.get(sess_id=sess_id)        
        print(sess_id)       
        if request.POST['passcode'] == ins.passcode:
            ins.passres = 1
            ins.save()
        return redirect('register')
        # ins.dtsite = 
        # ins.searchkey = request.POST['searchkey']
        # ins.save()
        # searchkaggle(request.POST['searchkey']) 
        # # return redirect('index')
        #         obj = Userreg(sess_id=sess_id)
        # obj.save()
