# Generated by Django 3.1.1 on 2021-05-04 21:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appFactInv', '0004_auto_20210504_1319'),
    ]

    operations = [
        migrations.AddField(
            model_name='encabezado_factura',
            name='descuentot',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=6),
        ),
    ]
