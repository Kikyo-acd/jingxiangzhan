import streamlit as st
import requests
import time
import json
import random

# 页面配置
st.set_page_config(
    page_title="AI智能对话",
    page_icon="💬",
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
    
    /* 建议按钮 */
    .suggestion-btn {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 0.75rem 1rem;
        margin: 0.25rem;
        color: #475569;
        font-size: 0.9rem;
        cursor: pointer;
        transition: all 0.2s ease;
        text-align: left;
        width: 100%;
    }
    
    .suggestion-btn:hover {
        background: #f1f5f9;
        border-color: #cbd5e1;
        transform: translateY(-1px);
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
    
    /* 二级按钮 */
    .secondary-btn {
        background: white !important;
        color: #475569 !important;
        border: 1px solid #d1d5db !important;
    }
    
    .secondary-btn:hover {
        background: #f8fafc !important;
        border-color: #9ca3af !important;
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
    
    /* 标签样式 */
    .tag {
        display: inline-block;
        background: #ede9fe;
        color: #7c3aed;
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
        font-size: 0.8rem;
        font-weight: 500;
        margin: 0.25rem 0.25rem 0.25rem 0;
    }
    
    /* 统计信息 */
    .stats-container {
        display: flex;
        justify-content: center;
        gap: 2rem;
        margin: 1rem 0;
        padding: 1rem;
        background: white;
        border-radius: 8px;
        border: 1px solid #e2e8f0;
    }
    
    .stat-item {
        text-align: center;
    }
    
    .stat-value {
        font-size: 1.5rem;
        font-weight: 700;
        color: #3b82f6;
    }
    
    .stat-label {
        font-size: 0.8rem;
        color: #64748b;
        margin-top: 0.25rem;
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
        
        .stats-container {
            flex-direction: column;
            gap: 1rem;
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
    if 'conversation_count' not in st.session_state:
        st.session_state.conversation_count = 0

def get_system_prompt():
    """获取系统提示词"""
    return """
你是一个友好、专业的AI助手，具备以下特点：
- 回答准确、有帮助
- 语言表达清晰易懂
- 能够处理各种类型的问题
- 保持礼貌和专业的态度

当前用户：Kikyo-acd
当前时间：2025-08-08 09:38:54 (UTC)

请根据用户的问题提供最有价值的回答。
"""

def call_github_models_api(user_message, system_prompt, api_key):
    """调用GitHub Models API进行对话"""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    messages = [
        {"role": "system", "content": system_prompt}
    ]

    # 添加聊天历史
    if len(st.session_state.chat_messages) > 0:
        recent_messages = st.session_state.chat_messages[-10:]
        for msg in recent_messages:
            messages.append({
                "role": msg['role'],
                "content": msg['content']
            })

    messages.append({"role": "user", "content": user_message})

    payload = {
        "messages": messages,
        "model": "gpt-4o-mini",
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
        else:
            return f"API调用失败：{response.status_code}", False

    except Exception as e:
        return f"连接错误：{str(e)[:100]}", False

def get_smart_suggestions():
    """获取智能建议"""
    suggestions = [
        "💡 解释一个有趣的科学现象",
        "📚 推荐一本值得阅读的书籍",
        "💻 教我一个编程技巧",
        "🎨 给我一些创意写作的灵感",
        "🌍 介绍一个不为人知的地理知识",
        "🔬 解释人工智能的工作原理",
        "📈 分析当前的技术趋势",
        "🎵 推荐适合工作的背景音乐",
        "🏃 给我一些健康生活的建议",
        "🤔 讲一个哲学思想实验"
    ]
    return random.sample(suggestions, 6)

def render_header():
    """渲染页面头部"""
    st.markdown("""
    <div class="main-title">AI智能对话</div>
    <div class="subtitle">简洁、优雅、高效的AI对话体验</div>
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

    # API状态显示
    status_class = "connected" if st.session_state.github_api_key else "disconnected"
    dot_class = "online" if st.session_state.github_api_key else "offline"
    status_text = "已连接" if st.session_state.github_api_key else "未连接"
    
    st.markdown(f"""
    <div class="api-status {status_class}">
        <div class="status-dot {dot_class}"></div>
        <span>API状态: {status_text}</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_suggestions():
    """渲染建议区域"""
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("#### 💡 热门话题")
    
    suggestions = get_smart_suggestions()
    cols = st.columns(2)
    
    for i, suggestion in enumerate(suggestions):
        with cols[i % 2]:
            if st.button(suggestion, key=f"suggest_{i}", use_container_width=True):
                if st.session_state.github_api_key:
                    topic = suggestion.split(" ", 1)[-1]
                    process_chat_message(topic)
                else:
                    st.error("请先配置API密钥")
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_chat_history():
    """渲染聊天历史"""
    if st.session_state.chat_messages:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("#### 💬 对话记录")
        
        # 显示最近的对话
        for msg in st.session_state.chat_messages[-10:]:
            timestamp = time.strftime("%H:%M", time.localtime(msg.get('timestamp', time.time())))
            
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
                        {msg['content']}
                        <div class="message-time">{timestamp}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

def render_input_area():
    """渲染输入区域"""
    st.markdown('<div class="card">', unsafe_allow_html=True)
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
        if st.button("发送消息", use_container_width=True, type="primary"):
            if not st.session_state.github_api_key:
                st.error("请先配置API密钥")
            elif user_input.strip():
                process_chat_message(user_input.strip())
                st.rerun()
            else:
                st.warning("请输入内容")

    with col2:
        if st.button("随机话题", use_container_width=True):
            if st.session_state.github_api_key:
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
                st.error("请先配置API密钥")

    with col3:
        if st.button("清空记录", use_container_width=True):
            st.session_state.chat_messages = []
            st.session_state.conversation_count = 0
            st.rerun()

    with col4:
        if st.button("导出记录", use_container_width=True):
            if st.session_state.chat_messages:
                export_data = "\n\n".join([
                    f"{'用户' if msg['role'] == 'user' else 'AI'}: {msg['content']}"
                    for msg in st.session_state.chat_messages
                ])
                st.download_button(
                    "下载对话记录",
                    export_data,
                    file_name=f"chat_history_{int(time.time())}.txt",
                    mime="text/plain"
                )
            else:
                st.warning("暂无对话记录")
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_stats():
    """渲染统计信息"""
    if st.session_state.conversation_count > 0:
        total_messages = len(st.session_state.chat_messages)
        user_messages = len([m for m in st.session_state.chat_messages if m['role'] == 'user'])
        ai_messages = len([m for m in st.session_state.chat_messages if m['role'] == 'assistant'])
        
        st.markdown(f"""
        <div class="stats-container">
            <div class="stat-item">
                <div class="stat-value">{st.session_state.conversation_count}</div>
                <div class="stat-label">对话轮数</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">{user_messages}</div>
                <div class="stat-label">用户消息</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">{ai_messages}</div>
                <div class="stat-label">AI回复</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

def process_chat_message(user_message):
    """处理聊天消息"""
    if not st.session_state.github_api_key.strip():
        st.error("请先配置API密钥")
        return

    # 添加用户消息
    st.session_state.chat_messages.append({
        'role': 'user',
        'content': user_message,
        'timestamp': time.time()
    })

    # 显示思考动画
    thinking_placeholder = st.empty()
    with thinking_placeholder:
        st.markdown("""
        <div class="typing-indicator">
            <span>AI正在思考</span>
            <div class="typing-dots">
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # 获取AI响应
    system_prompt = get_system_prompt()
    ai_response, success = call_github_models_api(
        user_message, system_prompt, st.session_state.github_api_key
    )

    thinking_placeholder.empty()

    # 添加AI响应
    st.session_state.chat_messages.append({
        'role': 'assistant',
        'content': ai_response,
        'timestamp': time.time()
    })

    # 更新统计
    st.session_state.conversation_count += 1

    if success:
        st.success("回复已生成")
    else:
        st.error("生成失败，请检查API配置")
    
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
    render_suggestions()
    render_chat_history()
    render_input_area()
    render_stats()
    
    # 页脚
    st.markdown("""
    <div style="text-align: center; margin-top: 2rem; padding: 1rem; color: #94a3b8; font-size: 0.9rem;">
        <p>🤖 AI智能对话 - 简洁高效的对话体验</p>
        <p>当前用户：Kikyo-acd | 时间：2025-08-08 09:38:54 UTC</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
