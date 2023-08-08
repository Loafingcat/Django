# ASGI서버를 설정하는 파일이다. ASGI는 비동기 웹 서버와 웹 애플리케이션 프레임워크 간의 표준 인터페이스로
# 장고 애플리케이션을 비동기적으로 실행하고 처리할 수 있도록 지원한다. 빠른 요청과 응답 처리, 고성능 및 확장성을 위해 사용이 됨.

"""
ASGI config for do_it_django_prj project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'do_it_django_prj.settings')

application = get_asgi_application()
