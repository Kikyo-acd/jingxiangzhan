import streamlit as st
import openai
import requests
import json
import time
import pandas as pd
import plotly.express as px
from datetime import datetime
import tiktoken
import os
from typing import List, Dict, Optional
import streamlit as st
import requests
import json
import time

# 页面配置
st.set_page_config(
    page_title="AI Chat 镜像站",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS样式
st.markdown("""
<style>
.main-header {
    font-size: 3rem;
    font-weight: bold;
    text-align: center;
    background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 2rem;
}

.feature-card {
    background: #f0f2f6;
    padding: 1rem;
    border-radius: 0.5rem;
    margin: 0.5rem 0;
    border-left: 4px solid #4ECDC4;
}

.status-good {
    color: #28a745;
    font-weight: bold;
}

.status-error {
    color: #dc3545;
    font-weight: bold;
}

.chat-message {
    padding: 1rem;
    border-radius: 0.5rem;
    margin: 0.5rem 0;
}

.user-message {
    background-color: #e3f2fd;
    border-left: 4px solid #2196f3;
}

.assistant-message {
    background-color: #f3e5f5;
    border-left: 4px solid #9c27b0;
}
</style>
""", unsafe_allow_html=True)

class AIService:
    def __init__(self):
        self.base_url = None
        self.api_key = None
        self.client = None
        self.available_models = []
        
    def initialize_client(self, api_key: str, base_url: str):
        """初始化AI客户端"""
        try:
            self.api_key = api_key
            self.base_url = base_url
            self.client = openai.OpenAI(
                api_key=api_key,
                base_url=base_url
            )
            return True
        except Exception as e:
            st.error(f"初始化客户端失败: {str(e)}")
            return False
    
    def fetch_models(self) -> List[str]:
        """获取可用模型列表"""
        try:
            if not self.client:
                return []
            
            response = self.client.models.list()
            models = [model.id for model in response.data]
            self.available_models = sorted(models)
            return self.available_models
        except Exception as e:
            st.error(f"获取模型列表失败: {str(e)}")
            return []
    
    def test_connection(self) -> bool:
        """测试连接状态"""
        try:
            if not self.client:
                return False
            
            # 尝试获取模型列表来测试连接
            self.client.models.list()
            return True
        except Exception as e:
            st.error(f"连接测试失败: {str(e)}")
            return False
    
    def chat_completion(self, messages: List[Dict], model: str, **kwargs) -> Optional[str]:
        """发送聊天请求"""
        try:
            if not self.client:
                return None
            
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                **kwargs
            )
            return response.choices[0].message.content
        except Exception as e:
            st.error(f"聊天请求失败: {str(e)}")
            return None

def count_tokens(text: str, model: str = "gpt-3.5-turbo") -> int:
    """计算token数量"""
    try:
        encoding = tiktoken.encoding_for_model(model)
        return len(encoding.encode(text))
    except:
        # 如果模型不支持，使用近似计算
        return len(text.split()) * 1.3

def get_preset_prompts() -> Dict[str, str]:
    """获取预设提示词"""
    return {
        "💼 专业助手": "你是一个专业的AI助手，请用准确、清晰、有条理的方式回答问题。",
        "🎨 创意写作": "你是一个富有创意的写作助手，请帮助用户进行创意写作，包括故事、诗歌、剧本等。",
        "💻 编程专家": "你是一个资深的编程专家，精通多种编程语言，请帮助用户解决编程问题。",
        "📚 学习导师": "你是一个耐心的学习导师，请用通俗易懂的方式解释复杂概念，并提供学习建议。",
        "🌍 翻译助手": "你是一个专业的翻译助手，请准确翻译用户提供的文本，并解释语言细节。",
        "🧠 分析专家": "你是一个逻辑思维清晰的分析专家，请对用户的问题进行深入分析并提供见解。",
        "🎯 产品经理": "你是一个经验丰富的产品经理，请从产品角度分析问题并提供解决方案。",
        "📊 数据分析师": "你是一个专业的数据分析师，请帮助用户分析数据并提供洞察。"
    }

