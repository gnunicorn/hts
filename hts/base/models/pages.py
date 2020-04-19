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

from django.utils.functional import cached_property

from misago.users.models import User
from misago.threads.models.post import Post
from misago.readtracker.poststracker import make_read
from wagtailmetadata.models import MetadataPageMixin
from fontawesome.fields import IconField

from ..blocks import DEFAULT_BLOCKS

class CommonPageProperties(MetadataPageMixin, models.Model):
    css_page_classes = models.CharField(max_length=255, blank=True, null=True,
        verbose_name="Custom html body classes")
    
    promote_panels = MetadataPageMixin.promote_panels + [
        MultiFieldPanel([FieldPanel('css_page_classes')], "Page Customisation")
    ]

    class Meta:
        abstract = True


class Author(CommonPageProperties, Page):
    user = models.ForeignKey(User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True)

    avatar = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    name = models.CharField(max_length=255, blank=True, null=True)
    website = models.CharField(max_length=255, blank=True, null=True)
    bio = RichTextField(blank=True, null=True)
    
    content_panels = Page.content_panels + [
        FieldPanel('user'),
        MultiFieldPanel([
            ImageChooserPanel('avatar'),
            FieldPanel('name'),
            FieldPanel('website'),
            FieldPanel('bio'),
            ], "Author Overwrites")
    ]

    def _get_inner(self, local, profile_field):
        if local:
            return local

        if self.user:
            return self.user.profile_fields.get(profile_field, None) 

    def get_name(self):
        return self._get_inner(self.name, "real_name")

    def get_any_name(self):
        name = self.get_name()

        if not name and self.user:    
            name = self.user.username
        return name

    def get_website(self):
        return self._get_inner(self.website, "website")

    def get_bio(self):
        return self._get_inner(self.bio, "bio")

    def get_pronoun(self):
        if self.user:
            return self.user.profile_fields.get("pronouns", None)

    def get_twitter(self):
        if self.user:
            return self.user.profile_fields.get("twitter", None)

    @cached_property
    def get_articles(self):
        articles = [a.article for a in self.articles
        # FIXME: Also shows non-public right now
            # .filter("article__live=True")
            .order_by('-article__last_published_at')
            .prefetch_related("article")[:12]]
        return articles

class AuthorArticleRel(Orderable):
    author = ParentalKey(Author, on_delete=models.CASCADE,
        related_name="articles")
    article = ParentalKey('Article', related_name="authors",
        on_delete=models.CASCADE)

class ArticleTag(TaggedItemBase):
    content_object = ParentalKey('base.Article',
        on_delete=models.CASCADE, related_name='tagged_items')


class RegularPage(CommonPageProperties, Page):

    content = StreamField(
        DEFAULT_BLOCKS, verbose_name="Article", blank=True
    )
    content_panels = Page.content_panels + [
        StreamFieldPanel('content'),
    ]


class Article(CommonPageProperties, Page):
    """
    A generic content page. On this demo site we use it for an about page but
    it could be used for any type of page content that only needs a title,
    image, introduction and body field
    """
    icon = IconField()
    background_color = models.CharField(max_length=120, blank=True, null=True)
    foreground_color = models.CharField(max_length=120, blank=True, null=True)
    cover = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    tags = ClusterTaggableManager(through=ArticleTag, blank=True)
    related_discussion = models.ForeignKey("misago_threads.Thread",
        blank=True, null=True, on_delete=models.SET_NULL)

    content = StreamField(
        DEFAULT_BLOCKS, verbose_name="Article", blank=True
    )
    content_panels = Page.content_panels + [
        StreamFieldPanel('content'),
        InlinePanel(
            'authors', label="Author(s)",
            panels=None, min_num=1),
        InstanceSelectorPanel("related_discussion"),
    ]

    promote_panels = [
        MultiFieldPanel([
            FieldPanel('icon'),
            ImageChooserPanel('cover'),
            FieldPanel('background_color'),
            FieldPanel('foreground_color'),
        ], "Page Design"),
        FieldPanel('tags'),
    ] + CommonPageProperties.promote_panels

    @cached_property
    def comments(self):
        comments = self.discussions_query().order_by('likes')[:5]
        make_read(comments)
        return comments
    
    @cached_property
    def get_authors(self):
        return [a.author for a in self.authors.prefetch_related("author")]

    def discussions_query(self):
        return Post.objects.filter(
            models.Q(
                thread=self.related_discussion,
                is_hidden=False,
                is_event=False,
                is_unapproved=False)
            & ~models.Q(thread__first_post=models.F("id"))
            )
