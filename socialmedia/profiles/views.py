# profiles/views.py
from django.views.generic import DetailView, CreateView, UpdateView
from .models import Profile
from .forms import ProfileForm
from social.models import Friendship  
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from authentication.models import User
from posts.models import Post

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

        # Lấy danh sách bạn bè
        friends = Friendship.objects.filter( user1=self.request.user, user2=self.object.user,status = 'Friends')
        friends = User.objects.filter(
            Q(friendships1__user2=self.object.user, friendships1__status='friends') |
            Q(friendships2__user1=self.object.user, friendships2__status='friends')
        ).distinct()[:6]
        num_friends = friends.count()
        post_list = Post.objects.filter(user=self.object.user).order_by('-created_at')

        context['friendship'] = friendship
        context['friends'] = friends
        context['num_friends'] = num_friends
        context['post_list'] = post_list
        print(friendship)
        return context  


class ProfileCreateView(CreateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'profiles/profile_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class ProfileUpdateView(UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'profiles/profile_form.html'