def initialize_session_state():
    """初始化会话状态"""
    if 'ai_service' not in st.session_state:
        st.session_state.ai_service = AIService()
    
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    if 'conversation_count' not in st.session_state:
        st.session_state.conversation_count = 0
    
    if 'total_tokens' not in st.session_state:
        st.session_state.total_tokens = 0
    
    if 'settings' not in st.session_state:
        st.session_state.settings = {
            'temperature': 0.7,
            'max_tokens': 2048,
            'top_p': 1.0,
            'frequency_penalty': 0.0,
            'presence_penalty': 0.0
        }

def call_github_models_api(user_message, system_prompt, api_key):
    """调用GitHub Models API进行对话 - 修正版本"""
    
    # GitHub Models API的正确端点
    url = "https://models.inference.ai.azure.com/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "User-Agent": "Chinese-Medicine-App/1.0"
    }

    # 构建对话消息
    messages = [
        {"role": "system", "content": system_prompt}
    ]
    
    # 添加聊天历史上下文（最近3轮对话）
    if len(st.session_state.chat_messages) > 0:
        recent_messages = st.session_state.chat_messages[-6:]  # 最近3轮对话
        for msg in recent_messages:
            messages.append({
                "role": msg['role'],
                "content": msg['content']
            })
    
    # 添加当前用户消息
    messages.append({"role": "user", "content": user_message})

    payload = {
        "messages": messages,
        "model": "gpt-4o-mini",  # GitHub Models支持的模型
        "max_tokens": 1500,
        "temperature": 0.7,
        "top_p": 0.95,
        "frequency_penalty": 0,
        "presence_penalty": 0
    }

    try:
        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=30
        )
        
        # 详细的错误处理
        if response.status_code == 200:
            result = response.json()
            if 'choices' in result and len(result['choices']) > 0:
                ai_response = result['choices'][0]['message']['content']
                return f"🤖 **GitHub Copilot助手：**\n\n{ai_response}"
            else:
                return "❌ **响应格式错误**：API返回数据格式不正确"
                
        elif response.status_code == 401:
            return "❌ **认证失败**：GitHub API密钥无效或已过期。请检查您的API密钥是否正确。"
            
        elif response.status_code == 403:
            return "❌ **权限不足**：API密钥没有访问GitHub Models的权限。请检查您的订阅状态。"
            
        elif response.status_code == 429:
            return "⏰ **请求限制**：请求过于频繁，请稍后再试。"
            
        elif response.status_code == 400:
            try:
                error_detail = response.json()
                return f"❌ **请求错误**：{error_detail.get('error', {}).get('message', '请求格式不正确')}"
            except:
                return f"❌ **请求错误**：{response.text[:200]}"
                
        elif response.status_code == 500:
            return "❌ **服务器错误**：GitHub Models服务暂时不可用，请稍后重试。"
            
        else:
            return f"❌ **未知错误**：状态码 {response.status_code}\n错误信息：{response.text[:300]}"

    except requests.exceptions.Timeout:
        return "⏰ **请求超时**：网络连接超时，请检查网络连接后重试。"
        
    except requests.exceptions.ConnectionError:
        return "🔌 **连接错误**：无法连接到GitHub Models API，请检查网络连接。"
        
    except requests.exceptions.RequestException as e:
        return f"❌ **网络错误**：{str(e)[:200]}"
        
    except Exception as e:
        return f"❌ **未知错误**：{str(e)[:200]}"

def test_github_api_connection(api_key):
    """测试GitHub API连接"""
    if not api_key.strip():
        return False, "API密钥为空"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # 使用简单的测试请求
    test_payload = {
        "messages": [{"role": "user", "content": "Hello"}],
        "model": "gpt-4o-mini",
        "max_tokens": 10
    }
    
    try:
        response = requests.post(
            "https://models.inference.ai.azure.com/chat/completions",
            headers=headers,
            json=test_payload,
            timeout=10
        )
        
        if response.status_code == 200:
            return True, "连接成功"
        elif response.status_code == 401:
            return False, "API密钥无效"
        elif response.status_code == 403:
            return False, "权限不足"
        else:
            return False, f"连接失败：{response.status_code}"
            
    except Exception as e:
        return False, f"连接测试失败：{str(e)[:100]}"

