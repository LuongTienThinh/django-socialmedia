# profiles/views.py
from .models import Profile
from .forms import ProfileForm
from posts.forms import PostForm
from social.models import Friendship  
from django.db.models import Q
from authentication.models import User
from posts.models import Post, Share
from django.views.generic import DetailView, CreateView, View
from social.models import Group, GroupMembership, MessageGroup, Friendship, Follow, Block
from django.db.models import Q
from itertools import chain
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

@method_decorator(login_required(login_url='/auth/login/'), name='dispatch')
class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'profiles/profile_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        friendship = Friendship.objects.filter(
        user1=self.request.user, user2=self.object.user
        ).first() or Friendship.objects.filter(
        user1=self.object.user, user2=self.request.user
        ).first()

        fs = Friendship.objects.filter(user1=self.request.user, user2=self.object.user)

        if friendship:
            status = friendship.status
        else:
            status = 'none'

        invite_friends = Friendship.objects.filter(
            Q(user2=self.request.user, status='pending')
        ).order_by('-created_at')
        post_forms = []

        friends = User.objects.filter(
            Q(friendships1__user2=self.object.user, friendships1__status='friends') |
            Q(friendships2__user1=self.object.user, friendships2__status='friends')
        ).exclude(
            # Loại bỏ người dùng đã chặn người dùng hiện tại
            id__in=Block.objects.filter(blocker=self.request.user).values('blocked_user')
        ).exclude(
            # Loại bỏ người dùng đã bị người dùng hiện tại chặn
            id__in=Block.objects.filter(blocked_user=self.request.user).values('blocker')
        ).exclude(
            # Loại bỏ người dùng hiện tại
            pk=self.request.user.id
        ).distinct()
        



        num_friends = friends.count()
        user_post_list = Post.objects.filter(user=self.object.user).order_by('-created_at')
        shared_posts = Share.objects.filter(user=self.object.user).order_by('-shared_at')

        posts = sorted(
            chain(user_post_list, shared_posts),
            key=lambda post: post.created_at if hasattr(post, 'created_at') else post.shared_at,
            reverse=True
        )

        profile = Profile.objects.get(user=self.object.user)
        formprofile = ProfileForm(instance=profile)

        all_profiles = Profile.objects.all()

        # edit group post
        post_list = Post.objects.all().order_by('-created_at')
        post_forms = []

        for post in post_list:
            current_post = Post.objects.get(id=post.id)
            form = PostForm(instance=current_post)
            
            # Thêm biểu mẫu của bài viết hiện tại vào danh sách
            post_forms.append({'post': current_post, 'form': form})

         # hiển thị thông báo
        groups = Group.objects.filter(creator=self.request.user)
        memberships = GroupMembership.objects.filter(
            group__in=groups,
            status='requested'
        )
        # Lấy các group_ids mà có thông báo
        group_ids_with_messages = memberships.values_list('group', flat=True)
        messages = MessageGroup.objects.filter(group__in=group_ids_with_messages)

        user_block = Block.objects.filter(blocker=self.request.user, blocked_user=self.object.user).exists()

        # Kiểm tra xem người dùng hiện tại có bị chặn bởi profile_user không
        is_blocked = Block.objects.filter(blocker=self.object.user, blocked_user=self.request.user).exists()       

        # danh sách người dùng bị chặn
        user_block_list = Block.objects.filter(blocker = self.request.user)

        follows = Follow.objects.filter(follower=self.object.user).exclude(
            # Loại bỏ người dùng đã chặn người dùng hiện tại
            id__in=Block.objects.filter(blocker=self.request.user).values('blocked_user')
        ).exclude(
            # Loại bỏ người dùng đã bị người dùng hiện tại chặn
            id__in=Block.objects.filter(blocked_user=self.request.user).values('blocker')
        ).exclude(
            # Loại bỏ người dùng hiện tại
            pk=self.request.user.id
        ).distinct()
        
        following = Follow.objects.filter(followee=self.object.user).exclude(
            # Loại bỏ người dùng đã chặn người dùng hiện tại
            id__in=Block.objects.filter(blocker=self.request.user).values('blocked_user')
        ).exclude(
            # Loại bỏ người dùng đã bị người dùng hiện tại chặn
            id__in=Block.objects.filter(blocked_user=self.request.user).values('blocker')
        ).exclude(
            # Loại bỏ người dùng hiện tại
            pk=self.request.user.id
        ).distinct()
        can_follow = Follow.objects.filter(Q(followee=self.request.user,follower=self.object.user))
        
        context['friends'] = friends
        context['num_friends'] = num_friends
        context['post_list'] = posts
        context['formprofile'] = formprofile
        context['friendship'] = friendship
        context['post_forms'] = post_forms
        context['messages'] = messages
        context['status'] = status
        context['profiles'] = all_profiles
        context['follows'] = follows
        context['following'] = following
        context['can_follow'] = can_follow
        context['user_block'] = user_block
        context['is_blocked'] = is_blocked
        context['invite_friends'] = invite_friends
        context['user_block_list'] = user_block_list
        context['fs'] = fs
        return context  


# add post
@method_decorator(login_required(login_url='/auth/login/'), name='dispatch')
class AddPostView(View):
    
    template_name = 'profiles/profile_form.html'

    def get(self, request):
        form = PostForm()  # Tạo một mẫu trống để hiển thị
        return render(request, self.template_name, {'form': form}, pk=request.user.id)

    def post(self, request):
        form = PostForm(request.POST, request.FILES)  # Truyền dữ liệu từ POST và FILES vào mẫu
        if form.is_valid():
            post = form.save(commit=False)  # Tạo một bài viết nhưng chưa lưu vào cơ sở dữ liệu
            post.user = request.user  # Gán người dùng hiện tại cho bài viết

            post.save()  # Lưu bài viết vào cơ sở dữ liệu   
            return redirect('profiles:profile', pk=request.user.id)
        return render(request, self.template_name, {'form': form}, pk=request.user.id)
    

# delete post
@method_decorator(login_required(login_url='/auth/login/'), name='dispatch')
class DeletePost(View):
    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id, user=request.user)
        if request.user == post.user:
            post.delete()
        return redirect('profiles:profile', pk=request.user.id)
            
    def get(self, request, post_id):
        post = get_object_or_404(Post, id=post_id, user=request.user)
        if request.user == post.user:
            post.delete()

        return redirect('profiles:profile', pk=request.user.id)

# edit post
@method_decorator(login_required(login_url='/auth/login/'), name='dispatch')
class EditPostView(View):

    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        form = PostForm(request.POST, request.FILES, instance=post)

        if form.is_valid():
            form.save()
            return redirect('profiles:profile', pk=request.user.id)
        return redirect('profiles:profile',{'form': form, 'post': post}, pk=request.user.id)

class ProfileCreateView(CreateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'profiles/profile_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

@method_decorator(login_required(login_url='/auth/login/'), name='dispatch')
class ProfileUpdateView(View):
    template_name = 'profiles/profile_detail.html'

    def post(self, request, pk):
        profile = get_object_or_404(Profile, pk=pk)
        form = ProfileForm(request.POST, request.FILES, instance=profile)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

        return redirect('profiles:profile', pk=request.user.id)
