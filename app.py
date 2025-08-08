import streamlit as st
import requests
import time
import json

# 页面配置
st.set_page_config(
    page_title="AI智能助手",
    page_icon="🤖",
    layout="wide"
)

def initialize_chat_session():
    """初始化聊天会话"""
    if 'chat_messages' not in st.session_state:
        st.session_state.chat_messages = []
    if 'github_api_key' not in st.session_state:
        st.session_state.github_api_key = ""

def get_system_prompt():
    """获取系统提示词"""
    return """
你是中药多组分智能均化软件的专业AI助手。请用中文回答用户问题。

## 软件核心功能：
1. **数据管理**：Excel/CSV上传，自动清洗，单位转换(百分比↔mg/g)
2. **智能评分**：
   - 规则评分：基于VIP权重(甘草苷1.01558，甘草酸1.05139)
   - ML评分：LightGBM回归模型，1-10分制
3. **双优化引擎**：
   - SLSQP：单目标快速优化(质量/成本)
   - NSGA-II：多目标进化，帕累托前沿解集
4. **约束系统**：
   - 甘草模式：甘草苷≥4.5mg/g，甘草酸≥18mg/g，相似度≥0.9
   - 通用模式：用户自定义约束
5. **可视化**：质量分布、成分分析、优化结果、帕累托前沿

## 常见问题解决：
- **上传失败**：检查文件格式、编码(建议UTF-8)、列名规范
- **列匹配错误**：确保数据列包含数值，无空值，单位一致
- **优化失败**：放宽约束、增加批次选择、检查库存设置
- **NSGA-II无解**：降低目标值、增加种群大小、检查硬约束

请根据用户具体问题提供专业、准确的指导。
"""

def call_github_models_api(user_message, system_prompt, api_key):
    """调用GitHub Models API进行对话"""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    # 构建对话消息
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message}
    ]

    # 添加聊天历史上下文（最近2轮对话）
    if len(st.session_state.chat_messages) > 0:
        recent_messages = st.session_state.chat_messages[-4:]  # 最近2轮对话
        for msg in recent_messages:
            messages.append({
                "role": msg['role'],
                "content": msg['content']
            })

    payload = {
        "messages": messages,
        "model": "gpt-4o-mini",  # 使用GitHub Models支持的模型
        "max_tokens": 1000,
        "temperature": 0.7
    }

    try:
        response = requests.post(
            "https://models.inference.ai.azure.com/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )

        if response.status_code == 200:
            result = response.json()
            ai_response = result['choices'][0]['message']['content']
            return f"🤖 **AI助手回复：**\n\n{ai_response}"
        elif response.status_code == 401:
            return "❌ **API认证失败**：请检查GitHub API密钥是否正确且有效。"
        elif response.status_code == 400:
            error_detail = response.json() if response.headers.get('content-type', '').startswith(
                'application/json') else response.text
            return f"❌ **请求格式错误**：{error_detail}"
        elif response.status_code == 429:
            return "⏰ **请求过于频繁**：请稍后再试，或升级您的API配额。"
        else:
            return f"❌ **API调用失败**：状态码 {response.status_code}\n错误信息：{response.text[:300]}"

    except requests.exceptions.Timeout:
        return "⏰ **请求超时**：网络连接较慢，请稍后重试。"
    except requests.exceptions.ConnectionError:
        return "🔌 **连接错误**：无法连接到GitHub API，请检查网络连接。"
    except Exception as e:
        return f"❌ **未知错误**：{str(e)[:200]}"

def get_contextual_response(user_message):
    """基于上下文的智能响应"""
    # 关键词匹配和上下文响应
    if any(word in user_message for word in ['上传', '文件', '数据']):
        return """
**📁 数据上传指南：**

1. **支**

