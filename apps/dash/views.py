from django.shortcuts import render, HttpResponse, redirect

from django.contrib import messages
from .models import *
import bcrypt

def index(request):
    return render(request, "dash/index.html")

def signin(request):
    return render(request, "dash/login.html")

def register(request):
    return render(request, "dash/register.html")

def dashboard(request):
    if "user_id" not in request.session:
        return redirect('/')
    id= request.session["user_id"]
    u = User.objects.get(id=id)
    allu= User.objects.all()
    if u.user_level==9:
        return render(request, "dash/admin.html",{"users":allu})
    else:
        return render(request, "dash/dashboard.html", {"users":allu})

def wall(request,id):
    if "user_id" not in request.session:
        return redirect('/')
    
    else:
        request.session["current"]= id
        data={
            'user' : User.objects.get(id=id),
        }
        return render(request, "dash/wall.html", data)
        
def edit(request):
    if "user_id" not in request.session:
        return redirect('/')
    id = request.session["user_id"]
    userself = User.objects.get(id=id)
    return render(request, "dash/edit.html", {"userself":userself})
    
def adminedit(request,id):
    if "user_id" not in request.session:
        return redirect('/')
    userid= request.session["user_id"]
    u = User.objects.get(id=userid)

    ontable = User.objects.get(id=id)

    if u.user_level==9:
        return render(request, "dash/adminedit.html",{"ontable":ontable})
    else:
        return redirect("/edit")

def adminadd(request):
    if "user_id" not in request.session:
        return redirect('/')
    id= request.session["user_id"]
    u = User.objects.get(id=id)
    if u.user_level==9:
        return render(request, "dash/adminadd.html")
    else:
        return redirect("/dashboard")

def register_process(request):
    if request.method =="POST":
        errors = User.objects.validator(request.POST)
        request.session['first_name'] = request.POST['first_name']
        request.session['last_name'] = request.POST['last_name']
        request.session['email'] = request.POST['email']

        EmailExists= User.objects.filter(email=request.POST['email'])
        if not len(EmailExists) == 0:
            print("email exists error")
            messages.error(request, "Email " + request.POST['email'] + " is already registered")
            return redirect('/register')

        if len(errors):
            for key, value in errors.items():
                messages.error(request, value, extra_tags=key)
            return redirect('/register')
        else:
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            pwhashed = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())

            User.objects.create(first_name=first_name, last_name=last_name, email=email, password=pwhashed) 
            messages.success(request, "Successfully added")
            request.session.clear()
            return redirect('/signin')
        return redirect("/register")

def login(request):
    if request.method =="POST":
        email = request.POST['email']
        try:
            user = User.objects.get(email = email)
            if user:
                if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
                    id= user.id
                    messages.success(request, "Login Success")
                    request.session['user_id'] = id
                    return redirect('/dashboard')
                else:
                    messages.error(request, "Login Fail")
                    return redirect("/signin")
        except:
            messages.error(request, "Login Fail")
            return redirect("/signin")
    return redirect("/dashboard")

def add(request):
    if request.method =="POST":
        errors = User.objects.validator(request.POST)
        request.session['first_name'] = request.POST['first_name']
        request.session['last_name'] = request.POST['last_name']
        request.session['email'] = request.POST['email']

        EmailExists= User.objects.filter(email=request.POST['email'])
        if not len(EmailExists) == 0:
            print("email exists error")
            messages.error(request, "Email " + request.POST['email'] + " is already registered")
            return redirect('/add')

        if len(errors):
            for key, value in errors.items():
                messages.error(request, value, extra_tags=key)
            return redirect('/add')
        else:
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            pwhashed = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())

            User.objects.create(first_name=first_name, last_name=last_name, email=email, password=pwhashed) 
            messages.success(request, "Successfully added")
            return redirect("/dashboard")
        return redirect("/add")

def update(request,id):
    if id == request.session["user_id"]:
        if request.method == "POST":
            heyerrors = User.objects.infovalidator(request.POST)
            if len(heyerrors):
                for key, value in heyerrors.items():
                    messages.error(request, value)
                return redirect('/edit')
            
            else:
                EmailExists= User.objects.filter(email=request.POST['email'])
                if not len(EmailExists) == 0:
                    print("email exists error")
                    messages.error(request, "Email " + request.POST['email'] + " is already registered")
                    return redirect('/edit')
                user = User.objects.get(id = id)
                user.first_name = request.POST['first_name']
                user.last_name = request.POST['last_name']
                user.email = request.POST['email']
                user.save()
                messages.success(request, "User successfully updated")
                return redirect('/dashboard')
        else:
            return redirect("/dashboard")
    else: 
        return redirect("/dashboard")

