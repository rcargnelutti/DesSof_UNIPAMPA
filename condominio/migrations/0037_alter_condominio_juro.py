# Generated by Django 4.2 on 2023-05-24 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('condominio', '0036_alter_condominio_juro'),
    ]

    operations = [
        migrations.AlterField(
            model_name='condominio',
            name='juro',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=10, verbose_name='juro ao mês (em percentual %):'),
        ),
    ]
