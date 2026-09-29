# 진단 보고
- AI를 사용한 스크립트(buggy_4.py, buggy_5.py)는 AI 활용 기록을 포함해 작성하였다.
- buggy_4.py에서 AI에게 코드 설명을 요구하였고, 그 기록을 포함해 작성하였다.

## 1. buggy_1.py 진단 (AI 미사용)
### 진단 보고
1. 무엇이
    ```python
    ValueError: invalid literal for int() with base 10: '5,200'
    ```
2. 어디서
    ```python
    File "/Users/chaseyeon/dev/ai-studio/my_project/week04/buggy_1.py", line 19, in calc_total
        price = int(row["price"])        # <-- 여기가 문제의 줄
    ```
3. 왜
    - 가설: 값 '5,200' 안에 ','가 있어 숫자(int) 변환에 실패해 오류가 났을 것이다.

## 2. buggy_2.py 진단 (AI 미사용)
### 진단 보고
1. 무엇이
    ```python
    KeyError: '단가'
    ```
2. 어디서
    ```python
    File "/Users/chaseyeon/dev/ai-studio/my_project/week04/buggy_2.py", line 20, in summarize
        df["매출액"] = df["단가"] * df["수량"]        # <-- 여기가 문제의 줄
    ```
3. 왜
    - '단가'라는 키 값을 찾지 못해 오류가 났을 것이다.

## 3. buggy_3.py 진단 (AI 미사용)
### 진단 보고
1. 무엇이
    ```python
    AttributeError: 'NoneType' object has no attribute 'groupby'
    ```
2. 어디서
    ```python
    File "/Users/chaseyeon/dev/ai-studio/my_project/week04/buggy_3.py", line 28, in main
        result = df.groupby("category")["revenue"].sum()   # <-- 여기서 죽는다
    ```
3. 왜
    - groupby()를 호출하려는 변수에 데이터프레임이 아닌 None이 반환되어 오류가 났을 것이다.

## 4. buggy_4.py 진단 (AI 사용)
### 진단 보고
먼저 info()/describe()로 데이터 상태를 살펴보았다.
- 실행 결과:
    ```python
    === dirty_sales.csv 파일 내용 === 
    (500, 6)
    <class 'pandas.DataFrame'>
    RangeIndex: 500 entries, 0 to 499
    Data columns (total 6 columns):
    #   Column    Non-Null Count  Dtype  
    ---  ------    --------------  -----  
    0   date      500 non-null    str    
    1   product   500 non-null    str    
    2   category  490 non-null    str    
    3   price     498 non-null    float64
    4   quantity  500 non-null    int64  
    5   stock     485 non-null    float64
    dtypes: float64(2), int64(1), str(3)
    memory usage: 23.6 KB
    None
                price      quantity       stock
    count  4.980000e+02  5.000000e+02  485.000000
    mean   2.834237e+04  2.010569e+04  249.995876
    std    4.477810e+05  4.472088e+05  141.211450
    min   -4.500000e+03  1.000000e+00    1.000000
    25%    3.800000e+03  5.375000e+01  128.000000
    50%    5.000000e+03  1.120000e+02  250.000000
    75%    1.200000e+04  1.610000e+02  363.000000
    max    9.999999e+06  9.999999e+06  500.000000
    ```
해당 결과를 통해 알 수 있는 것은 다음과 같다.

1. price에 2개의 결측값이 있다. 500개의 행 중에 498개의 값 밖에 없기 때문이다.
2. price의 최솟값이 음수이고, 최댓값이 9999999 같은 값임을 알 수 있다. 이는 정상적인 값이라고 보기 어렵다.

따라서 현재의 스크립트 출력 결과는 틀렸다고 할 수 있다.