def render_chat_interface():
    """渲染聊天界面 - 修正版本"""
    with st.sidebar:
        st.markdown("---")
        with st.expander("🤖 GitHub Copilot助手", expanded=False):
            # API密钥输入和测试
            st.write("**🔑 GitHub API配置：**")
            api_key_input = st.text_input(
                "GitHub Models API密钥",
                value=st.session_state.get('github_api_key', ''),
                type="password",
                placeholder="ghp_xxxxxxxxxxxxxxxxxxxx",
                help="请输入您的GitHub Models API密钥"
            )

            if api_key_input != st.session_state.get('github_api_key', ''):
                st.session_state.github_api_key = api_key_input

            # API连接测试按钮
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🔍 测试连接", use_container_width=True):
                    if st.session_state.get('github_api_key'):
                        with st.spinner("测试中..."):
                            success, message = test_github_api_connection(st.session_state.github_api_key)
                            if success:
                                st.success(f"✅ {message}")
                            else:
                                st.error(f"❌ {message}")
                    else:
                        st.error("请先输入API密钥")

            with col2:
                # API状态显示
                if st.session_state.get('github_api_key'):
                    st.success("✅ 密钥已输入")
                else:
                    st.warning("⚠️ 请输入密钥")

            # 使用说明
            with st.expander("📖 API密钥获取说明"):
                st.markdown("""
                **获取GitHub Models API密钥：**
                
                1. 访问 [GitHub Settings](https://github.com/settings/tokens)
                2. 点击 "Generate new token" → "Generate new token (classic)"
                3. 选择权限范围，至少需要 `repo` 权限
                4. 生成并复制token（格式：ghp_xxxxxx）
                5. 确保您的账户有GitHub Models访问权限
                
                **注意：** API密钥只在当前会话有效，请妥善保管。
                """)

            # 快速问题按钮
            st.write("**💡 快速咨询：**")
            suggestions = get_smart_suggestions()

            for suggestion in suggestions[:3]:
                if st.button(suggestion, key=f"suggest_{hash(suggestion)}", use_container_width=True):
                    if st.session_state.get('github_api_key'):
                        process_chat_message(suggestion)
                    else:
                        st.error("请先输入并测试GitHub API密钥")

            # 自定义输入
            st.write("**💬 自定义问题：**")
            user_input = st.text_area(
                "",
                placeholder="输入您的问题...\n例如：优化失败怎么办？",
                height=80,
                key="chat_input"
            )

            if st.button("📤 发送", key="send_chat", use_container_width=True, type="primary"):
                if not st.session_state.get('github_api_key'):
                    st.error("请先输入GitHub API密钥")
                elif user_input.strip():
                    process_chat_message(user_input.strip())
                else:
                    st.warning("请输入问题内容")

            # 对话历史
            if st.session_state.get('chat_messages'):
                st.write("**📝 最近对话：**")
                recent_messages = st.session_state.chat_messages[-4:]
                for msg in recent_messages:
                    if msg['role'] == 'user':
                        st.markdown(f"**🙋 您：** {msg['content'][:50]}...")
                    else:
                        # 只显示回复的前50个字符
                        content_preview = msg['content'].replace('🤖 **GitHub Copilot助手：**\n\n', '')[:50]
                        st.markdown(f"**🤖 助手：** {content_preview}...")

                if st.button("🗑️ 清空对话", key="clear_chat"):
                    st.session_state.chat_messages = []
                    st.rerun()


