import pandas as pd

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView

from .models import Organization, Upload, EmissionRecord
from .serializers import EmissionRecordSerializer


class SAPUploadView(APIView):

    def post(self, request):

        file = request.FILES['file']

        df = pd.read_csv(file)

        organization = Organization.objects.first()

        upload = Upload.objects.create(
            organization=organization,
            source_type='SAP',
            file_name=file.name
        )

        for _, row in df.iterrows():

            status = 'PENDING'

            if row['quantity'] < 0:
                status = 'ERROR'

            EmissionRecord.objects.create(
                organization=organization,
                upload=upload,
                activity_type=row['activity_type'],
                quantity=row['quantity'],
                unit=row['unit'],
                scope=row['scope'],
                status=status
            )

        return Response({
            "message": "SAP CSV uploaded successfully"
        })


class UtilityUploadView(APIView):

    def post(self, request):

        file = request.FILES['file']

        df = pd.read_csv(file)

        organization = Organization.objects.first()

        upload = Upload.objects.create(
            organization=organization,
            source_type='UTILITY',
            file_name=file.name
        )

        for _, row in df.iterrows():

            status = 'PENDING'

            if row['kwh'] < 0:
                status = 'ERROR'

            EmissionRecord.objects.create(
                organization=organization,
                upload=upload,
                activity_type='Electricity Usage',
                quantity=row['kwh'],
                unit='kWh',
                scope='Scope 2',
                status=status
            )

        return Response({
            "message": "Utility CSV uploaded successfully"
        })


class TravelUploadView(APIView):

    def post(self, request):

        file = request.FILES['file']

        df = pd.read_csv(file)

        organization = Organization.objects.first()

        upload = Upload.objects.create(
            organization=organization,
            source_type='TRAVEL',
            file_name=file.name
        )

        for _, row in df.iterrows():

            status = 'PENDING'

            if row['distance_km'] < 0:
                status = 'ERROR'

            EmissionRecord.objects.create(
                organization=organization,
                upload=upload,
                activity_type='Flight Travel',
                quantity=row['distance_km'],
                unit='km',
                scope='Scope 3',
                status=status
            )

        return Response({
            "message": "Travel CSV uploaded successfully"
        })


class EmissionRecordListView(ListAPIView):

    queryset = EmissionRecord.objects.all().order_by('-created_at')

    serializer_class = EmissionRecordSerializer