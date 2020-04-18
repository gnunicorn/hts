# Generated by Django 2.2.10 on 2020-04-18 16:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0001_squashed_0021'),
        ('base', '0008_auto_20200416_1731'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='css_page_classes',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Custom html body classes'),
        ),
        migrations.AddField(
            model_name='article',
            name='search_image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image', verbose_name='Search image'),
        ),
        migrations.AddField(
            model_name='author',
            name='css_page_classes',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Custom html body classes'),
        ),
        migrations.AddField(
            model_name='author',
            name='search_image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image', verbose_name='Search image'),
        ),
        migrations.AddField(
            model_name='regularpage',
            name='css_page_classes',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Custom html body classes'),
        ),
        migrations.AddField(
            model_name='regularpage',
            name='search_image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image', verbose_name='Search image'),
        ),
    ]
