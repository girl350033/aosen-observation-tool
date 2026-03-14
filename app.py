import streamlit as st
from openai import OpenAI

# 1. 網頁頁面設定
st.set_page_config(page_title="Aosen 專業觀察紀錄助手", page_icon="📝", layout="centered")

# 2. 側邊欄設定
with st.sidebar:
    st.title("⚙️ 系統設定")
    api_key = st.text_input("輸入 OpenAI API Key", type="password")
    st.divider()
    age_group = st.selectbox(
        "選擇幼生月齡階段：",
        ["0-3個月", "4-6個月", "7-12個月", "13-18個月", "19-24個月"]
    )

# 3. 主介面
st.title("👶 專業觀察紀錄自動生成器")
st.write("輸入內容，AI 將生成約 150-200 字的專業紀錄。")

# 4. 輸入區域
raw_input = st.text_area(
    "請貼入觀察草稿（無需去識別化）：",
    height=200,
    placeholder="直接貼上包含幼生名字的觀察內容即可..."
)

# 5. 生成按鈕與邏輯
if st.button("🚀 生成精簡版紀錄 (150-200字)", use_container_width=True):
    if not api_key:
        st.error("❌ 請先在左側輸入您的 API Key。")
    elif not raw_input:
        st.warning("⚠️ 請先輸入內容。")
    else:
        try:
            client = OpenAI(api_key=api_key)
            
            with st.spinner('撰寫中...'):
                # 核心指令微調：取消去識別化、嚴格限縮字數
                sys_prompt = f"""
                你是一位台灣托嬰中心老師。請針對「{age_group}」幼生撰寫觀察紀錄。
                
                【核心要求】：
                1. 字數控制：總字數「必須」介於 150 至 200 字之間，不可過長。
                2. 結構：一段式呈現，包含「活動過程」與「單一發展領域觀察」。
                3. 內容：請保留原始輸入中的幼生姓名，不需去識別化。
                4. 專業性：參考台灣托育指引，擇一領域（如：精細動作、語言溝通等）深入撰寫。
                5. 語氣：專業且精煉，刪除冗言贅句。
                """
                
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": sys_prompt},
                        {"role": "user", "content": f"這是觀察內容：{raw_input}"}
                    ],
                    temperature=0.7
                )
                
                result = response.choices[0].message.content

                # 6. 顯示結果
                st.success("✅ 生成完畢！")
                st.markdown("---")
                st.markdown("### 📋 專業觀察紀錄")
                st.write(result)
                
                # 即時字數統計，方便您確認
                st.caption(f"📊 當前字數統計：{len(result)} 字")
                
        except Exception as e:
            st.error(f"發生錯誤：{str(e)}")

# 頁尾
st.markdown("---")
st.caption("Aosen Wonderland 行政優化工具 - 150字精簡版")