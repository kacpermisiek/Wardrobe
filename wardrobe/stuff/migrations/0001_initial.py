# Generated by Django 4.1.2 on 2022-11-05 20:24

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('Dostępny', 'Dostępny'), ('Uszkodzony', 'Uszkodzony')], default='Dostępny', max_length=20)),
                ('date_added', models.DateField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='ItemTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(blank=True, max_length=200, null=True)),
                ('image', models.ImageField(default='default_item.png', upload_to='item_pics')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stuff.category')),
            ],
        ),
        migrations.CreateModel(
            name='SetTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='ItemRequired',
            fields=[
                ('itemtemplate_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='stuff.itemtemplate')),
                ('quantity_required', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('item_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='stuff.itemtemplate')),
            ],
            bases=('stuff.itemtemplate',),
        ),
        migrations.CreateModel(
            name='Set',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('set_status', models.CharField(default='Dostępny', max_length=20)),
                ('items', models.ManyToManyField(to='stuff.item')),
                ('set_template', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stuff.settemplate')),
            ],
            options={
                'ordering': ['set_status'],
            },
        ),
        migrations.CreateModel(
            name='ReservationEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField(blank=True, default=django.utils.timezone.now, null=True)),
                ('end_date', models.DateField(blank=True, default=django.utils.timezone.now, null=True)),
                ('taken', models.BooleanField(default=False)),
                ('set', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stuff.set')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='item',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stuff.itemtemplate'),
        ),
        migrations.AddField(
            model_name='settemplate',
            name='items_required',
            field=models.ManyToManyField(to='stuff.itemrequired'),
        ),
        migrations.CreateModel(
            name='CurrentSetTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('items_required', models.ManyToManyField(to='stuff.itemrequired')),
            ],
        ),
    ]
