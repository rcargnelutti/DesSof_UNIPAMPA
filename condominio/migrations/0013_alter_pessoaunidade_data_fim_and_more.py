# Generated by Django 4.2 on 2023-04-29 02:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('condominio', '0012_remove_pessoaunidade_pessoa_pessoaunidade_pessoa'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pessoaunidade',
            name='data_fim',
            field=models.DateField(blank=True, null=True, verbose_name='data de fim'),
        ),
        migrations.AlterField(
            model_name='pessoaunidade',
            name='data_inicio',
            field=models.DateField(null=True, verbose_name='data de início'),
        ),
        migrations.AlterField(
            model_name='pessoaunidade',
            name='vinculo',
            field=models.CharField(choices=[('Proprietário', 'Proprietário'), ('Locatário', 'Locatário')], max_length=15),
        ),
    ]
