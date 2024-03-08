import mimetypes
import os
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User, AnonymousUser
from rest_framework.authtoken.models import Token
from django.http import JsonResponse
from django.urls import reverse
from django.utils import timezone
from .models import (
    Image,
    InfoUser,
    Posts,
    Message,
    Voice,
    Media,
    Interact,
    Comments,
    Follows,
)
from .serializers import UserSerializer
from django.db.models import Count, Subquery, OuterRef
from django.http import HttpResponse, Http404
from django.conf import settings
from mimetypes import guess_type
from django.db.models import Q


@api_view(["POST"])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        # Kiểm tra xem email đã tồn tại chưa
        if InfoUser.objects.filter(email=request.data["email"]).exists():
            return Response(
                {"error": "Email đã tồn tại"}, status=status.HTTP_409_CONFLICT
            )
        else:
            serializer.save()
            user = User.objects.get(username=request.data["username"])
            user.set_password(request.data["password"])
            user.save()
            info_user = InfoUser.objects.create(
                user_id=user.id,
                user_name=user.username,
                phone=request.data["phone"],
                email=user.email,
                gender="nam",
                created_time=user.date_joined,
                online_time=user.date_joined,
                bg_url="null",
                avt_url="null",
            )
            token = Token.objects.create(user=user)
            return Response({"token": token.key, "user": serializer.data})
    else:
        return Response({"error": "Email đã tồn tại"}, status=status.HTTP_409_CONFLICT)


@api_view(["POST"])
def login(request):
    user = get_object_or_404(User, email=request.data["email"])
    if not user.check_password(request.data["password"]):
        return Response("missing user", status=status.HTTP_404_NOT_FOUND)
    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(user)
    return Response({"token": token.key, "user": serializer.data})


# @api_view(['GET'])
# @authentication_classes([SessionAuthentication, TokenAuthentication])
# @permission_classes([IsAuthenticated])


def get_all_user(request):
    all_users = InfoUser.objects.all()

    users_data = list(all_users.values())

    return JsonResponse({"users": users_data})


def get_user(request, user_id):
    try:
        user = InfoUser.objects.filter(user_id=user_id)
        users_data = list(user.values())
        return JsonResponse({"user": users_data})
    except InfoUser.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)


@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_authenticated_user(request):
    if isinstance(request.user, AnonymousUser):
        # Người dùng chưa đăng nhập, trả về phản hồi phù hợp hoặc thực hiện xử lý khác
        return JsonResponse({"message": "User not logged in"}, status=401)

    # Người dùng đã đăng nhập, truy cập thông tin và trả về
    user_data = {
        "id": request.user.id,
        "username": request.user.username,
        "email": getattr(request.user, "email", ""),
    }

    return JsonResponse({"user": user_data})


@api_view(["POST"])
def UploadPosts(request, format=None):
    media_file = request.FILES.get("media_post")
    text_post = request.data.get("text_post", "")
    user_id = request.data.get("user_id")
    user_name = request.data.get("user_name")
    avt_user = request.data.get("avt_user")
    post_time = request.data.get("post_time")
    media_file = request.FILES.get("media_post")

    if media_file:
        # Lưu tệp video trên server
        new_media = Media(media_file=media_file)
        new_media.save()

        _, extension = os.path.splitext(new_media.media_file.name)
        if extension.lower() in [".jpg", ".jpeg", ".png", ".gif"]:
            media_type = "text-image"
        elif extension.lower() in [".mp4", ".mov", ".avi"]:
            media_type = "text-video"
        media_path = os.path.basename(new_media.media_file.url)

        relative_path = reverse("get_media", kwargs={"media_path": media_path})

        base_url = request.build_absolute_uri(relative_path)

        media_relative_path = f"{base_url}"
    else:
        media_type = "text"
        media_relative_path = None

    post = Posts(
        post_id=request.data.get("post_id"),
        text_post=text_post,
        media_post=media_relative_path,
        user_name=user_name,
        user_id=InfoUser.objects.get(user_id=request.data.get("user_id")),
        post_time=post_time,
        avt_user=avt_user,
        post_type=media_type,
        is_edit=False,
    )
    post.save()

    return Response(
        {"message": "Post  uploaded successfully"}, status=status.HTTP_201_CREATED
    )


