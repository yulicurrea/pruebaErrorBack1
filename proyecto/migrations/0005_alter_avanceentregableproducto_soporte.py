# Generated by Django 5.0.1 on 2024-10-01 05:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proyecto', '0004_alter_avanceentregableproyecto_soporte'),
    ]

    operations = [
        migrations.AlterField(
            model_name='avanceentregableproducto',
            name='soporte',
            field=models.TextField(blank=True),
        ),
    ]
