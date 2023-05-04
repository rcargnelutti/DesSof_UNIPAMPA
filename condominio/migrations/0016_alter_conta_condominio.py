# Generated by Django 4.2 on 2023-05-04 18:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('condominio', '0015_remove_conta_unidade_conta_condominio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conta',
            name='condominio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contas', to='condominio.condominio'),
        ),
    ]