@api_view(["POST"])
def UploadMedia(request, *args, **kwargs):
    media_paths = []
    media_types = []
    sender_instance = InfoUser.objects.get(pk=request.data.get("sender_id"))
    receiver_instance = InfoUser.objects.get(pk=request.data.get("receiver_id"))
    if "message" in request.FILES:
        for media_file in request.FILES.getlist("message"):
            if media_file:
                # Lưu tệp video trên server
                new_media = Media(media_file=media_file)
                new_media.save()

                _, extension = os.path.splitext(new_media.media_file.name)
                if extension.lower() in [".jpg", ".jpeg", ".png", ".gif"]:
                    media_type = "image"
                elif extension.lower() in [".mp4", ".mov", ".avi"]:
                    media_type = "video"
                else:
                    media_type = "unknown"

                media_path = os.path.basename(new_media.media_file.url)
                # Lấy đường dẫn đến video trên server
                relative_path = reverse("get_media", kwargs={"media_path": media_path})

                base_url = request.build_absolute_uri(relative_path)

                media_relative_path = f"{base_url}"

                media_paths.append(media_relative_path)

                media_types.append(media_type)

        message = Message(
            room_id=request.data.get("room_id"),
            message=media_paths,
            sender_id=sender_instance,
            receiver_id=receiver_instance,
            send_time=request.data.get("send_time"),
            message_type=media_types,
            voice_duration="null",
        )
        message.save()
        return Response(
            {"message": "Video uploaded successfully"}, status=status.HTTP_201_CREATED
        )

    else:
        return Response(
            {"error": "Video not provided"}, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(["POST"])
def UploadVoiceMessageVoice(request, *args, **kwargs):

    voice_file = request.FILES.get("message")
    sender_instance = InfoUser.objects.get(pk=request.data.get("sender_id"))
    receiver_instance = InfoUser.objects.get(pk=request.data.get("receiver_id"))
    if voice_file:
        new_voice = Voice(voice_file=voice_file)

        new_voice.save()
        voice_path = os.path.basename(new_voice.voice_file.url)
        # Lấy đường dẫn đến video trên server
        relative_path = reverse("get_voice", kwargs={"voice_path": voice_path})

        base_url = request.build_absolute_uri(relative_path)

        voice_relative_path = f"{base_url}"
        message = Message(
            room_id=request.data.get("room_id"),
            message=voice_relative_path,
            sender_id=sender_instance,
            receiver_id=receiver_instance,
            send_time=request.data.get("send_time"),
            message_type="voice",
            voice_duration=request.data.get("voice_duration"),
        )
        message.save()
        return Response(
            {"message": "Video uploaded successfully"}, status=status.HTTP_201_CREATED
        )
    else:
        return Response(
            {"error": "Video not provided"}, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(["GET"])
def GetAllPost(request, *args, **kwargs):
    limit = request.GET.get("limit")
    user_id = request.GET.get("user_id")
    try:
        limit = int(limit)
    except (TypeError, ValueError):
        limit = None

    followed_users = Follows.objects.filter(my_user_id=user_id)[:1].values_list(
        "other_user_id", flat=True
    )
    user_name = InfoUser.objects.filter(user_id=user_id)[:1].values_list(
        "user_name", flat=True
    )
    posts_with_interact_count = (
        Posts.objects.filter(Q(user_id=user_id) | Q(user_id__in=followed_users))
        .annotate(
            interact_count=Count("interact"),
            comment_count=Subquery(
                Comments.objects.filter(post_id=OuterRef("pk"))
                .values("post_id")
                .annotate(comment_count=Count("id"))
                .values("comment_count")
            ),
        )
        .order_by("-post_time")
    )

    posts_data = []
    for post in posts_with_interact_count:
        interact_user_ids = Interact.objects.filter(post_id=post.post_id).values_list(
            "user_id", flat=True
        )
        user_name = InfoUser.objects.filter(user_id=post.user_id.user_id).first()
        avt_user_info = InfoUser.objects.filter(user_id=post.user_id.user_id).first()
        avt_url = avt_user_info.avt_url if avt_user_info else None
        post_info = {
            "post_id": post.post_id,
            "text_post": post.text_post,
            "media_post": post.media_post,
            "user_name": user_name.user_name,
            "avt_user": avt_url,
            "post_time": post.post_time,
            "post_type": post.post_type,
            "is_edit": post.is_edit,
            "interact_count": post.interact_count,
            "post_user_id": post.user_id.user_id,
            "interact_user_ids": list(interact_user_ids),
            "comment_count": post.comment_count,
        }
        posts_data.append(post_info)

    if limit and limit > 0:
        posts_data = posts_data[:limit]

    return JsonResponse({"posts": posts_data})


@api_view(["GET"])
def GetPostFromUser(request, *args, **kwargs):
    limit = request.GET.get("limit")
    user_id = request.GET.get("user_id")
    try:
        limit = int(limit)
        user_id = int(user_id)
    except (TypeError, ValueError):
        limit = None

    # Lấy tất cả các bài đăng và số lượng tương tác tương ứng
    posts_with_interact_count = (
        Posts.objects.filter(user_id=user_id)
        .annotate(
            interact_count=Count("interact"),
            comment_count=Subquery(
                Comments.objects.filter(post_id=OuterRef("pk"))
                .values("post_id")
                .annotate(comment_count=Count("id"))
                .values("comment_count")
            ),
        )
        .order_by("-post_time")
    )

    posts_data = []
    for post in posts_with_interact_count:
        interact_user_ids = Interact.objects.filter(post_id=post.post_id).values_list(
            "user_id", flat=True
        )
        user_name = InfoUser.objects.filter(user_id=post.user_id.user_id).first()
        avt_user_info = InfoUser.objects.filter(user_id=post.user_id.user_id).first()
        avt_url = avt_user_info.avt_url if avt_user_info else None
        post_info = {
            "post_id": post.post_id,
            "text_post": post.text_post,
            "media_post": post.media_post,
            "user_name": user_name.user_name,
            "avt_user": avt_url,
            "post_time": post.post_time,
            "post_type": post.post_type,
            "is_edit": post.is_edit,
            "interact_count": post.interact_count,
            "post_user_id": post.user_id.user_id,
            "interact_user_ids": list(interact_user_ids),
            "comment_count": post.comment_count,
        }
        posts_data.append(post_info)

    if limit and limit > 0:
        posts_data = posts_data[:limit]
    return JsonResponse({"posts": posts_data})


@api_view(["DELETE"])
def DeletePost(request, post_id):
    try:
        post = Posts.objects.get(post_id=post_id)
        post.delete()
        return Response(
            {"message": "Post deleted successfully"}, status=status.HTTP_200_OK
        )
    except Posts.DoesNotExist:
        return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(["POST"])
def AddLike(request, *args, **kwargs):
    post_id = request.data.get("post_id")

    user_id = request.data.get("user_id")
    user_instance = InfoUser.objects.get(pk=user_id)

    post_instance = Posts.objects.get(pk=post_id)

    interact = Interact(
        post_id=post_instance, user_id=user_instance, updated_at=timezone.now()
    )
    interact.save()
    return Response(
        {"message": "Add Like successfully"}, status=status.HTTP_201_CREATED
    )


@api_view(["POST"])
def UnLike(request, *args, **kwargs):
    post_id = request.data.get("post_id")
    user_id = request.data.get("user_id")
    interact = get_object_or_404(Interact, post_id=post_id, user_id=user_id)
    interact.delete()
    return Response({"message": "UnLike successfully"}, status=status.HTTP_201_CREATED)


@api_view(["PUT"])
def UpdateAvt(request, format=None):
    user_id = request.data.get("user_id")
    image_file = request.FILES.get("avt_url") or request.FILES.get("bg_url")
    if image_file:
        old_avt_path = None
        try:
            image = Image.objects.get(user_id=user_id)
            old_avt_path = image.image_file
            image.delete()
            image.image_file = image_file
            image.save()

        except Image.DoesNotExist:
            new_image = Image(image_file=image_file, user_id=user_id)
            image = new_image
            new_image.save()

        image_path = os.path.basename(image.image_file.url)
        relative_path = reverse("get_image", kwargs={"image_path": image_path})

        base_url = request.build_absolute_uri(relative_path)
        image_relative_path = f"{base_url}"

        if "avt_url" in request.data:
            if "phone" in request.data or "gender" in request.data:
                infouser, created = InfoUser.objects.update_or_create(
                    user_id=user_id,
                    defaults={
                        "user_name": request.data.get("user_name"),
                        "avt_url": image_relative_path,
                        "upload_time": request.data.get("upload_time"),
                        "phone": request.data.get("phone"),
                        "gender": request.data.get("gender"),
                    },
                )
            else:
                infouser, created = InfoUser.objects.update_or_create(
                    user_id=user_id,
                    defaults={
                        "user_name": request.data.get("user_name"),
                        "avt_url": image_relative_path,
                        "upload_time": request.data.get("upload_time"),
                    },
                )
        elif "bg_url" in request.data:
            infouser, created = InfoUser.objects.update_or_create(
                user_id=user_id,
                defaults={
                    "user_name": request.data.get("user_name"),
                    "bg_url": image_relative_path,
                    "upload_time": request.data.get("upload_time"),
                },
            )
        if old_avt_path:
            delete_old_avt(old_avt_path)
    else:
        infouser, created = InfoUser.objects.update_or_create(
            user_id=user_id,
            defaults={
                "user_name": request.data.get("user_name"),
                "upload_time": request.data.get("upload_time"),
                "phone": request.data.get("phone"),
                "gender": request.data.get("gender"),
            },
        )
    return Response(
        {"message": "Image uploaded successfully"}, status=status.HTTP_201_CREATED
    )


@api_view(["PUT"])
def UpdatePost(request, format=None):
    post_id = request.data.get("post_id")
    media_file = request.FILES.get("media_post")

    if post_id:
        # Save video file on the server
        new_media = Media(media_file=media_file)
        new_media.save()

        _, extension = os.path.splitext(new_media.media_file.name)
        if extension.lower() in [".jpg", ".jpeg", ".png", ".gif"]:
            media_type = "text-image"
        elif extension.lower() in [".mp4", ".mov", ".avi"]:
            media_type = "text-video"
        else:
            media_type = "unknown"

        media_path = os.path.basename(new_media.media_file.url)
        # Get path to the video on the server
        relative_path = reverse("get_media", kwargs={"media_path": media_path})
        base_url = request.build_absolute_uri(relative_path)
        media_relative_path = f"{base_url}"
        # Update or create the post with the provided data
        infouser, created = Posts.objects.update_or_create(
            post_id=post_id,
            defaults={
                "text_post": request.data.get("text_post"),
                "media_post": media_relative_path,
                "post_type": media_type,
                "is_edit": True,
            },
        )
        return Response(
            {"message": "Update posts success"}, status=status.HTTP_201_CREATED
        )
    else:
        return Response(
            {"error": "error update posts"}, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(["POST"])
def Comment(request, *args, **kwargs):
    post_id = request.data.get("post_id")
    user_id = request.data.get("user_id")
    content_comment = request.data.get("content_comment")

    user_instance = InfoUser.objects.get(pk=user_id)
    post_instance = Posts.objects.get(pk=post_id)

    comment = Comments(
        post_id=post_instance,
        user_id=user_instance,
        creatd_at=timezone.now(),
        content_comment=content_comment,
    )
    comment.save()
    return Response(
        {"message": "Comments successfully"}, status=status.HTTP_201_CREATED
    )


@api_view(["GET"])
def GetCommentFromPostId(request, *args, **kwargs):
    limit = request.GET.get("limit")
    post_id = request.GET.get("post_id")
    try:
        limit = int(limit)
    except (TypeError, ValueError):
        limit = None

    comments = Comments.objects.filter(post_id=post_id).all()

    comments_data = []
    for comment in comments:
        user_data = InfoUser.objects.get(user_id=comment.user_id.user_id)
        comment_info = {
            "id": comment.id,
            "post_id": comment.post_id.post_id,
            "content_comment": comment.content_comment,
            "user_id": user_data.user_id,
            "avt_url": user_data.avt_url,
            "user_name": user_data.user_name,
            "creatd_at": comment.creatd_at,
            "is_edit": comment.is_edit,
        }
        comments_data.append(comment_info)

    if limit and limit > 0:
        comments_data = comments_data[:limit]
    return JsonResponse({"comments": comments_data})


@api_view(["DELETE"])
def DeleteComment(request, id):
    try:
        comment = Comments.objects.get(id=id)
        comment.delete()
        return Response(
            {"message": "Comment deleted successfully"}, status=status.HTTP_200_OK
        )
    except Posts.DoesNotExist:
        return Response(
            {"error": "Comment not found"}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["PUT"])
def UpdateComment(request, format=None):
    id = request.GET.get("id")
    content_comment = request.GET.get("content_comment")
    comment, created = Comments.objects.update_or_create(
        id=id,
        defaults={
            "content_comment": content_comment,
            "creatd_at": timezone.now(),
            "is_edit": True,
        },
    )
    return Response(
        {"message": "Update comments success"}, status=status.HTTP_201_CREATED
    )


@api_view(["POST"])
def FollowUser(request):
    user_id_follow = request.data.get("user_id_follow")
    user_id_send_follow = request.data.get("user_id_send_follow")

    user_id_follow_instance = InfoUser.objects.get(pk=user_id_follow)
    user_id_send_follow_instance = InfoUser.objects.get(pk=user_id_send_follow)

    follows = Follows(
        my_user_id=user_id_send_follow_instance, other_user_id=user_id_follow_instance
    )
    follows.save()
    return Response({"message": "Follow successfully"}, status=status.HTTP_201_CREATED)


@api_view(["POST"])
def UnFollow(request):
    try:
        user_id_follow = request.data.get("user_id_follow")
        user_id_send_follow = request.data.get("user_id_send_follow")

        follows = get_object_or_404(
            Follows, my_user_id=user_id_send_follow, other_user_id=user_id_follow
        )
        follows.delete()
        return Response({"message": "UnFollow successfully"}, status=status.HTTP_200_OK)
    except Posts.DoesNotExist:
        return Response(
            {"error": "UnFollow not found"}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["GET"])
def GetFollowUser(request):
    user_id_follow = request.GET.get("user_id_follow")
    user_id_send_follow = request.GET.get("user_id_send_follow")

    follows = Follows.objects.filter(
        my_user_id=user_id_send_follow, other_user_id=user_id_follow
    )
    follows_list = list(follows.values())
    return JsonResponse({"follows": follows_list})


def delete_old_avt(old_avt_path):
    try:
        avt_path = os.path.join(settings.MEDIA_ROOT, str(old_avt_path))
        if os.path.exists(avt_path):
            os.remove(avt_path)
            print(f"Deleted old avatar at {avt_path }")
        else:
            print(f"Old avatar file not found at {avt_path}")
    except Exception as e:
        print(f"Error deleting old avatar file: {e}")


def GetVideoView(request, video_path):
    # Xác định đường dẫn tuyệt đối đến thư mục chứa video
    absolute_video_path = os.path.join(settings.MEDIA_ROOT, "video", video_path)

    try:
        # Mở và đọc file video
        with open(absolute_video_path, "rb") as video_file:
            # Tạo HttpResponse và trả về nó
            response = HttpResponse(video_file.read(), content_type="video/mp4")
            return response
    except FileNotFoundError:
        # Nếu file không tồn tại, raise Http404
        raise Http404("Video not found")


def GetImageView(request, image_path):
    # Xác định đường dẫn tuyệt đối đến thư mục chứa image
    absolute_image_path = os.path.join(settings.MEDIA_ROOT, "images", image_path)

    try:
        # Mở và đọc file image
        with open(absolute_image_path, "rb") as image_file:
            # Tạo HttpResponse và trả về nó
            response = HttpResponse(image_file.read(), content_type="image/png")
            return response
    except FileNotFoundError:
        # Nếu file không tồn tại, raise Http404
        raise Http404("Image not found")


def GetMedia(request, media_path):
    # Xác định đường dẫn tuyệt đối đến thư mục chứa video hoặc hình ảnh
    absolute_media_path = os.path.join(settings.MEDIA_ROOT, "all", media_path)

    try:
        # Mở và đọc file
        with open(absolute_media_path, "rb") as media_file:
            # Xác định loại của tệp tin
            content_type, _ = guess_type(absolute_media_path)
            if content_type is None:
                content_type = "application/octet-stream"

            # Tạo HttpResponse và trả về nó
            response = HttpResponse(media_file.read(), content_type=content_type)
            return response
    except FileNotFoundError:
        # Nếu file không tồn tại, raise Http404
        raise Http404("File not found")


def GetVoiceView(request, voice_path):
    absolute_voice_path = os.path.join(settings.MEDIA_ROOT, "voices", voice_path)
    try:
        with open(absolute_voice_path, "rb") as voice_file:
            content_type, encoding = mimetypes.guess_type(voice_path)
            if content_type is None:
                content_type = "application/octet-stream"

            # Trả về HttpResponse với nội dung của file âm thanh và loại MIME tương ứng
            response = HttpResponse(voice_file.read(), content_type=content_type)
            response["Content-Disposition"] = f'inline; filename="{voice_path}"'
            return response
    except FileNotFoundError:
        # Nếu file không tồn tại, raise Http404
        raise Http404("Voice not found")


def test_token(request):
    return Response("passed!")
