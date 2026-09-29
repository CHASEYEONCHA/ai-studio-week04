# -*- coding: utf-8 -*-
"""
buggy_2.py  ―  카테고리별 매출 집계 (pandas 버전)

dirty_sales.csv를 pandas로 읽어 카테고리별 매출 합계를 구하려 한다.
그런데 실행하자마자 죽는다.

[과제] Traceback을 얻어 예외 타입을 확인하고,
       '원인을 데이터에서 직접 확인'한 뒤(힌트: 실제 컬럼명이 무엇인가?)
       코드를 수정하라.
"""
import pandas as pd

# FIXED: 데이터 점검 코드 추가. '단가'라는 키 값이 있는지, 없다면 실제 컬럼명이 무엇인지 확인한다.
"""데이터 점검"""
# df = pd.read_csv("./week04/dirty_sales.csv", encoding="utf-8")

# print(" === dirty_sales.csv 파일 내용 === ")
# print(df.head()) #
# print(df.shape) # (행 수, 열 수)
# print(df.info()) # 열 이름, 타입, 결측 여부

"""실행 결과"""
# === dirty_sales.csv 파일 내용 === 
#          date product category  price  quantity  stock
# 0  2026-01-29     텀블러       굿즈  15000         7  379.0
# 1  2026-03-04    크루아상     베이커리   3800        58   71.0
# 2  2026-01-27     에코백       굿즈  12000       174  379.0
# 3  2026-01-23  콜롬비아원두       원두  18000       152  216.0
# 4  2026-01-08   아메리카노       음료   4500        24  111.0
# (500, 6)
# <class 'pandas.DataFrame'>
# RangeIndex: 500 entries, 0 to 499
# Data columns (total 6 columns):
#  #   Column    Non-Null Count  Dtype  
# ---  ------    --------------  -----  
#  0   date      500 non-null    str    
#  1   product   500 non-null    str    
#  2   category  490 non-null    str    
#  3   price     498 non-null    str    
#  4   quantity  500 non-null    int64  
#  5   stock     485 non-null    float64
# dtypes: float64(1), int64(1), str(4)


def load(path):
    df = pd.read_csv(path, encoding="utf-8")
    return df

def summarize(df):
    # 단가 x 수량으로 매출액 컬럼을 만든 뒤 카테고리별 합계를 낸다

    # FIXED: 'price'의 데이터 타입이 str이기 때문에, 계산 전 먼저 숫자로 변환함.
    df["price"] = (pd.to_numeric(df["price"].astype(str)
                                 .str.replace(",", "", regex = False)
                                 .str.replace("원", "", regex = False),
                                 errors = "coerce"
                                 )
                                 .astype("Int64"))

    # FIXED: 실제 컬럼명이 '단가', '수량'이 아닌 'price', 'quantity'이기에 수정함. 
    df["매출액"] = df["price"] * df["quantity"]

    return df.groupby("category")["매출액"].sum()

if __name__ == "__main__":
    df = load("./week04/dirty_sales.csv")
    result = summarize(df)
    print(result)