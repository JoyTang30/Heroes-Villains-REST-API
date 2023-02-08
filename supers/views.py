from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import SuperSerializer
from .models import Super

@api_view(['GET','POST'])
def supers_list(request):
    if request.method == 'GET':
        supers= Super.objects.all()
        supers_type_param= request.query_params.get('type')

        if supers_type_param:
            supers= supers.filter(super_type__type= supers_type_param)

            serializer= SuperSerializer(supers, many=True)
            return Response(serializer.data)
        else:
            custom_response_dictionary = {}

            #for super_type in supers:
            hero_info = Super.objects.filter(super_type_id=1)
            villian_info = Super.objects.filter(super_type_id=2)


            hero_serializer = SuperSerializer(hero_info, many=True)
            villian_serializer = SuperSerializer(villian_info, many=True)
            custom_response_dictionary = {
                "heroes":hero_serializer.data,
                "villians":villian_serializer.data
            }

            return Response(custom_response_dictionary)
    elif request.method == 'POST':
        serializer = SuperSerializer(data= request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status= status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def supers_detail(request, pk):
    supers = get_object_or_404(Super, pk=pk)
    if request.method == 'GET':
        serializer = SuperSerializer(supers)
        return Response(serializer.data)
    elif request.method == 'PUT':
       serializer=SuperSerializer(supers, data= request.data)
       serializer.is_valid(raise_exception= True)
       serializer.save()
       return Response(serializer.data)
    elif request.method == 'DELETE':
        supers.delete()
        return Response(status= status.HTTP_204_NO_CONTENT)


#    @api_view(['GET'])
#    def supers_type(request):
#        supers_type_param= request.query_params.get('type')
#
#        all_type= Super.objects.all()
#        print(supers_type_param)
#
#        if supers_type_param:
#            all_type= all_type.filter(super__type= supers_type_param)
#
#        serializer= SuperSerializer(supers, many=True)
#        
#        return Response(serializer.data)
