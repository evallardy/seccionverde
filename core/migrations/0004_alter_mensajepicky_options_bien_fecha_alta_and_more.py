# Generated by Django 4.0.4 on 2023-03-05 01:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_remove_mensajepicky_opcion0_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mensajepicky',
            options={'ordering': ['number', '-fecha_alta'], 'verbose_name': 'Mensaje picky', 'verbose_name_plural': 'Mensajes picky'},
        ),
        migrations.AddField(
            model_name='bien',
            name='fecha_alta',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Fecha alta'),
        ),
        migrations.AlterField(
            model_name='prueba',
            name='fecha',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Fecha'),
        ),
    ]
