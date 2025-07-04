# Generated by Django 4.2.10 on 2025-06-25 13:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_alter_student_marks'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='marks',
        ),
        migrations.RemoveField(
            model_name='student',
            name='subject',
        ),
        migrations.RemoveField(
            model_name='student',
            name='user',
        ),
        migrations.CreateModel(
            name='StudentMark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=100)),
                ('marks', models.PositiveIntegerField()),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.student')),
            ],
        ),
    ]
