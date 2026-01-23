import requests
import base64

# 配置你的 API Key
API_KEY = "cbbae83471e146a3af7fb551a9603d70.xOKLWyeE9RgAzH1Z"
API_URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"

def detect_pest(image_bytes):
    """
    调用大模型识别害虫
    :param image_bytes: 图片的字节数据
    :return: 识别结果（害虫名称）或 None
    """
    try:
        # 将图片转为 Base64
        img_base64 = base64.b64encode(image_bytes).decode("utf-8")
        
        # 构造请求体
        headers = {
            "Content-Type": "application/json",
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
                            "text": "请识别这张图片中的害虫名称，只返回名称，不要其他描述。"
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
        
        # 发送请求
        response = requests.post(API_URL, headers=headers, json=data, timeout=15)
        response.raise_for_status()
        result = response.json()
        
        # 提取识别结果
        pest_name = result["choices"][0]["message"]["content"].strip()
        return pest_name if pest_name else None
    
    except Exception as e:
        print(f"识别失败：{str(e)}")
        return None
