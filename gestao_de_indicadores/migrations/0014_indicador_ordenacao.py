# Generated by Django 5.1.3 on 2024-11-12 01:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestao_de_indicadores', '0013_vincular_indicador_pai_painel_kpi'),
    ]

    operations = [
        migrations.AddField(
            model_name='indicador',
            name='ordenacao',
            field=models.IntegerField(default=1),
        ),
    ]