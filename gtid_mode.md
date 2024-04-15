
## 정의
gtid_mode는 바이너리 로그에 트랜잭션들이 GTID 기반으로 로깅될 수 있는지 여부와 트랜잭션 유형별로, MySQL 서버에서의 처리 가능 여부를 제어한다.

트랜잭션 유형에는 다음 두 가지가 있다.
- 익명 트랜잭션: GTID가 부여되지 않은 트랜잭션, 바이너리 로그 파일명과 위치로 식별
- GTID 트랜잭션: GTID가 부여된 트랜잭션

![[Pasted image 20240409140815.png]]
![[Pasted image 20240409140833.png]]