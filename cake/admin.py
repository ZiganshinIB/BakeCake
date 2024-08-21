from django.contrib import admin

from .models import Client, Cake, CakeLevel, CakeShape, CakeTopping, CakeBerry, Order, CakeDecor


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("name", "phone_number", "email")



@admin.register(Cake)
class CakeAdmin(admin.ModelAdmin):
    list_display = ("title", "level", "shape", "topping", "berry")
    ordering = ["-title"]


@admin.register(CakeLevel)
class CakeLevelAdmin(admin.ModelAdmin):
    list_display = ("level_count", "price")
    ordering = ["level_count"]


@admin.register(CakeShape)
class CakeShapeAdmin(admin.ModelAdmin):
    list_display = ("shape", "price")
    ordering = ["shape"]


@admin.register(CakeTopping)
class CakeToppingAdmin(admin.ModelAdmin):
    list_display = ("cake_topping", "price")
    ordering = ["cake_topping"]


@admin.register(CakeBerry)
class CakeBerryAdmin(admin.ModelAdmin):
    list_display = ("cake_berry", "price")
    ordering = ["cake_berry"]


@admin.register(CakeDecor)
class CakeDecorAdmin(admin.ModelAdmin):
    list_display = ("cake_decor", "price")
    ordering = ["cake_decor"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("customer", "cake", "registered_at")
    ordering = ["-registered_at"]

    @admin.display(description='Delivery Comments')
    def get_deliv_comments(self, obj):
        return obj.cake.deliv_comments

