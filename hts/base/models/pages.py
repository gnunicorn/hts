from __future__ import unicode_literals

from django.db import models

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel

from wagtail.admin.edit_handlers import (
    FieldPanel,
    FieldRowPanel,
    InlinePanel,
    MultiFieldPanel,
    PageChooserPanel,
    StreamFieldPanel,
)

from instance_selector.edit_handlers import InstanceSelectorPanel

from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Collection, Page, Orderable
from wagtail.documents.models import Document
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.documents.edit_handlers import DocumentChooserPanel
from wagtail.search import index
from wagtail.snippets.models import register_snippet
from modelcluster.models import ClusterableModel
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

from misago.users.models import User

from ..blocks import DEFAULT_BLOCKS


class Author(Page):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content_panels = Page.content_panels + [
        FieldPanel('user'),
    ]

class AuthorArticleRel(Orderable):
    author = ParentalKey(Author, on_delete=models.CASCADE)
    article = ParentalKey('Article', related_name="authors", on_delete=models.CASCADE)

class ArticleTag(TaggedItemBase):
    content_object = ParentalKey('base.Article',
        on_delete=models.CASCADE, related_name='tagged_items')


class RegularPage(Page):

    content = StreamField(
        DEFAULT_BLOCKS, verbose_name="Article", blank=True
    )
    content_panels = Page.content_panels + [
        StreamFieldPanel('content'),
    ]


class Article(Page):
    """
    A generic content page. On this demo site we use it for an about page but
    it could be used for any type of page content that only needs a title,
    image, introduction and body field
    """

    tags = ClusterTaggableManager(through=ArticleTag, blank=True)
    related_discussion = models.ForeignKey("misago_threads.Thread", null=True, on_delete=models.SET_NULL)

    content = StreamField(
        DEFAULT_BLOCKS, verbose_name="Article", blank=True
    )
    content_panels = Page.content_panels + [
        StreamFieldPanel('content'),
        FieldPanel('tags'),
        InlinePanel(
            'authors', label="Author(s)",
            panels=None, min_num=1),
        InstanceSelectorPanel("related_discussion"),
    ]
