from django.views.generic import CreateView, UpdateView, DeleteView, View
from django.urls import reverse_lazy
from .models import Friendship, Follow
from .forms import FriendshipForm, FollowForm
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404,redirect
from django.http import Http404
from profiles.models import Profile
from django.contrib.auth.decorators import login_required



User = get_user_model()
# views.py
class SendFriendRequestView(CreateView):
    model = Friendship
    form_class = FriendshipForm

    def dispatch(self, request, *args, **kwargs):
        user2 = get_object_or_404(User, pk=kwargs['user_id'])
        user1 = request.user
        friendship, created = Friendship.objects.get_or_create(
            user1=user1,
            user2=user2,
            defaults={'status': 'pending'}
        )
        if created:
            # Yêu cầu kết bạn được tạo mới
            pass  # Bạn có thể thêm mã xử lý tại đây nếu cần
        else:
            # Yêu cầu kết bạn đã tồn tại
            pass  # Bạn có thể thêm mã xử lý tại đây nếu cần

        return redirect(reverse_lazy('profiles:profile', kwargs={'pk': user2.id}))

    def get_success_url(self):
        # Phương thức này không còn cần thiết nữa, vì chúng ta đã xử lý mọi thứ trong dispatch
        pass


class AcceptFriendRequestView(UpdateView):
    model = Friendship
    form_class = FriendshipForm

    def post(self, request, *args, **kwargs):
        friendship = get_object_or_404(Friendship, pk=kwargs['pk'])
        
        # Đảm bảo rằng người dùng hiện tại là người nhận yêu cầu kết bạn
        if friendship.user2 == request.user and friendship.status == 'pending':
            friendship.status = 'friends'
            friendship.save()

            # Tạo một đối tượng Friendship mới cho người dùng khác
            new_friendship = Friendship.objects.create(
                user1=friendship.user2,
                user2=friendship.user1,
                status='friends'
            )
        elif friendship.user1 == request.user:
            # Người dùng hiện tại là người đã gửi yêu cầu kết bạn, 
            # họ không thể chấp nhận yêu cầu kết bạn của chính họ
            raise Http404("Bạn không thể chấp nhận yêu cầu kết bạn của chính bạn.")
        else:
            # Người dùng hiện tại không liên quan đến yêu cầu kết bạn này
            raise Http404("Yêu cầu kết bạn không hợp lệ.")

        return redirect(reverse_lazy('profiles:profile', kwargs={'pk': friendship.user1.pk}))
    
    def get_success_url(self):
        # Phương thức này không còn cần thiết nữa, vì chúng ta đã xử lý mọi thứ trong post
        pass

class RejectFriendRequestView(CreateView):
    def post(self, request, pk):
        friend_request = get_object_or_404(Friendship, id=pk)        
        friend_request.delete()
        return redirect('profiles:profile', pk=friend_request.user2.profile.pk)


class FollowUserView(View):
    def dispatch(self, request, *args, **kwargs):
        _follower = get_object_or_404(User, pk=kwargs['user_id'])
        follower, created = Follow.objects.get_or_create(follower=_follower, followee=request.user)
        return redirect(reverse_lazy('profiles:profile', kwargs={'pk': _follower.pk}))

class UnfollowUserView(View):
    def dispatch(self, request, *args, **kwargs):
        try:
            _follower = get_object_or_404(User, pk=kwargs['user_id'])
            follower = Follow.objects.get(follower=_follower, followee=request.user)
            follower.delete()
        except Follow.DoesNotExist:
            raise Http404("Bạn chưa theo dõi người dùng này.")

        return redirect(reverse_lazy('profiles:profile', kwargs={'pk': _follower.pk}))
