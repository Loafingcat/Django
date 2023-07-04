from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post, Category


class PostList(ListView):  # ListView 클래스를 상속해서 만든다.
    model = Post  # model은 Post다 라고 선언해주면 아까 index 함수와 같은 기능을 하게 된다.
    ordering = '-pk'  # index에서 order by의 역할

    def get_context_data(self, **kwargs):
        context = super(PostList, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()

        return context


class PostDetail(DetailView):  # DetailView는 단일 인스턴스를 보여주는 기능
    model = Post  # PostDetail은 Post 모델의 단일 포스트를 보여주는 역할
    # PostDetail 클래스는 DetailView 기능을 활용해서 Post 모델의 특정 포스트를
    # 가져와서 해당 포스트의 상세 내용을 보여주는 역할
    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()

        return context


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
        category = '미분류'  # 만약 no_category인 경우 미분류로 설정하고 카테고리가 없는 포스트를 필터링해서 post_list에
                            # 할당한다
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
