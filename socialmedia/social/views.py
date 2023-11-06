from django.views.generic import CreateView, UpdateView, DeleteView,DetailView
from django.urls import reverse_lazy
from .models import Friendship, Group, GroupPost, GroupMembership, JoinRequest
from .forms import FriendshipForm, GroupForm, GroupPostForm
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect, render
from django.http import Http404, HttpResponseRedirect
from profiles.models import Profile
from django.db import models


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

# class FollowUserView(CreateView):
#     model = Follow
#     form_class = FollowForm
#     template_name = 'social/follow_form.html'

#     def form_valid(self, form):
#         form.instance.follower = self.request.user
#         return super().form_valid(form)

#     def get_success_url(self):
#         return reverse_lazy('profiles:profile', kwargs={'pk': self.object.follower.pk})

# class UnfollowUserView(DeleteView):
#     model = Follow
#     template_name = 'social/unfollow_confirm.html'

#     def get_success_url(self):
#         return reverse_lazy('profiles:profile', kwargs={'pk': self.object.follower.pk})

# group 

class CreateGroup(CreateView):
    template_name = 'groups.html'

    def get(self, request):
        form = GroupForm()  # Tạo một mẫu trống để hiển thị
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = GroupForm(request.POST, request.FILES)  # Truyền dữ liệu từ POST và FILES vào mẫu
        if form.is_valid():
            group = form.save()  # Lưu nhóm vào cơ sở dữ liệu
            # group.creator = self.request.user
            GroupMembership.objects.create(user=self.request.user, group=group)
            return redirect('group_posts', group_id=group.id)  # Chuyển hướng đến trang bài viết của nhóm vừa tạo

        return render(request, self.template_name, {'form': form})

class CreateGroupPostView(CreateView):
    model = GroupPost
    form_class = GroupPostForm
    template_name = 'create_group_post.html'

    def form_valid(self, form):
        group_id = self.kwargs.get('group_id')
        group = get_object_or_404(Group, id=group_id)
        post = form.save(commit=False)
        post.group = group
        post.author = self.request.user
        post.save()
        return super().form_valid(form)
    
    def get_success_url(self):
        group_id = self.kwargs.get('group_id')
        return reverse_lazy('group_posts', args=[group_id])

def Group_Posts(request, group_id):
    # Lấy thông tin nhóm dựa trên group_id
    group = Group.objects.get(id=group_id)
    
    # Lấy tất cả bài viết thuộc nhóm đó
    posts = GroupPost.objects.filter(group=group)

    group_list = request.user.custom_groups.all()
    
    context = {
        'group': group,
        'posts': posts,
        'group_list':group_list
    }
    
    return render(request, 'group_posts.html', context)

class JoinGroupView(CreateView):
    def get(self, request, group_id):
        group = Group.objects.get(id=group_id)
        # Kiểm tra xem người dùng đã gửi yêu cầu trước đó chưa
        request_sent = JoinRequest.objects.filter(user=request.user, group=group, is_approved=False).exists()
        if not request_sent:
            join_request = JoinRequest(user=request.user, group=group)
            join_request.save()
        return redirect('group-detail', group_id=group_id)
    
class ApproveJoinRequestView(CreateView):
    def get(self, request, request_id):
        join_request = JoinRequest.objects.get(id=request_id)
        # Kiểm tra xem người đăng nhập có quyền phê duyệt yêu cầu không (là người tạo nhóm)
        if join_request.group.creator == request.user:
            join_request.is_approved = True
            join_request.save()
        return redirect('group-detail', group_id=join_request.group.id)