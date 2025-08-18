from django.db import models


class ContactInfo(models.Model):
    """Модель для хранения контактной информации."""
    email = models.EmailField(verbose_name='email', help_text='Email address')
    country = models.CharField(max_length=100, verbose_name='country', help_text='Country name')
    city = models.CharField(max_length=100, verbose_name='city', help_text='City name')
    street = models.CharField(max_length=100, verbose_name='street', help_text='Street')
    house_number = models.CharField(max_length=50, verbose_name='house_number', help_text='House number')

    class Meta:
        verbose_name = "контактная информация"
        verbose_name_plural = "контактные информации"

    def __str__(self):
        return f'{self.email} - {self.country}, {self.city}, {self.street}, {self.house_number}'


class Product(models.Model):
    """Модель для хранения продуктов."""
    title = models.CharField(max_length=100, verbose_name='name', help_text='Product name')
    model = models.CharField(max_length=100, verbose_name='model', help_text='Product model')
    launched_at = models.DateField(auto_now_add=False, verbose_name='launched product date',)

    class Meta:
        verbose_name = "продукт"
        verbose_name_plural = "продукты"

    def __str__(self):
        return f'{self.title} - {self.model}'


class Vendor(models.Model):
    """Модель для хранения поставщиков."""
    LEVELS = [
        (0, "Завод"),
        (1, "Розничная сеть"),
        (2, "Индивидуальный предприниматель"),
    ]
    title = models.CharField(max_length=150, verbose_name='vendor title', help_text='Vendor name')
    level = models.IntegerField(choices=LEVELS, verbose_name='vendor level', help_text='Vendor level')
    contact = models.ForeignKey(ContactInfo, verbose_name='contacts', on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, verbose_name='products', related_name='products')
    supplier = models.ForeignKey('self', verbose_name='supplier', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='created at',)
    debt_to_supplier = models.DecimalField(decimal_places=2, max_digits=15, default=0, verbose_name='debt to supplier')

    class Meta:
        verbose_name = "поставщик"
        verbose_name_plural = "поставщики"

    def __str__(self):
        return f'{self.title} - {self.level} - {self.debt_to_supplier}'
