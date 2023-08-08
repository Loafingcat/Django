# WSGI 서버를 설정하는 파일이다. 장고 애플리케이션을 웹 서버와 연결하는 웹 요청을 처리하는 역할을 함.
# 장고를 기본적인 웹 서버와 호환이 되도록 만들어주는 역할을 함.

"""
WSGI config for do_it_django_prj project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'do_it_django_prj.settings')

application = get_wsgi_application()
