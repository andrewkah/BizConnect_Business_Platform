# Generated by Django 5.0.6 on 2024-07-03 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Bizconnect', '0008_scheduledmeeting_denial_reason'),
    ]

    operations = [
        migrations.CreateModel(
            name='InvestmentFunds',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('industry', models.CharField(max_length=100)),
                ('type', models.CharField(choices=[('equity', 'Equity'), ('debt', 'Debt'), ('convertible_note', 'Conertible Note')], max_length=100)),
                ('investment_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('contact_method', models.CharField(choices=[('email', 'Email'), ('phone', 'Phone')], max_length=100)),
                ('notes', models.TextField()),
                ('supporting_documents', models.FileField(blank=True, null=True, upload_to='supporting_documents/')),
            ],
        ),
        migrations.CreateModel(
            name='Investor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('individual', 'Individual'), ('organization', 'Organization')], max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('contact', models.CharField(max_length=20)),
                ('country', models.CharField(max_length=50)),
                ('capital', models.CharField(max_length=100)),
                ('information', models.TextField()),
                ('surname', models.CharField(blank=True, max_length=100, null=True)),
                ('firstname', models.CharField(blank=True, max_length=100, null=True)),
                ('gender', models.CharField(blank=True, max_length=10, null=True)),
                ('company', models.CharField(blank=True, max_length=100, null=True)),
                ('tourism', models.BooleanField(default=False)),
                ('media', models.BooleanField(default=False)),
                ('commercial', models.BooleanField(default=False)),
                ('estate', models.BooleanField(default=False)),
                ('manufacturing', models.BooleanField(default=False)),
                ('education', models.BooleanField(default=False)),
                ('health', models.BooleanField(default=False)),
                ('wholesale', models.BooleanField(default=False)),
            ],
        ),
    ]
