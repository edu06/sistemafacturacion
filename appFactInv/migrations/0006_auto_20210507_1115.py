# Generated by Django 3.1.1 on 2021-05-07 17:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appFactInv', '0005_encabezado_factura_descuentot'),
    ]

    operations = [
        migrations.RenameField(
            model_name='encabezado_factura',
            old_name='descuentot',
            new_name='descuento',
        ),
    ]
