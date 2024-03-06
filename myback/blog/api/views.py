from wagtail.api.v2.views import PagesAPIViewSet
from wagtail.images.api.v2.views import ImagesAPIViewSet
from rest_framework.renderers import JSONRenderer

from blog.models import BlogPage, BlogPageIndexTag

class BlogPostAPIViewSet(PagesAPIViewSet):
    renderer_classes = [JSONRenderer]
    model = BlogPage
    name = "posts"

    def get_queryset(self):
        return self.model.objects.live().order_by('-first_published_at')

class TagPostAPIViewSet(PagesAPIViewSet):
    renderer_classes = [JSONRenderer]
    model = BlogPageIndexTag
    name = "tags"

class PostImagesAPIViewSet(ImagesAPIViewSet):
    renderer_classes = [JSONRenderer]
    name = "images"