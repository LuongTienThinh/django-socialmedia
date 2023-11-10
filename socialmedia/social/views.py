from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, View
from django.urls import reverse_lazy
from .models import Friendship, Follow, Group, GroupPost, GroupMembership,  MessageGroup
from .forms import FriendshipForm, FollowForm, GroupForm, GroupPostForm
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect, render
from django.http import Http404
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from posts.models import Post


User = get_user_model()
# views.py
@method_decorator(login_required(login_url='/auth/login/'), name='dispatch')
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


@method_decorator(login_required(login_url='/auth/login/'), name='dispatch')
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



# Group 

@method_decorator(login_required(login_url='/auth/login/'), name='dispatch')
class CreateGroup(CreateView):
    template_name = 'groups.html'

    def get(self, request):
        form = GroupForm()  # Tạo một mẫu trống để hiển thị
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = GroupForm(request.POST, request.FILES)  # Truyền dữ liệu từ POST và FILES vào mẫu
        if form.is_valid():
            group = form.save()  # Lưu nhóm vào cơ sở dữ liệu
            group.creator = self.request.user
            GroupMembership.objects.create(user=self.request.user, group=group, creator=self.request.user)
            return redirect('social:group_posts', group_id=group.id)  # Chuyển hướng đến trang bài viết của nhóm vừa tạo

        return render(request, self.template_name, {'form': form})

@method_decorator(login_required(login_url='/auth/login/'), name='dispatch')
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

        message = MessageGroup.objects.create(
            group=group,
            user=self.request.user,
            message=f"Đã thêm bài viết mới: {post.title}",
            post=post
        )

        return super().form_valid(form)
    
    def get_success_url(self):
        group_id = self.kwargs.get('group_id')
        return reverse_lazy('social:group_posts', args=[group_id])

@login_required(login_url='/auth/login/')
def Group_Posts(request, group_id):
    # Lấy thông tin nhóm dựa trên group_id
    group = Group.objects.get(id=group_id)
    
    # Lấy tất cả bài viết thuộc nhóm đó
    posts = GroupPost.objects.filter(group=group)
    # danh sách người dùng tham gia nhóm
    user_groups = GroupMembership.objects.filter(user=request.user, status='approved')
    # danh sách nhóm đã tham gia    
    groups_joined = GroupMembership.objects.filter(user=request.user, status='approved').values_list('group', flat=True)
    # danh sách nhóm bị từ chối
    groups_rejected = GroupMembership.objects.filter(user=request.user, status='rejected').values('group')
    # danh sách nhom chưa tham gia
    groups_not_joined = Group.objects.exclude(
    Q(id__in=groups_joined) | Q(id__in=groups_rejected)
    ) 
    # kiểm tra là thành viên của nhóm
    is_member = GroupMembership.objects.filter(user=request.user, group=group).exists()
    # trạng thái
    status = GroupMembership.objects.get(user=request.user, group=group).status if is_member else None

    # hiển thị thông báo
    groups = Group.objects.filter(creator=request.user)
    memberships = GroupMembership.objects.filter(
        group__in=groups,
        status='requested'
    )
    # Lấy các group_ids mà có thông báo
    group_ids_with_messages = memberships.values_list('group', flat=True)
    messages = MessageGroup.objects.filter(group__in=group_ids_with_messages)

    context = {
        'group': group,
        'posts': posts,
        'groups_joined':user_groups,
        'groups_not_joined':groups_not_joined,
        'is_member':is_member,
        'status':status,
        'messages':messages,
    }
    
    return render(request, 'group_posts.html', context)

@method_decorator(login_required(login_url='/auth/login/'), name='dispatch')
class ManageGroupMembershipView(CreateView):
    def post(self, request, group_id, user_id, action):
        group = get_object_or_404(Group, id=group_id)
        user = get_object_or_404(User, id=user_id)
        if request.user == group.creator:
            membership = GroupMembership.objects.get(user=user, group=group)
            if action == 'approve':
                membership.status = 'approved'
            elif action == 'reject':
                membership.status = 'rejected'
            membership.save()
        return redirect('social:group_posts', group_id=group.id)

@method_decorator(login_required(login_url='/auth/login/'), name='dispatch')
class JoinGroupView(CreateView):
    def get(self, request, group_id):
        group = get_object_or_404(Group, id=group_id)
        membership, created = GroupMembership.objects.get_or_create(user=request.user, group=group)
        message = f"{request.user.username} đã yêu cầu tham gia nhóm {group.name}"
        MessageGroup.objects.create(user=request.user, group=group, message=message)
        if created:
            membership.status = 'requested'
            membership.save()
        
        # Kiểm tra xem người dùng hiện tại có phải là người tạo nhóm hay không
        if request.user == group.creator:
            return redirect('social:membership-requests', group_id=group.id)
        else:
            # Lựa chọn một URL bạn muốn chuyển hướng người dùng trong trường hợp người tạo nhóm không thấy thông báo.
            # Ví dụ: return redirect('social:group_posts', group_id=group.id)
            return redirect('social:group_posts', group_id=group_id) 

@method_decorator(login_required(login_url='/auth/login/'), name='dispatch')
class LeaveGroupView(CreateView):
    def get(self, request, group_id):
        try:
            membership = GroupMembership.objects.get(user=request.user, group_id=group_id)
            membership.delete()  # Xóa mối quan hệ của người dùng với nhóm
        except GroupMembership.DoesNotExist:
            pass  # Người dùng không tham gia nhóm, không cần thực hiện gì

        return redirect('social:group_posts', group_id=group_id) 
