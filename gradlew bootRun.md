---
cssclasses:
  - my_style_width_100
---

spring initalizer를 통해서 제일 처음 스프링 부트를 다운 받으면 `./gradlew bootRun` 이라는 명령어로 스프링 애플리케이션을 실행시킵니다.
당연하게 스프링 애플리케이션을 실행시키는 명령어겠지? 정도로 받아들이다가 스프링이 없는 자바 프로젝트를 만들게 되면 bootRun 명령어가 없는 것을 알 수 있습니다.

gradle을 알게 된 이후로 스프링 프로젝트를 실행시킬 때는 대부분 ./gradlew bootRun을 실행시키거나 자바 파일 하나를 실행시키고자 할 때는 `java Main.java` 명령어를 통해 실행시킵니다.
크게 의식하지 않을 때는 스프링을 실행 시키는 것과 자바를 실행시키는 건 다르구나 정도로 이해했습니다.

하지만 스프링은 자바로 만들어진 프레임워크임에도 불구하고 실행하는 방법이 다른 것은 이해가 가지 않습니다. 

처음 스프링 부트가 어떻게 톰캣을 사용하는지 그리고 톰캣을 실행시키기는 전까지 과정이 무엇인지 하나씩 확인해보고 싶었습니다. 하지만 첫 단추부터 이해가 가지 않았기에 bootRun부터 시작하고자 합니다.

# gradle 

먼저 Gradle은 그루비를 기반으로 한 빌드 도구입니다. 처음 등장했을 때 부터 오픈소스였으며 개인적으로 자주 사용하는 빌드 도구입니다. (잘 쓰지는 못함)
Gradle은 `build.gradle`을 활용해 스크립트를 작성하는데 여기서 의존성 혹은 플러그인을 설정합니다.



- 태스크 이야기




# bootRun

다시 돌아와서 gradle에는 태스크와 플러그인이라는 기능이 존재합니다.
실제로 bootRun은 스프링에서 제공해주는 태스크입니다. 그러나 스프링 부트에서 제공해주는 태스크지만 왜 스프링은 우리가 직접 자바 파일을 실행하는 것이 아닌 bootRun이라는 기능을 제공할까요?


![[Pasted image 20240119012452.png]]


### 참조 
https://baeldung.com/java-gradle-bootrun-pass-jvm-options