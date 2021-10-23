# crud_board_project
### 구현한 방법과 간단한 내용
python & django을 사용하여 기초적인 crud 게시판을 구현하였습니다. 

## 실행 환경
- Mac OS
- Conda 4.9.2
- Django 3.2.6
- SQLite3
- django-cors-headers-3.10.0

## Datebase Modeling
![스크린샷 2021-10-22 오후 11 02 34](https://user-images.githubusercontent.com/40171383/138491083-c2a780bf-74f3-47fc-a6f0-dc2430d5b6b4.png)

## 사용된 스택
- Python,
- Django,
- SQLite3
- unittest
- etc : Postman

## 구현 사항
- 회원 가입
    - email validation
    - bcrypt 사용한 암호화
    - jwt 토큰 발행
- 로그인
    - bcrypt 사용한 암호화, 저장 시에는 decode
- 구현 기능 전체 unittest 진행

## Endpoint 호출 방법
### users
1. 회원가입 API
    - POST : users/signup HTTP/1.1
    - Host : http://127.0.0.1:8000/
    - post 메서드를 사용, Body에 정보를 JSON에 담아 전달.
```python
Request
{
    "email"    : "modmodmod@gmail.com",
    "password" : "1234",
    "name"     : "하석진"
}
```
```python
Response
{
    "message": "SUCCUSS"
}
```
2. 로그인 API
    - POST : users/signin HTTP/1.1
    - Host : http://127.0.0.1:8000/
    - post 메서드를 사용, Body에 정보를 JSON에 담아 전달.
    - 기존 가입된 id와 password가 일치하면 향후 게시판 글쓰기 인가용 token 발행.
```python
Request
{
    "email"   : "testing2@gmail.com",
    "password" : "1234"
}
```
```python
Response
{
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6OH0.I7M5CBPlxVn9g83S-P23PNh5_0gZAub0d6n1RHy_8To",
    "message": "SUCCESS"
}
```
3. 데코레이터 API (단순 확인용)
    - POST : users/decorator-test HTTP/1.1
    - Host : http://127.0.0.1:8000/
    - request.headers의 담에 'Authorization'이라는 key의 value 값을 확인하여 인가절차 수행.
    - 인가 절차가 완료되면 해당 토큰의 user_name을 Resonse
```python
Request
{
    "Authorization" : "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6Mn0.K3LT0TtAMaJLcY5jxz_5dwLh5ENBojWSCHkA49e_kgE"
}
```
```python
Response
{
    "user_name": "이광수"
}
```
### boards
1. board posting API
    - POST : users/boards/post HTTP/1.1
    - Host : http://127.0.0.1:8000/
    - title, content, tag 등을 json에 담아 전달.
```python
Request
{
    "content": "testtsetst",
    "tag": "1",
    "title": "testing_2"
}
```
```python
Response
{
    "message": "SUCCESS"
}
```
### api 명세(request/response 서술 필요)
