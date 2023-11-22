- 서버 측에서는 인메모리 캐시를 통해 이전에 연결한 사용자가 다시 연결할 때 더 빠르게 재인증할 수 있습니다.
- RSA 기반의 비밀번호 교환은 MySQL이 연결되어 있는 SSL 라이브러리에 상관없이 가능합니다.
- Unix 소켓 파일 및 공유 메모리 프로토콜을 사용하는 클라이언트 연결에 대한 지원이 제공됩니다


https://dev.mysql.com/doc/refman/8.0/en/caching-sha2-pluggable-authentication.html



MySQL 서버의 Caching SHA-2 Authentication은 SCRAM 인증 방식을 사용합니다.
- SCRAM 인증 방식은 평문 비밀번호를 이용해서 5000번 이상 암호화 해시 함수를 실행해야 MySQL 서버로 로그인 요청을 보낼 수 있기 때문에 무작위로 비밀번호를 입력하는 무차별 대임 공격을 어렵게 만듭니다.
- <u>단 이런 인증 방식은 일반 유저, 애플리케이션의 연결도 느리게 만듭니다.</u>
- 그리고 여전히 서버의 CPU자원을 많이 소모하게 된다.