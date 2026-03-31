# 7. 흐름 제어 및 조건 루프

---

## 7.1 명령 조합: Shell의 본질

단일 명령은 능력이 제한적입니다. 그것들을 **조합**해야만 복잡한 작업을 완료할 수 있습니다.

AI가 강력한 이유는 주로 이러한 조합을 마스터하기 때문입니다:

```bash
cat access.log | grep "ERROR" | sort | uniq -c | sort -rn | head -10
```

이것은 의미합니다: "access.log에서 오류를 찾고, 발생 횟수를 세고, 상위 10개를 표시"

---

## 7.2 `|` (파이프): 데이터 흐름의 기술

파이프는 이전 명령의 **출력**을 다음 명령의 **입력**으로 만듭니다.

```bash
# 파일 내용 정렬
cat unsorted.txt | sort

# 가장 흔한 명령 찾기
history | awk '{print $2}' | sort | uniq -c | sort -rn | head -10

# 로그에서 IP 추출 및 카운트
cat access.log | awk '{print $1}' | sort | uniq -c | sort -rn | head -5
```

### stderr 파이핑

```bash
# stderr를 파이프로 보내기
command1 2>&1 | command2

# 또는 Bash 4+
command1 |& command2
```

---

## 7.3 `&&`: 성공한 경우에만 다음 실행

**command1이 성공한 경우에만 (종료 코드 = 0) command2가 실행됩니다.**

```bash
# 디렉토리 생성 후 이동
mkdir -p project && cd project

# 컴파일 후 실행
gcc -o program source.c && ./program

# 다운로드 후 압축 해제
curl -L -o archive.tar.gz http://example.com/file && tar -xzf archive.tar.gz
```

---

## 7.4 `||`: 실패한 경우에만 다음 실행

**command1이 실패한 경우에만 (종료 코드 ≠ 0) command2가 실행됩니다.**

```bash
# 파일이 없으면 생성
[ -f config.txt ] || echo "Config missing" > config.txt

# 한 가지 방식으로 시도하고, 안 되면 다른 것으로
cd /opt/project || cd /home/user/project

# 실패해도 성공 확보 (makefile에서 흔함)
cp file.txt file.txt.bak || true
```

### `&&`와 `||` 조합

```bash
# 조건 표현식
[ -f config ] && echo "Found" || echo "Not found"

# 다음と同등:
if [ -f config ]; then
    echo "Found"
else
    echo "Not found"
fi
```

---

## 7.5 `;`: 관계없이 실행

```bash
# 세 개 모두 실행
mkdir /tmp/test ; cd /tmp/test ; pwd
```

---

## 7.6 `$()`: 명령 치환

**명령을 실행하고, `$()`를 그 출력으로 대체합니다.**

```bash
# 기본 사용
echo "Today is $(date +%Y-%m-%d)"
# 출력: Today is 2026-03-22

# 변수에서
FILES=$(ls *.txt)

# 디렉토리 이름 얻기
DIR=$(dirname /path/to/file.txt)
BASE=$(basename /path/to/file.txt)

# 계산
echo "Result is $((10 + 5))"
# 출력: Result is 15
```

### 백틱과의 비교

```bash
# 둘 다 동일
echo "Today is $(date +%Y)"
echo "Today is `date +%Y`"

# 하지만 $()는 중첩 가능
echo $(echo $(echo nested))
```

---

## 7.7 `[[ ]]`와 `[ ]`: 조건 테스트

### 파일 테스트

```bash
[[ -f file.txt ]]      # 일반 파일 존재
[[ -d directory ]]     # 디렉토리 존재
[[ -e path ]]           # 모든 타입 존재
[[ -L link ]]           # 심볼릭 링크 존재
[[ -r file ]]           # 읽기 가능
[[ -w file ]]           # 쓰기 가능
[[ -x file ]]           # 실행 가능
[[ file1 -nt file2 ]]  # file1이 file2보다 최신
```

### 문자열 테스트

```bash
[[ -z "$str" ]]        # 문자열이 비어있음
[[ -n "$str" ]]        # 문자열이 비어있지 않음
[[ "$str" == "value" ]] # 같음
[[ "$str" =~ pattern ]]  # 정규식 일치
```

### 숫자 테스트

```bash
[[ $num -eq 10 ]]      # 같음
[[ $num -ne 10 ]]      # 같지 않음
[[ $num -gt 10 ]]      # 큼
[[ $num -lt 10 ]]      # 작음
```

---

## 7.8 `if`: 조건문

```bash
if [[ condition ]]; then
    # something
elif [[ condition2 ]]; then
    # something else
else
    # fallback
fi
```

### 완전한 예시

```bash
#!/bin/bash

FILE="config.yaml"

if [[ ! -f "$FILE" ]]; then
    echo "Error: $FILE does not exist"
    exit 1
fi

if [[ -r "$FILE" ]]; then
    echo "File is readable"
else
    echo "File is not readable"
fi
```

---

## 7.9 `for`: 루프

### 기본 문법

```bash
for variable in list; do
    # use $variable
done
```

### AI의 일반적인 패턴

```bash
# 모든 .txt 파일 처리
for file in *.txt; do
    echo "Processing $file"
done

# 숫자 범위
for i in {1..10}; do
    echo "Iteration $i"
done

# 배열
for color in red green blue; do
    echo $color
done

# C 스타일 루프 (Bash 3+)
for ((i=0; i<10; i++)); do
    echo $i
done
```

---

## 7.10 `while`: 조건 루프

```bash
# 행 읽기
while IFS= read -r line; do
    echo "Read: $line"
done < file.txt

# 카운트 루프
count=0
while [[ $count -lt 10 ]]; do
    echo $count
    ((count++))
done
```

---

## 7.11 `case`: 패턴 매칭

```bash
case $ACTION in
    start)
        echo "Starting service..."
        ;;
    stop)
        echo "Stopping service..."
        ;;
    restart)
        $0 stop
        $0 start
        ;;
    *)
        echo "Usage: $0 {start|stop|restart}"
        exit 1
        ;;
esac
```

### 와일드카드 패턴

```bash
case "$filename" in
    *.txt)
        echo "Text file"
        ;;
    *.jpg|*.png|*.gif)
        echo "Image file"
        ;;
    *)
        echo "Unknown type"
        ;;
esac
```

---

## 7.12 빠른 참조

| 기호 | 이름 | 설명 |
|------|------|------|
| `\|` | 파이프 | 출력을 다음 입력으로 전달 |
| `&&` | AND | 이전이 성공하면 다음 실행 |
| `\|\|` | OR | 이전이 실패하면 다음 실행 |
| `;` | 세미콜론 | 관계없이 실행 |
| `$()` | 명령 치환 | 실행 후 출력으로 대체 |
| `[[ ]]` | 조건 테스트 | 권장 테스트 문법 |
| `if` | 조건문 | 조건에 따른 분기 |
| `for` | 카운트 루프 | 목록 반복 |
| `while` | 조건 루프 | 조건이 참인 동안 반복 |
| `case` | 패턴 매칭 | 다중 분기 |

---

## 7.13 연습 문제

1. `|`를 사용하여 `ls`, `grep`, `wc`를 결합하여 `.log` 파일 수 세기
2. `&&`를 사용하여 `cd`가 성공한后才 진행하기
3. `for` 루프로 10개의 디렉토리 생성 (dir1부터 dir10까지)
4. `while read`를 사용하여 /etc/hosts 읽고 표시
5. `case`로 간단한 계산기 작성 (덧셈, 뺄셈, 곱셈, 나눗셈)
