from django.core.exceptions import ValidationError
from django.db import models
from django.core.validators import MinLengthValidator


class Menu(models.Model):
    """Модель меню"""

    title = models.CharField(
        max_length=50,
        verbose_name="Название меню",
        validators=[MinLengthValidator(3)],
    )
    slug = models.SlugField(
        max_length=60,
        verbose_name="Слаг меню",
        validators=[MinLengthValidator(3)],
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Меню"
        verbose_name_plural = "Меню"


class MenuItem(models.Model):
    """Модель пункта древовидного меню"""

    title = models.CharField(
        max_length=80,
        verbose_name="Название пункта",
    )
    url = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name="Ссылка",
    )
    menu = models.ForeignKey(
        Menu,
        on_delete=models.CASCADE,
        verbose_name="Меню",
        related_name="menu_items",
    )
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        verbose_name="Пункт родитель",
        null=True,
        blank=True,
        related_name="children",
    )

    def __str__(self):
        return self.title

    def clean(self):
        if self.menu and self.parent:
            parent_menu = self.parent.menu
            if parent_menu != self.menu:
                raise ValidationError(
                    "Пункт меню должен ссылаться на тоже меню, что и родитель."
                )
            if self.parent.pk == self.pk:
                raise ValidationError("Пункт меню не может быть родителем самого себя.")

    class Meta:
        verbose_name = "Пункт меню"
        verbose_name_plural = "Пункты меню"