def process_chat_message(user_message):
    """处理聊天消息 - 修正版本"""
    # 检查API密钥
    if not st.session_state.get('github_api_key', '').strip():
        st.error("请先在侧边栏输入您的GitHub API密钥")
        return

    # 添加用户消息
    if 'chat_messages' not in st.session_state:
        st.session_state.chat_messages = []
        
    st.session_state.chat_messages.append({
        'role': 'user',
        'content': user_message,
        'timestamp': time.time()
    })

    # 获取响应
    with st.spinner('🤖 GitHub Copilot思考中...'):
        system_prompt = get_system_prompt()
        
        # 使用修正后的API调用
        ai_response = call_github_models_api(
            user_message, 
            system_prompt, 
            st.session_state.github_api_key
        )

        # 如果GitHub API调用失败，使用本地智能响应作为备用
        if "❌" in ai_response:
            ai_response += f"\n\n---\n\n**💡 本地建议：**\n\n{get_contextual_response(user_message)}"

    # 添加AI响应
    st.session_state.chat_messages.append({
        'role': 'assistant',
        'content': ai_response,
        'timestamp': time.time()
    })

    # 显示最新回复
    st.success("✅ 回复已生成！")

    # 自动展开聊天框显示结果
    with st.expander("💬 最新回复", expanded=True):
        st.markdown(ai_response)



