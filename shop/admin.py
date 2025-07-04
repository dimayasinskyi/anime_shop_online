from django.contrib import admin
from image_cropping import ImageCroppingMixin

from .models import Good, Category
from user.models import Comment

admin.site.site_header = 'Admin'
admin.site.site_title = 'User'
admin.site.index_title = 'Admin'


class GoodInline(admin.TabularInline):
    model = Good
    extra = 0

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'good_count']
    inlines = [GoodInline]

    def good_count(self, obj):
        return Good.objects.filter(category=obj).count()
    good_count.short_description = 'Good'



class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1

@admin.register(Good)
class GoodAdmin(ImageCroppingMixin, admin.ModelAdmin):
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