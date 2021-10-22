# crud_board_project
### 구현한 방법과 간단한 내용
python & django을 사용하여 기초적인 crud 게시판을 구현하였습니다. 

### 실행 환경
- Mac OS
- Conda 4.9.2
- Django 3.2.6
- SQLite3
- django-cors-headers-3.10.0

### Datebase Modeling
![스크린샷 2021-10-22 오후 11 02 34](https://user-images.githubusercontent.com/40171383/138491083-c2a780bf-74f3-47fc-a6f0-dc2430d5b6b4.png)

### 사용된 스택
- Python,
- Django,
- SQLite3
- unittest
- etc : Postman

### 구현 사항
- 회원 가입
    - email validation
    - bcrypt 사용한 암호화
    - jwt 토큰 발행
- 로그인
    - bcrypt 사용한 암호화, 저장 시에는 decode
- 구현 기능 전체 unittest 진행

### Endpoint 호출 방법
1. 회원가입 API 호출
- post 메서드를 사용, Body에 정보를 JSON에 담아 전달. 
```python
{
    "email"    : "modmodmod@gmail.com",
    "password" : "1234",
    "name"     : "하석진"
}
=> {
    "message": "SUCCUSS"
}
```

### api 명세(request/response 서술 필요)
- api 명세서 첨부
