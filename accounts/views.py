from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404,redirect
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login,logout
from django.http import JsonResponse
from .serializers import UserSerializer
from django.contrib import messages

def signup_view(request):
    if request.method=='POST':
        username=request.POST['username']
        email = request.POST['email']
        password= request.POST['password']
        confirmpassword= request.POST['confirmpassword']

        if password==confirmpassword:
            if User.objects.filter(username=username).exists():
                    messages.info(request,'username already exist!')
            else :
             data=User.objects.create_user(username=username,email=email,password=password)
             data.save()
             token = Token.objects.create(user=data)
            return redirect('login_form-view')  

    return render(request, 'register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            print(token.key)
            return redirect('home-view')
        else:
            return JsonResponse({'error': 'Invalid login credentials'}, status=400)

    return render(request, 'login.html')

# @api_view(['POST'])
# def login(request):
#     user = get_object_or_404(User, username=request.data['username'])
#     if not user.check_password(request.data['password']):
#         return Response("missing user", status=status.HTTP_404_NOT_FOUND)
#     token, created = Token.objects.get_or_create(user=user)
#     serializer = UserSerializer(user)
#     return Response({'token': token.key, 'user': serializer.data})


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def logout_view(request):
    # Đăng xuất người dùng
    logout(request)

    # Xoá token (nếu bạn muốn)
    request.auth.delete()
    
    return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)

def home(request):

    if 'user_id' in request.session and 'username' in request.session:
        user_id = request.session['user_id']
        username = request.session['username']
        
        return render(request, 'dashboard/index.html', {'user_id': user_id, 'username': username})
    else:
        return render(request,'dashboard/index.html')
    

def managerment_user(request):
    all_users = User.objects.all()
    return render(request,'dashboard/tables/datatables.html',{'all_users': all_users})