용어 정리
- [[소스 아이디]]
- [[트랜잭션 아이디]]
- [[server_uuid]]
- [[GTID셋]]
## 정의
GTID는 서버에서 커밋된 각 트랜잭션과 연결된 고유한 식별자입니다. 


## 특징
- 물리적인 파일의 이름이나 위치와는 전혀 무관하게 생성
- 트랜잭션이 발생한 서버에서 고유할뿐만 아니라 서버가 속한 토폴로지 내 모든 서버에서 고유함
	- 🤔 이건 어떻게 가능함?
- 소스 아이디와 트랜잭션 아이디 값의 조합으로 생성되며 콜론 문자로 구분되어 표시
	- `GTID=[source_id]:[transaction_id]`




## GTID값 확인하는 방법

1. [[mysql.gtid_executed 테이블]] 조회
![[Pasted image 20240408173246.png]]
2. show global variables
![[Pasted image 20240408173316.png]]
3. show master status
![[Pasted image 20240408173405.png]]

