---
cssclasses:
  - my_style_width_100
---

## JPA는 어떻게 MySQL 버전을 맞춰 Dialect를 선택할까?

JPA는 dialect(방언)을 통해서 데이터베이스 밴더 및 버전에 따라 적절한 쿼리를 만들어냅니다. 
하지만 코드를 작성하는 사람들은 어떤 데이터베이스 드라이버만 사용하고 있는지 정보만 넘겨줄 뿐 크게 다른점은 없습니다. 

간단하게 풀어가보면 먼저 Connector j 내부적으로 현재 사용하고 있는 MySQL버전을 넘겨줍니다.
실제로 JDBC에서도 현재 사용하는 데이터베이스의 버전을 식별해주고 있으며 실제 쿼리를 작성하기 때문에 JDBC가 버전을 식별하는 기능을 포함하는지는 모르고 있었을 겁니다.
![[Pasted image 20240514020404.png]]

이렇게 Driver에서 실제 MySQL버전 정보를 가지고 있으며 JP는 JDBC의 이런 버정 정보를 직접 가져와서 Dialect를 설정합니다. 
![[Pasted image 20240514021548.png]]
실제로 내부적으로 `DialectResolutionInfo`객체가 사용중인 MySQL 정보를 가지고 있는데 JDBC에서 정보를 미리 가져오는 방식으로 현재 상황에 맞는 dialect를 맞춰줍니다.

![[Pasted image 20240514125547.png]]

https://github.com/hibernate/hibernate-orm/blob/main/hibernate-core/src/main/java/org/hibernate/dialect/MySQLDialect.java