# 웹 폼을 정의하고 처리하는 데 사용되는 파일이다. 웹 폼은 사용자로부터 입력을 받아서 서버로 전송하거나
# 데이터를 수정하는데 사용됨. 양식을 생성하고 유효성 검사를 수행해서 데이터를 처리할 수 있다.

from .models import Comment
from django import forms


class CommentForm(forms.ModelForm):  # CommentForm 클래스 정의.
    # 이 클래스는 forms.ModelForm 클래스를 상속받아서 댓글 모델을 기반으로한 폼을 생성함
    class Meta:  # Meta 클래스 내부에는 폼의 메타 정보를 정의함
        model = Comment  # 폼이 사용할 모델을 Comment로 설정함 폼이 Comment 모델과 관련된 데이터를 다룰 수 있게 됨
        fields = ('content',)  # 폼에서 사용할 필드를 지정함 content 필드만 폼에서 사용 가능, content 필드는 댓글 내용을 나타냄
