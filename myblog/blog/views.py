from django.shortcuts import render

# Create your views here.
# blog/views.py
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Comment
from .form import SearchForm
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth import login, logout
from django.urls import reverse
from django.urls import reverse_lazy
from django.contrib.auth.forms import AuthenticationForm

def logout_view(request):
    logout(request)
    return redirect(reverse('home'))
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('blog:post_list')  # Redirect to your post list view
    else:
        form = AuthenticationForm(request)
    return render(request, 'blog/login.html', {'form': form})
def home(request):
    return render(request, 'blog/default.html')
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

class PostCreateView(CreateView):
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'content']
    success_url = reverse_lazy('blog:post_list')  # Redirect to your post list view

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(UpdateView):
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'content']
    success_url = reverse_lazy('blog:post_list')

class PostDeleteView(DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('blog:post_list')


def search_view(request):
    form = SearchForm(request.GET)
    query = request.GET.get('query', '')
    posts = Post.objects.filter(Q(title__icontains=query) | Q(content__icontains=query))

    context = {'form': form, 'query': query, 'posts': posts}
    return render(request, 'blog/search_results.html', context)

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = Comment.objects.filter(post=post)

    if request.method == 'POST':
        text = request.POST.get('text', '')
        if text:
            comment = Comment(user=request.user, post=post, text=text)
            comment.save()
            messages.success(request, 'Comment added successfully!')

            # Fetch comments again after adding a new comment
            comments = Comment.objects.filter(post=post)

    

@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        text = request.POST.get('text', '')
        if text:
            comment = Comment(user=request.user, post=post, text=text)
            comment.save()

    # Fetch comments again after adding a new comment
    comments = Comment.objects.filter(post=post)

    # Redirect back to post_detail page with comments in the context
    return render(request, 'blog/post_detail.html', {'post': post, 'comments': comments})

@login_required
def toggle_share(request, pk):
    post = get_object_or_404(Post, pk=pk)
    
    if request.method == 'POST':
        user = request.user
        if user in post.shares.all():
            post.shares.remove(user)
        else:
            post.shares.add(user)
            messages.success(request, 'Post shared successfully!')

    # Redirect back to post_detail page
    return redirect('blog:post_detail', pk=post.pk)

def profile(request):
    return render(request, 'blog/profile.html')

