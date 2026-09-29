# -*- coding: utf-8 -*-
"""
buggy_1.py  ―  판매 데이터 매출 집계 (csv 모듈 버전)

dirty_sales.csv를 한 줄씩 읽어 '매출액 = 단가 x 수량'을 누적한다.
잘 돌아가는 것처럼 보이지만, 어떤 행에서 갑자기 멈춘다.

[과제] 이 스크립트를 실행해 Traceback을 얻고,
       진단 3단계 루틴(무엇이 / 어디서 / 왜)으로 원인을 특정한 뒤
       전처리로 해결하라. (힌트: 예외 타입은 무엇인가?)
"""
import csv

# FIXED: 데이터 전처리 전 데이터 점검
"""데이터 점검"""
import pandas as pd
df = pd.read_csv("./week04/dirty_sales.csv", encoding="utf-8")

# print(" === dirty_sales.csv 파일 내용 === ")
# print(df.shape) # (행 수, 열 수)
# print(df.info()) # 열 이름, 타입, 결측 여부
# print(df.isna().sum()) # 컬럼별 결측치 개수
# print(df[df["price"].isna()].head()) # 결측이 있는 행 직접 눈으로 확인

"""실행 결과"""
# "price"의 non-null 개수: 2
# "price"의 결측치 개수: 2
# 결측이 있는 행:
#            date product category price  quantity  stock
# 399  2026-01-13   아메리카노       음료   NaN        86  124.0
# 468  2026-05-17     마들렌     베이커리   NaN       181  117.0

def calc_total(path):
    total = 0
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)  # 사전타입으로 데이터를 읽음.
        for i, row in enumerate(reader):

            # FIXED: 데이터 점검 내용을 토대로 데이터 전처리 코드 작성
            # 전처리 내용: 콤마, "원" 삭제, 결측치 NaN를 0으로 변환
            price = row["price"].replace(",", "").replace("원", "").strip()
            if price == "":
                price = 0
            else:
                price = int(price)

            qty = int(row["quantity"])
            total += price * qty
    return total

if __name__ == "__main__":
    total = calc_total("./week04/dirty_sales.csv")
    print(f"총 매출액: {total:,}원")
