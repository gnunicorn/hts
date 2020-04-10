"""
Blocks module entry point. Used to cleanly organize blocks into
individual files based on purpose, but provide them all as a
single `blocks` module.
"""

from django.utils.translation import gettext_lazy as _

from wagtail.core import blocks

from .html_blocks import (
    ButtonBlock,
    EmbedGoogleMapBlock,
    ImageBlock,
    ImageLinkBlock,
    DownloadBlock,
    EmbedVideoBlock,
    PageListBlock,
    PagePreviewBlock,
    QuoteBlock,
    RichTextBlock,
)
from .content_blocks import (  # noqa
    CardBlock,
    CollectionCardBlock,
    CarouselBlock,
    ContentWallBlock,
    ImageGalleryBlock,
    ModalBlock,
    NavDocumentLinkWithSubLinkBlock,
    NavExternalLinkWithSubLinkBlock,
    NavPageLinkWithSubLinkBlock,
    PriceListBlock,
    ReusableContentBlock
)
from .layout_blocks import (
    CardGridBlock,
    GridBlock,
    HeroBlock
)
from .base_blocks import (  # noqa
    BaseBlock,
    HeadingBlock,
    BaseLayoutBlock,
    BaseLinkBlock,
    ClassifierTermChooserBlock,
    CoderedAdvColumnSettings,
    CoderedAdvSettings,
    CoderedAdvTrackingSettings,
    CollectionChooserBlock,
    MultiSelectBlock,
    BlockQuote,
    EmbedBlock
)

DEFAULT_BLOCKS = [
    ("heading_block", HeadingBlock()),
    ("paragraph_block", RichTextBlock(
            icon="fa-paragraph",
            template="blocks/paragraph_block.html"
        )),
    ("block_quote", BlockQuote()),
]

# Collections of blocks commonly used together.

HTML_STREAMBLOCKS = [
    ('text', RichTextBlock(icon='fa-file-text-o')),
    ('button', ButtonBlock()),
    ('image', ImageBlock()),
    ('image_link', ImageLinkBlock()),
    ("block_quote", BlockQuote()),
    ('html', blocks.RawHTMLBlock(icon='code', classname='monospace', label=_('HTML'), )),
    ('download', DownloadBlock()),
    ('embed_video', EmbedVideoBlock()),
    ('quote', QuoteBlock()),
    ('google_map', EmbedGoogleMapBlock()),
    ('page_list', PageListBlock()),
    ('page_preview', PagePreviewBlock()),
    ("embed_block", EmbedBlock(
        help_text='Insert an embed URL e.g https://www.youtube.com/embed/SGJFWirQ3ks',
        icon="fa-s15",
        template="blocks/embed_block.html")),
]

CONTENT_STREAMBLOCKS = HTML_STREAMBLOCKS + [
    ('card', CardBlock()),
    ('collection_card', CollectionCardBlock()),
    ('carousel', CarouselBlock()),
    ('image_gallery', ImageGalleryBlock()),
    ('modal', ModalBlock(HTML_STREAMBLOCKS)),
    ('pricelist', PriceListBlock()),
    ('reusable_content', ReusableContentBlock()),
]

NAVIGATION_STREAMBLOCKS = [
    ('page_link', NavPageLinkWithSubLinkBlock()),
    ('external_link', NavExternalLinkWithSubLinkBlock()),
    ('document_link', NavDocumentLinkWithSubLinkBlock()),
]

BASIC_LAYOUT_STREAMBLOCKS = [
    ('row', GridBlock(CONTENT_STREAMBLOCKS)),
    ('html', blocks.RawHTMLBlock(icon='code', classname='monospace', label=_('HTML'))),
]

LAYOUT_STREAMBLOCKS = [
    ('hero', HeroBlock([
        ('row', GridBlock(CONTENT_STREAMBLOCKS)),
        ('cardgrid', CardGridBlock([
            ('card', CardBlock()),
        ])),
        ('html', blocks.RawHTMLBlock(icon='code', classname='monospace', label=_('HTML'))),
    ])),
    ('row', GridBlock(CONTENT_STREAMBLOCKS)),
    ('cardgrid', CardGridBlock([
        ('card', CardBlock()),
        ('collection', CollectionCardBlock())
    ])),
    ('html', blocks.RawHTMLBlock(icon='code', classname='monospace', label=_('HTML'))),
]

DEFAULT_BLOCKS = CONTENT_STREAMBLOCKS + LAYOUT_STREAMBLOCKS + BASIC_LAYOUT_STREAMBLOCKS
