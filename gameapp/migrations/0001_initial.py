# Generated by Django 3.2.12 on 2024-03-29 19:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=200)),
                ('Description', models.TextField()),
                ('Rules', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='game_matrix',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game_code', models.CharField(max_length=6)),
                ('matrix_map', models.CharField(default='[1,2,3,4,5,6,7,8,9]', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='game_room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Player2', models.CharField(max_length=100)),
                ('GameName', models.CharField(max_length=100)),
                ('game_code', models.CharField(max_length=6, unique=True)),
                ('Player1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('game_matrix', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gameapp.game_matrix')),
            ],
        ),
    ]
