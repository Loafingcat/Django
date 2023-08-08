# 관리자 인터페이스를 설정하는 파일. 장고 자체에 내장된 관리자 인터페이스를 제공해서 데이터베이스 모델을
# 쉽게 관리하고 수정할 수 있는 기능을 제공한다. 이 파일을 사용해서 데이터베이스 모델을 관리자 페이지에서
# 편리하게 조작할 수 있는 방법을 지정할 수 있음.

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

