from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from ..models import UserProfile
from ..serializers import UserProfileSerializer


# --------- PROFILE VIEWS (For managing user profiles) --------- #

# Get/update the logged-in user's profile
@api_view(['GET', 'PUT'])
def user_profile_detail(request):
    user = request.user  # Get the currently logged-in user
    try:
        profile = UserProfile.objects.get(user=user, is_deleted=False)  # Check for soft deletion
    except UserProfile.DoesNotExist:
        return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        # Return the user's profile information
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)

    elif request.method == 'PUT':
        # Update the user's profile
        serializer = UserProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
