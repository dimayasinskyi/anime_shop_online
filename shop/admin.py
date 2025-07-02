from django.contrib import admin
from image_cropping import ImageCroppingMixin

from .models import Goods, Categories
from user.models import Comment

admin.site.site_header = 'Admin'
admin.site.site_title = 'User'
admin.site.index_title = 'Admin'


class GoodsInline(admin.TabularInline):
    model = Goods
    extra = 0

@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ['title', 'goods_count']
    inlines = [GoodsInline]

    def goods_count(self, obj):
        return Goods.objects.filter(category=obj).count()
    goods_count.short_description = 'Goods'



class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1

@admin.register(Goods)
class GoodsAdmin(ImageCroppingMixin, admin.ModelAdmin):
    list_display = ('title', 'comment_count','price')
    fieldsets = [
        (None, {'fields':['id', 'title', 'image', 'cropping']}),
        (None, {'fields':['description', 'com_qty', 'sel_qty', 'category']}),
        (None, {'fields':['price']})
        ]
    readonly_fields = ['id']
    search_fields = ['title']
    inlines = [CommentInline]

    def comment_count(self, obj):
        return Comment.objects.filter(good=obj).count()
    comment_count.short_description = 'Comments'