# Generated by Django 3.1.14 on 2022-03-19 23:21

from django.db import migrations, IntegrityError
from nautobot.dcim.choices import InterfaceStatusChoices
from nautobot.extras.management import export_statuses_from_choiceset


def populate_interface_status(app, schema):

    Status = app.get_model("extras.Status")
    Interface = app.get_model("dcim.Interface")
    ContentType = app.get_model("contenttypes.ContentType")

    interface_content_type = ContentType.objects.get_for_model(Interface)
    choices = export_statuses_from_choiceset(InterfaceStatusChoices)

    # Create Interface Statuses and add dcim.Interface to its content_types
    for choice_kwargs in choices:
        try:
            obj, created = Status.objects.get_or_create(**choice_kwargs)
        except IntegrityError:
            choice_kwargs.pop("color")
            obj, created = Status.objects.get_or_create(**choice_kwargs)
        except Exception as err:
            raise SystemExit(
                f"Unexpected error while running data migration to populate" f"status for dcim.interface: {err}"
            )

        obj.content_types.add(interface_content_type)

    # populate existing interfaces status
    active_status = Status.objects.get(slug=InterfaceStatusChoices.STATUS_ACTIVE)
    for interface in Interface.objects.all():
        interface.status = active_status
        interface.save()


def reverse_populate_interface_status(app, schema_editor):
    Status = app.get_model("extras.Status")
    Interface = app.get_model("dcim.Interface")
    ContentType = app.get_model("contenttypes.ContentType")

    interface_content_type = ContentType.objects.get_for_model(Interface)

    for interface in Interface.objects.filter(status__slug=InterfaceStatusChoices.STATUS_ACTIVE):
        interface.status = None
        interface.save()

    for status in Status.objects.filter(content_types__in=[interface_content_type]):
        status.content_types.remove(interface_content_type)


class Migration(migrations.Migration):

    dependencies = [
        ("dcim", "0010_interface_status"),
    ]

    operations = [
        migrations.RunPython(populate_interface_status, reverse_populate_interface_status),
    ]
