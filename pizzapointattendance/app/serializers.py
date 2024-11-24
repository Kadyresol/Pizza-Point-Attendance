from rest_framework import serializers
from .models import Employee, Record

class RecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Record
        fields = ['id', 'date', 'duration', 'price']

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'name', 'surname', 'phone_number', 'hourly_earning']

class EmployeeDetailSerializer(serializers.ModelSerializer):

    records = RecordSerializer(many=True, read_only=True)

    class Meta:
        model = Employee
        fields = ['id', 'name', 'surname', 'phone_number', 'hourly_earning', 'pay_price', 'status', 'records']
