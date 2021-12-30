from backendCRUD.models import Company
from rest_framework.test import APITestCase
from rest_framework import status


class CompanyTests(APITestCase):
    """
        Pruebas para el CRUD de Compañías.
    """
    def test_create_company(self):
        """
        Método para testear la creación de una nueva compañía.
        """
        url = "/api/company/"
        data = {
            'nameCompany' : 'testCompany',
            'dscCompany' : "descripción de la compañía",
            'tickerCompany' : 'A',
            'valCompany' : None
        }
        response = self.client.post(url,data,format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Company.objects.count(),1)
        self.assertEqual(Company.objects.get().tickerCompany, 'A')

    def test_get_company(self):
        """
            Método para testear el obtener las companías
        """
        url = "/api/company/"
        data = {
            'nameCompany' : 'testCompany',
            'dscCompany' : "descripción de la compañía",
            'tickerCompany' : 'A',
            'valCompany' : None
        }
        response = self.client.post(url,data,format='json')
        response = self.client.get(url,format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['tickerCompany'],'A')

    def test_update_company(self):
        """
            Método para testear la actualización de una compañía
        """
        url = "/api/company/"
        data = {
            'nameCompany' : 'testCompany',
            'dscCompany' : "descripción de la compañía",
            'tickerCompany' : 'A',
            'valCompany' : None
        }
        response = self.client.post(url,data,format='json')
        response = self.client.get(url,format='json')
        
        
        newData = {
            'nameCompany' : 'UpdateTestCompany',
            'dscCompany' : "descripción de la compañía",
            'tickerCompany' : 'A',
            'valCompany' : response.data[0]['valCompany']
        }
        response = self.client.put(url+response.data[0]['uuidCompany']+"/",newData,format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_company(self):
        """
            Método para testear el borrar una compañía.
        """
        url = "/api/company/"
        data = {
            'nameCompany' : 'testCompany',
            'dscCompany' : "descripción de la compañía",
            'tickerCompany' : 'A',
            'valCompany' : None
        }
        response = self.client.post(url,data,format='json')
        response = self.client.get(url,format='json')

        response = self.client.delete(url+response.data[0]['uuidCompany']+"/",format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
