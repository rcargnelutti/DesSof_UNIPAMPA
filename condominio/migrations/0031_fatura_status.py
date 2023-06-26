# Generated by Django 4.2 on 2023-05-11 23:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('condominio', '0030_remove_fatura_pessoa_remove_fatura_vinculo_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='fatura',
            name='status',
            field=models.CharField(choices=[('ABERTO', 'Aberto'), ('PAGO', 'Pago')], default='ABERTO', max_length=6),
            preserve_default=False,
        ),
    ]
