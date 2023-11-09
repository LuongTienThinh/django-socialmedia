# profiles/views.py
from django.views.generic import DetailView, CreateView, UpdateView
from .models import Profile
from .forms import ProfileForm
from social.models import Friendship, Follow # Đảm bảo rằng bạn đã import model Friendship
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy, reverse



class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'profiles/profile_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        friendship = Friendship.objects.filter(
        Q(user1=self.request.user) and
        Q(user1=self.object.user)
        ).first()

        follows = Follow.objects.filter(Q(follower=self.object.user))
        can_follow = Follow.objects.filter(Q(followee=self.request.user,follower=self.object.user))
        context['follows'] = follows
        context['friendship'] = friendship
        context['can_follow'] = can_follow
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

