from django.shortcuts import render
from django.utils import timezone
from .models import Post
from django.shortcuts import render, get_object_or_404
from .forms import PostForm
from django.shortcuts import redirect

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})


def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user

            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user


            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})


def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})




def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)


def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')



def calculator(request):

    return render(request, 'blog/calculator.html')


def calc(request):

    val1 = int(request.POST['val1'])

    val2 = int(request.POST['val2'])

    answer_add = val1 + val2

    answer_sub = val1 - val2

    answer_mult = val1 * val2

    if val2 == 0:
        answer_div = "NAN"
    else:
        answer_div = val1/val2

    context = {
        'val1_add':val1,
        'val2_add':val2,

        'val1_sub':val1,
        'val2_sub':val2,

        'val1_mult':val1,
        'val2_mult':val2,

        'val1_div':val1,
        'val2_div':val2,



        'answer_add': answer_add,
        'answer_sub': answer_sub,
        'answer_mult': answer_mult,
        'answer_div': answer_div,

    }

    return render(request, 'blog/calculator.html', context)
