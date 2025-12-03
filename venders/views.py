from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import VendorRegistrationSerializer

class VendorRegisterAPIView(APIView):
    def post(self, request):
        serializer = VendorRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            vendor = serializer.save()
            return Response(VendorRegistrationSerializer(vendor).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)