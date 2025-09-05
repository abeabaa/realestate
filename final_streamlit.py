import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt



# 한글 폰트 설정 (Windows)
plt.rcParams['font.family'] = 'NanumGothic'
plt.rcParams['axes.unicode_minus'] = False

# 파일 경로 (배포용은 GitHub 또는 cloud storage 경로 권장)
file_path = "20250818_주간시계열.xlsx"

# --- 데이터 불러오기 ---
# 매매증감
sale = pd.read_excel(file_path, sheet_name="1.매매증감", skiprows=[0,2,3])
sale = sale[sale.iloc[:,0].notna()]
sale.rename(columns={sale.columns[0]: "날짜"}, inplace=True)
sale["날짜"] = pd.to_datetime(sale["날짜"])

# 전세증감
rent = pd.read_excel(file_path, sheet_name="2.전세증감", skiprows=[0,2,3])
rent = rent[rent.iloc[:,0].notna()]
rent.rename(columns={rent.columns[0]: "날짜"}, inplace=True)
rent["날짜"] = pd.to_datetime(rent["날짜"])

# 병합
df = pd.merge(sale, rent, on="날짜", suffixes=("_매매","_전세"))

# 지역 목록
regions = [col.replace("_매매","") for col in df.columns if col.endswith("_매매")]

# --- Streamlit 앱 ---
st.title("부동산 4분면 그래프")

# 사용자 입력 UI
region = st.selectbox("지역 선택", regions, index=0)
start_date = st.date_input("시작일", value=df["날짜"].min())
end_date = st.date_input("종료일", value=df["날짜"].max())

# --- 그래프 그리기 ---
data = df[["날짜", f"{region}_매매", f"{region}_전세"]].dropna()
data = data[(data["날짜"] >= pd.to_datetime(start_date)) & (data["날짜"] <= pd.to_datetime(end_date))]

fig, ax = plt.subplots(figsize=(8,8))
ax.axhline(0, color="black", linewidth=1)
ax.axvline(0, color="black", linewidth=1)
ax.scatter(data[f"{region}_매매"], data[f"{region}_전세"], alpha=0.6, label="기간 데이터")

if not data.empty:
    latest = data.iloc[-1]
    ax.scatter(latest[f"{region}_sale"], latest[f"{region}_jeonse"], color="red", s=100, label="latest week")

ax.set_title(f"{region} graph")
ax.set_xlabel("sale (%)")
ax.set_ylabel("jeonse (%)")
ax.legend()
ax.grid(True)

st.pyplot(fig)







