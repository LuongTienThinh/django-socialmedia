from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from .models import Post, Comment, Reply
from .forms import PostForm, CommentForm, ReplyForm
from django.http import HttpResponseRedirect
from authentication.models import User

# Create your views here.

def index(request, page):
    post_list = Post.objects.all().order_by('-created_at')    
    return render(request, 'index.html', {'page': page,'post_list':post_list})
def home(request):
    post_list = Post.objects.all().order_by('-created_at')
    return render(request, 'index.html',{'post_list':post_list})

class AddPostView(View):
    
    template_name = 'index.html'

    def get(self, request):
        post_list = Post.objects.all()
        form = PostForm()  # Tạo một mẫu trống để hiển thị
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = PostForm(request.POST, request.FILES)  # Truyền dữ liệu từ POST và FILES vào mẫu
        if form.is_valid():
            post = form.save(commit=False)  # Tạo một bài viết nhưng chưa lưu vào cơ sở dữ liệu
            post.user = request.user  # Gán người dùng hiện tại cho bài viết

            post.save()  # Lưu bài viết vào cơ sở dữ liệu   
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        return render(request, self.template_name, {'form': form})

# Comment

class AddCommentView(View):
    def post(self, request, post_id):
        post = Post.objects.get(pk=post_id)

        form = CommentForm(request.POST) 
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()  
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

        return redirect('home1')
    
class DeleteCommentView(View):
    def get(self, request, comment_id):
        comment = Comment.objects.get(pk=comment_id)

        if request.user == comment.user:
            comment.delete()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

class EditCommentView(View):
    def post(self, request, comment_id):
        comment = get_object_or_404(Comment, pk=comment_id)

        if request.user == comment.user:
            form = CommentForm(request.POST, instance=comment)

            if form.is_valid():
                form.save()
            return redirect('home1')
        else:
            return redirect('home1')
        
# Reply

class DeleteReplyView(View):
    def get(self, request, reply_id):
        reply = Reply.objects.get(pk=reply_id)

        if request.user == reply.user:
            reply.delete()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

class EditReplyView(View):
    def post(self, request, reply_id):
        reply = get_object_or_404(Reply, pk=reply_id)

        if request.user == reply.user:
            form = ReplyForm(request.POST, instance=reply)

            if form.is_valid():
                form.save()
            return redirect('home1')
        else:
            return redirect('home1')
    
class AddReplyView(View):
    def post(self, request, comment_id):
        comment = get_object_or_404(Comment, pk=comment_id)
        reply_form = ReplyForm(request.POST)

        if reply_form.is_valid():
            content = reply_form.cleaned_data['content']
            user = request.user  # Lấy người dùng hiện tại
            reply = Reply(content=content, comment=comment, user=user)
            reply.save()
            return redirect('home1')
        return redirect('home1')
    
# Like

def Like_Post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    
    # Kiểm tra xem người dùng hiện tại đã thích bài viết chưa.
    if request.user.is_authenticated:
        if request.user in post.likes.all():
            post.likes.remove(request.user)  # Nếu đã thích, loại bỏ thích.
        else:
            post.likes.add(request.user)  # Nếu chưa thích, thêm thích.
            
    return redirect('home1')
