from django.db import models
from django_extensions.db.models import TimeStampedModel
from django.db.utils import IntegrityError
from django.utils.translation import ugettext_lazy as _

from user_app import models as uam

"""
All the models are inherited from TimeStampedModel from django_extensions :
It adds 2 cols : created and modified as timestamps in the models
"""


class Category(TimeStampedModel):
    """
    categories for a product (many to many relationship with the product table)
    nb_prod is to search the substitutes first in categories which have more products
    """
    cname = models.CharField(max_length=150, verbose_name=_("category name"), unique=True)
    nb_prod = models.IntegerField(verbose_name=_("products number"), default=0)

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return self.cname


class Store(TimeStampedModel):
    """
    stores for a product (many to many relationship with the product table)
    """
    sname = models.CharField(max_length=150, verbose_name=_("Store name"), unique=True)

    class Meta:
        verbose_name = _("Store")
        verbose_name_plural = _("Stores")

    def __str__(self):
        return self.sname


class Brand(TimeStampedModel):
    """
    Brand for a product (on brand per product) (one to many - foreignkey - relationship with product)
    """
    bname = models.CharField(max_length=150, verbose_name=_("Brand Product"), unique=True)

    class Meta:
        verbose_name = _("Brand")
        verbose_name_plural = _("Brands")

    def __str__(self):
        return self.bname


class Product(TimeStampedModel):
    """
    Product model
    Name and barcode are unique
    Index on nutriscore_grade --> always used to select the products in the search_bookmarks view wich
        is also ordered by it.
    Choice for Nutrient levels --> used in detail view to have colored icons

    Foreign key with Brand model One product --> One Brand but One Brand for many Products
    "Basic" many to many relationship with Category, Store
    "Trough" many to many relationship with himself for bookmarks : A bookmarked product is a product which
        is bookmarked for a specific user !
    All the many to many relationships have the same related name : product --> easy to use

    2 methods :
    A property which return the nutrient_levels for a product
    A clasmethod which search for a product a return a queryset (1 or more product(s))
    """

    class nutrient_levels(models.TextChoices):
        HIGH = "H", _("High")
        MODERATE = "M", _("Moderate")
        LOW = "L", _("Low")
        UNKNOWN = "U", _("Unknown")

    pname = models.CharField(max_length=150, verbose_name=_("Product name"), unique=True)
    code = models.CharField(max_length=20, verbose_name=_("Barcode"), unique=True)
    product_url = models.URLField(verbose_name=_("OpenFoodFact product URL"))
    nutriscore_score = models.SmallIntegerField(verbose_name=_("Nutriscore score"))
    nutriscore_grade = models.CharField(max_length=1, verbose_name=_("Nutriscore notation"))
    desc = models.TextField(verbose_name=_("Description"))
    photo_url = models.URLField(verbose_name=_("OpenFoodFact photo URL"))
    nb_scans = models.IntegerField(verbose_name=_("Scans number"), default=0)
    salt = models.CharField(max_length=1, verbose_name=_("Salt"), choices=nutrient_levels.choices,
                            default=nutrient_levels.UNKNOWN)
    sugar = models.CharField(max_length=1, verbose_name=_("Sugar"), choices=nutrient_levels.choices,
                             default=nutrient_levels.UNKNOWN)
    fat = models.CharField(max_length=1, verbose_name=_("Fat"), choices=nutrient_levels.choices,
                           default=nutrient_levels.UNKNOWN)
    saturated_fat = models.CharField(max_length=1, verbose_name=_("Saturated fat"), choices=nutrient_levels.choices,
                                     default=nutrient_levels.UNKNOWN)

    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, verbose_name=_("Product brand"), related_name="products",
                              null=True)
    store = models.ManyToManyField(Store, verbose_name=_("Product store"), related_name="products")
    category = models.ManyToManyField(Category, verbose_name=_("Product category"), related_name="products")
    bookmark = models.ManyToManyField('Product', through='Bookmark', blank=True, symmetrical=False, default=None,
                                      related_name='products')

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")
        indexes = [
            models.Index(fields=['nutriscore_grade'], name='I_nutriscore_grade'),
        ]
        ordering = ['nutriscore_grade']

    def __str__(self):
        return self.pname

    @property
    def get_nutrient_levels(self):
        """
            return all the nutrient levels in a dict (for the detail view)
        """
        return {'salt': [self.salt, self.get_salt_display()],
                'sugar': [self.sugar, self.get_sugar_display()],
                'fat': [self.fat, self.get_fat_display()],
                'satured_fat': [self.saturated_fat, self.get_saturated_fat_display()],
                }

    @classmethod
    def search_product(cls, prod_to_search):
        """
            Search for a product in database

            Args : product to search (name)

            search a specific product in 2 times :
            - search the product exactly (name = prod_to_search in arg) and name is unique
            if found --> return a queryset with only one product
            if not -->
            - search products which name match in order by nb_scans (more popular)
            - return the queryset
            if error --> return None and 0
            The 2nd value of the return is treated by the caller
        """
        try:
            prod = Product.objects.filter(pname=prod_to_search)
            if len(prod) == 0:
                prod = Product.objects.filter(pname__icontains=prod_to_search).order_by('nb_scans')
        except:
            return None
        if len(prod) > 0:
            return prod
        else:
            return {}


class ProductsWish(TimeStampedModel):
    """
    Use to store products not found and wanted by users --> fetch from API as the others
    The indb attribute is to know if the product has been fetched or not
    The fetching method is a background method. the unique constraint on the pwname is to
        avoid the user to click several times on the "fetch" button and register the product
        more than 1. The insert catch the error !
    """
    pwname = models.CharField(max_length=150, verbose_name=_("product whished by client"))
    indb = models.BooleanField(default=False, verbose_name=_("product in database"))

    class Meta:
        verbose_name = _("Products Wish")
        verbose_name_plural = _("Products Wishes")
        constraints = [
            models.UniqueConstraint(fields=['pwname'], name='unique_pwname'),
        ]

    def __str__(self):
        return self.pwname


class Bookmark(TimeStampedModel):
    """
    The Bookmark model
    - USed with product model as a many to many trough relationship to have a user in the relationship
    - The constraint is to avoid an error --> same bookmark for the same user (not possible in the GUI)
    - The index on user because the datas are always fetched for a specific user (connected).

    class method to create a bookmark : not to create an instance because not used later !
    """
    buser = models.ForeignKey(uam.User, on_delete=models.CASCADE, related_name='bookmarks',
                              null=True, default=None)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='pbookmarks',
                                null=True, default=None)
    substitute = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='sbookmarks',
                                   null=True, default=None)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['product', 'substitute', 'buser'], name='unique_bookmark')
        ]
        indexes = [
            models.Index(fields=['buser'], name='I_buser'),
        ]

    def __str__(self):
        return f"{self.substitute} se substitue à {self.product} pour {self.buser}"

    @classmethod
    def create_bookmark(cls, user, prod, subst):
        subst = Product.objects.get(code=str(subst))
        user = uam.User.objects.get(username=user)
        prod = Product.objects.get(code=str(prod))
        try:
            new_bookmark = Bookmark(buser=user, product=prod, substitute=subst)
            new_bookmark.save()
        except IntegrityError:
            pass
        return

    @classmethod
    def remove_bookmark(cls, user, prod, subst):
        subst = Product.objects.get(code=str(subst))
        user = uam.User.objects.get(username=user)
        prod = Product.objects.get(code=str(prod))
        try:
            old_bookmark = Bookmark.objects.get(buser=user, product=prod, substitute=subst)
            old_bookmark.delete()
        except IntegrityError:
            pass
        return
