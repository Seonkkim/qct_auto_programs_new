# Generated by Django 2.0.9 on 2018-12-26 07:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0004_auto_20181226_0658'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='build',
            name='description',
        ),
        migrations.AddField(
            model_name='build',
            name='gvm_id',
            field=models.TextField(blank=True, db_column='GVM_ID', null=True),
        ),
        migrations.AddField(
            model_name='build',
            name='project_name',
            field=models.TextField(blank=True, db_column='PROJECT_NAME', null=True),
        ),
        migrations.AlterField(
            model_name='build',
            name='apps_id',
            field=models.TextField(blank=True, db_column='APPS_ID', null=True),
        ),
        migrations.AlterField(
            model_name='build',
            name='au_tag',
            field=models.TextField(blank=True, db_column='AU_TAG', null=True),
        ),
        migrations.AlterField(
            model_name='build',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='build',
            name='release_date',
            field=models.TextField(blank=True, db_column='RELEASE_DATE', null=True),
        ),
        migrations.AlterField(
            model_name='build',
            name='release_note',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='build',
            name='sp_id_fk',
            field=models.ForeignKey(db_column='sp_id_fk', on_delete=django.db.models.deletion.CASCADE, to='db.Sp'),
        ),
        migrations.AlterField(
            model_name='build',
            name='status',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='build',
            name='wiki',
            field=models.TextField(blank=True, null=True),
        ),
    ]