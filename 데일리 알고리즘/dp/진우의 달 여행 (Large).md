우주비행이 꿈이였던 진우는 음식점 '매일매일싱싱'에서 열심히 일한 결과 달 여행에 필요한 자금을 모두 마련하였다! 지구와 우주사이는 N X M 행렬로 나타낼 수 있으며 각 원소의 값은 우주선이 그 공간을 지날 때 소모되는 연료의 양이다.

![](https://upload.acmicpc.net/9e155c65-43ea-492b-af73-d3f9f9c9dc44/-/preview/)

진우는 여행경비를 아끼기 위해 조금 특이한 우주선을 선택하였다. 진우가 선택한 우주선의 특징은 아래와 같다.

**1. 지구 -> 달로 가는 경우 우주선이 움직일 수 있는 방향은 아래와 같다.**

![](https://upload.acmicpc.net/8f6fc516-9870-4ef6-8474-b5d82f7b6f21/-/preview/)![](https://upload.acmicpc.net/eb6f87f0-f4d0-43cc-8e9d-5d94bfc41936/-/preview/)![](https://upload.acmicpc.net/e7b501aa-c92c-4a17-aed7-c7868b89af7a/-/preview/)

**2. 우주선은 전에 움직인 방향으로 움직일 수 없다. 즉, 같은 방향으로 두번 연속으로 움직일 수 없다.**

진우의 목표는 **연료를 최대한 아끼며 지구의 어느위치에서든 출발하여 달의 어느위치든 착륙하는 것**이다.

최대한 돈을 아끼고 살아서 달에 도착하고 싶은 진우를 위해 달에 도달하기 위해 필요한 연료의 최소값을 계산해 주자.

## 입력

첫줄에 지구와 달 사이 공간을 나타내는 행렬의 크기를 나타내는 **N, M (2 ≤ N, M ≤ 1000)**이 주어진다.

다음 N줄 동안 각 행렬의 원소 값이 주어진다. 각 행렬의 원소값은 100 이하의 자연수이다.

## 출력

달 여행에 필요한 최소 연료의 값을 출력한다.

```
탑 다운으로 쉽게 풀 수 있을 것 같은데요?

이전 방향을 제외하고 가야 함

2번의 최적화가 가능하다고 생각함

최대값이 이미 구해진 경우 - 해당 경우는 더 이상 앞으로 나아갈 이유가 없음
캐시값이 있는 경우

추가로 고려해봐야 할 부분은 아마 이전 방향이 문제인데

지구에서 달까지 가는 것도 배열로 쳐야하나?

이차원 배열에서 출발해야 할 것 같은데 ?

[1, 2, 3, 4]
[5, 8, 5, 1]
[1, 2, 3, 4]

1 -> 5 -> 2
1 -> 5 -> 1(x)

2 -> 5 -> 1(0)
2 -> 5 -> 2(0)

2 -> 8 -> 1
2 -> 8 -> 3

2 -> 5 -> 2

결국에 캐시를 다루려면 행 열 방향 이렇게 3가지를 모두 포함해야 함

0 -> 5


<<풀이>> 
먼저 지구에서 달까지 가기 위해 중간 영역이 존재합니다.

한 가지 간과해서 안되는 부분은 중간 영역에서 첫 번째 출발지의 선택지를 고르는 과정입니다.

[1, 2, 3, 4] <---- 지구
[5, 8, 5, 1] <---- 중간 영역
[1, 2, 3, 4] <---- 달

1번에서 출발할때 선택지는 [5,8] 두 선택지를 고를 수 있습니다.
2번에서 출발할때 선택지는 [5,8,5] 선택지를 고를 수 있습니다.
4번에서 출발할때 선택지는 [5,1] 선택지를 고를 수 있습니다.

여기서 도달한 위치는 어떤 방향에서 오는지에 따라 다른 방향을 고를 수 있습니다.
선택지의 구분이 없다면 상관이 없지만 방향이 정해져 있기 때문에 추가적으로 고려해야 할 수 있습니다.

1번 선택지에서 출발할 때 [5,8]을 선택할 수 있었습니다.
그러면 2번 선택지를 보면 [5,8,5]를 선택할 수 있습니다.

여기서 공통적으로 [5,8] 이라는 선택지가 존재하는데 먼저 출발한 선택지에 따라 다음 출발할 방향이 다르기 때문에 서로는 개별적인 영역으로 구분해야 합니다.



```


```java
import java.io.*;
import java.util.*;
import java.util.function.*;
import java.util.stream.*;

public class Main{
    public static void main(String...args) throws Exception{
        final var br = new BufferedReader(new InputStreamReader(System.in));
        var st = new StringTokenizer(br.readLine());
        final var  N = Integer.parseInt(st.nextToken());
        final var  M = Integer.parseInt(st.nextToken());
        final var space = new int[N+2][M];
        final var cache = new int[N+2][M][3];

        for(int i = 1; i <= N; i++){
            st = new StringTokenizer(br.readLine());
            for(int j = 0; j < M; j++){
                space[i][j] = Integer.parseInt(st.nextToken());
            }
        }

        Search search = (index, column, direction, func) -> {
            if(index == N+1) {
                return 0;
            }

            if(cache[index][column][direction+1] != 0){
                return cache[index][column][direction+1];
            }

            IntBinaryOperator findMinSearchValue = (acc,next) -> Math.min(acc, func.apply(index + 1, column + next, next, func));
            IntPredicate moveCondition = (i) -> {
                var next = i + column;
                return next != direction && next >= 0 && next < M;

            };
            return cache[index][column][direction+1] = space[index][column] + IntStream.rangeClosed(-1, 1)
                    .filter(moveCondition)
                    .reduce(Integer.MAX_VALUE,findMinSearchValue);
        };
      
        IntStream.range(0, M)
                .map(i -> search.apply(0, i, 0, search))
                .min()
                .ifPresent(System.out::println);
    }

}


@FunctionalInterface
interface Search{
    int apply(int index, int column, int direction,  Search search);
}

```