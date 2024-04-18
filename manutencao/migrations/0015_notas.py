# Generated by Django 4.2.9 on 2024-04-18 13:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('manutencao', '0014_alter_especime_nome_cientifico'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateField(verbose_name='Data da manutenção')),
                ('titulo', models.CharField(max_length=200)),
                ('texto', models.TextField()),
                ('aquario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notas', to='manutencao.aquario')),
            ],
            options={
                'verbose_name': 'Nota',
                'verbose_name_plural': 'Notas',
                'ordering': ['data'],
            },
        ),
    ]