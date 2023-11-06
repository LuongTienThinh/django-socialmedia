from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from .models import Post, Comment, Reply
from .forms import PostForm, CommentForm, ReplyForm
from django.http import HttpResponseRedirect, JsonResponse
from authentication.models import User
from social.models import Group, GroupPost
from django.db.models import Q
# Create your views here.

def index(request, page):
    friends = User.objects.filter(
            Q(friendships1__user2=request.user, friendships1__status='friends') |
            Q(friendships2__user1=request.user, friendships2__status='friends')
        ).distinct()
    num_friends = friends.count()
    post_list = Post.objects.all().order_by('-created_at') 
    group_list = request.user.custom_groups.all()
    group_post = GroupPost.objects.all()
    if page == 'home':
        return render(request, 'index.html', {'page': page,'post_list':post_list, 'group_list':group_list})
    elif page == 'friend':
        return render(request, 'friends.html', {'page': page, 'post_list':post_list, 'friends':friends, 'num_friends':num_friends})
    else:
        return render(request, 'groups.html', {'page': page, 'post_list':post_list, 'group_list':group_list, 'group_post':group_post })

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

            # Trả về phản hồi JSON với thông tin comment mới (nếu cần)
            response_data = {
                'comment_id': comment.id,
                'content': comment.content,
                'user': comment.user.username,
                'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M:%S')
            }
            return JsonResponse(response_data)

        return JsonResponse({'error': 'Invalid form data'})
    
class DeleteCommentView(View):
    def post(self, request, comment_id):
        comment = Comment.objects.get(pk=comment_id)

        if request.user == comment.user:
            comment.delete()

            response_data = {'message': 'Comment deleted successfully'}
        return JsonResponse(response_data)
    def get(self, request, comment_id):
        comment = Comment.objects.get(pk=comment_id)

        if request.user == comment.user:
            comment.delete()

            response_data = {'message': 'Comment deleted successfully'}
        return JsonResponse(response_data)


class EditCommentView(View):
    def post(self, request, comment_id):
        comment = get_object_or_404(Comment, pk=comment_id)

        if request.user == comment.user:
            form = CommentForm(request.POST, instance=comment)

            if form.is_valid():
                form.save()
                response_data = {
                'comment_id': comment.id,
                'content': comment.content,
                'user': comment.user.username,
                'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M:%S')
            }
            return JsonResponse(response_data)
        return JsonResponse({'message': 'Permission denied'}, status=403)
        
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
    liked = False
    
    # Kiểm tra xem người dùng hiện tại đã thích bài viết chưa.
    if request.user.is_authenticated:
        if request.user in post.likes.all():
            post.likes.remove(request.user)  # Nếu đã thích, loại bỏ thích.
        else:
            post.likes.add(request.user)  # Nếu chưa thích, thêm thích.
            liked = True
    
    response_data = {
        'liked': liked,
        'total_likes': post.likes.count()
    }
    
    return JsonResponse(response_data)