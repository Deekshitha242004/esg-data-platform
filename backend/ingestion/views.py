import pandas as pd

from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Organization, Upload, EmissionRecord


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