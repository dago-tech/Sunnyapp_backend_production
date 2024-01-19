from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .serializers import DataItemSerializer
from .models import DataItem
from datetime import datetime, timedelta
import random


class CreateAPIView(generics.CreateAPIView):
    """
    Creación de fecha consecutiva y valor aleatorio
    """

    serializer_class = DataItemSerializer

    def create(self, request, *args, **kwargs):
        last_date = (
            DataItem.objects.latest("fecha").fecha
            if DataItem.objects.exists()
            else datetime.strptime("01/01/2024", "%d/%m/%Y")
        )

        new_date = last_date + timedelta(days=1)
        new_value = round(random.uniform(24.0, 29.9), 1)

        nuevo_item = {
            "fecha": new_date.strftime("%d/%m/%Y"),
            "valor": new_value,
        }

        serializer = self.get_serializer(data=nuevo_item)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class DataItemListAPIView(generics.ListAPIView):
    """
    Lista de DataItem con el metodo GET
    """

    serializer_class = DataItemSerializer
    queryset = DataItem.objects.all()

    def get(self, request, *args, **kwargs):
        try:
            # Verificar si ya existen registros en la base de datos
            if not DataItem.objects.exists():
                # Si no existen registros, crea unos nuevos
                self.create_initial_data()

            # Obtener todos los registros y retornar la respuesta
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

    def create_initial_data(self):
        """
        Crear la data inicial y guardarla en la base de datos
        """
        initial_data = [
            {"fecha": "01/01/2024", "valor": 29.1},
            {"fecha": "02/01/2024", "valor": 28.5},
            {"fecha": "03/01/2024", "valor": 28.1},
            {"fecha": "04/01/2024", "valor": 25.6},
            {"fecha": "05/01/2024", "valor": 24.8},
            {"fecha": "06/01/2024", "valor": 27.10},
            {"fecha": "07/01/2024", "valor": 29.9},
        ]

        for item in initial_data:
            new_item = DataItem(
                fecha=datetime.strptime(item["fecha"], "%d/%m/%Y"), valor=item["valor"]
            )
            new_item.save()


class DataItemDeleteAPIView(generics.DestroyAPIView):
    """
    Borrar un registro con el Metodo DELETE
    """

    serializer_class = DataItemSerializer
    queryset = DataItem.objects.all()
