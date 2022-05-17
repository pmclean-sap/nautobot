# Generated by Django 3.2.13 on 2022-05-16 23:22

import django.core.serializers.json
from django.db import migrations, models
import django.db.models.deletion
import nautobot.core.fields
import nautobot.extras.models.groups
import nautobot.extras.models.mixins
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('extras', '0033_add__optimized_indexing'),
    ]

    operations = [
        migrations.CreateModel(
            name='DynamicGroupProxy',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('extras.dynamicgroup',),
        ),
        migrations.CreateModel(
            name='SavedFilter',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created', models.DateField(auto_now_add=True, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                ('_custom_field_data', models.JSONField(blank=True, default=dict, encoder=django.core.serializers.json.DjangoJSONEncoder)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('slug', nautobot.core.fields.AutoSlugField(blank=True, max_length=100, populate_from='name', unique=True)),
                ('description', models.CharField(blank=True, max_length=200)),
                ('filter', models.JSONField(default=dict, editable=False, encoder=django.core.serializers.json.DjangoJSONEncoder)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
            ],
            options={
                'ordering': ['content_type', 'name'],
            },
            bases=(nautobot.extras.models.groups.DynamicGroupFilteringMixin, models.Model, nautobot.extras.models.mixins.DynamicGroupMixin),
        ),
        migrations.CreateModel(
            name='DynamicGroupMembership',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('operator', models.CharField(default='union', max_length=12)),
                ('filter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dynamic_group_memberships', to='extras.savedfilter')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dynamic_group_groups', to='extras.dynamicgroupproxy')),
                ('parent_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dynamic_group_memberships', to='extras.dynamicgroup')),
            ],
            options={
                'ordering': ['parent_group', 'group', 'filter'],
                'unique_together': {('filter', 'parent_group'), ('group', 'parent_group')},
            },
        ),
        migrations.CreateModel(
            name='DynamicGroupMembershipProxy',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('extras.dynamicgroupmembership',),
        ),
        migrations.AddField(
            model_name='dynamicgroup',
            name='filters',
            field=models.ManyToManyField(related_name='dynamic_groups', through='extras.DynamicGroupMembership', to='extras.SavedFilter'),
        ),
        migrations.AddField(
            model_name='dynamicgroup',
            name='groups',
            field=models.ManyToManyField(related_name='dynamic_groups', through='extras.DynamicGroupMembershipProxy', to='extras.DynamicGroupProxy'),
        ),
    ]
