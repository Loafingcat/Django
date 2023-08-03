from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin
from .models import Post, Category, Tag, Comment

admin.site.register(Post, MarkdownxModelAdmin)
admin.site.register(Comment)


# CategoryAdmin 클래스를 생성하고, prepopulated_fields를 사용하여 slug 필드를 name 필드의 값으로 미리 채워지도록 설정
# 이렇게 함으로써 카테고리 생성 시 슬러그(slug) 필드가 자동으로 생성됨
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}


# 마찬가지로 TagAdmin 클래스 생성하고 prepopulated_fields를 사용하여 slug 필드를 name 필드의 값으로 미리 채워지도록 설정
class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}
# prepopulated_fields는 장고 관리자 패널에서 모델의 필드 값을 자동으로 생성하거나 채우는데 사용하는 기능임


admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)

