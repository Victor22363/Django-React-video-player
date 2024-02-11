from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import VideoSerializer
from one.models import Video

@api_view(['GET'])
def getAllData(request):
    raw = Video.objects.all()
    data = VideoSerializer(raw, many=True)
    return Response(data.data)

@api_view(['GET'])
def getSpecificData(request, index):
    raw = Video.objects.filter(id=index).first()
    data = VideoSerializer(raw, many=False)
    return Response(data.data)