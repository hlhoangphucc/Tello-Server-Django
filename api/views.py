import mimetypes
import os
from smtplib import SMTPResponseException
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User,AnonymousUser
from rest_framework.authtoken.models import Token
from django.http import JsonResponse
from django.urls import reverse
from .models import Image, InfoUser, Posts, Video,Message, Voice
from .serializers import MessageSerializer, UserSerializer

from django.http import HttpResponse, Http404
from django.conf import settings

@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username=request.data['username'])
        user.set_password(request.data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return Response({'token': token.key, 'user': serializer.data})
    return Response(serializer.errors, status=status.HTTP_200_OK)

@api_view(['POST'])
def login(request):
    user = get_object_or_404(User, username=request.data['username'])
    if not user.check_password(request.data['password']):
        return Response("missing user", status=status.HTTP_404_NOT_FOUND)
    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(user)
    return Response({'token': token.key, 'user': serializer.data})


# @api_view(['GET'])
# @authentication_classes([SessionAuthentication, TokenAuthentication])
# @permission_classes([IsAuthenticated])

def get_all(request):
    all_users = User.objects.all()
    
    # Serialize the queryset to a list of dictionaries
    users_data = [{'id':user.id,'username': user.username, 'email': user.email} for user in all_users]

    return JsonResponse({'users': users_data})

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_authenticated_user(request):
    if isinstance(request.user, AnonymousUser):
        # Người dùng chưa đăng nhập, trả về phản hồi phù hợp hoặc thực hiện xử lý khác
        return JsonResponse({'message': 'User not logged in'}, status=401)

    # Người dùng đã đăng nhập, truy cập thông tin và trả về
    user_data = {
        'id': request.user.id,
        'username': request.user.username,
        'email': getattr(request.user, 'email', ''),
    }

    return JsonResponse({'user': user_data})


@api_view(['POST'])
def UploadImage(request, format=None):
    image_file = request.FILES.get('media_post') or request.FILES.get('message')

    if image_file:
        # Lưu tệp hình ảnh trên server
        new_image = Image(image_file=image_file)
        new_image.save()

        image_path = os.path.basename(new_image.image_file.url)
        # Lấy đường dẫn đến hình ảnh trên server
        relative_path = reverse('get_image', kwargs={'image_path': image_path})

        base_url = request.build_absolute_uri(relative_path)
        image_relative_path = f'{base_url}'

        if 'media_post' in request.data:
            # Nếu là yêu cầu cho bài đăng
            post = Posts(
                post_id=request.data.get('post_id'),
                text_post=request.data.get('text_post'),
                media_post=image_relative_path,
                user_name=request.data.get('user_name'),
                user_id=request.data.get('user_id'),
                post_time=request.data.get('post_time'),
                post_type='text-image',
            )
            post.save()
        elif 'message' in request.FILES:
            # Nếu là yêu cầu cho tin nhắn
            message = Message(
                room_id=request.data.get('room_id'),
                message=image_relative_path,
                sender_id=request.data.get('sender_id'),
                receiver_id=request.data.get('receiver_id'),
                send_time=request.data.get('send_time'),
                message_type='image',
                voice_duration='null'

            )
            message.save()

        return Response({'message': 'Image uploaded successfully'}, status=status.HTTP_201_CREATED)
    else:
        return Response({'error': 'Image not provided'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def UploadVideoToMessage(request, *args, **kwargs):
    video_file = request.FILES.get('message') or request.FILES.get('media_post')
    if video_file:
        # Lưu tệp video trên server
        new_video = Video(video_file=video_file)
        new_video.save()

        video_path = os.path.basename(new_video.video_file.url)
        # Lấy đường dẫn đến video trên server
        relative_path = reverse('get_video', kwargs={'video_path': video_path})
    
        base_url = request.build_absolute_uri(relative_path)
   
        video_relative_path = f'{base_url}'
     
     
        if 'media_post' in request.data:
            post = Posts(
                post_id=request.data.get('post_id'),
                text_post=request.data.get('text_post'),
                media_post=video_relative_path,
                user_name=request.data.get('user_name'),
                user_id=request.data.get('user_id'),
                post_time=request.data.get('post_time'),
                post_type='text-video',
            )
            post.save()
        elif 'message' in request.FILES:
            message = Message(
                room_id=request.data.get('room_id'),
                message=video_relative_path,
                sender_id=request.data.get('sender_id'),
                receiver_id=request.data.get('receiver_id'),
                send_time=request.data.get('send_time'),
                message_type='video',
                voice_duration='null'

            )
            message.save()

        return Response({'message': 'Video uploaded successfully'}, status=status.HTTP_201_CREATED)
    else:
        return Response({'error': 'Video not provided'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def UploadVoiceMessageVoice(request,*args, **kwargs):
    voice_file=request.FILES.get('message')
    if voice_file:
        new_voice = Voice(voice_file=voice_file)
        
        new_voice.save()
        voice_path = os.path.basename(new_voice.voice_file.url)
        # Lấy đường dẫn đến video trên server
        relative_path = reverse('get_voice', kwargs={'voice_path': voice_path})
    
        base_url = request.build_absolute_uri(relative_path)
   
        voice_relative_path = f'{base_url}'
        message = Message(
                room_id=request.data.get('room_id'),
                message=voice_relative_path,
                sender_id=request.data.get('sender_id'),
                receiver_id=request.data.get('receiver_id'),
                send_time=request.data.get('send_time'),
                message_type='voice',
                voice_duration=request.data.get('voice_duration')
            )
        message.save()
        return Response({'message': 'Video uploaded successfully'}, status=status.HTTP_201_CREATED)
    else:
        return Response({'error': 'Video not provided'}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['PUT'])
def UpdateAvt(request, format=None):
    user_id = request.data.get('user_id')
    image_file = request.FILES.get('avt_url') or request.FILES.get('bg_url')

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
    relative_path = reverse('get_image', kwargs={'image_path': image_path})

    base_url = request.build_absolute_uri(relative_path)
    image_relative_path = f'{base_url}'

    if 'avt_url'in request.data:
        infouser, created = InfoUser.objects.update_or_create(
             user_id=user_id,
             defaults={
                'user_name':request.data.get('user_name'),
                'avt_url':image_relative_path,  
                'upload_time':request.data.get('upload_time'),
             }
            )
    elif  'bg_url' in request.data :
        infouser, created = InfoUser.objects.update_or_create(
            user_id=user_id,
             defaults={
                'user_name':request.data.get('user_name'),
                'bg_url':image_relative_path,  
                'upload_time':request.data.get('upload_time'),
             }
            )
    if(old_avt_path):
        delete_old_avt(old_avt_path)
    
     
    return Response({'message': 'Image uploaded successfully'}, status=status.HTTP_201_CREATED)

def delete_old_avt(old_avt_path):
    try:
        avt_path = os.path.join(settings.MEDIA_ROOT, str(old_avt_path))
        if os.path.exists(avt_path ):
            os.remove(avt_path )
            print(f"Deleted old avatar at {avt_path }")
        else:
            print(f"Old avatar file not found at {avt_path}")
    except Exception as e:
        print(f"Error deleting old avatar file: {e}")
    
def GetVideoView(request,video_path ):
    # Xác định đường dẫn tuyệt đối đến thư mục chứa video
    absolute_video_path = os.path.join(settings.MEDIA_ROOT, 'videos', video_path)

    try:
        # Mở và đọc file video
        with open(absolute_video_path, 'rb') as video_file:
            # Tạo HttpResponse và trả về nó
            response = HttpResponse(video_file.read(), content_type='video/mp4')
            return response
    except FileNotFoundError:
        # Nếu file không tồn tại, raise Http404
        raise Http404("Video not found")

def GetImageView(request,image_path ):
    # Xác định đường dẫn tuyệt đối đến thư mục chứa image
    absolute_image_path = os.path.join(settings.MEDIA_ROOT, 'images', image_path)

    try:
        # Mở và đọc file image
        with open(absolute_image_path, 'rb') as image_file:
            # Tạo HttpResponse và trả về nó
            response = HttpResponse(image_file.read(), content_type='image/png')
            return response
    except FileNotFoundError:
        # Nếu file không tồn tại, raise Http404
        raise Http404("Image not found")
    
def GetVoiceView(request,voice_path):
    absolute_voice_path=os.path.join(settings.MEDIA_ROOT,'voices',voice_path)
    try:
        with open(absolute_voice_path, 'rb') as voice_file:
            content_type, encoding = mimetypes.guess_type(voice_path)
            if content_type is None:
                    content_type = 'application/octet-stream'

                # Trả về HttpResponse với nội dung của file âm thanh và loại MIME tương ứng
            response = HttpResponse(voice_file.read(), content_type=content_type)
            response['Content-Disposition'] = f'inline; filename="{voice_path}"'
            return response
    except FileNotFoundError:
        # Nếu file không tồn tại, raise Http404
        raise Http404("Voice not found")
    
def test_token(request):
    return Response("passed!")