# profiles/views.py
from django.views.generic import DetailView, CreateView, UpdateView
from .models import Profile
from .forms import ProfileForm
from social.models import Friendship, Follow # Đảm bảo rằng bạn đã import model Friendship
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy, reverse
from authentication.models import User
from posts.models import Post

class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'profiles/profile_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        friendship = Friendship.objects.filter(
            (Q(user1=self.request.user, user2=self.object.user)) |
            (Q(user2=self.request.user, user1=self.object.user))
        )

        follows = Follow.objects.filter(Q(follower=self.object.user))
        can_follow = Follow.objects.filter(Q(followee=self.request.user,follower=self.object.user))
        context['friendship'] = friendship
        context['follows'] = follows
        context['can_follow'] = can_follow

        friends = User.objects.filter(
            Q(friendships1__user2=self.object.user, friendships1__status='friends') |
            Q(friendships2__user1=self.object.user, friendships2__status='friends')
        ).distinct()[:6]
        num_friends = friends.count()
        post_list = Post.objects.filter(user=self.object.user).order_by('-created_at')

        context['friends'] = friends
        context['num_friends'] = num_friends
        context['post_list'] = post_list
        context['status'] = friendship.first().status if friendship else 'none'

        invite_friends = Friendship.objects.filter(
            (Q(user2=self.request.user, status='pending'))
        )
        context['invite_friends'] = invite_friends

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


    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)
    

    def get_success_url(self):
        return reverse('profiles:profile', kwargs={'pk': self.object.pk})