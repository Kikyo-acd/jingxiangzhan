import streamlit as st
import requests
import time
import json
import random
from datetime import datetime

# 页面配置
st.set_page_config(
    page_title="AI智能对话平台",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

def apply_styles():
    """应用样式和本地存储JavaScript"""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
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
    
    /* 侧边栏样式 */
    .css-1d391kg {
        background: linear-gradient(180deg, #f8fafc 0%, #e2e8f0 100%);
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
    
    /* 消息样式 */
    .user-message {
        background: linear-gradient(135deg, #3b82f6, #1d4ed8);
        color: white;
        padding: 1rem 1.2rem;
        border-radius: 18px 18px 4px 18px;
        margin: 0.8rem 0;
        margin-left: auto;
        max-width: 70%;
        font-weight: 500;
        box-shadow: 0 2px 8px rgba(59, 130, 246, 0.3);
        word-wrap: break-word;
    }
    
    .ai-message {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        color: #334155;
        padding: 1rem 1.2rem;
        border-radius: 18px 18px 18px 4px;
        margin: 0.8rem 0;
        margin-right: auto;
        max-width: 70%;
        line-height: 1.6;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        word-wrap: break-word;
    }
    
    .message-time {
        font-size: 0.75rem;
        color: rgba(255,255,255,0.7);
        margin-top: 0.5rem;
    }
    
    .ai-message .message-time {
        color: #94a3b8;
    }
    
    .message-model {
        font-size: 0.8rem;
        color: #7c3aed;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    /* 模型选择卡片 */
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
        font-size: 0.85rem;
        color: #64748b;
        margin-bottom: 0.5rem;
        line-height: 1.4;
    }
    
    .model-tags {
        display: flex;
        gap: 0.3rem;
        flex-wrap: wrap;
    }
    
    .model-tag {
        background: #f1f5f9;
        color: #475569;
        padding: 0.2rem 0.5rem;
        border-radius: 4px;
        font-size: 0.7rem;
        font-weight: 500;
    }
    
    .model-tag.premium { background: #fef3c7; color: #92400e; }
    .model-tag.fast { background: #d1fae5; color: #065f46; }
    .model-tag.recommended { background: #ddd6fe; color: #6b21a8; }
    
    /* 状态指示器 */
    .status-indicator {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        font-size: 0.9rem;
        font-weight: 500;
        margin: 0.5rem 0;
    }
    
    .status-connected {
        background: #f0fdf4;
        border: 1px solid #bbf7d0;
        color: #166534;
    }
    
    .status-disconnected {
        background: #fef2f2;
        border: 1px solid #fecaca;
        color: #dc2626;
    }
    
    .status-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
    }
    
    .dot-online {
        background: #22c55e;
        box-shadow: 0 0 0 2px rgba(34, 197, 94, 0.2);
    }
    
    .dot-offline {
        background: #ef4444;
        box-shadow: 0 0 0 2px rgba(239, 68, 68, 0.2);
    }
    
    /* 输入框样式 */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        border: 1px solid #d1d5db !important;
        border-radius: 8px !important;
        padding: 0.75rem !important;
        font-size: 1rem !important;
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
        30% { transform: translateY(-8px); }
    }
    
    /* 隐藏默认元素 */
    #MainMenu, .stDeployButton, footer { visibility: hidden; }
    
    /* 响应式设计 */
    @media (max-width: 768px) {
        .main-title { font-size: 2rem; }
        .user-message, .ai-message { max-width: 90%; }
    }
    </style>
    
    <script>
    // 本地存储管理
    window.ChatStorage = {
        // 保存聊天数据
        save: function(data) {
            try {
                const chatData = {
                    messages: data.messages || [],
                    apiKey: data.apiKey || '',
                    selectedModel: data.selectedModel || 'gpt-4o-mini',
                    conversationCount: data.conversationCount || 0,
                    lastSaved: new Date().toISOString()
                };
                localStorage.setItem('ai_chat_data', JSON.stringify(chatData));
                console.log('✅ 聊天数据已保存', chatData.messages.length + ' 条消息');
                return true;
            } catch(e) {
                console.error('❌ 保存失败:', e);
                return false;
            }
        },
        
        // 加载聊天数据
        load: function() {
            try {
                const data = localStorage.getItem('ai_chat_data');
                if (data) {
                    const parsed = JSON.parse(data);
                    console.log('✅ 已加载聊天数据', parsed.messages.length + ' 条消息');
                    return parsed;
                }
                return null;
            } catch(e) {
                console.error('❌ 加载失败:', e);
                return null;
            }
        },
        
        // 清空数据
        clear: function() {
            try {
                localStorage.removeItem('ai_chat_data');
                console.log('✅ 聊天数据已清空');
                return true;
            } catch(e) {
                console.error('❌ 清空失败:', e);
                return false;
            }
        },
        
        // 获取存储大小
        getSize: function() {
            try {
                const data = localStorage.getItem('ai_chat_data');
                return data ? (data.length / 1024).toFixed(1) + 'KB' : '0KB';
            } catch(e) {
                return '未知';
            }
        }
    };
    
    // 页面加载时尝试恢复数据
    window.addEventListener('load', function() {
        const savedData = window.ChatStorage.load();
        if (savedData && savedData.messages.length > 0) {
            console.log('🔄 发现本地聊天记录，准备恢复...');
            // 触发自定义事件通知Streamlit
            window.dispatchEvent(new CustomEvent('chatDataFound', { 
                detail: savedData 
            }));
        }
    });
    
    // 自动保存函数
    window.autoSaveChatData = function(messages, apiKey, selectedModel, conversationCount) {
        return window.ChatStorage.save({
            messages: messages,
            apiKey: apiKey,
            selectedModel: selectedModel,
            conversationCount: conversationCount
        });
    };
    </script>
    """, unsafe_allow_html=True)

def initialize_session_state():
    """初始化会话状态并恢复本地数据"""
    defaults = {
        'chat_messages': [],
        'github_api_key': '',
        'available_models': [],
        'selected_model': 'gpt-4o-mini',
        'models_loaded': False,
        'conversation_count': 0,
        'auto_save_enabled': True,
        'data_restored': False,
        'chat_sessions': {},
        'current_session_id': None,
        'session_counter': 0
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
    
    # 尝试从本地存储恢复数据
    if not st.session_state.data_restored:
        restore_from_local_storage()

def try_restore_data():
    """尝试从JavaScript恢复的数据中读取并应用到session_state"""
    # 添加一个JavaScript检查器
    st.markdown("""
    <script>
    function applyRestoredData() {
        const hiddenInput = document.getElementById('restored-chat-data');
        if (hiddenInput && hiddenInput.value) {
            try {
                const data = JSON.parse(hiddenInput.value);
                console.log('📥 准备应用恢复的数据:', data);
                
                // 触发Streamlit重新运行以应用数据
                window.streamlitRestoredData = data;
                
                // 创建一个事件通知Streamlit
                const event = new CustomEvent('dataRestored', { detail: data });
                window.dispatchEvent(event);
                
                return true;
            } catch (error) {
                console.error('❌ 应用恢复数据失败:', error);
            }
        }
        return false;
    }
    
    // 延迟执行，确保DOM完全加载
    setTimeout(applyRestoredData, 1500);
    </script>
    """, unsafe_allow_html=True)

def restore_from_local_storage():
    """从本地存储恢复数据"""
    st.session_state.data_restored = True
    
    # 添加JavaScript来恢复数据
    st.markdown("""
    <script>
    function restoreChatData() {
        try {
            // 尝试恢复完整数据
            const completeData = localStorage.getItem('ai_chat_complete_data');
            if (completeData) {
                const data = JSON.parse(completeData);
                console.log('🔄 发现完整聊天数据:', data);
                
                // 将数据存储到一个全局变量供Streamlit读取
                window.restoredChatData = {
                    currentMessages: data.current_messages || [],
                    currentSessionId: data.current_session_id || null,
                    sessions: data.sessions || {},
                    sessionCounter: data.session_counter || 0,
                    apiKey: data.api_key || '',
                    selectedModel: data.selected_model || 'gpt-4o-mini',
                    conversationCount: data.conversation_count || 0,
                    dataFound: true
                };
                
                // 显示恢复信息
                if (data.current_messages && data.current_messages.length > 0) {
                    console.log(`✅ 恢复 ${data.current_messages.length} 条当前会话消息`);
                }
                if (data.sessions && Object.keys(data.sessions).length > 0) {
                    console.log(`✅ 恢复 ${Object.keys(data.sessions).length} 个历史会话`);
                }
                
                return true;
            }
            
            // 如果没有完整数据，尝试恢复旧格式数据
            const oldData = localStorage.getItem('ai_chat_data');
            if (oldData) {
                const data = JSON.parse(oldData);
                console.log('🔄 发现旧版聊天数据:', data);
                
                window.restoredChatData = {
                    currentMessages: data.messages || [],
                    currentSessionId: null,
                    sessions: {},
                    sessionCounter: 0,
                    apiKey: data.apiKey || '',
                    selectedModel: data.selectedModel || 'gpt-4o-mini',
                    conversationCount: data.conversationCount || 0,
                    dataFound: true
                };
                
                console.log(`✅ 恢复 ${data.messages ? data.messages.length : 0} 条消息`);
                return true;
            }
            
            console.log('ℹ️ 未找到本地聊天数据');
            window.restoredChatData = { dataFound: false };
            return false;
            
        } catch (error) {
            console.error('❌ 恢复数据失败:', error);
            window.restoredChatData = { dataFound: false };
            return false;
        }
    }
    
    // 立即尝试恢复数据
    restoreChatData();
    
    // 如果页面还在加载，等待加载完成后再次尝试
    if (document.readyState !== 'complete') {
        window.addEventListener('load', restoreChatData);
    }
    </script>
    """, unsafe_allow_html=True)
    
    # 等待JavaScript执行
    time.sleep(0.5)
    
    # 通过JavaScript检查是否有数据需要恢复
    restore_check = st.empty()
    with restore_check:
        st.markdown("""
        <script>
        setTimeout(() => {
            if (window.restoredChatData && window.restoredChatData.dataFound) {
                const data = window.restoredChatData;
                
                // 创建一个隐藏的input来传递数据给Streamlit
                const hiddenInput = document.createElement('input');
                hiddenInput.type = 'hidden';
                hiddenInput.id = 'restored-chat-data';
                hiddenInput.value = JSON.stringify(data);
                document.body.appendChild(hiddenInput);
                
                // 显示恢复提示
                const restoreDiv = document.createElement('div');
                restoreDiv.style.cssText = `
                    position: fixed; top: 20px; right: 20px; z-index: 9999;
                    background: #f0fdf4; border: 1px solid #bbf7d0; color: #166534;
                    padding: 1rem; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);
                    font-family: Inter, sans-serif; font-size: 14px; max-width: 300px;
                `;
                
                const messageCount = data.currentMessages ? data.currentMessages.length : 0;
                const sessionCount = data.sessions ? Object.keys(data.sessions).length : 0;
                
                restoreDiv.innerHTML = `
                    <div style="font-weight: 600; margin-bottom: 0.5rem;">🔄 发现本地聊天记录</div>
                    <div>当前会话: ${messageCount} 条消息</div>
                    <div>历史会话: ${sessionCount} 个</div>
                    <div style="margin-top: 0.5rem; font-size: 12px; opacity: 0.8;">数据正在恢复中...</div>
                `;
                
                document.body.appendChild(restoreDiv);
                
                // 3秒后移除提示
                setTimeout(() => {
                    if (restoreDiv.parentNode) {
                        restoreDiv.parentNode.removeChild(restoreDiv);
                    }
                }, 3000);
            }
        }, 1000);
        </script>
        """, unsafe_allow_html=True)
    
    # 尝试读取恢复的数据
    try_restore_data()

def get_all_supported_models():
    """获取所有支持的AI模型"""
    return [
        {
            'id': 'gpt-4o',
            'name': 'GPT-4o',
            'description': 'OpenAI最新的GPT-4 Omni模型，具备强大的多模态能力和理解力',
            'tags': ['多模态', '最新', '高质量']
        },
        {
            'id': 'gpt-4o-mini',
            'name': 'GPT-4o Mini',
            'description': '轻量化版本的GPT-4o，响应速度快，成本更低，适合日常对话',
            'tags': ['快速', '经济', '推荐']
        },
        {
            'id': 'gpt-4-turbo',
            'name': 'GPT-4 Turbo',
            'description': 'OpenAI的增强版GPT-4，支持更长的上下文，处理能力强',
            'tags': ['长上下文', '稳定', '强大']
        },
        {
            'id': 'gpt-3.5-turbo',
            'name': 'GPT-3.5 Turbo',
            'description': 'OpenAI的经典模型，在性能和成本之间取得良好平衡',
            'tags': ['经典', '平衡', '可靠']
        },
        {
            'id': 'claude-3-5-sonnet',
            'name': 'Claude 3.5 Sonnet',
            'description': 'Anthropic最新的Claude模型，擅长分析、推理和创作',
            'tags': ['分析', '推理', '创作']
        },
        {
            'id': 'claude-3-haiku',
            'name': 'Claude 3 Haiku',
            'description': 'Claude系列中速度最快的模型，适合快速响应',
            'tags': ['快速', 'Anthropic', '轻量']
        },
        {
            'id': 'llama-3.1-405b-instruct',
            'name': 'Llama 3.1 405B',
            'description': 'Meta最大规模的开源模型，在推理和数学方面表现优异',
            'tags': ['开源', '大模型', '推理']
        },
        {
            'id': 'llama-3.1-70b-instruct',
            'name': 'Llama 3.1 70B',
            'description': 'Meta的中等规模模型，平衡了性能和效率',
            'tags': ['开源', '平衡', 'Meta']
        },
        {
            'id': 'llama-3.1-8b-instruct',
            'name': 'Llama 3.1 8B',
            'description': 'Meta的轻量级模型，响应速度极快',
            'tags': ['开源', '轻量', '快速']
        },
        {
            'id': 'qwen-2.5-72b-instruct',
            'name': 'Qwen 2.5 72B',
            'description': '阿里巴巴通义千问最新模型，中文理解能力强',
            'tags': ['中文优化', '阿里巴巴', '最新']
        },
        {
            'id': 'qwen-2.5-32b-instruct',
            'name': 'Qwen 2.5 32B',
            'description': '通义千问中等规模模型，中英文双语能力出色',
            'tags': ['中文', '双语', '通义']
        },
        {
            'id': 'qwen-2.5-7b-instruct',
            'name': 'Qwen 2.5 7B',
            'description': '通义千问轻量级模型，适合快速中文对话',
            'tags': ['中文', '轻量', '快速']
        },
        {
            'id': 'mistral-large-2407',
            'name': 'Mistral Large',
            'description': 'Mistral AI的大型模型，多语言能力强',
            'tags': ['多语言', 'Mistral', '欧洲']
        },
        {
            'id': 'mistral-small',
            'name': 'Mistral Small',
            'description': 'Mistral AI的轻量级模型，成本效益高',
            'tags': ['轻量', '经济', 'Mistral']
        }
    ]

def test_model_availability(api_key, model_id):
    """测试模型可用性"""
    if not api_key:
        return False
        
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    
    payload = {
        "messages": [{"role": "user", "content": "hi"}],
        "model": model_id,
        "max_tokens": 5
    }
    
    try:
        response = requests.post(
            "https://models.inference.ai.azure.com/chat/completions",
            headers=headers,
            json=payload,
            timeout=10
        )
        return response.status_code == 200
    except:
        return False

def save_chat_data():
    """保存聊天数据到本地存储，包括会话管理"""
    if st.session_state.get('auto_save_enabled', True):
        # 准备当前会话数据
        messages_data = []
        for msg in st.session_state.chat_messages:
            messages_data.append({
                'role': msg['role'],
                'content': msg['content'],
                'timestamp': msg.get('timestamp', time.time()),
                'model': msg.get('model', 'unknown')
            })
        
        # 准备会话管理数据
        sessions_data = {}
        for session_id, session_info in st.session_state.get('chat_sessions', {}).items():
            sessions_data[session_id] = {
                'messages': session_info['messages'],
                'created_time': session_info['created_time'].isoformat() if hasattr(session_info['created_time'], 'isoformat') else str(session_info['created_time']),
                'message_count': session_info['message_count'],
                'title': session_info['title']
            }
        
        # 保存完整数据
        complete_data = {
            'current_messages': messages_data,
            'current_session_id': st.session_state.get('current_session_id'),
            'sessions': sessions_data,
            'session_counter': st.session_state.get('session_counter', 0),
            'api_key': st.session_state.github_api_key,
            'selected_model': st.session_state.selected_model,
            'conversation_count': st.session_state.conversation_count,
            'save_timestamp': time.time()
        }
        
        # 执行JavaScript保存
        st.markdown(f"""
        <script>
        try {{
            const data = {json.dumps(complete_data)};
            localStorage.setItem('ai_chat_complete_data', JSON.stringify(data));
            console.log("💾 完整会话数据已保存 - 消息数:", data.current_messages.length);
        }} catch (error) {{
            console.error("❌ 保存失败:", error);
        }}
        </script>
        """, unsafe_allow_html=True)

def restore_chat_data():
    """从本地存储恢复聊天数据"""
    if not st.session_state.get('data_restored', False):
        st.session_state.data_restored = True
        
        # 尝试从本地存储恢复
        st.markdown("""
        <script>
        setTimeout(() => {
            const savedData = window.ChatStorage.load();
            if (savedData && savedData.messages && savedData.messages.length > 0) {
                // 显示恢复提示
                const event = new CustomEvent('showRestoreNotification', {
                    detail: {
                        messageCount: savedData.messages.length,
                        lastSaved: savedData.lastSaved
                    }
                });
                window.dispatchEvent(event);
            }
        }, 1000);
        </script>
        """, unsafe_allow_html=True)

def get_system_prompt():
    """获取系统提示词"""
    return f"""
你是一个友好、专业的AI助手，具备以下特点：
- 回答准确、有帮助
- 语言表达清晰易懂
- 能够处理各种类型的问题
- 保持礼貌和专业的态度
- 总是用中文回复

当前用户：Kikyo-acd
当前时间：2025-08-08 09:57:08 (UTC)

请根据用户的问题提供最有价值的回答。
"""

def call_ai_api(user_message, model_id, api_key):
    """调用AI API进行对话"""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    messages = [{"role": "system", "content": get_system_prompt()}]

    # 添加最近的聊天历史
    if st.session_state.chat_messages:
        recent_messages = st.session_state.chat_messages[-10:]
        for msg in recent_messages:
            if msg['role'] in ['user', 'assistant']:
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
            return result['choices'][0]['message']['content'], True
        elif response.status_code == 401:
            return "❌ API认证失败，请检查密钥", False
        elif response.status_code == 404:
            return f"❌ 模型 {model_id} 不可用", False
        else:
            return f"❌ API调用失败: {response.status_code}", False

    except Exception as e:
        return f"❌ 连接错误: {str(e)[:100]}", False

def render_sidebar():
    """渲染侧边栏"""
    with st.sidebar:
        st.markdown("# 🤖 AI对话控制台")
        
        # API配置区域
        st.markdown("### 🔧 API配置")
        api_key = st.text_input(
            "GitHub Models API密钥",
            value=st.session_state.github_api_key,
            type="password",
            placeholder="输入您的API密钥..."
        )
        
        if api_key != st.session_state.github_api_key:
            st.session_state.github_api_key = api_key
            st.session_state.models_loaded = False
        
        # API状态显示
        if st.session_state.github_api_key:
            st.markdown("""
            <div class="status-indicator status-connected">
                <div class="status-dot dot-online"></div>
                <span>API已连接</span>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="status-indicator status-disconnected">
                <div class="status-dot dot-offline"></div>
                <span>请输入API密钥</span>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # 模型选择区域
        st.markdown("### 🎯 选择AI模型")
        
        if not st.session_state.models_loaded:
            if st.session_state.github_api_key:
                with st.spinner("检测可用模型..."):
                    all_models = get_all_supported_models()
                    available_models = []
                    
                    # 测试模型可用性
                    for model in all_models:
                        if test_model_availability(st.session_state.github_api_key, model['id']):
                            available_models.append(model)
                    
                    st.session_state.available_models = available_models if available_models else all_models
                    st.session_state.models_loaded = True
                    st.rerun()
            else:
                st.session_state.available_models = get_all_supported_models()
                st.session_state.models_loaded = True
        
        # 显示当前选择的模型
        current_model = next((m for m in st.session_state.available_models 
                            if m['id'] == st.session_state.selected_model), None)
        if current_model:
            st.info(f"当前模型：**{current_model['name']}**")
        
        # 模型列表
        for model in st.session_state.available_models:
            is_selected = model['id'] == st.session_state.selected_model
            
            # 构建标签
            tags_html = ""
            for tag in model['tags']:
                tag_class = ""
                if tag in ['最新', '高质量', '多模态']:
                    tag_class = "premium"
                elif tag in ['快速', '经济', '轻量']:
                    tag_class = "fast"
                elif tag in ['推荐']:
                    tag_class = "recommended"
                
                tags_html += f'<span class="model-tag {tag_class}">{tag}</span>'
            
            # 模型卡片
            card_class = "model-card selected" if is_selected else "model-card"
            st.markdown(f"""
            <div class="{card_class}">
                <div class="model-name">{model['name']}</div>
                <div class="model-description">{model['description']}</div>
                <div class="model-tags">{tags_html}</div>
            </div>
            """, unsafe_allow_html=True)

            # 选择按钮
            button_text = "✓ 已选择" if is_selected else f"选择 {model['name']}"
            if st.button(
                button_text,
                key=f"select_{model['id']}",
                disabled=is_selected,
                use_container_width=True
            ):
                st.session_state.selected_model = model['id']
                st.success(f"✅ 已切换到 {model['name']}")
                save_chat_data()  # 保存模型选择
                st.rerun()
        
        st.markdown("---")
        
        # 数据管理区域
        st.markdown("### 💾 数据管理")
        
        # 存储状态
        if st.session_state.chat_messages:
            message_count = len(st.session_state.chat_messages)
            st.markdown(f"📊 聊天记录：{message_count} 条")
        
        # 自动保存开关
        auto_save = st.checkbox(
            "🔄 自动保存",
            value=st.session_state.get('auto_save_enabled', True),
            help="每次对话后自动保存到浏览器"
        )
        st.session_state.auto_save_enabled = auto_save
        
        # 数据操作按钮
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💾 手动保存", use_container_width=True):
                save_chat_data()
                st.success("已保存到本地")
        
        with col2:
            if st.button("🗑️ 清空记录", use_container_width=True):
                st.session_state.chat_messages = []
                st.session_state.conversation_count = 0
                # 清空本地存储
                st.markdown("""
                <script>
                if (window.ChatStorage) {
                    window.ChatStorage.clear();
                }
                </script>
                """, unsafe_allow_html=True)
                st.success("记录已清空")
                st.rerun()
        
        # 导出功能
        if st.session_state.chat_messages:
            export_data = {
                'export_time': datetime.now().isoformat(),
                'model_used': st.session_state.selected_model,
                'message_count': len(st.session_state.chat_messages),
                'messages': st.session_state.chat_messages
            }
            
            st.download_button(
                "📤 导出JSON",
                json.dumps(export_data, ensure_ascii=False, indent=2),
                file_name=f"ai_chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )
        
        st.markdown("---")
        
        # 统计信息
        st.markdown("### 📊 使用统计")
        st.markdown(f"对话轮数：{st.session_state.conversation_count}")
        st.markdown(f"当前用户：Kikyo-acd")
        st.markdown(f"时间：2025-08-08 09:57:08")

def render_main_content():
    """渲染主要内容区域 - 三栏布局"""
    # 页面标题
    st.markdown("""
    <div class="main-title">🤖 AI智能对话平台</div>
    <div class="subtitle">支持多种AI模型的智能对话体验</div>
    """, unsafe_allow_html=True)
    
    # 恢复数据提示
    restore_chat_data()
    
    # 创建三栏布局：主要内容 + 聊天记录选择栏
    main_col, chat_history_col = st.columns([3, 1])
    
    with main_col:
        # 原有的主要内容（聊天历史显示 + 输入区域）
        render_main_chat_area()
    
    with chat_history_col:
        # 新增的聊天记录选择栏
        render_chat_history_panel()

def render_main_chat_area():
    """渲染主要聊天区域"""
    # 聊天历史显示
    if st.session_state.chat_messages:
        st.markdown("### 💬 对话记录")
        
        # 创建聊天容器
        chat_container = st.container()
        with chat_container:
            for msg in st.session_state.chat_messages:
                timestamp = time.strftime("%H:%M", time.localtime(msg.get('timestamp', time.time())))
                model_used = msg.get('model', '未知模型')
                
                if msg['role'] == 'user':
                    st.markdown(f"""
                    <div class="user-message">
                        {msg['content']}
                        <div class="message-time">{timestamp}</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="ai-message">
                        <div class="message-model">🤖 {model_used}</div>
                        {msg['content']}
                        <div class="message-time">{timestamp}</div>
                    </div>
                    """, unsafe_allow_html=True)
    
    # 输入区域
    st.markdown("### ✨ 开始对话")
    
    # 显示当前模型
    current_model = next((m for m in st.session_state.available_models 
                        if m['id'] == st.session_state.selected_model), None)
    if current_model:
        st.info(f"当前使用模型：**{current_model['name']}** - {current_model['description']}")
    
    user_input = st.text_area(
        "",
        placeholder="在这里输入您的问题或想法...",
        height=100,
        key="chat_input",
        label_visibility="collapsed"
    )

    col1, col2, col3 = st.columns([3, 1, 1])
    
    with col1:
        send_disabled = not st.session_state.github_api_key
        if st.button("🚀 发送消息", use_container_width=True, type="primary", disabled=send_disabled):
            if not st.session_state.github_api_key:
                st.error("请在侧边栏配置API密钥")
            elif user_input.strip():
                process_chat_message(user_input.strip())
                st.rerun()
            else:
                st.warning("请输入内容")

    with col2:
        if st.button("🎲 随机话题", use_container_width=True, disabled=send_disabled):
            if st.session_state.github_api_key:
                topics = [
                    "给我讲一个有趣的科学事实",
                    "推荐一本值得读的书",
                    "解释一下人工智能的原理",
                    "创作一首关于秋天的诗",
                    "分析一下当前的科技趋势"
                ]
                random_topic = random.choice(topics)
                process_chat_message(random_topic)
            else:
                st.error("请先配置API密钥")

    with col3:
        if st.button("🔄 刷新模型", use_container_width=True):
            st.session_state.models_loaded = False
            st.rerun()

def render_chat_history_panel():
    """渲染聊天记录选择面板"""
    st.markdown("### 📚 聊天记录")
    
    # 初始化聊天会话管理
    if 'chat_sessions' not in st.session_state:
        st.session_state.chat_sessions = {}
    if 'current_session_id' not in st.session_state:
        st.session_state.current_session_id = None
    if 'session_counter' not in st.session_state:
        st.session_state.session_counter = 0
    
    # 新建会话按钮
    if st.button("➕ 新建对话", use_container_width=True, type="primary"):
        # 保存当前会话
        if st.session_state.current_session_id and st.session_state.chat_messages:
            st.session_state.chat_sessions[st.session_state.current_session_id] = {
                'messages': st.session_state.chat_messages.copy(),
                'created_time': datetime.now(),
                'message_count': len(st.session_state.chat_messages),
                'title': get_session_title(st.session_state.chat_messages)
            }
        
        # 创建新会话
        st.session_state.session_counter += 1
        new_session_id = f"session_{st.session_state.session_counter}_{int(time.time())}"
        st.session_state.current_session_id = new_session_id
        st.session_state.chat_messages = []
        st.session_state.conversation_count = 0
        save_chat_data()
        st.rerun()
    
    st.markdown("---")
    
    # 显示会话列表
    if st.session_state.chat_sessions:
        st.markdown("**历史会话：**")
        
        # 按创建时间排序显示会话
        sorted_sessions = sorted(
            st.session_state.chat_sessions.items(),
            key=lambda x: x[1]['created_time'],
            reverse=True
        )
        
        for session_id, session_data in sorted_sessions:
            is_current = session_id == st.session_state.current_session_id
            
            # 会话信息
            created_time = session_data['created_time'].strftime("%m-%d %H:%M")
            message_count = session_data['message_count']
            title = session_data['title']
            
            # 会话卡片样式
            card_style = "border: 2px solid #3b82f6; background: #eff6ff;" if is_current else "border: 1px solid #e2e8f0;"
            
            st.markdown(f"""
            <div style="padding: 0.75rem; margin: 0.5rem 0; border-radius: 8px; {card_style}">
                <div style="font-weight: 600; color: #1e293b; margin-bottom: 0.25rem;">
                    {'🟢 ' if is_current else ''}📄 {title}
                </div>
                <div style="font-size: 0.8rem; color: #64748b;">
                    {created_time} • {message_count} 条消息
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                if not is_current:
                    if st.button(f"切换", key=f"switch_{session_id}", use_container_width=True):
                        # 保存当前会话
                        if st.session_state.current_session_id and st.session_state.chat_messages:
                            st.session_state.chat_sessions[st.session_state.current_session_id] = {
                                'messages': st.session_state.chat_messages.copy(),
                                'created_time': st.session_state.chat_sessions.get(st.session_state.current_session_id, {}).get('created_time', datetime.now()),
                                'message_count': len(st.session_state.chat_messages),
                                'title': get_session_title(st.session_state.chat_messages)
                            }
                        
                        # 切换到选择的会话
                        st.session_state.current_session_id = session_id
                        st.session_state.chat_messages = session_data['messages'].copy()
                        st.session_state.conversation_count = len([m for m in session_data['messages'] if m['role'] == 'user'])
                        save_chat_data()
                        st.rerun()
                else:
                    st.markdown("**当前**")
            
            with col2:
                # 导出单个会话
                export_data = {
                    'session_id': session_id,
                    'title': title,
                    'created_time': created_time,
                    'messages': session_data['messages']
                }
                st.download_button(
                    "📤",
                    json.dumps(export_data, ensure_ascii=False, indent=2),
                    file_name=f"chat_session_{created_time.replace(':', '-')}.json",
                    mime="application/json",
                    key=f"export_{session_id}",
                    help="导出此会话"
                )
            
            with col3:
                if st.button("🗑️", key=f"delete_{session_id}", help="删除此会话"):
                    del st.session_state.chat_sessions[session_id]
                    if session_id == st.session_state.current_session_id:
                        st.session_state.current_session_id = None
                        st.session_state.chat_messages = []
                        st.session_state.conversation_count = 0
                    save_chat_data()
                    st.rerun()
    
    else:
        st.info("暂无历史会话")
    
    st.markdown("---")
    
    # 批量操作
    if st.session_state.chat_sessions:
        st.markdown("**批量操作：**")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📤 导出全部", use_container_width=True):
                all_sessions_data = {
                    'export_time': datetime.now().isoformat(),
                    'user': 'Kikyo-acd',
                    'session_count': len(st.session_state.chat_sessions),
                    'sessions': st.session_state.chat_sessions
                }
                st.download_button(
                    "下载全部会话",
                    json.dumps(all_sessions_data, ensure_ascii=False, indent=2),
                    file_name=f"all_chat_sessions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
        
        with col2:
            if st.button("🗑️ 清空全部", use_container_width=True):
                if st.checkbox("确认清空所有会话", key="confirm_clear_all"):
                    st.session_state.chat_sessions = {}
                    st.session_state.current_session_id = None
                    st.session_state.chat_messages = []
                    st.session_state.conversation_count = 0
                    save_chat_data()
                    st.rerun()

def get_session_title(messages):
    """根据聊天消息生成会话标题"""
    if not messages:
        return "新对话"
    
    # 取第一条用户消息作为标题
    for msg in messages:
        if msg['role'] == 'user':
            content = msg['content']
            if len(content) > 20:
                return content[:20] + "..."
            return content
    
    return f"对话 - {datetime.now().strftime('%H:%M')}"

def process_chat_message(user_message):
    """处理聊天消息"""
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

    # 自动保存
    save_chat_data()

    if success:
        st.success(f"✅ {current_model_name} 回复已生成并保存")
    else:
        st.error(f"❌ {current_model_name} 生成失败")

def apply_restored_data_if_available():
    """检查并应用JavaScript恢复的数据"""
    # 使用st.query_params或其他方式检查是否有数据需要恢复
    # 这里我们添加一个检查机制
    
    if 'restore_attempted' not in st.session_state:
        st.session_state.restore_attempted = True
        
        # 添加检查脚本
        data_check = st.empty()
        with data_check:
            st.markdown("""
            <script>
            setTimeout(() => {
                if (window.streamlitRestoredData) {
                    const data = window.streamlitRestoredData;
                    console.log('🔧 开始应用恢复的数据...');
                    
                    // 将数据写入到一个特殊的DOM元素中供Streamlit读取
                    let dataContainer = document.getElementById('streamlit-restored-data');
                    if (!dataContainer) {
                        dataContainer = document.createElement('div');
                        dataContainer.id = 'streamlit-restored-data';
                        dataContainer.style.display = 'none';
                        document.body.appendChild(dataContainer);
                    }
                    
                    dataContainer.textContent = JSON.stringify(data);
                    
                    // 设置一个标志表示数据已准备好
                    window.dataReadyForStreamlit = true;
                    
                    console.log('✅ 数据已准备好供Streamlit读取');
                }
            }, 2000);
            </script>
            """, unsafe_allow_html=True)
        
        # 等待数据准备
        time.sleep(2.5)
        data_check.empty()
        
        # 尝试通过components读取数据（如果可能的话）
        try:
            # 这里可以添加实际的数据读取逻辑
            # 由于Streamlit限制，我们使用一个变通方法
            restore_data_from_storage()
        except Exception as e:
            st.error(f"数据恢复过程中出现错误: {e}")

def restore_data_from_storage():
    """从存储中恢复数据的变通方法"""
    # 创建一个用户可操作的恢复界面
    if st.session_state.get('show_restore_interface', False):
        return
    
    # 检查是否有本地数据
    st.markdown("""
    <script>
    setTimeout(() => {
        const completeData = localStorage.getItem('ai_chat_complete_data');
        const oldData = localStorage.getItem('ai_chat_data');
        
        if (completeData || oldData) {
            // 显示恢复按钮
            let restoreButton = document.getElementById('manual-restore-button');
            if (!restoreButton) {
                restoreButton = document.createElement('button');
                restoreButton.id = 'manual-restore-button';
                restoreButton.innerHTML = '🔄 点击恢复聊天记录';
                restoreButton.style.cssText = `
                    position: fixed; top: 80px; right: 20px; z-index: 9999;
                    background: #3b82f6; color: white; border: none;
                    padding: 0.75rem 1rem; border-radius: 8px;
                    font-family: Inter, sans-serif; font-weight: 600;
                    cursor: pointer; box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
                `;
                
                restoreButton.onclick = function() {
                    try {
                        const data = completeData ? JSON.parse(completeData) : JSON.parse(oldData);
                        
                        // 手动恢复数据到sessionStorage供Streamlit读取
                        sessionStorage.setItem('manual_restore_data', JSON.stringify(data));
                        
                        // 提示用户刷新页面
                        alert('数据已准备好！请刷新页面完成恢复。');
                        
                        // 自动刷新页面
                        window.location.reload();
                        
                    } catch (error) {
                        alert('恢复失败: ' + error.message);
                    }
                };
                
                document.body.appendChild(restoreButton);
                
                // 5秒后自动隐藏按钮
                setTimeout(() => {
                    if (restoreButton.parentNode) {
                        restoreButton.style.opacity = '0.7';
                    }
                }, 5000);
            }
        }
    }, 1000);
    </script>
    """, unsafe_allow_html=True)
    
    # 检查是否有手动恢复的数据
    st.markdown("""
    <script>
    const manualData = sessionStorage.getItem('manual_restore_data');
    if (manualData) {
        try {
            const data = JSON.parse(manualData);
            console.log('📦 发现手动恢复数据:', data);
            
            // 将数据存储到全局变量
            window.manualRestoreData = data;
            
            // 清除sessionStorage中的数据
            sessionStorage.removeItem('manual_restore_data');
            
            // 通知用户恢复成功
            const successDiv = document.createElement('div');
            successDiv.style.cssText = `
                position: fixed; top: 20px; right: 20px; z-index: 9999;
                background: #f0fdf4; border: 1px solid #bbf7d0; color: #166534;
                padding: 1rem; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);
                font-family: Inter, sans-serif; font-size: 14px;
            `;
            successDiv.innerHTML = `
                <div style="font-weight: 600;">✅ 聊天记录恢复成功！</div>
                <div style="font-size: 12px; margin-top: 0.5rem;">
                    恢复了 ${data.current_messages ? data.current_messages.length : 0} 条消息
                </div>
            `;
            document.body.appendChild(successDiv);
            
            setTimeout(() => {
                if (successDiv.parentNode) {
                    successDiv.parentNode.removeChild(successDiv);
                }
            }, 3000);
            
        } catch (error) {
            console.error('❌ 手动恢复失败:', error);
        }
    }
    </script>
    """, unsafe_allow_html=True)

def main():
    """主程序"""
    # 应用样式
    apply_styles()
    
    # 初始化
    initialize_session_state()
    
    # 检查并应用恢复的数据
    apply_restored_data_if_available()
    
    # 渲染界面
    render_sidebar()
    render_main_content()

if __name__ == "__main__":
    main()
