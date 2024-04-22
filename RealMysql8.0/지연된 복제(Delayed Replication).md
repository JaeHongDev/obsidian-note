

## 목적
복제의 목적은 소스 서버와 레플리카 서버를 빠르게 동기화해서 동일한 상태로 만드는 것
하지만 개발자 혹은 DBA가 소스 서버에서 실수로 중요한 테이블, 데이터를 삭제 했을 때 레플리카 서버까지 동기화가 되는 것을 막기 위해 지연된 복제기능이 등장했습니다.

> [!NOTE] 참고
> MySQL 5.6 버전에 처음 도입
> MySQL 8.0 버전에서 기능 개선이 이루어짐



## 개선점

- `CHANGE REPLICATION SOURCE TO` 구문에 `SOURCE_DELAY` 혹은 `MASTER_DELAY` 옵션을 사용
	- 해당 옵션을 통해서 얼마나 지연시킬 것인지 지정
![[Pasted image 20240422175518.png]]
> 하루 정도 지연시켜서 저장

- 바이너리 로그에 
	- [[OCT(original_commit_timestamp)]]
	- [[ICT(immediate_commit_timestamp)]] 
	타임스탬프 추가
	- [[ICT 타임스탬프 값을 사용했을 때 장점]]