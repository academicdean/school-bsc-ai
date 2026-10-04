import streamlit as st
from openai import OpenAI
import pandas as pd

# ==========================================
# 初始化 Session State
# ==========================================
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'vision' not in st.session_state:
    st.session_state.vision = ""
if 'stakeholders' not in st.session_state:
    st.session_state.stakeholders = []
if 'step1_result' not in st.session_state:
    st.session_state.step1_result = ""
if 'selected_actions' not in st.session_state:
    st.session_state.selected_actions = {}
if 'step2_result' not in st.session_state:
    st.session_state.step2_result = ""
if 'step3_result' not in st.session_state:
    st.session_state.step3_result = ""

# ==========================================
# 介面與 API 設定
# ==========================================
st.set_page_config(page_title="能動平衡計分卡 AI 引導系統", layout="wide")
st.title("🎯 能動平衡計分卡 AI 引導系統")
st.markdown("本系統扮演「引導教練」，透過分步對話協助校務團隊將抽象願景轉化為具體的策略地圖與數據化指標。")

with st.sidebar:
    st.header("⚙️ 系統設定")
    api_key = st.text_input("請輸入您的 OpenAI API Key", type="password")
    if api_key:
        client = OpenAI(api_key=api_key)
    st.markdown("---")
    st.markdown("**開發提醒**：為避免 AI 產生企業術語，系統已於後台強制鎖定 AI 身分為高中校務治理專家，並嚴格限縮於四大構面框架中。")

def call_openai(system_prompt, user_prompt):
    if not api_key:
        st.error("請先於左側欄位輸入 OpenAI API Key")
        st.stop()
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    
    with st.spinner("AI 治理專家正在生成建議，請稍候..."):
        try:
            # 已更新為 Luna 模型並移除不支援的 temperature 參數
            response = client.chat.completions.create(
                model="gpt-6-luna", 
                messages=messages
            )
            return response.choices[0].message.content
        except Exception as e:
            st.error(f"API 呼叫發生錯誤: {e}")
            st.stop()

# ==========================================
# 步驟一：學校願景與利害關係人盤點
# ==========================================
if st.session_state.step == 1:
    st.header("步驟一：學校願景與利害關係人盤點")
    st.info("說明：能動平衡計分卡作為社會實踐策略地圖，幫助我們聚焦方向與影響力。")
    
    vision = st.text_area("請簡述我們學校近三年的核心願景或重點發展特色：", 
                          value="（例如：推動數位雙語、深耕在地社區、發展科學教育等）")
    stakeholders = st.multiselect("這次的計畫，我們最需要向哪些利害關係人交代或滿足他們的期待？", 
                                  ["學生", "家長", "教育局", "社區夥伴", "大學端"])
    
    if st.button("下一步：生成行動項目建議"):
        if vision and stakeholders:
            st.session_state.vision = vision
            st.session_state.stakeholders = stakeholders
            
            system_prompt = "你是一位精通「能動平衡計分卡」的高中校務治理專家。你的任務是協助學校將抽象願景轉化為具體的策略地圖。"
            user_prompt = f"""
            我們學校的核心願景是「{vision}」，主要關注的利害關係人包含「{', '.join(stakeholders)}」。
            請根據這些資訊，在能動平衡計分卡的四大策略構面（計畫治理、人才培育、主題共融、夥伴關係）中，
            為每個構面建議 2 個具體的「行動項目」。請以列點方式呈現，並簡短說明為什麼這項行動能回應利害關係人的需求。
            """
            st.session_state.step1_result = call_openai(system_prompt, user_prompt)
            st.session_state.step = 2
            st.rerun()
        else:
            st.warning("請填寫願景並至少選擇一個利害關係人。")

