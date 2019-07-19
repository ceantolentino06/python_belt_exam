from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.contrib import messages
import bcrypt
from datetime import datetime, date

########## ROOT RENDER PAGE ###########
def index(request):
    context = {
        'date': date.today().strftime("%Y-%m-%d")
    }
    return render(request, 'my_app/index.html', context)

########## LOGIN PROCESS ROUTE ########
def login(request):
    result = User.objects.filter(email = request.POST['login_email'])
    if len(result) > 0:
        if bcrypt.checkpw(request.POST['login_password'].encode(), result[0].password.encode()):
            request.session['id'] = result[0].id
            request.session['fname'] = result[0].first_name
            messages.add_message(request, messages.INFO, 'Successfully logged in!', extra_tags='userflash')
            return redirect('/success')
    
    messages.add_message(request, messages.INFO, 'Login Failed', extra_tags="loginError")
    print('no')
    return redirect('/')

########## SUCCESS RENDER PAGE ##########
def success(request):
    if 'id' not in request.session:
        messages.add_message(request, messages.INFO, 'You need to be logged in to access the next page', extra_tags="successError")
        return redirect('/')
    else:
        user = User.objects.get(id=request.session['id'])
        context = {
            'user': user,
            'jobs': Job.objects.exclude(users_who_added=user)
        }
        return render(request, 'my_app/succes.html',context)

########## REGISTER PROCESS ROUTE ###########
def register(request):
    errors = User.objects.basic_validator(request.POST)

    if len(errors):
        for tag, error in errors.items():
            messages.error(request, error, extra_tags=tag)
        return redirect('/')
    else:
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        birthday = request.POST['bday']
        hashed = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())

        print(birthday)

        newUser = User.objects.create(first_name=fname, last_name=lname, birthday=birthday, email=email, password=hashed)

        request.session['id'] = newUser.id
        request.session['fname'] = newUser.first_name
        messages.add_message(request, messages.INFO, 'User successfully created!', extra_tags="userflash")
        return redirect('/success')

########## CREATE JOB RENDER ROUTE ##########
def render_create(request):

    return render(request, 'my_app/create.html')

########## CREATE JOB POST ROUTE ############
def add_job(request):
    errors = Job.objects.job_validator(request.POST)
    if len(errors):
        for tag, error in errors.items():
            messages.error(request, error, extra_tags=tag)
        print(request.POST.getlist('cat'))
        return redirect('/jobs/new')
    else:
        categories = request.POST.getlist('cat')
        if '' in categories:
            categories.pop(categories.index(''))
        if (len(categories)) == 0:
            messages.add_message(request, messages.ERROR, 'Please provide a category', extra_tags="jobcat")
            return redirect('/jobs/new')
        else:
            print(categories)
            cat_to_add = ','.join(categories)
            print(cat_to_add)
            user = User.objects.get(id=request.POST['userID'])
            title = request.POST['title']
            desc = request.POST['desc']
            location = request.POST['location']

        Job.objects.create(title=title, description=desc, location=location, created_by=user, category=cat_to_add)
        return redirect('/success')

############ EDIT JOB RENDER ROUTE ############
def render_edit(request, job_id):
    context = {
        'job': Job.objects.get(id=job_id)
    }
    return render(request, 'my_app/edit.html', context)

############ EDIT JOB POST ROUTE #############
def edit_job(request):
    errors = Job.objects.job_validator(request.POST)

    if len(errors):
        for tag, error in errors.items():
            messages.error(request, error, extra_tags=tag)
        return redirect('/jobs/edit/'+str(request.POST['job_id']))
    else:
        job = Job.objects.get(id=request.POST['job_id'])
        job.title = request.POST['title']
        job.description = request.POST['desc']
        job.location = request.POST['location']
        job.updated_at = datetime.today()
        job.save()
        return redirect('/success')

############ VIEW JOB RENDER ROUTE ###########
def render_view(request, job_id):
    job =  Job.objects.get(id=job_id)
    categories = job.category.split(',')
    if '' in categories:
        categories.pop(categories.index(''))
    cat_to_add = ''
    for i in range(len(categories)):
        if i == len(categories)-1:
            cat_to_add += categories[i]
        else:
            cat_to_add += categories[i] + ", "
    print(cat_to_add)
    context = {
        'job': job,
        'user': User.objects.get(id=request.session['id']),
        'categories': cat_to_add
    }
    return render(request, 'my_app/view.html', context)

########### DELETE JOB ROUTE ###########
def delete_job(request, job_id):
    job = Job.objects.get(id=job_id)
    job.delete()

    return redirect('/success')

########### ADD JOB ROUTE ############
def add_user_job(request, job_id):
    user = User.objects.get(id=request.session['id'])
    job = Job.objects.get(id=job_id)
    user.my_jobs.add(job)
    user.save()
    messages.add_message(request, messages.INFO, 'Job Added!', extra_tags="jobadd")
    return redirect('/success')

########### GIVE UP JOB ROUTE ###########
def remove_user_job(request, job_id):
    user = User.objects.get(id=request.session['id'])
    job = Job.objects.get(id=job_id)
    user.my_jobs.remove(job)
    user.save()
    messages.add_message(request, messages.INFO, 'Job removed!', extra_tags="jobadd")
    return redirect('/success')

########## REMOVE SESSION #############
def logout(request):
    del request.session['id']
    del request.session['fname']
    return redirect('/')
