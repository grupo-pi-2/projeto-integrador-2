# Generated by Django 5.1.2 on 2024-10-26 03:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestao_de_indicadores', '0001_initial'),
        ('gestao_de_indicadores', '0003_indicador'),
        ('gestao_de_indicadores', '0007_cliente'),
    ]

    operations = [
        migrations.CreateModel(
            name='Servico',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_hora_inicio', models.DateTimeField()),
                ('data_hora_fim', models.DateTimeField()),
                ('status', models.CharField(choices=[('CON', 'Concluído'), ('PEN', 'Pendente'), ('CAN', 'Cancelado')], default='PEN', max_length=3)),
                ('periodo', models.CharField(max_length=7)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestao_de_indicadores.cliente')),
                ('indicador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestao_de_indicadores.indicador')),
                ('setor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestao_de_indicadores.setor')),
            ],
        ),
    ]