## AI 활용 기록(1)
- 프롬포트 전문:
    1. csv 데이터를 읽어 총 매출액을 집계하는 스크립트입니다.
    2. 코드:
        ```python
        def main():
        df = pd.read_csv("./week04/dirty_sales.csv", encoding="utf-8")

        # price를 숫자로 바꾼다 (빈 값은 NaN이 된다 — 그런데 그 규모를 확인하지 않았다)
        df["price"] = (df["price"].astype(str)
                                .str.replace(",", "")
                                .str.replace("원", "")
                                .str.strip())
        df["price"] = pd.to_numeric(df["price"], errors="coerce")

        # 매출액 = 단가 x 수량 (NaN이 섞이면 그 행의 매출액도 NaN)
        df["revenue"] = df["price"] * df["quantity"]

        # sum()은 NaN을 조용히 건너뛰고, 음수/극단값은 그대로 더한다
        total = df["revenue"].sum()
        avg_price = df["price"].mean()

        print(f"총 매출액: {total:,.0f}원")
        print(f"평균 단가: {avg_price:,.0f}원")
        ```
    3. 에러는 발생하지 않지만 결과값이 틀린 것 같습니다. 왜냐하면 info()/describe()로 데이터 상태를 살펴보았을 때, 다음을 확인할 수 있었기 떄문입니다.
        1. price에 2개의 결측값이 있다. 500개의 행 중에 498개의 값 밖에 없기 때문이다.
        2. 또한 price의 최솟값이 음수이고, 최댓값이 9999999 같은 값임을 알 수 있다. 이는 정상적인 값이라고 보기 어렵다.
    4. 이러한 오류의 원인을 설명하고, 원인 검증용 코드를 먼저 제안해 주세요. 수정 코드는 그 다음 진행하겠습니다.
- AI 답변 요지:
    수정 전에 다음 네 가지를 확인할 것을 추천한다.
    | 확인 항목 | 검증 방법                    | 확인 목적          |
    | ----- | ------------------------ | -------------- |
    | 결측값   | `isna().sum()`           | 가격 누락 여부       |
    | 결측 행  | `df[df["price"].isna()]` | 어떤 데이터가 누락됐는지  |
    | 음수 가격 | `df[df["price"] < 0]`    | 비정상적인 가격 존재 여부 |
    | 극단값   | `nlargest(10, "price")`  | 비정상적으로 큰 가격 확인 |
- 채택/기각:
    - 채택:
        - `isna().sum()`를 통해 누락된 가격의 규모를 확인하였다.
        - `df[df["price"].isna()]`를 통해 어떤 데이터가 누락됐는지 확인하였다.
        - `df[df["price"] < 0]`를 통해 음수 값을 확인하였다.
    - 기각:
        - 비정상적으로 큰 값을 확인할 때에는 AI 답변대로가 아닌 `print(df.sort_values("price").tail(5))`로 확인하였다.
- 검증 결과:
    - 다음과 같이 정확한 결측 규모를 파악할 수 있었다.
        ```
        2
           date product category  price  quantity  stock
        399  2026-01-13   아메리카노       음료    NaN        86  124.0
        468  2026-05-17     마들렌     베이커리    NaN       181  117.0
                date product category   price  quantity  stock
        199  2026-02-04     마들렌     베이커리 -4500.0       119   93.0
                date  product category      price  quantity  stock
        261  2026-03-19  에티오피아원두       원두    21000.0        22  127.0
        280  2026-03-15  에티오피아원두       원두    21000.0       113   63.0
        250  2026-02-19     카페라떼       음료  9999999.0        76  116.0
        399  2026-01-13    아메리카노       음료        NaN        86  124.0
        468  2026-05-17      마들렌     베이커리        NaN       181  117.0
        ```