# ==========================================
# 步驟二：建構四大構面與挑選行動項目
# ==========================================
elif st.session_state.step == 2:
    st.header("步驟二：建構四大構面與挑選行動項目")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.subheader("💡 AI 行動項目建議")
        st.markdown(st.session_state.step1_result)
        if st.button("回上一步重新生成"):
            st.session_state.step = 1
            st.rerun()

    with col2:
        st.subheader("🎯 挑選或修改行動項目")
        st.markdown("請參考左側建議，在四個構面中各「挑選或修改」1 個最優先執行的行動項目。")
        
        act_1 = st.text_input("1. 計畫治理 (Plan Governance)", placeholder="請輸入選定的計畫治理行動項目")
        act_2 = st.text_input("2. 人才培育 (Talent Cultivation)", placeholder="請輸入選定的人才培育行動項目")
        act_3 = st.text_input("3. 主題共融 (Theme Integration)", placeholder="請輸入選定的主題共融行動項目")
        act_4 = st.text_input("4. 夥伴關係 (Partnership)", placeholder="請輸入選定的夥伴關係行動項目")
        
        if st.button("下一步：設計 KPI 與影響力帳戶"):
            if all([act_1, act_2, act_3, act_4]):
                st.session_state.selected_actions = {
                    "計畫治理": act_1,
                    "人才培育": act_2,
                    "主題共融": act_3,
                    "夥伴關係": act_4
                }
                
                system_prompt = "你現在要協助學校啟動計畫的「影響力帳戶」。請為使用者選定的行動項目，設計可量化的關鍵績效指標（KPI）。"
                user_prompt = f"""
                我們選定的行動項目如下：
                1. 計畫治理：{act_1}
                2. 人才培育：{act_2}
                3. 主題共融：{act_3}
                4. 夥伴關係：{act_4}
                請為上述 4 個行動項目，分別設計 2 個「具體、可衡量」的目標值（KPI），讓我們能透過形成性歷程的評估來時時存入影響力。
                """
                st.session_state.step2_result = call_openai(system_prompt, user_prompt)
                st.session_state.step = 3
                st.rerun()
            else:
                st.warning("請完成四個構面的行動項目填寫。")

# ==========================================
# 步驟三：落實「行為數據化」
# ==========================================
elif st.session_state.step == 3:
    st.header("步驟三：落實「行為數據化」")
    
    st.subheader("📊 我們的關鍵績效指標 (KPI)")
    st.markdown(st.session_state.step2_result)
    
    st.markdown("為達成上述 KPI，我們需要將日常工作轉化為『行為數據化』的資料工作。")
    
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("生成數據蒐集建議", type="primary"):
            system_prompt = "你的任務是將校務管理的 KPI，轉化為第一線教師與行政人員可以落實的「行為數據化」操作建議。"
            user_prompt = f"""
            我們的目標 KPI 是：
            {st.session_state.step2_result}
            
            請問在高中校園的日常運作中，各處室可以透過哪些既有的系統（如：刷卡機、數位學習平臺後台、電子簽到表、線上報修系統等）來蒐集對應的客觀數據，以取代傳統的主觀感受？
            請為每個 KPI 給出 1 個最容易執行的資料蒐集方法。
            """
            st.session_state.step3_result = call_openai(system_prompt, user_prompt)
            st.session_state.step = 4
            st.rerun()
    with col2:
        if st.button("回上一步修改行動項目"):
            st.session_state.step = 2
            st.rerun()

# ==========================================
# 步驟四：匯出專屬計分卡
# ==========================================
elif st.session_state.step == 4:
    st.header("步驟四：專屬計分卡與落實策略統整")
    
    st.subheader("📍 最終方案統整")
    
    st.markdown("### 1. 核心願景與利害關係人")
    st.write(f"**願景**：{st.session_state.vision}")
    st.write(f"**利害關係人**：{', '.join(st.session_state.stakeholders)}")
    
    st.markdown("### 2. 四大構面行動項目與 KPI")
    st.markdown(st.session_state.step2_result)
    
    st.markdown("### 3. 行為數據化落實方案")
    st.markdown(st.session_state.step3_result)
    
    st.markdown("---")
    
    # 建立統整表格以供匯出
    export_data = []
    for dimension, action in st.session_state.selected_actions.items():
        export_data.append({
            "構面": dimension,
            "行動項目": action,
            "願景對齊": st.session_state.vision
        })
    df_export = pd.DataFrame(export_data)
    
    st.subheader("📥 匯出計分卡資料")
    st.markdown("您可以將資料匯出為表格 (CSV) 帶入會議討論，或下載完整文字報告 (TXT) 貼入計畫書中。")
    
    # 使用欄位排版並排顯示兩顆下載按鈕
    col1, col2 = st.columns(2)
    
    with col1:
        # 1. 原始的 CSV 下載
        csv = df_export.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label="📊 下載計分卡行動清單 (CSV)",
            data=csv,
            file_name='能動平衡計分卡.csv',
            mime='text/csv',
            use_container_width=True
        )
        
    with col2:
        # 2. 新增的 TXT 完整報告下載
        full_report_text = f"""【能動平衡計分卡 - 完整規劃報告】

一、核心願景與利害關係人
願景：{st.session_state.vision}
利害關係人：{', '.join(st.session_state.stakeholders)}

二、四大構面行動項目與 KPI
{st.session_state.step2_result}

三、行為數據化落實方案
{st.session_state.step3_result}
"""
        st.download_button(
            label="📄 下載完整文字報告 (TXT)",
            data=full_report_text,
            file_name='能動平衡計分卡_完整報告.txt',
            mime='text/plain',
            use_container_width=True
        )
    
    st.markdown("---")
    if st.button("重新開始新計畫", type="primary"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
