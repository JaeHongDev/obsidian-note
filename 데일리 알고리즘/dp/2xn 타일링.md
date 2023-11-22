https://www.acmicpc.net/problem/11726
|시간 제한|메모리 제한|제출|정답|맞힌 사람|정답 비율|
|---|---|---|---|---|---|
|1 초|256 MB|145185|55773|41299|36.332%|

## 문제

2×n 크기의 직사각형을 1×2, 2×1 타일로 채우는 방법의 수를 구하는 프로그램을 작성하시오.

아래 그림은 2×5 크기의 직사각형을 채운 한 가지 방법의 예이다.

![](https://onlinejudgeimages.s3-ap-northeast-1.amazonaws.com/problem/11726/1.png)


### 풀이
2xn 크기의 직사각형을 채우는 경우의 수를 구하는 문제이다.
채울 수 있는 직사각형의 타일의 크기는 1x2, 2x1 타일이다.
```
2x1 = 1 [2x1 블록만 가능]
|
|
2x2 = 2
-- ||
-- ||
2x1블록 2개와
1x2블록 2개가 필요함

2x3 = 3
|-- --| |||
|-- --| |||
2x1 + 1x2
1x2 + 2x1
2x1 + 2x1 + 2x1
와 같은 형태가 필요함

2x4 = 5
|--| ||-- --|| ---- ||||
|--| ||-- --|| ---- ||||

2x1 + 1x2 + 1x2 + 2x1
1x2 + 1x2 + 1x2 + 2x1 
1x2 + 1x2 + 2x1 + 2x1

2x5 =
```

위에 처럼 블록을 하나씩 쌓아가면서 생각해볼 수 있지만 조금 더 쉽게 생각하는 방법이 있다.
```
2x10의 블록을 만들어야 하는 상황이 발생했다면 다음과 같이 생각할 수 있다.
2x9 + 2x1
2x8 + 1x2(2)

이전에 어떤 블록이 들어오더라도 마지막에 들어가는 블록으 2x1인지 1x2인지에 따라서 나올 수 있는 블록의 개수는 달라진다.

마찬가지로
2x9는
2x8 + 2x1
2x7 + 1x2(2)
와 같이 표현이 가능하다.

그렇기 때문에 다음과 같은 점화식으로 표현이 가능해진다.
f(n) = f(n-1)x1 + f(n-2)x1
f(n) = f(n-1) + f(n-2)
1을 곱하는 거는 기존에 블록뒤에 2x1혹은 1x2블록이 포함이 되기 때문이다.

```

```java
import java.io.*; 
import java.util.*;

public class Main{
	public static void main(String...args)throws Exception{
		var br = new BufferedReader(new InputStreamReader(System.in));
		var n = Integer.parseInt(br.readLine());

		var cache = new int[1001];
		
		cache[1] = 1;
		cache[2] = 2;

		for(int i = 3; i <= 1000; i++){
			cache[i] = (cache[i-1] + cache[i-2]) % 10_007;
		}

		System.out.println(cache[n]);
		

	}
}

```
![[Pasted image 20230629104036.png]]