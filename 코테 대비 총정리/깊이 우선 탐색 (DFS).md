


## 그래프 탐색
- 일반적으로 DFS는 스택으로 구현하며, 재귀를 이용하면 좀 더 간단하게 구현할 수 있다. 

### 재귀 구조로 표현
```
DFS(G, v)
	label v as discovered
	for all directed edges from v to w that are in G.adjancetEges(v) do
		if vertex w is not labeled as discovered then
			recursively call DFS(G, w)
```

- 위 수도코드에는 정점 v의 모든 인접 유향 간선들을 반복하라고 표기돼 있으며![[Pasted image 20240403173143.png]]
- 자바 코드로 구현하면 다음과 같다. 
- 여기서 방문했던 정점, 즉 discovered를 계속 누적된 결과로 만들기 위해 리턴하는 형태만 받아오도록 처리했을 뿐, 변수명까지 동일하게 수도코드와 맞춰서 작성됐다. 
- ![[Pasted image 20240403173244.png | 300]]