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
    initial_sidebar_state="collapsed"
)

def apply_light_theme():
    """应用简洁浅色主题CSS + 本地存储支持"""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* 之前的CSS样式保持不变 */
    .stApp {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        font-family: 'Inter', sans-serif;
    }
    
    .main .block-container {
        padding: 2rem 1rem;
        max-width: 1200px;
        margin: 0 auto;
    }
    
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
    
    /* 消息样式 */
    .user-message {
        align-self: flex-end;
        background: linear-gradient(135deg, #3b82f6, #1d4ed8);
        color: white;
        padding: 0.75rem 1rem;
        border-radius: 18px 18px 4px 18px;
        max-width: 70%;
        font-weight: 500;
        box-shadow: 0 2px 8px rgba(59, 130, 246, 0.3);
        margin: 0.5rem 0;
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
        margin: 0.5rem 0;
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
    
    /* 存储状态指示器 */
    .storage-status {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.5rem 1rem;
        background: #f0fdf4;
        border: 1px solid #bbf7d0;
        border-radius: 6px;
        color: #166534;
        font-size: 0.9rem;
        margin: 1rem 0;
    }
    
    /* 其他样式保持不变... */
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
    
    #MainMenu, .stDeployButton, footer { visibility: hidden; }
    </style>
    
    <!-- 本地存储JavaScript -->
    <script>
    // 保存数据到本地存储
    function saveToLocalStorage(key, data) {
        try {
            localStorage.setItem('ai_chat_' + key, JSON.stringify(data));
            return true;
        } catch(e) {
            console.error('保存到本地存储失败:', e);
            return false;
        }
    }
    
    // 从本地存储读取数据
    function loadFromLocalStorage(key) {
        try {
            const data = localStorage.getItem('ai_chat_' + key);
            return data ? JSON.parse(data) : null;
        } catch(e) {
            console.error('从本地存储读取失败:', e);
            return null;
        }
    }
    
    // 清空本地存储
    function clearLocalStorage() {
        try {
            const keys = Object.keys(localStorage);
            keys.forEach(key => {
                if (key.startsWith('ai_chat_')) {
                    localStorage.removeItem(key);
                }
            });
            return true;
        } catch(e) {
            console.error('清空本地存储失败:', e);
            return false;
        }
    }
    
    // 暴露函数给Streamlit使用
    window.aiChatStorage = {
        save: saveToLocalStorage,
        load: loadFromLocalStorage,
        clear: clearLocalStorage
    };
    
    // 监听页面卸载，自动保存数据
    window.addEventListener('beforeunload', function() {
        if (window.streamlitData) {
            saveToLocalStorage('auto_save', window.streamlitData);
        }
    });
    </script>
    """, unsafe_allow_html=True)

def init_local_storage():
    """初始化本地存储功能"""
    # 创建与前端JavaScript交互的组件
    st.markdown("""
    <script>
    // 检查本地存储支持
    function checkLocalStorageSupport() {
        try {
            return typeof(Storage) !== "undefined";
        } catch(e) {
            return false;
        }
    }
    
    // 获取存储大小
    function getStorageSize() {
        let total = 0;
        for (let key in localStorage) {
            if (localStorage.hasOwnProperty(key) && key.startsWith('ai_chat_')) {
                total += localStorage[key].length;
            }
        }
        return total;
    }
    
    // 设置状态到页面
    if (checkLocalStorageSupport()) {
        const size = getStorageSize();
        const status = document.createElement('div');
        status.className = 'storage-status';
        status.innerHTML = `✅ 本地存储已启用 (${(size/1024).toFixed(1)}KB)`;
        
        // 尝试插入到页面中
        setTimeout(() => {
            const container = document.querySelector('.main .block-container');
            if (container && !document.querySelector('.storage-status')) {
                container.insertBefore(status, container.firstChild);
            }
        }, 1000);
    }
    </script>
    """, unsafe_allow_html=True)

def save_chat_data():
    """保存聊天数据到本地存储"""
    chat_data = {
        'messages': st.session_state.get('chat_messages', []),
        'api_key': st.session_state.get('github_api_key', ''),
        'selected_model': st.session_state.get('selected_model', 'gpt-4o-mini'),
        'conversation_count': st.session_state.get('conversation_count', 0),
        'last_updated': datetime.now().isoformat()
    }
    
    # 使用Streamlit的JavaScript接口
    st.markdown(f"""
    <script>
    if (window.aiChatStorage) {{
        const data = {json.dumps(chat_data)};
        window.aiChatStorage.save('chat_data', data);
        console.log('聊天数据已保存到本地存储');
    }}
    </script>
    """, unsafe_allow_html=True)

def load_chat_data():
    """从本地存储加载聊天数据"""
    # 首次加载时尝试从本地存储恢复
    if 'data_loaded' not in st.session_state:
        st.session_state.data_loaded = True
        
        # 显示加载提示
        loading_placeholder = st.empty()
        with loading_placeholder:
            st.info("🔄 正在从本地存储恢复聊天记录...")
        
        # 使用JavaScript加载数据
        st.markdown("""
        <script>
        setTimeout(() => {
            if (window.aiChatStorage) {
                const data = window.aiChatStorage.load('chat_data');
                if (data) {
                    // 将数据传递给Streamlit
                    const event = new CustomEvent('localStorageData', { detail: data });
                    window.dispatchEvent(event);
                    console.log('从本地存储加载数据成功');
                }
            }
        }, 500);
        </script>
        """, unsafe_allow_html=True)
        
        time.sleep(1)  # 等待JavaScript执行
        loading_placeholder.empty()

def initialize_chat_session():
    """初始化聊天会话，支持本地存储"""
    # 默认值初始化
    default_values = {
        'chat_messages': [],
        'github_api_key': "",
        'available_models': [],
        'selected_model': "gpt-4o-mini",
        'models_loaded': False,
        'conversation_count': 0,
        'auto_save_enabled': True
    }
    
    for key, default_value in default_values.items():
        if key not in st.session_state:
            st.session_state[key] = default_value
    
    # 尝试从本地存储加载数据
    load_chat_data()

def auto_save_chat():
    """自动保存聊天记录"""
    if st.session_state.get('auto_save_enabled', True):
        save_chat_data()

def render_storage_controls():
    """渲染存储控制面板"""
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("#### 💾 数据存储管理")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("💾 手动保存", use_container_width=True):
            save_chat_data()
            st.success("✅ 聊天记录已保存到浏览器")
    
    with col2:
        if st.button("📥 导入记录", use_container_width=True):
            # 触发从本地存储加载
            st.markdown("""
            <script>
            if (window.aiChatStorage) {
                const data = window.aiChatStorage.load('chat_data');
                if (data && data.messages) {
                    // 可以在这里实现导入逻辑
                    alert('找到 ' + data.messages.length + ' 条历史记录');
                } else {
                    alert('未找到历史记录');
                }
            }
            </script>
            """, unsafe_allow_html=True)
    
    with col3:
        if st.button("📤 导出记录", use_container_width=True):
            if st.session_state.chat_messages:
                # 创建导出数据
                export_data = {
                    'messages': st.session_state.chat_messages,
                    'export_time': datetime.now().isoformat(),
                    'message_count': len(st.session_state.chat_messages),
                    'conversation_count': st.session_state.conversation_count
                }
                
                # 生成下载链接
                json_str = json.dumps(export_data, ensure_ascii=False, indent=2)
                st.download_button(
                    "下载聊天记录",
                    json_str,
                    file_name=f"ai_chat_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
            else:
                st.warning("暂无聊天记录可导出")
    
    with col4:
        if st.button("🗑️ 清空存储", use_container_width=True):
            # 清空session state
            st.session_state.chat_messages = []
            st.session_state.conversation_count = 0
            
            # 清空本地存储
            st.markdown("""
            <script>
            if (window.aiChatStorage && window.aiChatStorage.clear()) {
                alert('✅ 本地存储已清空');
            } else {
                alert('❌ 清空失败');
            }
            </script>
            """, unsafe_allow_html=True)
            
            st.success("✅ 聊天记录已清空")
            st.rerun()
    
    # 自动保存设置
    auto_save = st.checkbox("🔄 自动保存聊天记录", 
                           value=st.session_state.get('auto_save_enabled', True),
                           help="每次发送消息后自动保存到浏览器本地存储")
    st.session_state.auto_save_enabled = auto_save
    
    # 存储状态显示
    if st.session_state.chat_messages:
        message_count = len(st.session_state.chat_messages)
        last_message_time = "刚刚" if st.session_state.chat_messages else "无"
        st.info(f"📊 当前记录：{message_count} 条消息 | 最后活动：{last_message_time}")
    
    st.markdown('</div>', unsafe_allow_html=True)

def get_system_prompt():
    """获取系统提示词"""
    current_time = "2025-08-08 09:51:23"
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

    # 添加聊天历史（最近10条）
    if len(st.session_state.chat_messages) > 0:
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
            ai_response = result['choices'][0]['message']['content']
            return ai_response, True
        else:
            return f"API调用失败：{response.status_code}", False

    except Exception as e:
        return f"连接错误：{str(e)[:100]}", False

def render_header():
    """渲染页面头部"""
    st.markdown("""
    <div class="main-title">🤖 AI智能对话平台</div>
    <div class="subtitle">支持本地存储的多模型AI对话体验</div>
    """, unsafe_allow_html=True)

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
        
        st.markdown('</div>', unsafe_allow_html=True)

def process_chat_message(user_message):
    """处理聊天消息并自动保存"""
    if not st.session_state.github_api_key.strip():
        st.error("请先配置API密钥")
        return

    # 添加用户消息
    st.session_state.chat_messages.append({
        'role': 'user',
        'content': user_message,
        'timestamp': time.time(),
        'model': st.session_state.selected_model
    })

    # 获取AI响应
    ai_response, success = call_ai_api(
        user_message, st.session_state.selected_model, st.session_state.github_api_key
    )

    # 添加AI响应
    st.session_state.chat_messages.append({
        'role': 'assistant',
        'content': ai_response,
        'timestamp': time.time(),
        'model': st.session_state.selected_model
    })

    # 更新统计
    st.session_state.conversation_count += 1

    # 自动保存
    if st.session_state.get('auto_save_enabled', True):
        auto_save_chat()

    if success:
        st.success("回复已生成并保存")
    else:
        st.error("生成失败")
    
    st.rerun()

def main():
    """主程序"""
    # 应用样式和JavaScript
    apply_light_theme()
    init_local_storage()
    
    # 初始化
    initialize_chat_session()
    
    # 渲染界面
    render_header()
    render_storage_controls()  # 新增存储控制面板
    
    # API配置（简化版）
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("#### 🔧 API配置")
    api_key = st.text_input("GitHub Models API密钥", 
                           value=st.session_state.github_api_key,
                           type="password")
    if api_key != st.session_state.github_api_key:
        st.session_state.github_api_key = api_key
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 聊天界面
    render_chat_history()
    
    # 输入区域
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("#### ✨ 开始对话")
    user_input = st.text_area("", placeholder="输入您的问题...", height=80, key="chat_input")
    
    if st.button("发送消息", type="primary"):
        if user_input.strip():
            process_chat_message(user_input.strip())
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 页脚
    st.markdown(f"""
    <div style="text-align: center; margin-top: 2rem; padding: 1rem; color: #94a3b8; font-size: 0.9rem;">
        <p>🤖 支持本地存储的AI对话平台</p>
        <p>当前用户：Kikyo-acd | 时间：2025-08-08 09:51:23 UTC</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
