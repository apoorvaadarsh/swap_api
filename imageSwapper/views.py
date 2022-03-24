from django.http import JsonResponse
from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response

from ml.Helper import Helper

STATIC_IMAGE_PATH = "./images/temp.jpg"

@api_view(['POST'])
def checkImages(request):
        image_url=request.data['image_url']
        signature_url=request.data['signature_url']
        face_found = True

        model_helper = Helper()
        model_helper.download_img(image_url)
        if models.find_face(STATIC_IMAGE_PATH) == False :
            face_found = False
        
        model_helper.download_img(signature_url)
        if models.find_face(STATIC_IMAGE_PATH) == False :
            pass
            
        if face_found == False :


        
        response={
            'image_url':image_url,
            'signature_url':signature_url,
            'SUCCESS':'true',
            'request':request.data,
        }
        print(request.data,'this is request')
        return Response(response)
