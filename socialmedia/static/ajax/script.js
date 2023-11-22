// like event 
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
$(document).ready(function() {
    // Lấy CSRF token từ cookie
    const csrftoken = getCookie('csrftoken');
    $('.like-button').click(function(e) {
        e.preventDefault();
        var post_id = $(this).data('post-id');
        var like_button = $(this);
        var likeCountSpan = $('#like-count-' + post_id);
        var likeCountIcon = $('#like-icon-' + post_id);
        $.ajax({
            type: 'POST',
            url: '/like/' + post_id + '/',
            data: {
                csrfmiddlewaretoken: csrftoken  // Đặt CSRF token trong dữ liệu yêu cầu
            },
            dataType: 'json',
            success: function(response) {
                // Cập nhật biểu tượng like và số lượng like
                if (response.liked) {
                    like_button.css('color', '#0866ff');
                    likeCountIcon.css('color', '#0866ff');
                    likeCountSpan.text(response.total_likes)
                } else {
                    likeCountSpan.text(response.total_likes)
                    like_button.css('color', '');                                            
                    likeCountIcon.css('color', '');                                            
                }
            },
            error: function(xhr, status, error) {
                console.error(xhr.responseText);
            }
        });
    });

    $('.like-button').click(function(e) {
        e.preventDefault();
        var post_id = $(this).data('post-id');
        var like_button = $(this);
        var likeCountSpan = $('#like-count-' + post_id);
        var likeCountIcon = $('#like-icon-' + post_id);
        $.ajax({
            type: 'POST',
            url: '/social/like/' + post_id + '/',
            data: {
                csrfmiddlewaretoken: csrftoken  // Đặt CSRF token trong dữ liệu yêu cầu
            },
            dataType: 'json',
            success: function(response) {
                // Cập nhật biểu tượng like và số lượng like
                if (response.liked) {
                    like_button.css('color', '#0866ff');
                    likeCountIcon.css('color', '#0866ff');
                    likeCountSpan.text(response.total_likes)
                } else {
                    likeCountSpan.text(response.total_likes)
                    like_button.css('color', '');                                            
                    likeCountIcon.css('color', '');                                            
                }
            },
            error: function(xhr, status, error) {
                console.error(xhr.responseText);
            }
        });
    });

    $('.like-button').click(function(e) {
        e.preventDefault();
        var post_id = $(this).data('post-id');
        var group_id = $(this).data('group-id');
        var like_button = $(this);
        var likeCountSpan = $('#like-count-' + post_id);
        var likeCountIcon = $('#like-icon-' + post_id);
        $.ajax({
            type: 'POST',
            url: '/social/group/' + group_id + '/like/' + post_id + '/',
            data: {
                csrfmiddlewaretoken: csrftoken  // Đặt CSRF token trong dữ liệu yêu cầu
            },
            dataType: 'json',
            success: function(response) {
                // Cập nhật biểu tượng like và số lượng like
                if (response.liked) {
                    like_button.css('color', '#0866ff');
                    likeCountIcon.css('color', '#0866ff');
                    likeCountSpan.text(response.total_likes)
                } else {
                    likeCountSpan.text(response.total_likes)
                    like_button.css('color', '');                                            
                    likeCountIcon.css('color', '');                                            
                }
            },
            error: function(xhr, status, error) {
                console.error(xhr.responseText);
            }
        });
    });
});


