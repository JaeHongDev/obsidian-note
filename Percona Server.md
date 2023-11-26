---
cssclasses:
  - my_style_width_100
---

Percona Server의 스레드 풀은 기본적으로 CPU 코어의 개수만큼 스레드 그룹을 생성함.

일반적으로 CPU 코어의 개수는 thread_pool_size 시스템 변수를 변경해서 조정할 수 있지만 CPU 코어의 개수와 맞추는 것이 CPU 프로세서 친화도를 높이는데 좋다.


(이거 다시 봐야 할듯 현재 크게 중요할지는 모르겠다)