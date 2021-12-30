from django.shortcuts import get_object_or_404
from rest_framework import serializers, viewsets
from rest_framework.response import Response
from rest_framework.status import HTTP_202_ACCEPTED, HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR
from .models import Company
from .serializers import CompanySerializers
from random import random
import pandas as pd
from django.conf import settings
from django.db import IntegrityError
import os
import logging
logger = logging.getLogger('django')


# Create your views here.
class CompanyViewsets(viewsets.ModelViewSet):
    """
        Clase para montar el API del CRUD para las Compañías
        
        @method [POST,GET,PUT,DELETE]
        
        @responses: 
            - 200:
                OK
            - 201:
                CREATED
            - 204:
                DELETED
            - 404:
                NOT FOUND
            - 400:
                BAD REQUEST
            - 500:
                INTERNAL SERVER ERROR
    """
    try:
        http_method_names = ['get', 'post','put','delete']
        queryset = Company.objects.all()
        serializer_class = CompanySerializers

        def create(self, request, *args, **kwargs):
            """
                Función que se manda llamar por POST
                @method: 
                    POST
                @params:
                    - nameCompany : String
                    - dscCompany : String
                    - tickerCompany : String
                    - valCompany : list[int]
                
                @response:
                    - 201 : CREATED
                    - 400 : BAD REQUEST
                    - 500 : INTERNAL SERVER ERROR
            """
            try:
                if 'valCompany' not in request.data or request.data['valCompany'] is None:
                    request.data['valCompany'] = self.generate_random_values()
                
                if not self.validate_ticker():
                    data = {
                        "tickerCompany": [
                            "Formato de Ticker no permitido!"
                        ]
                    }
                    return Response(data=data,status=HTTP_400_BAD_REQUEST)
                
                if not self.validate_valCompany():
                    data = {
                        "valCompany": [
                            "El formato o contenido de los valores de la compañía son incorrectos!"
                        ]
                    }
                    return Response(data=data,
                                    status=HTTP_400_BAD_REQUEST)

                company_serializer = CompanySerializers(data=request.data)
                if company_serializer.is_valid():
                    return super().create(request, *args, **kwargs)
                
                return Response(company_serializer.errors,status=HTTP_400_BAD_REQUEST)
            except Exception as e:
                logger.error(e)
                return Response(status=HTTP_500_INTERNAL_SERVER_ERROR)
        
        def update(self, request, *args, **kwargs):
            """
                Función que se manda llamar por PUT para actualizar
                @method: 
                    PUT
                @params:
                    - uuidCompany : String
                
                @responses:
                    - 200 : OK
                    - 400 : BAD REQUEST
                    - 500 : INTERNAL SERVER ERROR
            """
            try:
                if 'valCompany' in request.data:
                    if not self.validate_valCompany():
                        data = {
                            "valCompany": [
                                "El formato o contenido de los valores de la compañía son incorrectos!"
                            ]
                        }
                        return Response(data=data,
                                        status=HTTP_400_BAD_REQUEST)
                return super().update(request, *args, **kwargs)
            except Exception as e:
                logger.error(e)
                return Response(status=HTTP_500_INTERNAL_SERVER_ERROR)

    except Exception as e:
        logger.error(e)

    def generate_random_values(self):
        """
            Función para generar los valores aleatorios para el arreglo de los Valores de mercado
            @return: 
                - list[float]
        """
        try:
            rdmList = [round(random()*100,2) for idx in range(50)]
            return rdmList
        except Exception as e:
            raise (e)

    def validate_ticker(self):
        """
            Función para validar el Ticker de la compañía y que este pertenezca a la lista 
            de NYSE
            @return:
                - bool
        """
        try:
            df = pd.read_csv(os.path.join(settings.BASE_DIR,"backendCRUD/utils/NYSE.csv"))
            df = list(df['Symbol'])
            if self.request.data['tickerCompany'] not in df:
                return False
            return True
        except Exception as e:
            raise(e)

    def validate_valCompany(self):
        """
            Función para validar que los valores del arreglo de valCompany sean correctos y esperados
            @return:
                - bool
        """
        try:
            if len(self.request.data['valCompany']) > 50 or not isinstance(
                self.request.data['valCompany'],list):
                return False
            
            for value in self.request.data['valCompany']:
                flag_value = False
                try:
                    value = int(value)
                except:
                    try:
                        value = float(value)
                    except:
                        return False
                if isinstance(value,float):
                    flag_value = True
                if isinstance(value,int):
                    flag_value = True
                
                if not flag_value:
                    return False
            
            return True
        except Exception as e:
            raise(e)