// add comment
$(document).ready(function() {
    var csrftoken = getCookie('csrftoken');

    
    // delete comment
    $('.delete-comment-button').on('click', function(event) {
        event.preventDefault(); // Ngăn chặn chuyển hướng mặc định

        var commentId = $(this).data('comment-id');
        var commentContainer = $(this).closest('.comment-content');  // Tìm phần tử chứa bình luận

        $.ajax({
            type: 'POST',
            url: `/delete_comment/${commentId}/`,
            data: {
                csrfmiddlewaretoken: csrftoken
            },
            dataType: 'json',
            success: function(response) {
                // Xử lý phản hồi từ máy chủ (nếu cần)

                // Xóa giao diện bình luận ngay lập tức
                commentContainer.remove();
            },
            error: function(xhr, status, error) {
                console.error(xhr.responseText);
            }
        });
    });

    $('.delete-reply-button').on('click', function(event) {
        event.preventDefault(); // Ngăn chặn chuyển hướng mặc định

        var commentId = $(this).data('reply-id');
        var commentContainer = $(this).closest('.reply-content');  // Tìm phần tử chứa bình luận

        $.ajax({
            type: 'POST',
            url: `/delete_reply/${commentId}/`,
            data: {
                csrfmiddlewaretoken: csrftoken
            },
            dataType: 'json',
            success: function(response) {
                // Xử lý phản hồi từ máy chủ (nếu cần)

                // Xóa giao diện bình luận ngay lập tức
                commentContainer.remove();
            },
            error: function(xhr, status, error) {
                console.error(xhr.responseText);
            }
        });
    });
   
    // delete groups post comment
    $('.delete-comment-button').on('click', function(event) {
        event.preventDefault(); // Ngăn chặn chuyển hướng mặc định

        var commentId = $(this).data('comment-id');
        var commentContainer = $(this).closest('.comment-content');  // Tìm phần tử chứa bình luận
            $.ajax({
                type: 'POST',
                url: `/delete_comment/${commentId}/`,
                data: {
                    csrfmiddlewaretoken: csrftoken
                },
                dataType: 'json',
                success: function(response) {
                    // Xử lý phản hồi từ máy chủ (nếu cần)
    
                    // Xóa giao diện bình luận ngay lập tức
                    commentContainer.remove();
                },
                error: function(xhr, status, error) {
                    console.error(xhr.responseText);
                }
            });

        $.ajax({
            type: 'POST',
            url: `/social/delete_comment/${commentId}/`,
            data: {
                csrfmiddlewaretoken: csrftoken
            },
            dataType: 'json',
            success: function(response) {
                // Xử lý phản hồi từ máy chủ (nếu cần)

                // Xóa giao diện bình luận ngay lập tức
                commentContainer.remove();
            },
            error: function(xhr, status, error) {
                console.error(xhr.responseText);
            }
        });
    }

    );
    $('.delete-reply-button').on('click', function(event) {
        event.preventDefault(); // Ngăn chặn chuyển hướng mặc định

        var commentId = $(this).data('reply-id');
        var commentContainer = $(this).closest('.reply-content');  // Tìm phần tử chứa bình luận

        $.ajax({
            type: 'POST',
            url: `/social/delete_reply/${commentId}/`,
            data: {
                csrfmiddlewaretoken: csrftoken
            },
            dataType: 'json',
            success: function(response) {
                // Xử lý phản hồi từ máy chủ (nếu cần)

                // Xóa giao diện bình luận ngay lập tức
                commentContainer.remove();
            },
            error: function(xhr, status, error) {
                console.error(xhr.responseText);
            }
        });
    });
});


    // $('.post-comment').on('submit', function(event) {
    //     event.preventDefault();
    //     var form = $(this); 
    //     var post_id = $(this).closest('.post-comment').data('post-id');
    //     console.log(post_id)
    //     var comment_content = $(this).find('.content').val();
        
    //     $.ajax({
    //         type: 'POST',
    //         url: '/add_comment/' + post_id + '/',
    //         data: {
    //             csrfmiddlewaretoken: csrftoken,
    //             content: comment_content
    //         },
    //         dataType: 'json',
    //         success: function(response) {
    //             // Xử lý phản hồi từ máy chủ (nếu cần)
    //             // Ví dụ: thêm comment mới vào danh sách hiển thị
    //             var newCommentHTML = `                    
    //                     <div class="mb-3 d-flex align-items-start">
    //                                 {% if ${ response.user } == ${response.profiles.user} %}             
    //                                 <img src="{% if ${response.profiles.profile_pic} %}
    //                                 ${response.profiles.profile_pic}
    //                                 {% else %} 
    //                                     https://scontent.fsgn2-3.fna.fbcdn.net/v/t1.30497-1/143086968_2856368904622192_1959732218791162458_n.png?stp=cp0_dst-png_p60x60&_nc_cat=1&ccb=1-7&_nc_sid=2b6aad&_nc_eui2=AeE1vTPkHb-3caw-Qa8LcUBUso2H55p0AlGyjYfnmnQCUZJq8s60z2bWHjSCVInwd04OWKdpTROsfDIQw33wpZKQ&_nc_ohc=x-5IH6VdBkQAX973AOb&_nc_ht=scontent.fsgn2-3.fna&oh=00_AfDK83mRdv0PL08D0btIF9cOTS3s8hnIALTSupH9AKV5XQ&oe=657722F8
    //                                 {% endif %} "
    //                                 class="card-img" alt="avatar">
    //                                 {% endif %}
    //                         <div class="author">
    //                             <a href="#" class="name">${ response.user }</a>
    //                             <!-- comment view -->
    //                             <p class="">
    //                                 ${ response.content }
    //                                 <a href="/delete_comment/${response.comment_id}/" data-comment-id="${response.comment_id}" class="delete-comment-button text-danger">(delete) </a>-
    //                                 <a href="#comment${response.comment_id}"  class="action-item text-info" data-bs-toggle="collapse" role="button" aria-expanded="false" aria-controls="collapseExample">(edit)</a> <br> 
    //                                 <a href="#reply${response.comment_id}" class="action-item text-info" data-bs-toggle="collapse" role="button" aria-expanded="false">(reply)</a>

    //                                 <!-- edit comment form -->
    //                                 <div class="collapse" id="comment${response.comment_id}">
    //                                     <hr>   
    //                                     <div class="form-group">
    //                                         <form method="post" action="{% url 'edit_comment' ${response.comment_id} %}">
    //                                             {% csrf_token %}
    //                                             <div style="display: flex; text-align: center;" class="ms-2 mb-3" >
    //                                                 {% for profile in ${response.profiles} %}   
    //                                                         {% if ${ response.user.id } == profile.user.id %}             
    //                                                         <img src="{% if profile.profile_pic %}
    //                                                             {{ profile.profile_pic.url  }}
    //                                                         {% else %} 
    //                                                             https://scontent.fsgn2-3.fna.fbcdn.net/v/t1.30497-1/143086968_2856368904622192_1959732218791162458_n.png?stp=cp0_dst-png_p60x60&_nc_cat=1&ccb=1-7&_nc_sid=2b6aad&_nc_eui2=AeE1vTPkHb-3caw-Qa8LcUBUso2H55p0AlGyjYfnmnQCUZJq8s60z2bWHjSCVInwd04OWKdpTROsfDIQw33wpZKQ&_nc_ohc=x-5IH6VdBkQAX973AOb&_nc_ht=scontent.fsgn2-3.fna&oh=00_AfDK83mRdv0PL08D0btIF9cOTS3s8hnIALTSupH9AKV5XQ&oe=657722F8
    //                                                         {% endif %} "
    //                                                         class="card-img" alt="avatar">
    //                                                         {% endif %}
    //                                                 {% endfor %}
    //                                                 <input name="content" class="ms-2 w-100 rounded-pill" value="${response.content}" required id="id_body">
    //                                                 <input type="hidden" name="parent_id" value="None">
    //                                                 <button class="btn "><i class="fa-solid fa-paper-plane fa-beat"></i></button>
    //                                             </div>
    //                                         </form>
    //                                     </div>
    //                                 </div>
    //                             </p>
    //                         </div>    
    //                     </div>
    //             `;
    //             form.find('#id_body').val('')  // Xóa nội dung comment sau khi gửi
    //             $(newCommentHTML).prependTo(('#comment-add'+post_id));
    //         },
    //         error: function(xhr, status, error) {
    //             console.error(xhr.responseText);
    //         }
    //     });
    // });
    