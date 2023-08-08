# 애플리케이션의 설정을 정의하는 파일. 애플리케이션은 프로젝트의 기능을 모듈화하고 관리하기 위해 사용된다.
# 이 파일을 통해서 애플리케이션의 이름, 레이블, 설정 등을 관리할 수 있음

# 장고의 애플리케이션 설정을 위해 AppConfig 클래스를 가져옴
from django.apps import AppConfig


class BlogConfig(AppConfig):  # BlogConfig 클래스를 정의해서 애플리케이션의 설정을 설정, BlogConfig는 AppConfig를 상속받음
    default_auto_field = 'django.db.models.BigAutoField'  # 데이터베이스 테이블의 기본 자동 생성 필드를 BigAutoField로 설정
    name = 'blog'  # 애플리케이션 이름을 blog로 설정, 식별자 역할을 하고 참조하는 데 사용 됨
