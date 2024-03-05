from django import forms
from django.db import models
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

from wagtail.models import Page, Orderable
from wagtail.snippets.models import register_snippet
from wagtail.fields import RichTextField, StreamField
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.search import index

class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'BlogPage',
        related_name='tagged_items',
        on_delete=models.SET_NULL,
        null=True
    )

class BlogIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
    ]

    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super().get_context(request)
        blogpages = self.get_children().live().order_by('-first_published_at')
        context['blogpages'] = blogpages
        return context
    
class BlogPageIndexTag(Page):
    def get_context(self, request):
        tag = request.GET.get('tag')
        blogpages = BlogPage.objects.filter(tags__name=tag)

        context = super().get_context(request)
        context['blogpages'] = blogpages
        return context

class BlogPage(Page):
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
    body = StreamField([
        ('heading', blocks.CharBlock(form_classname="title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock(required=False)),
        ('quote', blocks.BlockQuoteBlock(required=False)),
        ('video', EmbedBlock(required=False)),
        ('code_snippet', blocks.TextBlock(form_classname="Code Snippet", required=False))
    ], use_json_field=True)
    authors = ParentalManyToManyField('blog.Author', blank=True)
    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)

    def main_image(self):
        gallery_item = self.gallery_images.first()
        if gallery_item:
            return gallery_item.image
        else:
            return None
        
    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    caption = models.CharField(blank=True, max_length=250)

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('date'),
            FieldPanel('authors', widget=forms.CheckboxSelectMultiple),
        ], heading="Blog information"),
        FieldPanel('tags'),
        FieldPanel('intro'),
        FieldPanel('body', classname="full"),
        InlinePanel('gallery_images', label="Gallery images")
    ]

class BlogPageGallery(Orderable):
    page = ParentalKey(BlogPage, on_delete=models.SET_NULL, related_name='gallery_images', null=True)
    image = models.ForeignKey('wagtailimages.Image', on_delete=models.SET_NULL, related_name='+', null=True)
    caption = models.CharField(max_length=250, blank=True)

    panels = [
        FieldPanel('image'),
        FieldPanel('caption'),
    ]

@register_snippet
class Author(models.Model):
    name = models.CharField(max_length=255)
    author_image = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True, 
        on_delete=models.SET_NULL, 
        related_name='+'
    )

    panels = [
        FieldPanel('name'),
        FieldPanel('author_image'),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Authors'