from django.conf.urls import include, url
from django.urls import reverse
from django.utils.html import format_html

from wagtail.admin.rich_text import HalloPlugin
from wagtail.core import hooks
from wagtail.embeds import urls
from wagtail.embeds.rich_text import MediaEmbedHandler


@hooks.register('register_admin_urls')
def register_admin_urls():
    return [
        url(r'^embeds/', include(urls, namespace='wagtailembeds')),
    ]


@hooks.register('insert_editor_js')
def editor_js():
    return format_html(
        """
            <script>
                window.chooserUrls.embedsChooser = '{0}';
            </script>
        """,
        reverse('wagtailembeds:chooser')
    )


@hooks.register('register_rich_text_features')
def register_embed_feature(features):
    features.register_editor_plugin(
        'hallo', 'embed',
        HalloPlugin(
            name='hallowagtailembeds',
            js=['wagtailembeds/js/hallo-plugins/hallo-wagtailembeds.js'],
        )
    )
    features.default_features.append('embed')


@hooks.register('register_rich_text_embed_handler')
def register_media_embed_handler():
    return ('media', MediaEmbedHandler)
