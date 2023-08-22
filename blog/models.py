# 파일 이름 그대로 데이터베이스 모델을 정의한다. 데이터베이스 모델은 데이터를 구조화하고 저장하기 위한 클래스로
# 객체 지향적인 방식으로 데이터베이스 테이블을 정의함. 이 파일을 통해 데이터 구조와 속성을 정의할 수 있고
# 데이터베이스 테이블의 상호작용을 처리할 수 있음.

from django.db import models
from django.contrib.auth.models import User
from markdownx.models import MarkdownxField
from markdownx.utils import markdown
import os


class Tag(models.Model):  # 모델 블로그 글에 대한 태그
    name = models.CharField(max_length=50, unique=True)  # 태그 이름을 나타내는 문자열 필드
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)  # URL 슬러그를 나태내는 필드, 태그 기반으로 자동생성

    def __str__(self):  # 객체를 문자열로 표현할 떄 사용되는 메서드
        return self.name

    def get_absolute_url(self):  # 객체의 절대 URL을 반환하는 메서드
        return f'/blog/tag/{self.slug}/'


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/blog/category/{self.slug}/'

    class Meta:  # 모델의 메타 정보를 설정하는 클래스
        verbose_name_plural = 'Categories'


class Post(models.Model):
    title = models.CharField(max_length=30)
    hook_text = models.CharField(max_length=100, blank=True)  # 공백도 ㄱㅊ
    content = MarkdownxField()

    head_image = models.ImageField(upload_to='blog/images/%Y/%m/%d/', blank=True)
    file_upload = models.FileField(upload_to='blog/files/%Y/%m/%d/', blank=True)
    created_at = models.DateTimeField(auto_now=True)  # 저장 될 때 시간 자동 업데이트
    updated_at = models.DateTimeField(auto_now=True)
    # author: 추후 작성 예정
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)  # null값 ㄱㅊ, 삭제되는 객체를 NULL 값으로 설정

    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)

    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        # [1]첫 번째 글 :: 준호 뭐 이런식으로 보여지게 된다
        return f'[{self.pk}]{self.title} :: {self.author}'

    def get_absolute_url(self):
        return f'/blog/{self.pk}/'

    def get_file_name(self):
        return os.path.basename(self.file_upload.name)

    def get_file_ext(self):
        return self.get_file_name().split('.')[-1]

    def get_content_markdown(self):
        return markdown(self.content)


    def get_avatar_url(self):
        if self.author.socialaccount_set.exists():
            return self.author.socialaccount_set.first().get_avatar_url()
        else:
            return f'https://doitdjango.com/avatar/id/1618/e06fe162ad3cac7f/svg/{self.author.email}'


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)  # 블로그 글이 삭제되면 그 글에 달린 모든 댓글도 삭제됨
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # 이것도 마찬가지
    content = models.TextField()
    created_at = models.DateTimeField(auto_now=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.author}::{self.content}'

    def get_avatar_url(self):
        if self.author.socialaccount_set.exists():
            return self.author.socialaccount_set.first().get_avatar_url()
        else:
            return f'https://doitdjango.com/avatar/id/1618/e06fe162ad3cac7f/svg/{self.author.email}'

    def get_absolute_url(self):
        return f'{self.post.get_absolute_url()}#comment-{self.pk}'
    # Comment 객체의 get_absolute_url 메서드를 호출하면 글의 상세페이지로 이동하는 URL이 생성됨
    # Comment 객체의 pk가 42이고 해당 댓글이 속한 글의 get_absolute_url이 /blog/1/ 반환하면
    # get_absolute_url 호출 결과는 /blog/1/#comment-42 가 된다는 소리

