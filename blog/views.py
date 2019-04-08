from django.shortcuts import render, get_object_or_404
# Create your views here.
from .models import Post, Journal
from .forms import PostForm
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from datetime import datetime
from django.utils import timezone

# Create your views here.
DEFAULT = datetime.strptime('Jun 1 2030  1:33PM', '%b %d %Y %I:%M%p')

def post_list(request):
    posts = Post.objects.all()
    return render(request, 'baback/post_list.html', {'posts': posts})

def post_fresh(request):
    posts = Post.objects.filter(time_death = DEFAULT, deleted = False)
    return render(request, 'baback/post_list.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    j_cancel = Journal.objects.filter(id_jp = post.id_post, deleted = False).count()
    j_list = []
    j_restore = Journal.objects.filter(id_jp = post.id_post, deleted = True).count()
    r_list = []
    for j in range(j_cancel):
        j_list.append(j)
    for r in range(j_restore):
       r_list.append(r)
    return render(request, 'baback/post_detail.html', {'post':post, 'j_list':j_list, 'r_list':r_list})

def post_new(request):
    name = 'New Post'
    ctime = datetime.now()
    posts = Post.objects.all()
    try:
        pid = Post.objects.latest('id_post').id_post
    except:
        pid = 0
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            
            post = form.save(commit=False)
            post.time_create = ctime
            post.id_post = pid+1;
            post.save()
            j = Journal.objects.create(id_jp = post.id_post, time = ctime, operation = 'INSERT')

            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'baback/post_edit.html', {'form': form, 'name':name})

def post_cancel(request, pk):
    ctime = datetime.now()
    post = get_object_or_404(Post, pk=pk)
    journal = Journal.objects.filter(id_jp = post.id_post, deleted = False)
    max_time = journal.latest('time')
    journal = max_time
    if journal.operation == 'INSERT':
        post.deleted = True
        post.save()
    elif journal.operation == 'UPDATE':
        previous_post = Post.objects.get(id_post = post.id_post, time_death = post.time_create)
        post.deleted = True
        previous_post.time_death = DEFAULT
        post.save()
        previous_post.save()
    elif journal.operation == 'DELETE':
        post.time_death = DEFAULT
        post.save()
    journal.deleted = True
    journal.save()
    #return HttpResponseRedirect("/")
    return 0

def post_restore(request, pk):
    ctime = datetime.now()
    post = get_object_or_404(Post, pk=pk)
    journal = Journal.objects.filter(id_jp = post.id_post, deleted = True)
    #journal = journal.latest('time')
    journal = journal.earliest('time')
    if journal.operation == 'INSERT':
        post.deleted = False
        post.save()
    
    elif journal.operation == 'UPDATE':
        npost = Post.objects.get(id_post = journal.id_jp, deleted = True, time_create = journal.time)
        npost.deleted = False
        post.time_death = journal.time
        post.save()
        npost.save()
    elif journal.operation == 'DELETE':
        post.time_death = journal.time
        post.save()
        
    journal.deleted = False
    journal.save()
    #return HttpResponseRedirect("/")
    return 0
        
    

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    old = post
    ctime = datetime.now()
    if request.method == "POST":
        p = Post.objects.create(id_post = old.id_post, time_create = old.time_create, time_death = ctime, row1 = old.row1, row2 = old.row2)
        form = PostForm(request.POST, instance=post)
        last = Post.objects.latest('id').id
        if form.is_valid():
            
            post  = form.save(commit = False)
            post.time_death = DEFAULT
            post.time_create = ctime
            post.save()

            j = Journal.objects.create(id_jp = post.id_post, time = ctime, operation = 'UPDATE')


            return redirect('post_detail', pk=post.pk)
    else:
         form = PostForm(instance=post)
    return render(request, 'baback/post_edit.html', {'form': form})

def post_delete(request, pk):
    ctime = datetime.now()
    post = get_object_or_404(Post, pk=pk)
    try:
        post.time_death = ctime
        post.save()

        j = Journal.objects.create(id_jp = post.id_post, time = ctime, operation = 'DELETE')
        return HttpResponseRedirect("/")
    except Post.DoesNotExist:
        return HttpResponseNotFound("<h2>Not found</h2>")


def journal_list(request):
    js = Journal.objects.all()
    return render(request, 'baback/journal_list.html', {'js': js})

def post_iter(request, pk, jk):
    #jk = int(jk)+1
    jk = int(jk)+1
    for j in range(jk):
        post_cancel(request, pk)
    return HttpResponseRedirect("/")

def post_rest(request, pk, rk):
    rk = int(rk)+1
    #rk = int(rk)
    for r in range(rk):
        post_restore(request, pk)
    return HttpResponseRedirect("/")
