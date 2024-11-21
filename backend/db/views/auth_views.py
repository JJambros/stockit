from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.contrib.auth import authenticate


# --------- AUTHENTICATION VIEWS --------- #

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    from django.contrib.auth.models import User  # Import moved here
    from rest_framework.authtoken.models import Token  # Import moved here
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user is not None:
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'user_id': user.id}, status=200)
    return Response({'error': 'Invalid Credentials'}, status=400)

@api_view(['POST'])
def logout_view(request):
    request.user.auth_token.delete()
    return Response({'success': 'Logged out'}, status=status.HTTP_200_OK)


# --------- REGISTER USER VIEWS --------- #

@api_view(['POST'])
@permission_classes([AllowAny])  # Allow unauthenticated access
def register_user(request):
    from django.contrib.auth.models import User  # Import moved here
    username = request.data.get('username')
    password = request.data.get('password')
    if not username or not password:
        return Response({'error': 'Username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists.'}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=username, password=password)
    return Response({'message': 'User registered successfully!'}, status=status.HTTP_201_CREATED)


# --------- UPDATE PASSWORD VIEWS --------- #

@api_view(['PUT'])
def update_password(request):
    user = request.user
    old_password = request.data.get('old_password')
    new_password = request.data.get('new_password')

    if not old_password or not new_password:
        return Response({'error': 'Old and new passwords are required.'}, status=status.HTTP_400_BAD_REQUEST)

    if not user.check_password(old_password):
        return Response({'error': 'Old password is incorrect.'}, status=status.HTTP_400_BAD_REQUEST)

    user.set_password(new_password)
    user.save()
    return Response({'message': 'Password updated successfully.'}, status=status.HTTP_200_OK)
