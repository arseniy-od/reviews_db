from django.utils.text import slugify

from transliterate.exceptions import LanguageDetectionError
from transliterate import translit


class SlugifyMixin:
    slug = None

    def save(self, *args, **kwargs):
        if not self.slug:
            try:
                self.slug = slugify(translit(self.name, reversed=True))
            except LanguageDetectionError:
                self.slug = slugify(self.name)
        super().save(*args, **kwargs)
