# Generated by Django 5.1.2 on 2024-10-22 03:23

from django.db import migrations

def criar_setor(apps, schema_editor):
    Setor = apps.get_model('gestao_de_indicadores', 'Setor')
    Setor.objects.create(nome='Segurança')


class Migration(migrations.Migration):

    dependencies = [
        ('gestao_de_indicadores', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(criar_setor),
    ]
