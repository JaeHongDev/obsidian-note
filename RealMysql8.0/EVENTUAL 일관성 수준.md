이름 그대로 최종적으로는 그룹 멤버들이 일관된 데이터를 가지는 것을 의미함

## 특징 
- EVENTAUL 일관성 수준에서는 읽기 전용 및 읽기-쓰기 트랜잭션이 별도의 제약 없이 실행 가능
- 트랜잭션이 직접 실행된 멤버가 아닌 다른 그룹 멤버들에게는 일시적으로 변경 직전 상태의 데이터가 읽혀질 수 있음
- 프라이머리 페일오버가 발생한 경우 새로운 프라이머리가 이전 프라이머리의 트랜잭션을 모두 적용하기 전 새로운 프라이머리에서 트랜잭션이 실행 가능해서 읽기 트랜잭션의 경우 오래된 데이터를 읽을 수 있고 읽기-쓰기 트랝개션의 경우 커밋 시 이전 프라이머리의 트랜잭션과 충돌로 인해 롤백될 수 있음

![[Pasted image 20240430023918.png]]
