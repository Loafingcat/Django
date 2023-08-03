from .models import Comment
from django import forms


class CommentForm(forms.ModelForm):  # CommentForm 클래스 정의.
    # 이 클래스는 forms.ModelForm 클래스를 상속받아서 댓글 모델을 기반으로한 폼을 생성함
    class Meta:  # Meta 클래스 내부에는 폼의 메타 정보를 정의함
        model = Comment  # 폼이 사용할 모델을 Comment로 설정함 폼이 Comment 모델과 관련된 데이터를 다룰 수 있게 됨
        fields = ('content',)  # 폼에서 사용할 필드를 지정함 content 필드만 폼에서 사용 가능, content 필드는 댓글 내용을 나타냄
