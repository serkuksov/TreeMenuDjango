from django.contrib import admin

from menu.models import Menu, MenuItem


@admin.register(Menu)
class AdminMenu(admin.ModelAdmin):
    list_display = (
        "title",
        "slug",
    )
    prepopulated_fields = {"slug": ("title",)}


@admin.register(MenuItem)
class AdminMenuItem(admin.ModelAdmin):
    list_display = (
        "menu",
        "title",
        "url",
        "parent",
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """
        Метод ограничивает возможность выбора родителей пункта только теми
        которые связаны с ранее выбранным меню
        """
        if db_field.name == "parent":
            menu = None
            object_id = request.resolver_match.kwargs.get("object_id", None)
            kwargs["queryset"] = MenuItem.objects.exclude(pk=object_id)
            if object_id:
                obj = MenuItem.objects.get(id=object_id)
                menu = obj.menu
            if menu:
                kwargs["queryset"] = kwargs["queryset"].filter(menu=menu)
            # else:
            #     kwargs["queryset"] = MenuItem.objects.all()

        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_readonly_fields(self, request, obj=None):
        """
        Метод запрещает выбирать меню если уже выбран родитель.
        Ограничение введено для того чтобы небыло возможности назначать принадлежность
        к разным меню и родителя и предка
        """
        if obj and obj.parent:
            return ("menu",) + self.readonly_fields
        return self.readonly_fields
