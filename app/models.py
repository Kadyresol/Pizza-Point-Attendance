from decimal import Decimal
from django.db import models
from django.utils.timezone import now
from django.db.models.signals import pre_save
from django.db.models.signals import post_save
from django.db.models import Sum
from django.dispatch import receiver

class Employee(models.Model):
    STATUS_CHOICES = [
        ('inactive', 'Inactive'),
        ('active', 'Active'),
        ('terminated', 'Terminated'),
    ]
    name = models.CharField(max_length=100, blank=False)
    surname = models.CharField(max_length=100, blank=False)
    phone_number = models.CharField(max_length=100, blank=False)
    hourly_earning = models.DecimalField(decimal_places=2, max_digits=10, blank=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='inactive')
    pay_price = models.DecimalField(decimal_places=2, max_digits=10, default=0.00)
    

    def __str__(self):
        return f"{self.name} {self.surname}"

class Record(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='records', blank=False)
    date = models.DateField(blank=True, null=True)
    start_record_time = models.DateTimeField(null=True)
    end_record_time = models.DateTimeField(null=True)
    duration = models.DurationField(blank=True, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.start_record_time and self.end_record_time:
            self.date = self.start_record_time.date()
            self.duration = self.end_record_time - self.start_record_time
            hours_worked = Decimal(self.duration.total_seconds()) / Decimal(3600)
            self.price = round(hours_worked * self.employee.hourly_earning, 2)
        super().save(*args, **kwargs)

@receiver(pre_save, sender=Employee)
def create_or_update_record(sender, instance, **kwargs):
    if instance.pk:
        previous_status = Employee.objects.get(pk=instance.pk).status
        if previous_status == 'inactive' and instance.status == 'active':
            Record.objects.create(
                employee=instance,
                start_record_time=now()
            )
        elif previous_status == 'active' and instance.status == 'inactive':
            record = Record.objects.filter(employee=instance, end_record_time__isnull=True).last()
            if record:
                record.end_record_time = now()
                record.save()

    def __str__(self):
        return f"{self.employee.name} - {self.date}"

@receiver(post_save, sender=Record)
def update_employee_pay_price(sender, instance, **kwargs):
    employee = instance.employee
    employee.pay_price = employee.records.aggregate(total=Sum('price'))['total'] or Decimal('0.00')
    employee.save()

class ArchiveRecord(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, related_name='archived_records')
    start_record_time = models.DateTimeField(null=True)
    end_record_time = models.DateTimeField(blank=True, null=True)
    duration = models.DurationField(blank=True, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=True)
    archived_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Archived Record for {self.employee.name if self.employee else 'Unknown'}"