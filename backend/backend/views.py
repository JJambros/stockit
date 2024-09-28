from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET'])
def my_data(request):
    data = {
        'message': 'Hello from Django!'
    }
    return Response(data)
