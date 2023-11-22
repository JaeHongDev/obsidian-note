MySQL 5.7 버전까지 기본으로 사용되던 방식
- 비밀번호에 대한 해시 (SHA-1 알고리즘) 값을 저장, 클라이언트가 보낸 값과 저장된 해시값을 비교

https://dev.mysql.com/doc/refman/8.0/en/native-pluggable-authentication.html