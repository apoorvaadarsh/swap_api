from django.http import JsonResponse
from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['POST'])

def checkImages(request):
        image_url=request.data['image_url']
        signature_url=request.data['signature_url']
        response={
            'image_url':image_url,
            'signature_url':signature_url,
            'SUCCESS':'true',
            'request':request.data,
        }
        print(request.data,'this is request')
        return Response(response)
