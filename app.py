import streamlit as st
import requests
import time
import json
import random

# 页面配置
st.set_page_config(
    page_title="AI智能对话平台",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def apply_light_theme():
    """应用简洁浅色主题CSS"""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
    
    /* 全局样式 */
    .stApp {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        font-family: 'Inter', sans-serif;
    }
    
    /* 主容器 */
    .main .block-container {
        padding: 2rem 1rem;
        max-width: 1200px;
        margin: 0 auto;
    }
    
    /* 标题样式 */
    .main-title {
        font-family: 'Inter', sans-serif;
        font-size: 2.5rem;
        font-weight: 700;
        text-align: center;
        margin: 2rem 0 1rem 0;
        background: linear-gradient(135deg, #3b82f6, #8b5cf6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .subtitle {
        text-align: center;
        color: #64748b;
        font-size: 1.1rem;
        margin-bottom: 2rem;
        font-weight: 400;
    }
    
    /* 卡片容器 */
    .card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        border: 1px solid #e2e8f0;
        transition: all 0.2s ease;
    }
    
    .card:hover {
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        transform: translateY(-1px);
    }
    
    /* 模型卡片 */
    .model-card {
        background: white;
        border: 2px solid #e2e8f0;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        cursor: pointer;
        transition: all 0.2s ease;
    }
    
    .model-card:hover {
        border-color: #3b82f6;
        box-shadow: 0 2px 8px rgba(59, 130, 246, 0.2);
    }
    
    .model-card.selected {
        border-color: #3b82f6;
        background: #eff6ff;
        box-shadow: 0 2px 8px rgba(59, 130, 246, 0.3);
    }
    
    .model-name {
        font-weight: 600;
        color: #1e293b;
        margin-bottom: 0.25rem;
    }
    
    .model-description {
        font-size: 0.9rem;
        color: #64748b;
        margin-bottom: 0.5rem;
    }
    
    .model-tags {
        display: flex;
        gap: 0.5rem;
        flex-wrap: wrap;
    }
    
    .model-tag {
        background: #f1f5f9;
        color: #475569;
        padding: 0.2rem 0.5rem;
        border-radius: 4px;
        font-size: 0.75rem;
        font-weight: 500;
    }
    
    .model-tag.premium {
        background: #fef3c7;
        color: #92400e;
    }
    
    .model-tag.free {
        background: #d1fae5;
        color: #065f46;
    }
    
    /* API状态 */
    .api-status {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
        padding: 0.75rem 1rem;
        border-radius: 8px;
        font-weight: 500;
        margin: 1rem 0;
        transition: all 0.2s ease;
    }
    
    .api-status.connected {
        background: #f0fdf4;
        border: 1px solid #bbf7d0;
        color: #166534;
    }
    
    .api-status.disconnected {
        background: #fef2f2;
        border: 1px solid #fecaca;
        color: #dc2626;
    }
    
    .api-status.checking {
        background: #fef9c3;
        border: 1px solid #fde047;
        color: #a16207;
    }
    
    .status-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
    }
    
    .status-dot.online {
        background: #22c55e;
        box-shadow: 0 0 0 2px rgba(34, 197, 94, 0.2);
    }
    
    .status-dot.offline {
        background: #ef4444;
        box-shadow: 0 0 0 2px rgba(239, 68, 68, 0.2);
    }
    
    .status-dot.checking {
        background: #eab308;
        box-shadow: 0 0 0 2px rgba(234, 179, 8, 0.2);
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    /* 消息样式 */
    .message-container {
        margin: 1rem 0;
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
    }
    
    .user-message {
        align-self: flex-end;
        background: linear-gradient(135deg, #3b82f6, #1d4ed8);
        color: white;
        padding: 0.75rem 1rem;
        border-radius: 18px 18px 4px 18px;
        max-width: 70%;
        font-weight: 500;
        box-shadow: 0 2px 8px rgba(59, 130, 246, 0.3);
    }
    
    .ai-message {
        align-self: flex-start;
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        color: #334155;
        padding: 0.75rem 1rem;
        border-radius: 18px 18px 18px 4px;
        max-width: 70%;
        line-height: 1.6;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    .message-time {
        font-size: 0.75rem;
        color: #94a3b8;
        margin-top: 0.25rem;
    }
    
    .message-model {
        font-size: 0.7rem;
        color: #7c3aed;
        font-weight: 500;
        margin-bottom: 0.25rem;
    }
    
    /* 输入框样式 */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        border: 1px solid #d1d5db !important;
        border-radius: 8px !important;
        padding: 0.75rem !important;
        font-size: 1rem !important;
        transition: all 0.2s ease !important;
        background: white !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
    }
    
    /* 按钮样式 */
    .stButton > button {
        background: linear-gradient(135deg, #3b82f6, #1d4ed8) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.6rem 1.2rem !important;
        font-weight: 500 !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 2px 4px rgba(59, 130, 246, 0.2) !important;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #1d4ed8, #1e40af) !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 8px rgba(59, 130, 246, 0.3) !important;
    }
    
    /* 加载动画 */
    .typing-indicator {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        padding: 1rem;
        color: #64748b;
        font-style: italic;
    }
    
    .typing-dots {
        display: flex;
        gap: 4px;
    }
    
    .typing-dot {
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background: #94a3b8;
        animation: typingBounce 1.4s ease-in-out infinite;
    }
    
    .typing-dot:nth-child(1) { animation-delay: 0ms; }
    .typing-dot:nth-child(2) { animation-delay: 160ms; }
    .typing-dot:nth-child(3) { animation-delay: 320ms; }
    
    @keyframes typingBounce {
        0%, 60%, 100% { transform: translateY(0); }
        30% { transform: translateY(-10px); }
    }
    
    /* 隐藏默认元素 */
    #MainMenu, .stDeployButton, footer {
        visibility: hidden;
    }
    
    /* 响应式设计 */
    @media (max-width: 768px) {
        .main-title {
            font-size: 2rem;
        }
        
        .user-message, .ai-message {
            max-width: 90%;
        }
    }
    </style>
    """, unsafe_allow_html=True)

def initialize_chat_session():
    """初始化聊天会话"""
    if 'chat_messages' not in st.session_state:
        st.session_state.chat_messages = []
    if 'github_api_key' not in st.session_state:
        st.session_state.github_api_key = ""
    if 'available_models' not in st.session_state:
        st.session_state.available_models = []
    if 'selected_model' not in st.session_state:
        st.session_state.selected_model = "gpt-4o-mini"
    if 'models_loaded' not in st.session_state:
        st.session_state.models_loaded = False
    if 'conversation_count' not in st.session_state:
        st.session_state.conversation_count = 0

def get_available_models(api_key):
    """获取可用的AI模型列表"""
    if not api_key:
        return []
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    
    try:
        response = requests.get(
            "https://models.inference.ai.azure.com/models",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            models_data = response.json()
            models = []
            
            # 处理返回的模型数据
            if isinstance(models_data, dict) and 'data' in models_data:
                for model in models_data['data']:
                    models.append({
                        'id': model.get('id', ''),
                        'name': model.get('id', '').replace('-', ' ').title(),
                        'description': get_model_description(model.get('id', '')),
                        'tags': get_model_tags(model.get('id', ''))
                    })
            else:
                # 如果API返回格式不同，使用预定义的模型列表
                models = get_default_models()
            
            return models
        else:
            # API调用失败时返回默认模型
            return get_default_models()
            
    except Exception as e:
        # 网络错误或其他异常时返回默认模型
        return get_default_models()

def get_default_models():
    """获取默认模型列表"""
    return [
        {
            'id': 'gpt-4o',
            'name': 'GPT-4o',
            'description': '最新的GPT-4 Omni模型，多模态能力强，理解和生成质量极高',
            'tags': ['多模态', '最新', '高质量']
        },
        {
            'id': 'gpt-4o-mini',
            'name': 'GPT-4o Mini',
            'description': '轻量化版本的GPT-4o，速度快，成本低，适合日常对话',
            'tags': ['快速', '经济', '推荐']
        },
        {
            'id': 'gpt-4-turbo',
            'name': 'GPT-4 Turbo',
            'description': '增强版GPT-4，处理能力强，支持更长的上下文',
            'tags': ['长上下文', '强大', '稳定']
        },
        {
            'id': 'gpt-3.5-turbo',
            'name': 'GPT-3.5 Turbo',
            'description': '经典模型，平衡性能和成本，适合大多数应用场景',
            'tags': ['经典', '平衡', '可靠']
        }
    ]

def get_model_description(model_id):
    """根据模型ID获取描述"""
    descriptions = {
        'gpt-4o': '最新的GPT-4 Omni模型，多模态能力强，理解和生成质量极高',
        'gpt-4o-mini': '轻量化版本的GPT-4o，速度快，成本低，适合日常对话',
        'gpt-4-turbo': '增强版GPT-4，处理能力强，支持更长的上下文',
        'gpt-3.5-turbo': '经典模型，平衡性能和成本，适合大多数应用场景',
        'claude-3': '人类价值观对齐的AI助手，擅长分析和创作',
        'gemini-pro': '谷歌的大型语言模型，多语言支持良好'
    }
    return descriptions.get(model_id, '智能AI语言模型')

def get_model_tags(model_id):
    """根据模型ID获取标签"""
    tags_map = {
        'gpt-4o': ['多模态', '最新', '高质量'],
        'gpt-4o-mini': ['快速', '经济', '推荐'],
        'gpt-4-turbo': ['长上下文', '强大', '稳定'],
        'gpt-3.5-turbo': ['经典', '平衡', '可靠'],
        'claude-3': ['安全', '创作', '分析'],
        'gemini-pro': ['多语言', '谷歌', '创新']
    }
    return tags_map.get(model_id, ['AI模型'])

def test_model_availability(api_key, model_id):
    """测试特定模型是否可用"""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    
    payload = {
        "messages": [{"role": "user", "content": "测试"}],
        "model": model_id,
        "max_tokens": 10
    }
    
    try:
        response = requests.post(
            "https://models.inference.ai.azure.com/chat/completions",
            headers=headers,
            json=payload,
            timeout=5
        )
        return response.status_code == 200
    except:
        return False

def get_system_prompt():
    """获取系统提示词"""
    current_time = "2025-08-08 09:42:27"
    current_user = "Kikyo-acd"
    
    return f"""
你是一个友好、专业的AI助手，具备以下特点：
- 回答准确、有帮助
- 语言表达清晰易懂
- 能够处理各种类型的问题
- 保持礼貌和专业的态度
- 总是用中文回复

当前用户：{current_user}
当前时间：{current_time} (UTC)

请根据用户的问题提供最有价值的回答。
"""

def call_ai_api(user_message, model_id, api_key):
    """调用AI API进行对话"""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    messages = [
        {"role": "system", "content": get_system_prompt()}
    ]

    # 添加聊天历史
    if len(st.session_state.chat_messages) > 0:
        recent_messages = st.session_state.chat_messages[-10:]
        for msg in recent_messages:
            if 'model' not in msg or msg['model'] == model_id:  # 只添加相同模型的历史
                messages.append({
                    "role": msg['role'],
                    "content": msg['content']
                })

    messages.append({"role": "user", "content": user_message})

    payload = {
        "messages": messages,
        "model": model_id,
        "max_tokens": 2000,
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
            return ai_response, True
        elif response.status_code == 401:
            return "API认证失败，请检查密钥是否正确", False
        elif response.status_code == 429:
            return "请求过于频繁，请稍后再试", False
        elif response.status_code == 404:
            return f"模型 {model_id} 不可用或不存在", False
        else:
            return f"API调用失败：{response.status_code}", False

    except Exception as e:
        return f"连接错误：{str(e)[:100]}", False

def render_header():
    """渲染页面头部"""
    st.markdown("""
    <div class="main-title">🤖 AI智能对话平台</div>
    <div class="subtitle">支持多种AI模型，智能选择最适合的对话体验</div>
    """, unsafe_allow_html=True)

def render_api_config():
    """渲染API配置区域"""
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("#### 🔧 API配置")
    
    api_key_input = st.text_input(
        "GitHub Models API密钥",
        value=st.session_state.github_api_key,
        type="password",
        placeholder="请输入您的API密钥",
        help="获取密钥：https://github.com/settings/tokens"
    )

    if api_key_input != st.session_state.github_api_key:
        st.session_state.github_api_key = api_key_input
        st.session_state.models_loaded = False  # 重置模型加载状态

    # API状态显示
    if st.session_state.github_api_key:
        if not st.session_state.models_loaded:
            st.markdown(f"""
            <div class="api-status checking">
                <div class="status-dot checking"></div>
                <span>正在检测可用模型...</span>
            </div>
            """, unsafe_allow_html=True)
            
            # 异步加载模型
            with st.spinner("正在获取可用模型列表..."):
                models = get_available_models(st.session_state.github_api_key)
                st.session_state.available_models = models
                st.session_state.models_loaded = True
                st.rerun()
        else:
            model_count = len(st.session_state.available_models)
            st.markdown(f"""
            <div class="api-status connected">
                <div class="status-dot online"></div>
                <span>已连接 - 发现 {model_count} 个可用模型</span>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="api-status disconnected">
            <div class="status-dot offline"></div>
            <span>未连接 - 请输入API密钥</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_model_selector():
    """渲染模型选择器"""
    if st.session_state.available_models:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("#### 🎯 选择AI模型")
        
        # 显示当前选择的模型
        current_model = next((m for m in st.session_state.available_models 
                            if m['id'] == st.session_state.selected_model), None)
        if current_model:
            st.info(f"当前使用：**{current_model['name']}** - {current_model['description']}")
        
        # 模型网格显示
        cols = st.columns(2)
        for i, model in enumerate(st.session_state.available_models):
            with cols[i % 2]:
                is_selected = model['id'] == st.session_state.selected_model
                
                # 构建标签HTML
                tags_html = ""
                for tag in model['tags']:
                    tag_class = "premium" if tag in ['最新', '高质量'] else "free" if tag in ['推荐', '经济'] else ""
                    tags_html += f'<span class="model-tag {tag_class}">{tag}</span>'
                
                # 模型卡片
                card_class = "model-card selected" if is_selected else "model-card"
                st.markdown(f"""
                <div class="{card_class}" onclick="">
                    <div class="model-name">{model['name']}</div>
                    <div class="model-description">{model['description']}</div>
                    <div class="model-tags">{tags_html}</div>
                </div>
                """, unsafe_allow_html=True)
                
                # 选择按钮
                if st.button(f"选择 {model['name']}", key=f"select_{model['id']}", 
                           disabled=is_selected, use_container_width=True):
                    st.session_state.selected_model = model['id']
                    st.success(f"已切换到 {model['name']}")
                    st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

def render_chat_history():
    """渲染聊天历史"""
    if st.session_state.chat_messages:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("#### 💬 对话记录")
        
        # 显示最近的对话
        for msg in st.session_state.chat_messages[-10:]:
            timestamp = time.strftime("%H:%M", time.localtime(msg.get('timestamp', time.time())))
            model_used = msg.get('model', '未知模型')
            
            if msg['role'] == 'user':
                st.markdown(f"""
                <div class="message-container">
                    <div class="user-message">
                        {msg['content']}
                        <div class="message-time">{timestamp}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="message-container">
                    <div class="ai-message">
                        <div class="message-model">🤖 {model_used}</div>
                        {msg['content']}
                        <div class="message-time">{timestamp}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

def render_input_area():
    """渲染输入区域"""
    st.markdown('<div class="card">', unsafe_allow_html=True)
    
    # 显示当前选择的模型
    current_model = next((m for m in st.session_state.available_models 
                        if m['id'] == st.session_state.selected_model), None)
    if current_model:
        st.markdown(f"#### ✨ 与 **{current_model['name']}** 对话")
    else:
        st.markdown("#### ✨ 开始对话")
    
    user_input = st.text_area(
        "",
        placeholder="在这里输入您的问题或想法...",
        height=80,
        key="chat_input",
        label_visibility="collapsed"
    )

    col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
    
    with col1:
        send_disabled = not st.session_state.github_api_key or not st.session_state.available_models
        if st.button("发送消息", use_container_width=True, type="primary", disabled=send_disabled):
            if not st.session_state.github_api_key:
                st.error("请先配置API密钥")
            elif not st.session_state.available_models:
                st.error("暂无可用模型")
            elif user_input.strip():
                process_chat_message(user_input.strip())
                st.rerun()
            else:
                st.warning("请输入内容")

    with col2:
        if st.button("随机话题", use_container_width=True, disabled=send_disabled):
            if st.session_state.github_api_key and st.session_state.available_models:
                topics = [
                    "讲一个有趣的历史故事",
                    "解释一个科学概念",
                    "推荐一部电影",
                    "分享编程技巧",
                    "讨论哲学思想"
                ]
                random_topic = random.choice(topics)
                process_chat_message(random_topic)
            else:
                st.error("请先配置API密钥并选择模型")

    with col3:
        if st.button("清空记录", use_container_width=True):
            st.session_state.chat_messages = []
            st.session_state.conversation_count = 0
            st.rerun()

    with col4:
        if st.button("刷新模型", use_container_width=True):
            if st.session_state.github_api_key:
                st.session_state.models_loaded = False
                st.rerun()
            else:
                st.warning("请先输入API密钥")
    
    st.markdown('</div>', unsafe_allow_html=True)

def process_chat_message(user_message):
    """处理聊天消息"""
    if not st.session_state.github_api_key.strip():
        st.error("请先配置API密钥")
        return
    
    if not st.session_state.selected_model:
        st.error("请先选择AI模型")
        return

    # 添加用户消息
    st.session_state.chat_messages.append({
        'role': 'user',
        'content': user_message,
        'timestamp': time.time(),
        'model': st.session_state.selected_model
    })

    # 显示思考动画
    thinking_placeholder = st.empty()
    current_model_name = next((m['name'] for m in st.session_state.available_models 
                             if m['id'] == st.session_state.selected_model), 
                            st.session_state.selected_model)
    
    with thinking_placeholder:
        st.markdown(f"""
        <div class="typing-indicator">
            <span>{current_model_name} 正在思考</span>
            <div class="typing-dots">
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # 获取AI响应
    ai_response, success = call_ai_api(
        user_message, st.session_state.selected_model, st.session_state.github_api_key
    )

    thinking_placeholder.empty()

    # 添加AI响应
    st.session_state.chat_messages.append({
        'role': 'assistant',
        'content': ai_response,
        'timestamp': time.time(),
        'model': current_model_name
    })

    # 更新统计
    st.session_state.conversation_count += 1

    if success:
        st.success(f"{current_model_name} 回复已生成")
    else:
        st.error(f"{current_model_name} 生成失败")
    
    st.rerun()

def main():
    """主程序"""
    # 应用样式
    apply_light_theme()
    
    # 初始化
    initialize_chat_session()
    
    # 渲染界面
    render_header()
    render_api_config()
    render_model_selector()
    render_chat_history()
    render_input_area()
    
    # 页脚
    st.markdown("""
    <div style="text-align: center; margin-top: 2rem; padding: 1rem; color: #94a3b8; font-size: 0.9rem;">
        <p>🤖 AI智能对话平台 - 多模型支持，智能切换</p>
        <p>当前用户：Kikyo-acd | 时间：2025-08-08 09:42:27 UTC</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
