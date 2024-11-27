from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Employee, Record, ArchiveRecord
from rest_framework.decorators import permission_classes
from .serializers import EmployeeSerializer, EmployeeDetailSerializer
from rest_framework.permissions import IsAuthenticated


@permission_classes([IsAuthenticated])
class EmployeeViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return Employee.objects.filter(status__in=['active', 'inactive'])

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return EmployeeDetailSerializer
        return EmployeeSerializer

    def retrieve(self, request, *args, **kwargs):
        employee = get_object_or_404(Employee, pk=kwargs['pk'])
        if employee.status == 'terminated':
            return Response(
                {"detail": f"{employee.name} {employee.surname} has left the job."},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = self.get_serializer(employee)
        return Response({"data": serializer.data})

    def destroy(self, request, *args, **kwargs):
        return Response(
            {"detail": "You can not delete"},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )





@permission_classes([IsAuthenticated])
class MoveRecordsToArchiveView(APIView):
    def post(self, request, *args, **kwargs):
        employee_id = request.data.get('employee_id')
        if not employee_id:
            return Response({"error": "Employee ID is required."}, status=status.HTTP_400_BAD_REQUEST)
        employee = get_object_or_404(Employee, pk=employee_id)
        records = Record.objects.filter(employee=employee)
        if not records.exists():
            return Response({"message": "No records found for this employee."}, status=status.HTTP_200_OK)
        archive_records = []
        for record in records:
            archive_records.append(
                ArchiveRecord(
                    employee=record.employee,
                    start_record_time=record.start_record_time,
                    end_record_time=record.end_record_time,
                    duration=record.duration,
                    price=record.price
                )
            )
        ArchiveRecord.objects.bulk_create(archive_records)
        records.delete()
        return Response({"message": "Records moved to archive successfully."}, status=status.HTTP_200_OK)