def main():
    initialize_session_state()
    
    # 主标题
    st.markdown('<h1 class="main-header">🤖 AI Chat 镜像站</h1>', unsafe_allow_html=True)
    
    # 侧边栏配置
    with st.sidebar:
        st.header("⚙️ 配置设置")
        
        # API配置
        st.subheader("🔑 API 配置")
        api_key = st.text_input("API Key", type="password", value="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")
        base_url = st.text_input("Base URL", value="https://api.openai.com/v1")
        
        if st.button("🔄 连接测试"):
            if api_key and base_url:
                with st.spinner("正在测试连接..."):
                    if st.session_state.ai_service.initialize_client(api_key, base_url):
                        if st.session_state.ai_service.test_connection():
                            st.success("✅ 连接成功！")
                            # 获取模型列表
                            models = st.session_state.ai_service.fetch_models()
                            if models:
                                st.success(f"✅ 获取到 {len(models)} 个可用模型")
                        else:
                            st.error("❌ 连接失败")
            else:
                st.warning("⚠️ 请填写API Key和Base URL")
        
        # 模型选择
        st.subheader("🎯 模型选择")
        if st.session_state.ai_service.available_models:
            selected_model = st.selectbox(
                "选择模型",
                st.session_state.ai_service.available_models,
                index=0 if st.session_state.ai_service.available_models else None
            )
        else:
            selected_model = st.text_input("模型名称", value="gpt-3.5-turbo")
            if st.button("🔄 刷新模型列表"):
                if st.session_state.ai_service.client:
                    models = st.session_state.ai_service.fetch_models()
                    if models:
                        st.rerun()
        
        # 高级设置
        st.subheader("🛠️ 高级设置")
        with st.expander("参数调节"):
            st.session_state.settings['temperature'] = st.slider(
                "Temperature (创造性)", 0.0, 2.0, 
                st.session_state.settings['temperature'], 0.1
            )
            st.session_state.settings['max_tokens'] = st.slider(
                "Max Tokens", 1, 4096, 
                st.session_state.settings['max_tokens']
            )
            st.session_state.settings['top_p'] = st.slider(
                "Top P", 0.0, 1.0, 
                st.session_state.settings['top_p'], 0.1
            )
            st.session_state.settings['frequency_penalty'] = st.slider(
                "Frequency Penalty", -2.0, 2.0, 
                st.session_state.settings['frequency_penalty'], 0.1
            )
            st.session_state.settings['presence_penalty'] = st.slider(
                "Presence Penalty", -2.0, 2.0, 
                st.session_state.settings['presence_penalty'], 0.1
            )
        
        # 统计信息
        st.subheader("📊 使用统计")
        st.metric("对话次数", st.session_state.conversation_count)
        st.metric("总Token数", st.session_state.total_tokens)
        
        # 操作按钮
        st.subheader("🔧 操作")
        if st.button("🗑️ 清空对话历史"):
            st.session_state.chat_history = []
            st.session_state.conversation_count = 0
            st.session_state.total_tokens = 0
            st.rerun()
        
        if st.button("💾 导出对话"):
            if st.session_state.chat_history:
                export_data = {
                    "timestamp": datetime.now().isoformat(),
                    "conversation_count": st.session_state.conversation_count,
                    "total_tokens": st.session_state.total_tokens,
                    "chat_history": st.session_state.chat_history
                }
                st.download_button(
                    "📥 下载JSON文件",
                    json.dumps(export_data, ensure_ascii=False, indent=2),
                    file_name=f"chat_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
    
    # 主要内容区域
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("💬 对话区域")
        
        # 预设提示词
        st.subheader("🎭 预设角色")
        preset_prompts = get_preset_prompts()
        
        cols = st.columns(4)
        for i, (name, prompt) in enumerate(preset_prompts.items()):
            with cols[i % 4]:
                if st.button(name, key=f"preset_{i}"):
                    # 添加系统消息
                    if not st.session_state.chat_history or st.session_state.chat_history[0]["role"] != "system":
                        st.session_state.chat_history.insert(0, {
                            "role": "system",
                            "content": prompt,
                            "timestamp": datetime.now().strftime("%H:%M:%S")
                        })
                    else:
                        st.session_state.chat_history[0]["content"] = prompt
                    st.rerun()
        
        # 自定义系统提示词
        custom_system_prompt = st.text_area(
            "🎯 自定义系统提示词",
            placeholder="输入自定义的系统提示词来定义AI的角色和行为...",
            height=100
        )
        
        if st.button("🎯 设置系统提示词") and custom_system_prompt:
            if not st.session_state.chat_history or st.session_state.chat_history[0]["role"] != "system":
                st.session_state.chat_history.insert(0, {
                    "role": "system",
                    "content": custom_system_prompt,
                    "timestamp": datetime.now().strftime("%H:%M:%S")
                })
            else:
                st.session_state.chat_history[0]["content"] = custom_system_prompt
            st.success("✅ 系统提示词已设置")
        
        # 显示对话历史
        st.subheader("📝 对话历史")
        chat_container = st.container()
        
        with chat_container:
            for i, message in enumerate(st.session_state.chat_history):
                if message["role"] == "system":
                    with st.expander(f"🎯 系统提示词 ({message.get('timestamp', '')})"):
                        st.write(message["content"])
                elif message["role"] == "user":
                    st.markdown(f"""
                    <div class="chat-message user-message">
                        <strong>👤 用户 ({message.get('timestamp', '')}):</strong><br>
                        {message["content"]}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="chat-message assistant-message">
                        <strong>🤖 助手 ({message.get('timestamp', '')}):</strong><br>
                        {message["content"]}
                    </div>
                    """, unsafe_allow_html=True)
        
        # 用户输入
        st.subheader("💭 发送消息")
        
        # 多种输入方式
        input_method = st.radio("输入方式", ["💬 普通输入", "📝 多行输入", "🎤 语音输入(暂未实现)"], horizontal=True)
        
        user_input = ""
        if input_method == "💬 普通输入":
            user_input = st.text_input("输入您的消息:", key="user_input_text")
        elif input_method == "📝 多行输入":
            user_input = st.text_area("输入您的消息:", height=150, key="user_input_area")
        
        # 快速提示词
        st.write("🚀 快速提示词:")
        quick_prompts = [
            "请总结一下我们的对话",
            "请给我一些建议",
            "请详细解释这个概念",
            "请举个例子说明",
            "请列出要点",
            "请换个角度分析"
        ]
        
        cols = st.columns(3)
        for i, prompt in enumerate(quick_prompts):
            with cols[i % 3]:
                if st.button(prompt, key=f"quick_{i}"):
                    user_input = prompt
        
        # 发送按钮
        col_send, col_clear = st.columns([1, 1])
        with col_send:
            send_clicked = st.button("🚀 发送消息", type="primary")
        with col_clear:
            if st.button("🧹 清空输入"):
                st.rerun()
        
        # 处理发送消息
        if send_clicked and user_input and st.session_state.ai_service.client:
            # 添加用户消息
            st.session_state.chat_history.append({
                "role": "user",
                "content": user_input,
                "timestamp": datetime.now().strftime("%H:%M:%S")
            })
            
            # 准备发送给AI的消息
            messages_for_ai = [msg for msg in st.session_state.chat_history if msg["role"] in ["system", "user", "assistant"]]
            messages_for_ai = [{"role": msg["role"], "content": msg["content"]} for msg in messages_for_ai]
            
            # 发送请求
            with st.spinner("🤖 AI正在思考中..."):
                response = st.session_state.ai_service.chat_completion(
                    messages=messages_for_ai,
                    model=selected_model,
                    **st.session_state.settings
                )
                
                if response:
                    # 添加AI回复
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": response,
                        "timestamp": datetime.now().strftime("%H:%M:%S")
                    })
                    
                    # 更新统计
                    st.session_state.conversation_count += 1
                    user_tokens = count_tokens(user_input, selected_model)
                    response_tokens = count_tokens(response, selected_model)
                    st.session_state.total_tokens += user_tokens + response_tokens
                    
                    st.rerun()
        elif send_clicked and not st.session_state.ai_service.client:
            st.error("❌ 请先配置并测试API连接")
        elif send_clicked and not user_input:
            st.warning("⚠️ 请输入消息内容")
    
    with col2:
        st.header("📊 功能面板")
        
        # 连接状态
        st.subheader("🔌 连接状态")
        if st.session_state.ai_service.client:
            st.markdown('<p class="status-good">✅ 已连接</p>', unsafe_allow_html=True)
            if st.session_state.ai_service.available_models:
                st.write(f"🎯 可用模型: {len(st.session_state.ai_service.available_models)}个")
        else:
            st.markdown('<p class="status-error">❌ 未连接</p>', unsafe_allow_html=True)
        
        # Token使用情况图表
        if st.session_state.total_tokens > 0:
            st.subheader("📈 Token使用趋势")
            # 简单的使用统计（这里可以扩展为更详细的图表）
            fig = px.pie(
                values=[st.session_state.total_tokens, max(10000 - st.session_state.total_tokens, 0)],
                names=['已使用', '剩余'],
                title="Token使用情况"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # 模型信息
        st.subheader("🤖 当前模型")
        if 'selected_model' in locals():
            st.info(f"📱 **模型**: {selected_model}")
            st.info(f"🌡️ **Temperature**: {st.session_state.settings['temperature']}")
            st.info(f"📏 **Max Tokens**: {st.session_state.settings['max_tokens']}")
        
        # 实用工具
        st.subheader("🛠️ 实用工具")
        
        with st.expander("📊 对话分析"):
            if st.session_state.chat_history:
                user_messages = len([msg for msg in st.session_state.chat_history if msg["role"] == "user"])
                assistant_messages = len([msg for msg in st.session_state.chat_history if msg["role"] == "assistant"])
                
                st.write(f"👤 用户消息: {user_messages}")
                st.write(f"🤖 助手回复: {assistant_messages}")
                st.write(f"💬 总消息数: {len(st.session_state.chat_history)}")
                
                # 字符统计
                total_chars = sum(len(msg["content"]) for msg in st.session_state.chat_history)
                st.write(f"📝 总字符数: {total_chars}")
        
        with st.expander("🎨 主题设置"):
            theme = st.selectbox("选择主题", ["默认", "深色", "浅色"])
            if theme != "默认":
                st.info("主题功能开发中...")
        
        with st.expander("📋 快捷操作"):
            if st.button("📋 复制最后回复"):
                if st.session_state.chat_history:
                    last_assistant_msg = None
                    for msg in reversed(st.session_state.chat_history):
                        if msg["role"] == "assistant":
                            last_assistant_msg = msg["content"]
                            break
                    if last_assistant_msg:
                        st.code(last_assistant_msg)
                        st.success("✅ 内容已显示，可手动复制")
            
            if st.button("🔄 重新生成回复"):
                if (st.session_state.chat_history and 
                    st.session_state.chat_history[-1]["role"] == "assistant"):
                    # 移除最后的助手回复
                    st.session_state.chat_history.pop()
                    st.success("✅ 已移除最后回复，请重新发送消息")
        
        # 系统信息
        st.subheader("ℹ️ 系统信息")
        st.write(f"🕒 当前时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        st.write(f"🏷️ 版本: v1.0.0")
        st.write(f"⚡ Streamlit: {st.__version__}")

if __name__ == "__main__":
    main()
