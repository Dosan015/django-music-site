from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .serializers import AudioSerializer, AudioPrivateSerializer
from ..models import Audio


class AudioList(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        audios = Audio.objects.all()
        serializer = AudioPrivateSerializer(audios, many=True)
        return Response(serializer.data)

    def post(self, request):
        audio = AudioPrivateSerializer(data=request.data)
        if audio.is_valid():
            audio.save()
            return Response({"status":"success","data":audio.data},status=status.HTTP_200_OK)
        else:
            return Response({"status":"error","data":audio.errors},status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def audioDetail(request, pk):
    try:
        audios = Audio.objects.get(pk=pk)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = AudioSerializer(audios, many=False)
    return Response(serializer.data)
