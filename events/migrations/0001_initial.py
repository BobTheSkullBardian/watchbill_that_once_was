# Generated by Django 3.1.3 on 2020-12-10 16:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sailors', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.DateField(help_text='Day of the Watch', unique=False, verbose_name='Day of the Watch')),
                ('position', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.position', verbose_name='Position')),
                ('stander', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sailors.sailor', verbose_name='Watch Stander')),
                ('acknowledged', models.BooleanField(blank=True, default=False, verbose_name='Watch Acknowledged')),
            ],
            options={
                'ordering': ('day', 'position__qual', 'position__label'),
                'verbose_name': 'Duty Day',
                'verbose_name_plural': 'Duty Days'},

            # options={
            #     'verbose_name': 'Duty Day',
            #     'verbose_name_plural': 'Duty Days',
            # },
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.CharField(blank=True, max_length=15, null=True, verbose_name='Watch Position')),
                # ('qual', models.ManyToManyField(blank=True, to='sailors.Qual', verbose_name='Watch Position')),
                ('qual', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='sailors.qual', verbose_name='Watch Position')),
                ('start_time', models.TimeField(help_text='Watch starting time', verbose_name='Watch starting time')),
                ('label', models.CharField(blank=True, default='', max_length=15, verbose_name='Label')),
                ('duration', models.IntegerField(blank=True, default=12, null=True)),
            ],
            options={
                # 'ordering': ('day',), 'verbose_name': 'Duty Day', 'verbose_name_plural': 'Duty Days'
                'ordering': ('qual', 'label'),
            },
        ),
        # migrations.CreateModel(
        #     name='Watch',
        #     fields=[
        #         ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
        #         ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.event', verbose_name='Duty Day')),
        #         ('position', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='events.position', verbose_name='Position')),
        #         ('stander', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sailors.sailor', verbose_name='Watch Stander')),
        #     ],
        #     options={
        #         'verbose_name': 'Watch',
        #         'verbose_name_plural': 'Watches',
        #     },
        # ),
    ]
