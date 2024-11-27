from django.utils.timezone import now
from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Employee, Record


@receiver(pre_save, sender=Employee)
def create_or_update_record(sender, instance, **kwargs):
    # Avoid recursion using a signal-safe flag
    if hasattr(instance, '_signal_processing') and instance._signal_processing:
        return

    instance._signal_processing = True  # Set the flag to prevent recursion

    if instance.pk:  # Check if the instance exists in the database
        try:
            previous_status = Employee.objects.get(pk=instance.pk).status
        except Employee.DoesNotExist:
            previous_status = None

        # Transition from 'inactive' to 'active'
        if previous_status == 'inactive' and instance.status == 'active':
            Record.objects.create(
                employee=instance,
                start_record_time=now()
            )

        # Transition from 'active' to 'inactive'
        elif previous_status == 'active' and instance.status == 'inactive':
            record = Record.objects.filter(employee=instance, end_record_time__isnull=True).last()
            if record:
                record.end_record_time = now()
                record.save()

    instance._signal_processing = False  # Reset the flag