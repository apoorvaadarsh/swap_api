from django.http import JsonResponse
from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response

from ml.Helper import Helper

STATIC_IMAGE_PATH = "./images/temp.jpg"

@api_view(['POST'])
def checkImages(request):
        imageUrl=request.data['imageUrl']
        signatureUrl=request.data['signatureUrl']
        face_found,signature_found = False,False
        newFace,newSign=imageUrl,signatureUrl

        model_helper = Helper()
        
        model_helper.download_img(imageUrl)
        
        if model_helper.find_face(STATIC_IMAGE_PATH) == True :
            face_found=True
        else:
            signature_found=True
            newSign,newFace=imageUrl,signatureUrl
        
        
        model_helper.download_img(signatureUrl)
        if model_helper.find_face(STATIC_IMAGE_PATH) == True :
            face_found=True
            newSign,newFace=imageUrl,signatureUrl
            
        else:
            signature_found=True
            

        print(face_found,signature_found,36)    
        imageUrl,signatureUrl=newFace,newSign
        # if face_found == False :
        success=(face_found and signature_found)
        
        response={
            'imageUrl':imageUrl,
            'signatureUrl':signatureUrl,
            'SUCCESS':success,
        }

        
        if(not success):
            response['imageUrl']=request.data['imageUrl']
            response['signatureUrl']=request.data['signatureUrl']
        
        
        return Response(response)
