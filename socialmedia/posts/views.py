from django.shortcuts import render
from django.views.generic import View, CreateView
from .models import Post
from .forms import PostForm
from django.urls import reverse_lazy, reverse

# Create your views here.

def index(request, page):
    return render(request, 'index.html', {'page': page})

class AddPostView(CreateView):
    model = Post
    form_class = PostForm

    def form_valid(self, form):
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('upload_post.html')