def adminupdate(request,id):
    checkid= request.session["user_id"]
    u = User.objects.get(id=checkid)
    if not u.user_level==9:
        return redirect("/dashboard")
    else:
        if request.method == "POST":
            heyerrors = User.objects.infovalidator(request.POST)
            if len(heyerrors):
                for key, value in heyerrors.items():
                    messages.error(request, value)
                return redirect('/adminedit/'+id)
            else:
                EmailExists= User.objects.filter(email=request.POST['email'])
                if not len(EmailExists) == 0:
                    print("email exists error")
                    messages.error(request, "Email " + request.POST['email'] + " is already registered")
                    return redirect('/adminedit/'+id)
                user = User.objects.get(id = id)
                user.first_name = request.POST['first_name']
                user.last_name = request.POST['last_name']
                user.email = request.POST['email']
                user.user_level = request.POST['user_level']
                user.save()
                messages.success(request, "User successfully updated")
                return redirect('/dashboard')
        return redirect("/dashboard")

def updatepassword(request,id):
    if id == request.session["user_id"]:
        if request.method == "POST":
            heyerrors = User.objects.passvalidator(request.POST)
            if len(heyerrors):
                for key, value in heyerrors.items():
                    messages.error(request, value)
                return redirect('/edit')
            else:
                pwhashed = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
                user = User.objects.get(id = id)
                user.password = pwhashed
                user.save()
                messages.success(request, "User successfully updated")
                return redirect('/dashboard')
        return redirect("/dashboard")    
    else:
        return redirect("/dashboard")

def adminupdatepassword(request,id):
    if request.method == "POST":
        heyerrors = User.objects.passvalidator(request.POST)
        if len(heyerrors):
            for key, value in heyerrors.items():
                messages.error(request, value)
            return redirect('/adminedit/'+id)
        else:
            pwhashed = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
            user = User.objects.get(id = id)
            user.password = pwhashed
            user.save()
            messages.success(request, "User successfully updated")
            return redirect('/dashboard')
    return redirect("/dashboard")

def updatestatus(request,id):
    if id == request.session["user_id"]:
        if request.method == "POST":
            user = User.objects.get(id = id)
            user.status = request.POST['status']
            user.save()
            messages.success(request, "Status successfully updated")
            return redirect('/dashboard')
        return redirect("/dashboard")    
    else:
        return redirect("/dashboard")

def message(request,id):
    if "user_id" not in request.session:
            return redirect('/')
    else: 
        if request.method == "POST":
            content= request.POST["content"]
            if len(content) == 0:
                messages.error(request, "Message can not be empty")
                return redirect("/wall/"+id)
            else:
                sender_id= request.session['user_id']
                this_author= User.objects.get(id=sender_id)
                this_receiver= User.objects.get(id = id)
                Message.objects.create(messagecontext=content, author=this_author, receiver = this_receiver)
                return redirect("/wall/"+id)
    return redirect("/")

def comment(request,id):
    if "user_id" not in request.session:
        return redirect('/')
    else: 
        if request.method == "POST":
            current = request.session['current']            
            content= request.POST["content"]
            if len(content) == 0:
                messages.error(request, "Message can not be empty you fuck")
                return redirect('/wall/'+current)
            else:
                sender_id= request.session['user_id']                
                this_message= Message.objects.get(id=id)
                this_user= User.objects.get(id=sender_id)
                Comment.objects.create(commentcontext=content, user=this_user, message=this_message)
                return redirect('/wall/'+current)
    return redirect("/")

def clear(request):
    request.session.clear()
    return redirect("/")

def remove(request,id):
    b = User.objects.get(id=id)
    b.delete()
    return redirect("/dashboard")

def deletemessage(request,id):
    if "user_id" not in request.session:
        return redirect('/')
    else:
        d= Message.objects.get(id=id)
        d.delete()
        current = request.session['current']
        return redirect('/wall/'+current)

def deletecomment(request, id):
    if "user_id" not in request.session:
        return redirect('/')
    else:
        d= Comment.objects.get(id=id)
        d.delete()
        current = request.session['current']
        return redirect('/wall/'+current)