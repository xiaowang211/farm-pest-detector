import streamlit as st
import requests
import base64

# 配置智谱GLM-4V API
API_KEY = "你的APIKey"  # 替换为你的智谱API Key
API_URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"

def detect_pest_and_get_method(image_bytes):
    """调用GLM-4V识别害虫+生成含具体农药的防治建议（修复编码问题）"""
    try:
        # 图片转Base64编码
        img_base64 = base64.b64encode(image_bytes).decode("utf-8")
        
        # 构造请求体（指定UTF-8编码）
        headers = {
            "Content-Type": "application/json; charset=utf-8",  # 补充UTF-8编码
            "Authorization": f"Bearer {API_KEY}"
        }
        data = {
            "model": "glm-4v",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "请先识别这张图片中的害虫名称，再给出该害虫的农业防治方法，其中化学防治部分需补充具体的低毒高效农药名称（如常用的杀虫剂型号），格式为：\n害虫名称：XXX\n防治建议：\n1. 物理防治：XXX\n2. 化学防治：XXX（具体农药名称：如氯虫苯甲酰胺、阿维菌素等）\n3. 生物防治：XXX\n4. 农艺措施：XXX\n5. 监测预警：XXX"
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{img_base64}"
                            }
                        }
                    ]
                }
            ]
        }
        
        # 发送请求时指定UTF-8编码
        response = requests.post(
            API_URL,
            headers=headers,
            json=data,
            timeout=25,
            headers={"Content-Type": "application/json; charset=utf-8"}  # 确保编码
        )
        response.raise_for_status()
        # 强制用UTF-8解析响应
        result = response.json(encoding="utf-8")
        
        # 提取结果
        content = result["choices"][0]["message"]["content"].strip()
        if "未识别" in content or content == "":
            return "未识别到害虫"
        return content
    
    except Exception as e:
        return f"处理失败：{str(e)}"

# Streamlit前端页面
st.title("农业害虫识别+防治工具")
st.write("上传害虫图片，自动识别并获取含具体农药的防治建议")

# 图片上传组件
uploaded_file = st.file_uploader("选择害虫图片（JPG/PNG）", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # 显示上传的图片
    st.image(uploaded_file, caption="上传的图片", use_column_width=True)
    
    # 识别+获取建议按钮
    if st.button("识别并获取防治建议"):
        with st.spinner("分析中，请稍候..."):
            # 读取图片字节数据
            image_bytes = uploaded_file.getvalue()
            # 调用识别+建议函数
            result = detect_pest_and_get_method(image_bytes)
            # 显示结果
            st.success("处理完成：")
            st.write(result)
