# Generated by Django 4.2 on 2023-05-05 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('condominio', '0016_alter_conta_condominio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conta',
            name='status',
            field=models.CharField(choices=[('Ativa', 'Ativa'), ('Inativa', 'Inativa')], default='Ativa', max_length=10),
        ),
        migrations.AlterField(
            model_name='pessoa',
            name='status',
            field=models.CharField(choices=[('Ativa', 'Ativa'), ('Inativa', 'Inativa')], default='Ativa', max_length=10),
        ),
    ]
