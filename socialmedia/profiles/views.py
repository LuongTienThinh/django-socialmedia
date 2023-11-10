# profiles/views.py
from .models import Profile
from .forms import ProfileForm
from social.models import Friendship  
from authentication.models import User
from posts.models import Post, Share
from social.models import Group, GroupMembership, MessageGroup
from django.views.generic import DetailView, CreateView, View
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

@method_decorator(login_required(login_url='/auth/login/'), name='dispatch')
class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'profiles/profile_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Lấy đối tượng Friendship dựa trên user hiện tại và user của profile
        # Giả định rằng user1 là người gửi yêu cầu kết bạn và user2 là người nhận
        friendship = Friendship.objects.filter(
        user1=self.request.user, user2=self.object.user
        ).first() or Friendship.objects.filter(
        user1=self.object.user, user2=self.request.user
        ).first()

        # hiển thị thông báo
        groups = Group.objects.filter(creator=self.request.user)
        memberships = GroupMembership.objects.filter(
            group__in=groups,
            status='requested'
        )
        # Lấy các group_ids mà có thông báo
        group_ids_with_messages = memberships.values_list('group', flat=True)
        messages = MessageGroup.objects.filter(group__in=group_ids_with_messages)

        # Lấy danh sách bạn bè
        friends = Friendship.objects.filter( user1=self.request.user, user2=self.object.user,status = 'Friends')
        friends = User.objects.filter(
            Q(friendships1__user2=self.object.user, friendships1__status='friends') |
            Q(friendships2__user1=self.object.user, friendships2__status='friends')
        ).distinct()[:6]
        num_friends = friends.count()
        post_list = Post.objects.filter(user=self.object.user).order_by('-created_at')
        shared_posts = Share.objects.filter(user=self.object.user).order_by('shared_at')

        profile = Profile.objects.get(user=self.object.user)
        form = ProfileForm(instance=profile)

        context['friendship'] = friendship
        context['friends'] = friends
        context['num_friends'] = num_friends
        context['post_list'] = post_list
        context['shared_posts'] = shared_posts
        context['form'] = form
        context['messages'] = messages
        return context
    
class ProfileCreateView(CreateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'profiles/profile_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class ProfileUpdateView(View):
    template_name = 'profiles/profile_update.html'

    @login_required(login_url='/auth/login/')
    def post(self, request, pk):
        profile = get_object_or_404(Profile, pk=pk, user=request.user)
        form = ProfileForm(request.POST, request.FILES, instance=profile)

        if form.is_valid():
            updated_profile = form.save()
            return redirect('profiles:profile', pk=request.user.id)

        return render(request, self.template_name, {'form': form})
