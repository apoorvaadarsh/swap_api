from django.http import JsonResponse
from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response

from ml.Helper import Helper

STATIC_IMAGE_PATH = "./images/temp.jpg"

@api_view(['POST'])
def checkImages(request):
        faceUrl=request.data['faceUrl']
        signatureUrl=request.data['signatureUrl']
        face_found,signature_found = False,False
        newFace,newSign=faceUrl,signatureUrl

        model_helper = Helper()
        
        model_helper.download_img(faceUrl)
        
        if model_helper.find_face(STATIC_IMAGE_PATH) == True :
            face_found=True
        else:
            signature_found=True
            newSign,newFace=faceUrl,signatureUrl
        
        
        model_helper.download_img(signatureUrl)
        if model_helper.find_face(STATIC_IMAGE_PATH) == True :
            face_found=True
            newSign,newFace=faceUrl,signatureUrl
            
        else:
            signature_found=True
            

        print(face_found,signature_found,36)    
        faceUrl,signatureUrl=newFace,newSign
        # if face_found == False :
        success=(face_found and signature_found)
        
        response={
            'faceUrl':faceUrl,
            'signatureUrl':signatureUrl,
            'SUCCESS':success,
        }

        
        if(not success):
            response['faceUrl']=request.data['faceUrl']
            response['signatureUrl']=request.data['signatureUrl']
        
        
        return Response(response)
