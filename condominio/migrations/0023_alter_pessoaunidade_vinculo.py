# Generated by Django 4.2 on 2023-05-11 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('condominio', '0022_alter_despesa_rateio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pessoaunidade',
            name='vinculo',
            field=models.CharField(choices=[('P', 'Proprietário'), ('L', 'Locatário')], max_length=15),
        ),
    ]
