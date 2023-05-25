from django.db import models
from django.urls import reverse
from slugify import slugify


# Create your models here.






class SubscriptionPlan(models.Model):
    title = models.CharField(max_length=300)
    duration = models.PositiveIntegerField(help_text='مدت زمان اعتبار')
    price = models.DecimalField(max_digits=20, decimal_places=0, verbose_name='قیمت')
    short_description = models.CharField(verbose_name='توضحیات کوتاه', max_length=300, null=True, blank=True)
    description = models.TextField(verbose_name=' توضیحات اصلی', null=True, blank=True)
    is_active = models.BooleanField(default=False, verbose_name='فعال / غیر فعال')
    is_delete = models.BooleanField(default=False, verbose_name='حذف شده / حذف نشده')
    slug = models.SlugField(default="", null=False, blank=True, db_index=True, max_length=200, unique=True)
    start_date = models.DateField()
    end_date = models.DateField()



    def get_absolute_url(self):
        return reverse('product_detail', args=[self.slug])

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'({self.title} - {self.price})'

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'



