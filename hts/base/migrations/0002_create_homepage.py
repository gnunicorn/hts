# -*- coding: utf-8 -*-
from django.db import migrations


def create_homepage(apps, schema_editor):
    # Get models
    ContentType = apps.get_model('contenttypes.ContentType')
    Page = apps.get_model('wagtailcore.Page')
    Site = apps.get_model('wagtailcore.Site')
    RegularPage = apps.get_model('base.RegularPage')

    # Delete the default homepage
    # If migration is run multiple times, it may have already been deleted
    Page.objects.filter(id=2).delete()

    # Create content type for homepage model
    homepage_content_type, __ = ContentType.objects.get_or_create(
        model='regularpage', app_label='base')

    # Create a new homepage
    homepage = RegularPage.objects.create(
        title="Home",
        draft_title="Home",
        slug='home',
        content_type=homepage_content_type,
        path='00010001',
        depth=2,
        numchild=0,
        url_path='/home/',
    )

    # Create a site with the new homepage set as the root
    Site.objects.create(
        hostname='localhost', root_page=homepage, is_default_site=True)


def remove_homepage(apps, schema_editor):
    # Get models
    ContentType = apps.get_model('contenttypes.ContentType')
    RegularPage = apps.get_model('base.RegularPage')

    # Delete the default homepage
    # Page and Site objects CASCADE
    RegularPage.objects.filter(slug='home', depth=2).delete()



class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_homepage, remove_homepage),
    ]
