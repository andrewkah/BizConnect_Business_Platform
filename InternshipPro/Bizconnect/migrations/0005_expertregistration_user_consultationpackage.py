# Generated by Django 5.0.6 on 2024-06-27 11:43

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Bizconnect', '0004_alter_registration_user_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='expertregistration',
            name='user',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='ConsultationPackage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('package_type', models.CharField(choices=[('hourly', 'Hourly Rate'), ('retainer', 'Retainer-based'), ('project', 'Project-Based'), ('specialised', 'Specialised Challenge'), ('growth', 'Growth Strategy')], max_length=20)),
                ('package_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('expert', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Bizconnect.expertregistration')),
            ],
        ),
    ]
