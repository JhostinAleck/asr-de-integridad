from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .authentication import CustomAuthentication

class TestDataView(APIView):
    authentication_classes = [CustomAuthentication]
    
    def get(self, request):
        return Response({"message": "Data retrieved successfully"})
        
    def put(self, request):
        # Si llegamos aquí, la autenticación fue exitosa
        return Response({"message": "Data updated successfully"})