## AI에게 코드 설명 요구
- 프롬포트 전문:
    1. csv 데이터를 읽어 총 매출액을 집계하는 스크립트입니다.
    2. 코드:
        ```python
        """데이터 점검"""
        # df = pd.read_csv("./week04/dirty_sales.csv", encoding="utf-8")
        # df["price"] = (df["price"].astype(str)
        #                               .str.replace(",", "")
        #                               .str.replace("원", "")
        #                               .str.strip())
        # df["price"] = pd.to_numeric(df["price"], errors="coerce")

        # print(" === dirty_sales.csv 파일 내용 === ")
        # print(df.shape) # (행 수, 열 수)
        # print(df.info()) # 열 이름, 타입, 결측 여부
        # print(df.describe())

        def main():
            df = pd.read_csv("./week04/dirty_sales.csv", encoding="utf-8")

            # price를 숫자로 바꾼다 (빈 값은 NaN이 된다 — 그런데 그 규모를 확인하지 않았다)
            df["price"] = (df["price"].astype(str)
                                    .str.replace(",", "")
                                    .str.replace("원", "")
                                    .str.strip())
            df["price"] = pd.to_numeric(df["price"], errors="coerce")

            print(df["price"].isna().sum()) # FIXED: NaN 값 규모 확인 / 2개 확인함.
            print(df[df["price"].isna()]) # FIXED: NaN 행 데이터 확인
            print(df[df["price"] < 0]) # FIXED: 음수값 확인 / 1개(-4500) 확인함.
            print(df.sort_values("price").tail(5)) # FIXED: 최댓값 쪽 실제 행 확인 / 1개(9999999) 확인함.

            # FIXED: 가격 결측치를 0으로 처리
            df["price"] = df["price"].fillna(0)

            # FIXED: 비정상적인 가격 데이터 제거
            df = df[(df["price"] >= 0) & (df["price"] != 9999999)]

            # 매출액 = 단가 x 수량 (NaN이 섞이면 그 행의 매출액도 NaN)
            df["revenue"] = df["price"] * df["quantity"]

            # sum()은 NaN을 조용히 건너뛰고, 음수/극단값은 그대로 더한다
            total = df["revenue"].sum()
            avg_price = df["price"].mean()

            print(f"총 매출액: {total:,.0f}원")
            print(f"평균 단가: {avg_price:,.0f}원")
            # 출력은 그럴듯하지만, 이 숫자를 그대로 믿어도 될까?

        if __name__ == "__main__":
            main()
        ```
    3. 출력값은 다음과 같습니다.
        ```python
        # 데이터 점검
        === dirty_sales.csv 파일 내용 === 
        (500, 6)
        <class 'pandas.DataFrame'>
        RangeIndex: 500 entries, 0 to 499
        Data columns (total 6 columns):
        #   Column    Non-Null Count  Dtype  
        ---  ------    --------------  -----  
        0   date      500 non-null    str    
        1   product   500 non-null    str    
        2   category  490 non-null    str    
        3   price     498 non-null    float64
        4   quantity  500 non-null    int64  
        5   stock     485 non-null    float64
        dtypes: float64(2), int64(1), str(3)
        memory usage: 23.6 KB
        None
                    price      quantity       stock
        count  4.980000e+02  5.000000e+02  485.000000
        mean   2.834237e+04  2.010569e+04  249.995876
        std    4.477810e+05  4.472088e+05  141.211450
        min   -4.500000e+03  1.000000e+00    1.000000
        25%    3.800000e+03  5.375000e+01  128.000000
        50%    5.000000e+03  1.120000e+02  250.000000
        75%    1.200000e+04  1.610000e+02  363.000000
        max    9.999999e+06  9.999999e+06  500.000000

        # 출력값
        2
           date product category  price  quantity  stock
        399  2026-01-13   아메리카노       음료    NaN        86  124.0
        468  2026-05-17     마들렌     베이커리    NaN       181  117.0
                date product category   price  quantity  stock
        199  2026-02-04     마들렌     베이커리 -4500.0       119   93.0
                date  product category      price  quantity  stock
        261  2026-03-19  에티오피아원두       원두    21000.0        22  127.0
        280  2026-03-15  에티오피아원두       원두    21000.0       113   63.0
        250  2026-02-19     카페라떼       음료  9999999.0        76  116.0
        399  2026-01-13    아메리카노       음료        NaN        86  124.0
        468  2026-05-17      마들렌     베이커리        NaN       181  117.0
        총 매출액: 150,438,924,400원
        평균 단가: 8,271원
        ```
    4. 내가 작성한 코드를 설명해주세요. 그리고 코드를 평가해주세요.
