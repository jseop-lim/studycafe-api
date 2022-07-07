# Studycafe API



## 개요

Django REST framework를 이용하여 스터디카페 시스템의 API를 제작했다.

스터디카페 시스템 분석 및 데이터베이스 설계는 이미 완성된 상태이다. 자세한 과정은 [velog](https://velog.io/@azzurri21/series/MySQL)에 정리되어 있다.



## 프로젝트 목적

- **RESTful**에 대한 이해 - 데이터베이스를 RESTful하게 나타내는 URI 결정하기
- **MVT 패턴**에 대한 이해 - 주어진 데이터베이스를 사용자 요구에 맞게 조회하기 위한 View(Control)을 정의하기
- Django 및 DRF 연습



## App 구조

- `rental`: 자리 대여
  - Model) 학생, 자리, 이용권, 대여, 구매
  
- `common`: 계정 관련
  - Model) User
    <!--- `board`: 피드백 게시판-->
  
  

## 실행 환경

- python 3.9.7
- django 4.0.2
- django REST framework 3.13.1
- mysqlclient 2.1.0
- celery 5.2.3
- gevent 21.12.0
- (Ubuntu) rabbitmq-server



## 사용법

[docs/README.md](https://github.com/jseop-lim/studycafe-api/tree/main/docs)에 API endpoint가 나열되어 있다.

스터디카페 사용자의 프로세스는 [velog](https://velog.io/@azzurri21/MySQL-%EC%8A%A4%ED%84%B0%EB%94%94%EC%B9%B4%ED%8E%98-%EA%B4%80%EB%A6%AC%EC%8B%9C%EC%8A%A4%ED%85%9C-%EA%B0%9C%EB%B0%9C-2-%EC%8B%9C%EC%8A%A4%ED%85%9C-%EB%B6%84%EC%84%9D#process)에 정리되어 있다.

celery + rabbitMQ 환경 구축 및 실행은 [notion](https://jseoplim.notion.site/Celery-with-Django-122c3bcd38ef4b40940569da5ed24b98)을 참고하라.



## 개발 과정

API의 기능마다 branch를 새로 생성해 만들고 [Pull requests](https://github.com/jseop-lim/studycafe-api/pulls)에 세부 내용을 기록했다. 괄호 안은 기능이 포함된 app 이름이다.

* [registration](https://github.com/jseop-lim/studycafe-api/pull/8)(`common`): 회원가입, 로그인, 비밀번호 변경 등 계정 관련 기능, 학생 정보 저장을 위한 User 모델 확장
* [purchase](https://github.com/jseop-lim/studycafe-api/pull/19)(`rental`): 이용권 모델과 구매 관련 기능
* [rental](https://github.com/jseop-lim/studycafe-api/pull/25)(`rental`): 자리 모델과 대여 관련 기능

기타 구체적인 문제 해결 과정은 각각을 [Issues](https://github.com/jseop-lim/studycafe-api/issues?q=is%3Aissue)로 작성했다.

