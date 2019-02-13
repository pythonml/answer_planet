# Generated by Django 2.1.7 on 2019-02-12 12:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0003_auto_20190212_1207'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usermatch',
            name='question',
        ),
        migrations.RemoveField(
            model_name='usermatch',
            name='user',
        ),
        migrations.RemoveField(
            model_name='useranswer',
            name='match',
        ),
        migrations.RemoveField(
            model_name='useranswer',
            name='score',
        ),
        migrations.RemoveField(
            model_name='userevent',
            name='match',
        ),
        migrations.AddField(
            model_name='userevent',
            name='user_answer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='mainapp.UserAnswer'),
        ),
        migrations.DeleteModel(
            name='UserMatch',
        ),
    ]
