from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404
from .models import Post, Category, Tag, Comment
from .forms import CommentForm
from django.core.exceptions import PermissionDenied
from django.utils.text import slugify
from django.db.models import Q


class PostList(ListView):  # ListView 클래스를 상속해서 만든다.
    model = Post  # model은 Post다 라고 선언해주면 아까 index 함수와 같은 기능을 하게 된다.
    ordering = '-pk'  # index에서 order by의 역할
    paginate_by = 5  # 페이지 당 글 개수 제한

    def get_context_data(self, **kwargs):
        context = super(PostList, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()

        return context


class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['title', 'hook_text', 'content', 'head_image', 'file_upload', 'category', 'tags']

    template_name = 'blog/post_update_form.html'

    def get_context_data(self, **kwargs):
        context = super(PostUpdate, self).get_context_data()
        if self.object.tags.exists():
            tags_str_list = list()
            for t in self.object.tags.all():
                tags_str_list.append(t.name)
            context['tags_str_default'] = '; '.join(tags_str_list)

        return context

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(PostUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def form_valid(self, form):
        response = super(PostUpdate, self).form_valid(form)
        self.object.tags.clear()

        tags_str = self.request.POST.get('tags_str')
        if tags_str:
            tags_str = tags_str.strip()
            tags_str = tags_str.replace(',', ';')
            tags_list = tags_str.split(';')

            for t in tags_list:
                t = t.strip()
                tag, is_tag_created = Tag.objects.get_or_create(name=t)
                if is_tag_created:
                    tag.slug = slugify(t, allow_unicode=True)
                    tag.save()
                self.object.tags.add(tag)

        return response


class PostDetail(DetailView):  # DetailView는 단일 인스턴스를 보여주는 기능
    model = Post  # PostDetail은 Post 모델의 단일 포스트를 보여주는 역할
    # PostDetail 클래스는 DetailView 기능을 활용해서 Post 모델의 특정 포스트를
    # 가져와서 해당 포스트의 상세 내용을 보여주는 역할

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        context['comment_form'] = CommentForm

        return context


class PostCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Post
    fields = ['title', 'hook_text', 'content', 'head_image', 'file_upload', 'category']

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated and (current_user.is_staff or current_user.is_superuser):
            form.instance.author = current_user
            response = super(PostCreate, self).form_valid(form)

            tags_str = self.request.POST.get('tags_str')
            if tags_str:
                tags_str = tags_str.strip()

                tags_str = tags_str.replace(',', ';')
                tags_list = tags_str.split(';')

                for t in tags_list:
                    t = t.strip()
                    tag, is_tag_created = Tag.objects.get_or_create(name=t)
                    if is_tag_created:
                        tag.slug = slugify(t, allow_unicode=True)
                        tag.save()
                    self.object.tags.add(tag)

            return response

        else:
            return redirect('/blog/')
# def index(request): # 블로그의 포스트 리스트를 보여주는 역할을 함
#     # 이 함수는 장고의 render()함수를 사용해서 blog/post_list.html 템플릿을
#     # 렌더링 해서 엔드 유저에게 반환한다.
#     posts = Post.objects.all().order_by('-pk')
#     # Post 모델의 모든 객체를 가져오고 최신순으로 정렬하기 위해 이걸 사용해서 posts 변수에 저장
#
#     return render( # 그리고 render 함수를 호출해서 템플릿 렌더링
#         request, # 얘는 사용자의 요청 객체다. 장고가 뷰 함수에 전달하는 매개변수
#         'blog/post_list.html', # 렌더링 할 템플릿 파일의 경로
#         {
#             'posts': posts, # 템플릿에 전달할 컨텍스트 데이터
#             # render 함수는 템플릿을 렌더링한 결과를 HTTP 응답으로 반환한다.
#             # 이 응답은 사용자에게 웹 페이지를 보여주는 역할을 한다.
#             # 장고의 템플릿 언어를 사용하여 동적으로 HTML을 생성할 수 있다.
#         }
#     )


# def single_post_page(request, pk):
#     post = Post.objects.get(pk=pk)
#
#     return render(
#         request,
#         'blog/post_detail.html',
#         {
#             'post': post,
#         }
#     )


def category_page(request, slug):  # 엔드유저의 요청과 함께 slug 매개 변수를 받음
    if slug == 'no_category':  # if를 사용해서 slug 값이 no_category인 경우와 그렇지 않은 경우를 구분
        category = '미분류'  # 만약 no_category인 경우 미분류로 설정하고 카테고리가 없는 포스트를 필터링해서 post_list에 할당한다
        post_list = Post.objects.filter(category=None)
    else:
        category = Category.objects.get(slug=slug)  # 그렇지 않은 경우는 얘를 사용해서 slug 값에 해당하는
        # 카테고리를 가져와서 카테고리 변수에 할당한다
        post_list = Post.objects.filter(category=category)
        # 그리고 이걸 이용해서 해당 카테고리에 속하는 포스트들을 필터링해서 post_list에 할당한다.
    return render(
        request,
        'blog/post_list.html',  # post_list.html 템플릿을 렌더링. 이때 아래의 컨텍스트 데이터를 전달함.
        {
            'post_list': post_list,  # 필터링된 포스트 리스트를 post_list키로 전달
            'categories': Category.objects.all(),  # 모든 카테고리를 categories로 전달
            'no_category_post_count': Post.objects.filter(category=None).count(),
            # 카테고리가 없는 포스트의 개수를 no_category_post_count로 전달.
            'category': category,  # 선택된 카테고리를 category 키로 전달
        }
    )


def tag_page(request, slug):
    tag = Tag.objects.get(slug=slug)
    post_list = tag.post_set.all()

    return render(
        request,
        'blog/post_list.html',
        {
            'post_list': post_list,
            'tag': tag,
            'categories': Category.objects.all(),
            'no_category_post_count': Post.objects.filter(category=None).count(),
        }
    )


def new_comment(request, pk):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, pk=pk)

        if request.method == 'POST':
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.post = post
                comment.author = request.user
                comment.save()
                return redirect(comment.get_absolute_url())
            else:
                return redirect(post.get_absolute_url())
        else:
            raise PermissionDenied


class CommentUpdate(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(CommentUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied


def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post = comment.post
    if request.user.is_authenticated and request.user == comment.author:
        comment.delete()
        return redirect(post.get_absolute_url())
    else:
        raise PermissionDenied


class PostSearch(PostList):
    paginate_by = None

    def get_queryset(self):
        q = self.kwargs['q']
        post_list = Post.objects.filter(
            Q(title__contains=q) | Q(tags__name__contains=q)
        ).distinct()
        return post_list

    def get_context_data(self, **kwargs):
        context = super(PostSearch, self).get_context_data()
        q = self.kwargs['q']
        context['search_info'] = f'Search: {q} ({self.get_queryset().count()})'

        return context




