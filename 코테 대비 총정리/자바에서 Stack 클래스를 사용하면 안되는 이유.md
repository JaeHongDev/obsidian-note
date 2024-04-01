

먼저 Stack클래스는 1.2버전에서 등장해 현재 22버전이 나온 시점에서 보면 구현된지 오래된 클래스이다. 
또한 `Vector` 자료형을 기반으로 하는데 `Vector`는 모든 작업에 잠금이 수행된다. 
만약 64코어 CPU를 사용한다고 했을 때 64개의 코어를 사용하는 것이 1개 씩 사용한다. 
![[Pasted image 20240330170243.png]]

특히 현재는 멀티코어가 당여하기 때문에 실 서비스에 사용하면 성능 문제를 만날 수 밖에 없다.

추가로 자바의 하위 호화성을 지키는 특징 떄문에 스택을 개선하지 않고 그대로 두고 있다. 


## 개선하기
그래서 Stack클래스를 대신해서 ArrayDeque를 사용하면 된다. 단 ArrayDeque는 Thread-safe하지 않기 때문에 주의해야 한다. 물론 Thread-safe한 환경이 필요하다면 `LinkedBLockingDeque` 혹은 `ConcurrentLinkedDeque`를 사용하면 된다.