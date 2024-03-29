# Generated by Django 5.0.2 on 2024-03-24 23:35

import blog.custom
from django.db import migrations
import wagtail.blocks
import wagtail.embeds.blocks
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpage',
            name='body',
            field=wagtail.fields.StreamField([('heading', wagtail.blocks.CharBlock(form_classname='title')), ('subtitle', wagtail.blocks.CharBlock(form_classname='subtitle', required=False)), ('paragraph', wagtail.blocks.RichTextBlock()), ('image', blog.custom.ImageChooserBlock(required=False)), ('quote', wagtail.blocks.BlockQuoteBlock(required=False)), ('video', wagtail.embeds.blocks.EmbedBlock(required=False)), ('code_snippet', wagtail.blocks.TextBlock(form_classname='Code Snippet', required=False))], use_json_field=True),
        ),
    ]