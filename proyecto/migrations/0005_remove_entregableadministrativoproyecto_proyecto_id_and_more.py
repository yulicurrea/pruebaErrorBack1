# Generated by Django 5.0.1 on 2024-04-21 17:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('proyecto', '0004_remove_avanceentregableproducto_estadoproceso_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='entregableadministrativoproyecto',
            name='proyecto_id',
        ),
        migrations.DeleteModel(
            name='EntregableAdministrativoProducto',
        ),
        migrations.DeleteModel(
            name='EntregableAdministrativoProyecto',
        ),
    ]