- AI 답변 요지:
    - 수정하거나 생각해볼 점
        price의 결측값을 0으로 바꾼 뒤 필터링하고 있어, 결측 행이 제거되지 않고 0원으로 남습니다.
        따라서 평균 단가 계산에도 결측 행이 포함되어 평균값이 왜곡될 수 있습니다.
        가격을 알 수 없는 행은 0원으로 처리하기보다 집계에서 제외하는 것이 적절한지 검토할 필요가 있습니다.

- 본인 검증 의견:
    - AI의 분석과 같은 생각이다. 결측값을 0원으로 처리하면 실제 가격을 알 수 없는 데이터를 0원으로 간주하게 되므로, 해당 행을 매출 및 평균 단가 계산에서 제외하는 것이 더 적절하다고 생각되었다.

## 5. buggy_5.py 진단 (AI 사용)
### 진단 보고
1. 무엇이
    ```python
    IndexError: list index out of range
    ```
2. 어디서
    ```python
    FFile "/Users/chaseyeon/dev/ai-studio/my_project/week04/buggy_5.py", line 29, in find_big_jumps
        diff = prices[i + 1] - prices[i]      # <-- 여기가 문제의 줄
    ```
3. 왜
    - 리스트 범위 밖 인덱스를 참조해 오류가 났을 것이다.

## AI 활용 기록(2)
- 프롬포트 전문:
    1. csv 데이터를 읽어 '앞 행 대비 가격 변화'가 큰 행을 찾는 스크립트입니다.
    2. 코드:
        ```python
        def find_big_jumps(prices, threshold=100000):
        jumps = []
        for i in range(len(prices)):
            diff = prices[i + 1] - prices[i]      # <-- 여기가 문제의 줄
            if abs(diff) >= threshold:
                jumps.append((i, prices[i], prices[i + 1], diff))
        return jumps
        ```
    3. 에러 로그:
        ```python
        Traceback (most recent call last):
        File "/Users/chaseyeon/dev/ai-studio/my_project/week04/buggy_5.py", line 36, in <module>
            jumps = find_big_jumps(prices)
        File "/Users/chaseyeon/dev/ai-studio/my_project/week04/buggy_5.py", line 29, in find_big_jumps
            diff = prices[i + 1] - prices[i]      # <-- 여기가 문제의 줄
                ~~~~~~^^^^^^^
        IndexError: list index out of range
        ```
    4. 리스트 범위 밖 인덱스를 참조해 오류가 난 것 같습니다.
    5. 이 에러의 원인을 설명하고, 원인 검증 방법을 제안해 주세요. 수정 코드는 그 다음 진행하겠습니다.
- AI 답변 요지:
    - range(len(prices))는 마지막 요소의 인덱스까지 포함하지만, 코드에서는 모든 i에 대해 prices[i + 1]을 참조하고 있다. 따라서 마지막 반복에서 존재하지 않는 다음 인덱스를 참조하여 IndexError가 발생한다.
- 채택/기각:
    - 채택: AI의 답변을 통해 오류 원인을 정확히 이해할 수 있었다.
    - 기각:
        AI는 다음과 같이 코드를 작성해 원인을 검증할 것을 추천했다. 
        ```python
        print("prices 길이:", len(prices))
        print("prices:", prices)
        ```
        그러나 이번 오류는 코드 자체의 논리적 오류였기 때문에,
        코드를 작성해 이해한 사실을 다시 확인하기 보다는
        **중단점 설정**으로 실제로 언제 오류가 발생했는지 확인하는 방식을 취했다.
- 검증 결과:
    - 이해한 오류 원인을 바탕으로 코드를 수정하였고, 그 결과 오류를 해결하였다.
