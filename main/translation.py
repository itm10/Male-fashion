from modeltranslation.translator import translator, TranslationOptions
from .models import Product


class ProductTranslation(TranslationOptions):
    fields = ('product_name', 'description', 'brand', 'created_at')


translator.register(Product, ProductTranslation)
