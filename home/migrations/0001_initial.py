# Generated by Django 3.2.5 on 2022-05-09 20:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Userreg',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sess_id', models.CharField(max_length=400)),
                ('email', models.EmailField(max_length=254)),
                ('domain', models.CharField(max_length=20)),
                ('passcode', models.CharField(max_length=6)),
                ('passres', models.CharField(max_length=1)),
                ('errormsg', models.CharField(default='', max_length=100)),
                ('username', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Usersessn',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=10)),
                ('userbucket', models.CharField(max_length=30)),
                ('usertemplates', models.CharField(max_length=30)),
                ('dtsite', models.CharField(max_length=10)),
                ('searchkey', models.CharField(max_length=100)),
                ('sess_id', models.CharField(max_length=500)),
                ('sritems', models.JSONField(default=[])),
                ('metadata', models.JSONField(default={'currpg': 0, 'currvw': 0, 'dtsloc': 0, 'labels': {}, 'numitems': 0})),
                ('currimage', models.JSONField(default={})),
                ('dtssmrypg', models.CharField(max_length=100)),
                ('sgmk', models.JSONField(default={'instname': 0, 'insturl': 0, 'setuptime': 0, 'urltime': 0, 'vmtype': 0})),
                ('lclnb', models.JSONField(default={'instname': 0, 'insturl': 0, 'setuptime': 0, 'urltime': 0, 'vmtype': 0})),
            ],
        ),
    ]
