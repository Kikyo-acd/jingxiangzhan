import streamlit as st
import requests
import time
import json
import random

# 页面配置
st.set_page_config(
    page_title="AI智能对话站",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def apply_cyberpunk_style():
    """应用赛博朋克风格CSS"""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;500;600;700&display=swap');
    
    /* 全局背景 */
    .stApp {
        background: linear-gradient(135deg, #0c0c0c 0%, #1a1a2e 25%, #16213e 50%, #0f0f23 75%, #000000 100%);
        background-attachment: fixed;
        animation: backgroundShift 20s ease-in-out infinite;
    }
    
    @keyframes backgroundShift {
        0%, 100% { background: linear-gradient(135deg, #0c0c0c 0%, #1a1a2e 25%, #16213e 50%, #0f0f23 75%, #000000 100%); }
        50% { background: linear-gradient(135deg, #1a1a2e 0%, #16213e 25%, #0f0f23 50%, #000000 75%, #0c0c0c 100%); }
    }
    
    /* 主容器 */
    .main .block-container {
        padding: 2rem 1rem;
        max-width: 100%;
    }
    
    /* 霓虹标题 */
    .neon-title {
        font-family: 'Orbitron', monospace;
        font-size: 4rem;
        font-weight: 900;
        text-align: center;
        margin: 2rem 0;
        background: linear-gradient(45deg, #00f5ff, #ff00ff, #00ff00, #ffff00);
        background-size: 400% 400%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: neonGlow 3s ease-in-out infinite, gradientShift 8s ease-in-out infinite;
        text-shadow: 0 0 20px rgba(0, 245, 255, 0.5), 0 0 40px rgba(255, 0, 255, 0.3);
        position: relative;
    }
    
    .neon-title::before {
        content: attr(data-text);
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(45deg, #00f5ff, #ff00ff, #00ff00, #ffff00);
        background-size: 400% 400%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        filter: blur(2px);
        opacity: 0.7;
        z-index: -1;
        animation: gradientShift 8s ease-in-out infinite reverse;
    }
    
    @keyframes neonGlow {
        0%, 100% { filter: brightness(1) drop-shadow(0 0 20px rgba(0, 245, 255, 0.8)); }
        50% { filter: brightness(1.3) drop-shadow(0 0 30px rgba(255, 0, 255, 1)); }
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* 副标题 */
    .cyber-subtitle {
        font-family: 'Rajdhani', sans-serif;
        font-size: 1.5rem;
        font-weight: 300;
        text-align: center;
        color: #00f5ff;
        margin-bottom: 3rem;
        opacity: 0.8;
        letter-spacing: 3px;
        animation: pulse 2s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 0.6; }
        50% { opacity: 1; }
    }
    
    /* 玻璃态容器 */
    .glass-container {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 
            0 8px 32px rgba(0, 0, 0, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.1),
            0 0 50px rgba(0, 245, 255, 0.1);
        position: relative;
        overflow: hidden;
        transition: all 0.3s ease;
    }
    
    .glass-container:hover {
        transform: translateY(-5px);
        box-shadow: 
            0 15px 50px rgba(0, 0, 0, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.2),
            0 0 80px rgba(0, 245, 255, 0.2);
    }
    
    .glass-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
        transition: left 0.5s;
    }
    
    .glass-container:hover::before {
        left: 100%;
    }
    
    /* API状态指示器 */
    .api-status {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 10px;
        padding: 1rem;
        border-radius: 15px;
        font-family: 'Rajdhani', sans-serif;
        font-weight: 600;
        font-size: 1.1rem;
        margin: 1rem 0;
        transition: all 0.3s ease;
    }
    
    .api-status.connected {
        background: linear-gradient(45deg, rgba(0, 255, 0, 0.1), rgba(0, 245, 255, 0.1));
        border: 1px solid rgba(0, 255, 0, 0.3);
        color: #00ff00;
        box-shadow: 0 0 20px rgba(0, 255, 0, 0.2);
    }
    
    .api-status.disconnected {
        background: linear-gradient(45deg, rgba(255, 0, 0, 0.1), rgba(255, 100, 0, 0.1));
        border: 1px solid rgba(255, 0, 0, 0.3);
        color: #ff4444;
        box-shadow: 0 0 20px rgba(255, 0, 0, 0.2);
    }
    
    .status-indicator {
        width: 12px;
        height: 12px;
        border-radius: 50%;
        animation: statusPulse 2s ease-in-out infinite;
    }
    
    .status-indicator.online {
        background: radial-gradient(circle, #00ff00, #00aa00);
        box-shadow: 0 0 10px #00ff00;
    }
    
    .status-indicator.offline {
        background: radial-gradient(circle, #ff4444, #aa0000);
        box-shadow: 0 0 10px #ff4444;
    }
    
    @keyframes statusPulse {
        0%, 100% { transform: scale(1); opacity: 1; }
        50% { transform: scale(1.2); opacity: 0.7; }
    }
    
    /* 霓虹按钮 */
    .neon-button {
        background: linear-gradient(45deg, transparent, rgba(0, 245, 255, 0.1));
        border: 2px solid #00f5ff;
        border-radius: 15px;
        color: #00f5ff;
        font-family: 'Rajdhani', sans-serif;
        font-weight: 600;
        font-size: 1rem;
        padding: 0.8rem 1.5rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        cursor: pointer;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
        box-shadow: 0 0 20px rgba(0, 245, 255, 0.3);
    }
    
    .neon-button:hover {
        background: linear-gradient(45deg, rgba(0, 245, 255, 0.1), rgba(255, 0, 255, 0.1));
        border-color: #ff00ff;
        color: #ff00ff;
        box-shadow: 0 0 30px rgba(255, 0, 255, 0.5);
        transform: translateY(-2px);
    }
    
    .neon-button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        transition: left 0.5s;
    }
    
    .neon-button:hover::before {
        left: 100%;
    }
    
    /* 聊天气泡 */
    .chat-message {
        margin: 1rem 0;
        animation: slideInUp 0.5s ease-out;
    }
    
    .user-message {
        text-align: right;
    }
    
    .user-message .message-bubble {
        background: linear-gradient(135deg, #00f5ff, #0080ff);
        color: #000;
        border-radius: 20px 20px 5px 20px;
        padding: 1rem 1.5rem;
        margin-left: auto;
        max-width: 80%;
        font-family: 'Rajdhani', sans-serif;
        font-weight: 500;
        box-shadow: 0 5px 20px rgba(0, 245, 255, 0.3);
        position: relative;
    }
    
    .ai-message .message-bubble {
        background: linear-gradient(135deg, rgba(255, 0, 255, 0.1), rgba(0, 255, 255, 0.1));
        border: 1px solid rgba(255, 0, 255, 0.3);
        color: #ffffff;
        border-radius: 20px 20px 20px 5px;
        padding: 1rem 1.5rem;
        margin-right: auto;
        max-width: 80%;
        font-family: 'Rajdhani', sans-serif;
        font-weight: 400;
        backdrop-filter: blur(10px);
        box-shadow: 0 5px 20px rgba(255, 0, 255, 0.2);
    }
    
    @keyframes slideInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* 输入框样式 */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background: rgba(0, 0, 0, 0.3) !important;
        border: 1px solid rgba(0, 245, 255, 0.3) !important;
        border-radius: 15px !important;
        color: #ffffff !important;
        font-family: 'Rajdhani', sans-serif !important;
        font-size: 1rem !important;
        backdrop-filter: blur(10px) !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #ff00ff !important;
        box-shadow: 0 0 20px rgba(255, 0, 255, 0.3) !important;
    }
    
    /* 按钮重写 */
    .stButton > button {
        background: linear-gradient(45deg, transparent, rgba(0, 245, 255, 0.1)) !important;
        border: 2px solid #00f5ff !important;
        border-radius: 15px !important;
        color: #00f5ff !important;
        font-family: 'Rajdhani', sans-serif !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 0 20px rgba(0, 245, 255, 0.3) !important;
    }
    
    .stButton > button:hover {
        background: linear-gradient(45deg, rgba(0, 245, 255, 0.1), rgba(255, 0, 255, 0.1)) !important;
        border-color: #ff00ff !important;
        color: #ff00ff !important;
        box-shadow: 0 0 30px rgba(255, 0, 255, 0.5) !important;
        transform: translateY(-2px) !important;
    }
    
    /* 加载动画 */
    .cyber-loader {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 10px;
        margin: 2rem 0;
    }
    
    .cyber-loader .dot {
        width: 12px;
        height: 12px;
        border-radius: 50%;
        background: linear-gradient(45deg, #00f5ff, #ff00ff);
        animation: cyberPulse 1.5s ease-in-out infinite;
    }
    
    .cyber-loader .dot:nth-child(2) { animation-delay: 0.2s; }
    .cyber-loader .dot:nth-child(3) { animation-delay: 0.4s; }
    
    @keyframes cyberPulse {
        0%, 80%, 100% { transform: scale(0.8); opacity: 0.5; }
        40% { transform: scale(1.2); opacity: 1; }
    }
    
    /* 隐藏Streamlit默认元素 */
    #MainMenu, .stDeployButton, footer, .stActionButton {
        visibility: hidden;
    }
    
    /* 响应式设计 */
    @media (max-width: 768px) {
        .neon-title {
            font-size: 2.5rem;
        }
        
        .cyber-subtitle {
            font-size: 1.2rem;
        }
        
        .glass-container {
            padding: 1rem;
            margin: 0.5rem;
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
你是一个先进的AI助手，具备以下特点：
- 智能、友好、专业
- 能够理解复杂的问题并提供有价值的回答
- 支持多种领域的知识问答
- 可以进行创意写作、代码编程、学习辅导等
- 回复风格可以根据用户需求调整

请根据用户的问题提供最有帮助的回答。
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

    # 添加聊天历史上下文（最近6轮对话）
    if len(st.session_state.chat_messages) > 0:
        recent_messages = st.session_state.chat_messages[-12:]
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
        "temperature": 0.7,
        "stream": False
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
            return "❌ API认证失败：请检查API密钥是否正确", False
        elif response.status_code == 429:
            return "⏰ 请求过于频繁：请稍后再试", False
        else:
            return f"❌ API调用失败：{response.status_code}", False

    except requests.exceptions.Timeout:
        return "⏰ 请求超时：网络连接较慢", False
    except Exception as e:
        return f"❌ 连接错误：{str(e)[:100]}", False

def get_smart_suggestions():
    """提供智能建议"""
    suggestions_pool = [
        "💡 创意写作：帮我写一个科幻小说开头",
        "📚 学习辅导：解释量子物理的基本概念",
        "💻 代码编程：用Python写一个爬虫程序",
        "🎨 设计灵感：给我一些现代网页设计建议",
        "🌍 知识问答：介绍人工智能的发展历史",
        "🔬 科学探索：解释黑洞的形成原理",
        "📈 商业分析：如何制定有效的营销策略",
        "🎵 艺术创作：推荐一些音乐制作软件",
        "🏠 生活建议：如何提高工作效率",
        "🌟 哲学思考：什么是真正的幸福",
        "🎮 游戏开发：介绍游戏引擎的选择",
        "📱 技术趋势：分析5G技术的应用前景"
    ]
    
    return random.sample(suggestions_pool, 6)

def render_header():
    """渲染页面头部"""
    st.markdown("""
    <div class="neon-title" data-text="AI NEXUS">AI NEXUS</div>
    <div class="cyber-subtitle">// 下一代智能对话平台 //</div>
    """, unsafe_allow_html=True)

def render_api_status():
    """渲染API状态"""
    status_class = "connected" if st.session_state.github_api_key else "disconnected"
    indicator_class = "online" if st.session_state.github_api_key else "offline"
    status_text = "已连接" if st.session_state.github_api_key else "未连接"
    
    st.markdown(f"""
    <div class="api-status {status_class}">
        <div class="status-indicator {indicator_class}"></div>
        <span>API状态: {status_text}</span>
    </div>
    """, unsafe_allow_html=True)

def render_chat_interface():
    """渲染主要聊天界面"""
    
    # API密钥输入
    with st.container():
        st.markdown('<div class="glass-container">', unsafe_allow_html=True)
        st.markdown("#### 🔑 API配置")
        
        api_key_input = st.text_input(
            "",
            value=st.session_state.github_api_key,
            type="password",
            placeholder="输入您的GitHub Models API密钥...",
            label_visibility="collapsed"
        )

        if api_key_input != st.session_state.github_api_key:
            st.session_state.github_api_key = api_key_input

        render_api_status()
        st.markdown('</div>', unsafe_allow_html=True)

    # 快速建议
    with st.container():
        st.markdown('<div class="glass-container">', unsafe_allow_html=True)
        st.markdown("#### 💡 智能建议")
        
        suggestions = get_smart_suggestions()
        cols = st.columns(2)
        
        for i, suggestion in enumerate(suggestions):
            with cols[i % 2]:
                if st.button(suggestion, key=f"suggest_{i}", use_container_width=True):
                    if st.session_state.github_api_key:
                        process_chat_message(suggestion.split("：", 1)[-1])
                    else:
                        st.error("请先配置API密钥")
        
        st.markdown('</div>', unsafe_allow_html=True)

    # 对话历史
    if st.session_state.chat_messages:
        with st.container():
            st.markdown('<div class="glass-container">', unsafe_allow_html=True)
            st.markdown("#### 💬 对话记录")
            
            # 显示最近10条对话
            recent_messages = st.session_state.chat_messages[-20:]
            for msg in recent_messages:
                if msg['role'] == 'user':
                    st.markdown(f"""
                    <div class="chat-message user-message">
                        <div class="message-bubble">
                            <strong>🚀 你:</strong> {msg['content']}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="chat-message ai-message">
                        <div class="message-bubble">
                            <strong>🤖 AI:</strong><br>{msg['content']}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)

    # 输入区域
    with st.container():
        st.markdown('<div class="glass-container">', unsafe_allow_html=True)
        st.markdown("#### ⚡ 开始对话")
        
        user_input = st.text_area(
            "",
            placeholder="在这里输入你的问题或想法...",
            height=100,
            key="chat_input",
            label_visibility="collapsed"
        )

        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            if st.button("🚀 发送消息", use_container_width=True, type="primary"):
                if not st.session_state.github_api_key:
                    st.error("⚠️ 请先配置API密钥")
                elif user_input.strip():
                    process_chat_message(user_input.strip())
                    # 清空输入框
                    st.session_state.chat_input = ""
                    st.rerun()
                else:
                    st.warning("⚠️ 请输入内容")

        with col2:
            if st.button("🔄 随机话题", use_container_width=True):
                if st.session_state.github_api_key:
                    random_topics = [
                        "给我讲一个有趣的科学事实",
                        "推荐一本好书并说明理由",
                        "用简单的话解释区块链",
                        "创作一首关于星空的诗",
                        "分析当前科技发展趋势"
                    ]
                    random_topic = random.choice(random_topics)
                    process_chat_message(random_topic)
                else:
                    st.error("请先配置API密钥")

        with col3:
            if st.button("🗑️ 清空记录", use_container_width=True):
                st.session_state.chat_messages = []
                st.session_state.conversation_count = 0
                st.rerun()
        
        # 统计信息
        if st.session_state.conversation_count > 0:
            st.markdown(f"""
            <div style="text-align: center; margin-top: 1rem; color: #00f5ff; font-family: 'Rajdhani', sans-serif;">
                📊 已进行 {st.session_state.conversation_count} 轮对话
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

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

    # 显示加载动画
    with st.empty():
        st.markdown("""
        <div class="cyber-loader">
            <div class="dot"></div>
            <div class="dot"></div>
            <div class="dot"></div>
        </div>
        <div style="text-align: center; color: #00f5ff; font-family: 'Rajdhani', sans-serif; margin-top: 1rem;">
            AI正在思考中...
        </div>
        """, unsafe_allow_html=True)
        
        time.sleep(1)  # 模拟思考时间

    # 获取AI响应
    system_prompt = get_system_prompt()
    ai_response, success = call_github_models_api(
        user_message, system_prompt, st.session_state.github_api_key
    )

    # 添加AI响应
    st.session_state.chat_messages.append({
        'role': 'assistant',
        'content': ai_response,
        'timestamp': time.time()
    })

    # 更新对话计数
    st.session_state.conversation_count += 1

    # 显示结果
    if success:
        st.success("✨ 回复已生成！")
    else:
        st.error("❌ 生成失败，请检查API配置")
    
    st.rerun()

def main():
    """主程序"""
    # 应用样式
    apply_cyberpunk_style()
    
    # 初始化
    initialize_chat_session()
    
    # 渲染界面
    render_header()
    render_chat_interface()
    
    # 页脚
    st.markdown("""
    <div style="text-align: center; margin-top: 3rem; padding: 2rem; color: rgba(255, 255, 255, 0.3); font-family: 'Rajdhani', sans-serif;">
        <p>🚀 AI NEXUS - 连接未来的智能对话平台</p>
        <p style="font-size: 0.9rem;">Powered by GitHub Models API | Built with ❤️</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
