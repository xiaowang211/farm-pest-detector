import streamlit as st
import requests
import base64

# --------------------------
# 配置：替换为你的EasyDL API信息
# --------------------------
API_KEY = "ckxBJ2J8BEagLwGlwmZQCBql"
SECRET_KEY = "oxcUuf4sjnpGBaTFDSGWS7eOxjuPlKOi"
API_URL = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/classification/pest_recognition_v2"

# --------------------------
# 页面基础设置
# --------------------------
st.set_page_config(
    page_title="田间害虫识别工具",
    page_icon="🌾",
    layout="centered"
)

st.title("🌾 田间害虫识别工具")
st.write("上传一张清晰的害虫照片，即可快速识别种类并获取防治建议！")

# --------------------------
# 核心功能函数
# --------------------------
def get_access_token():
    """获取百度鉴权Token"""
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {
        "grant_type": "client_credentials",
        "client_id": API_KEY,
        "client_secret": SECRET_KEY
    }
    try:
        response = requests.post(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json().get("access_token")
    except Exception as e:
        st.error(f"获取Token失败：{str(e)}")
        return None

def detect_pest(image_bytes):
    """调用害虫识别API"""
    access_token = get_access_token()
    if not access_token:
        return None
    
    img_base64 = base64.b64encode(image_bytes).decode("utf-8")
    headers = {"Content-Type": "application/json"}
    data = {
        "image": img_base64,
        "threshold": 0.5
    }
    request_url = f"{API_URL}?access_token={access_token}"
    
    try:
        response = requests.post(request_url, headers=headers, json=data, timeout=15)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"识别请求失败：{str(e)}")
        return None

# --------------------------
# 防治建议库（可根据需要扩展）
# --------------------------
pest_control_advice = {
    "菜青虫": "可使用Bt乳剂、氯虫苯甲酰胺等药剂喷雾，也可人工捕捉幼虫。",
    "蚜虫": "可使用吡虫啉、啶虫脒等药剂，或释放瓢虫等天敌生物防治。",
    "红蜘蛛": "可使用螺螨酯、乙螨唑等杀螨剂，注意叶片背面的喷雾覆盖。",
    "稻飞虱": "可使用吡蚜酮、噻虫嗪等药剂，重点喷洒稻株中下部。"
}

# --------------------------
# 界面交互逻辑
# --------------------------
uploaded_file = st.file_uploader("📸 选择害虫图片（支持JPG/PNG）", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # 显示上传的图片
    st.image(uploaded_file, caption="上传的图片", use_column_width=True)
    
    # 调用识别接口
    with st.spinner("🔍 正在识别中，请稍候..."):
        image_bytes = uploaded_file.getvalue()
        result = detect_pest(image_bytes)
    
    # 展示识别结果
    if result and "result" in result and len(result["result"]) > 0:
        pest_info = result["result"][0]
        pest_name = pest_info["name"]
        confidence = pest_info["score"]
        
        st.success(f"✅ 识别结果：**{pest_name}**")
        st.write(f"置信度：{confidence:.2f}")
        
        # 显示防治建议
        if pest_name in pest_control_advice:
            st.info(f"💡 防治建议：{pest_control_advice[pest_name]}")
        else:
            st.info(f"💡 防治建议：请咨询当地农技人员获取针对{pest_name}的具体方案。")
    else:
        st.warning("⚠️ 未识别到害虫，请上传一张更清晰、主体更突出的图片重试。")

# --------------------------
# 底部提示
# --------------------------
st.markdown("---")
st.caption("💡 使用提示：请在光线充足的环境下拍摄，确保害虫主体清晰，避免模糊或大面积遮挡。")