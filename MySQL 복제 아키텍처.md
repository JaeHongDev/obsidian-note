
MySQL 복제 아키텍처에서 사용하는 용어는 다음과 같습니다.
- [[바이너리 로그]]
- [[이벤트]]
- [[릴레이 로그]]
- [[커넥션 메타 데이터]]
- [[어플라이어 메타 데이터]]
- [[바이너리 로그 덤프 스레드]]
- [[레플리케이션 IO 스레드]]
- [[레플리케이션 SQL 스레드]]


MySQL 복제 동기화 과정은 다음과 같습니다. 
![[Pasted image 20240407180443.png |600]]

1. 애플리케이션으로 부터 DML 요청 발생
2. 변경 사항을 바이너리 로그에 기록
3. 생성된 바이너리 로그를 레플리카 서버로 전송
4. 해당 내용을 로컬 데이터에 저장
5. 저장된 데이터를 데이터 파일에 반영하는 동기화 과정이 수행


🤔 만약 소스서버에서 사용자 계정을 등록하고 레플리카 서버에서 회원정보 조회를 할 떄 시간이 안맞으면 로그인이 안될 수 있네?
https://da-nyee.github.io/posts/db-replication-data-consistency-issue/


🤔 바이너리 로그의 잠금이 결정되는 시점은 언제인가요?
- 그림으로 봤을 때 트랜잭션 처리 스레드가 완료될 때 동작하는 것 같은데 맞는지 모르겠네용
-  The source creates a thread to send the binary log contents to a replica when the replica connects
- 소스는 복제본이 연결될 때 바이너리 로그 내용을 복제본으로 보내는 스레드를 생성합니다.
🤔 Replication I/O receiver thread  vs Replication I/O thread 두용어의 차이점
- 공식문서에서는 receiver thread라고 별도로 존재하네용?
- 같은 말임





