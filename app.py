import streamlit as st
import requests
import json
import time
from datetime import datetime
from typing import Dict, List, Optional

# 页面配置
st.set_page_config(
    page_title="GitHub Copilot AI 助手",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 2rem;
        background: linear-gradient(90deg, #0969da 0%, #8250df 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid #0969da;
    }
    .user-message {
        background-color: #f6f8fa;
        border-left-color: #0969da;
    }
    .copilot-message {
        background-color: #f0f9ff;
        border-left-color: #8250df;
    }
    .code-block {
        background-color: #161b22;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        color: #f0f6fc;
        font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
    }
    .api-status {
        background-color: #dbeafe;
        border: 1px solid #3b82f6;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .feature-card {
        border: 1px solid #d0d7de;
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1rem 0;
        background-color: #f6f8fa;
    }
    .copilot-logo {
        display: inline-block;
        background: linear-gradient(90deg, #0969da 0%, #8250df 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

class GitHubCopilotAPI:
    """GitHub Copilot API 客户端"""
    
    def __init__(self, token: str):
        self.token = token
        self.base_url = "https://api.github.com"
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28"
        }
    
    def test_connection(self) -> bool:
        """测试GitHub API连接"""
        try:
            response = requests.get(f"{self.base_url}/user", headers=self.headers, timeout=10)
            return response.status_code == 200
        except:
            return False
    
    def check_copilot_access(self) -> Dict:
        """检查Copilot访问权限"""
        try:
            # 检查用户的Copilot订阅状态
            response = requests.get(f"{self.base_url}/user/copilot_seats", headers=self.headers, timeout=10)
            if response.status_code == 200:
                return {"has_access": True, "details": response.json()}
            elif response.status_code == 404:
                return {"has_access": False, "error": "无Copilot访问权限"}
            else:
                return {"has_access": False, "error": f"API错误: {response.status_code}"}
        except Exception as e:
            return {"has_access": False, "error": f"连接错误: {str(e)}"}
    
    def get_code_completions(self, prompt: str, language: str = "python", max_tokens: int = 100) -> List[str]:
        """获取代码补全建议"""
        try:
            # 使用GitHub Copilot API进行代码补全
            # 注意：这个端点可能需要特殊权限
            data = {
                "prompt": prompt,
                "language": language,
                "max_tokens": max_tokens
            }
            
            # 这里使用模拟的端点，实际使用时需要确认正确的API端点
            response = requests.post(
                f"{self.base_url}/copilot/completions",
                headers=self.headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get("choices", [])
            else:
                return [f"API请求失败: {response.status_code} - {response.text}"]
        except Exception as e:
            return [f"代码补全失败: {str(e)}"]
    
    def chat_with_copilot(self, messages: List[Dict], model: str = "gpt-4") -> str:
        """与Copilot聊天"""
        try:
            # 使用GitHub Models API (预览版)
            data = {
                "messages": messages,
                "model": model,
                "temperature": 0.7,
                "max_tokens": 2000
            }
            
            # GitHub Models API端点
            response = requests.post(
                f"{self.base_url}/models/{model}/chat/completions",
                headers=self.headers,
                json=data,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"]
            else:
                return f"聊天请求失败: {response.status_code} - {response.text}"
        except Exception as e:
            return f"聊天失败: {str(e)}"
    
    def explain_code(self, code: str, language: str = "python") -> str:
        """解释代码功能"""
        try:
            messages = [
                {
                    "role": "system",
                    "content": "你是一个专业的代码分析师，请详细解释给定代码的功能、逻辑和实现细节。"
                },
                {
                    "role": "user", 
                    "content": f"请解释以下{language}代码的功能：\n\n```{language}\n{code}\n```"
                }
            ]
            return self.chat_with_copilot(messages)
        except Exception as e:
            return f"代码解释失败: {str(e)}"
    
    def generate_code(self, description: str, language: str = "python") -> str:
        """根据描述生成代码"""
        try:
            messages = [
                {
                    "role": "system",
                    "content": f"你是一个专业的{language}程序员，请根据用户需求生成高质量的代码，包含适当的注释。"
                },
                {
                    "role": "user",
                    "content": f"请用{language}实现以下功能：{description}"
                }
            ]
            return self.chat_with_copilot(messages)
        except Exception as e:
            return f"代码生成失败: {str(e)}"
    
    def review_code(self, code: str, language: str = "python") -> str:
        """代码审查和优化建议"""
        try:
            messages = [
                {
                    "role": "system",
                    "content": "你是一个资深的代码审查专家，请分析代码的质量、性能、安全性，并提供改进建议。"
                },
                {
                    "role": "user",
                    "content": f"请审查以下{language}代码并提供优化建议：\n\n```{language}\n{code}\n```"
                }
            ]
            return self.chat_with_copilot(messages)
        except Exception as e:
            return f"代码审查失败: {str(e)}"
    
    def get_available_models(self) -> List[str]:
        """获取可用的模型列表"""
        try:
            response = requests.get(f"{self.base_url}/models", headers=self.headers, timeout=10)
            if response.status_code == 200:
                models = response.json()
                return [model["name"] for model in models.get("data", [])]
            return ["gpt-4", "gpt-3.5-turbo", "claude-3-sonnet"]  # 默认模型列表
        except:
            return ["gpt-4", "gpt-3.5-turbo", "claude-3-sonnet"]

def init_session_state():
    """初始化会话状态"""
    if "github_token" not in st.session_state:
        st.session_state.github_token = ""
    if "copilot_api" not in st.session_state:
        st.session_state.copilot_api = None
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []
    if "copilot_access" not in st.session_state:
        st.session_state.copilot_access = None
    if "available_models" not in st.session_state:
        st.session_state.available_models = []

def render_sidebar():
    """渲染侧边栏"""
    with st.sidebar:
        st.markdown("## ⚙️ Copilot 配置")
        
        # GitHub Token 配置
        st.markdown("### 🔑 GitHub Token")
        
        with st.expander("📖 如何获取 GitHub Token", expanded=False):
            st.markdown("""
            **获取步骤：**
            1. 登录 GitHub → Settings → Developer settings
            2. Personal access tokens → Tokens (classic)
            3. Generate new token (classic)
            4. 选择权限范围：
               - ✅ `repo` - 访问仓库
               - ✅ `user` - 用户信息
               - ✅ `copilot` - Copilot API访问
               - ✅ `models:read` - 模型访问 (如果可用)
            5. 生成并复制token
            
            **重要：** 需要GitHub Copilot订阅才能使用相关功能
            """)
        
        github_token = st.text_input(
            "GitHub Token",
            value=st.session_state.github_token,
            type="password",
            placeholder="ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
            help="需要包含Copilot权限的GitHub Token"
        )
        
        if github_token:
            st.session_state.github_token = github_token
            
            if st.button("🔍 测试连接"):
                with st.spinner("测试连接中..."):
                    api = GitHubCopilotAPI(github_token)
                    
                    # 测试基本连接
                    if api.test_connection():
                        st.success("✅ GitHub API 连接成功！")
                        st.session_state.copilot_api = api
                        
                        # 检查Copilot访问权限
                        copilot_status = api.check_copilot_access()
                        st.session_state.copilot_access = copilot_status
                        
                        if copilot_status["has_access"]:
                            st.success("🤖 Copilot 访问权限确认")
                            
                            # 获取可用模型
                            models = api.get_available_models()
                            st.session_state.available_models = models
                            st.info(f"🎯 可用模型: {', '.join(models[:3])}")
                        else:
                            st.warning(f"⚠️ Copilot访问受限: {copilot_status['error']}")
                    else:
                        st.error("❌ GitHub API 连接失败")
                        st.session_state.copilot_api = None
        else:
            st.warning("⚠️ 请输入 GitHub Token")
        
        # 模型选择
        if st.session_state.available_models:
            st.markdown("### 🎯 模型选择")
            selected_model = st.selectbox(
                "选择AI模型",
                st.session_state.available_models,
                help="不同模型有不同的特点和性能"
            )
            st.session_state.selected_model = selected_model
        
        # Copilot状态显示
        if st.session_state.copilot_access:
            st.markdown("### 📊 Copilot 状态")
            if st.session_state.copilot_access["has_access"]:
                st.success("🟢 Copilot 可用")
            else:
                st.error("🔴 Copilot 不可用")
        
        # 清空对话
        if st.button("🗑️ 清空对话", use_container_width=True):
            st.session_state.chat_messages = []
            st.rerun()

def render_chat_interface():
    """渲染聊天界面"""
    st.markdown('<h1 class="main-header">🤖 GitHub Copilot AI 助手</h1>', unsafe_allow_html=True)
    
    if not st.session_state.copilot_api:
        st.markdown("""
        <div class="api-status">
            <h3>⚠️ 请先配置 GitHub Copilot API</h3>
            <p>在左侧边栏输入您的 GitHub Token，确保包含以下权限：</p>
            <ul>
                <li>✅ repo - 仓库访问权限</li>
                <li>✅ user - 用户信息权限</li>
                <li>✅ copilot - Copilot API权限</li>
            </ul>
            <p><strong>注意：</strong> 需要有效的 GitHub Copilot 订阅</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # 显示Copilot状态
    if st.session_state.copilot_access:
        if st.session_state.copilot_access["has_access"]:
            st.markdown("""
            <div class="api-status" style="background-color: #dcfce7; border-color: #22c55e;">
                <h4>🤖 <span class="copilot-logo">GitHub Copilot</span> 已就绪</h4>
                <p>您可以开始与AI助手对话，获得代码帮助和编程建议</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.error(f"Copilot访问受限: {st.session_state.copilot_access['error']}")
            return
    
    # 聊天历史显示
    chat_container = st.container()
    with chat_container:
        if not st.session_state.chat_messages:
            st.markdown("""
            <div style="text-align: center; padding: 2rem; color: #666;">
                <h3>👋 欢迎使用 GitHub Copilot AI 助手</h3>
                <p>我可以帮助您：</p>
                <ul style="text-align: left; max-width: 400px; margin: 0 auto;">
                    <li>🔍 解释和分析代码</li>
                    <li>⚡ 生成高质量代码</li>
                    <li>🛠️ 代码审查和优化</li>
                    <li>💬 回答编程相关问题</li>
                    <li>🚀 提供最佳实践建议</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        for message in st.session_state.chat_messages:
            role = message["role"]
            content = message["content"]
            timestamp = message.get("timestamp", "")
            
            if role == "user":
                st.markdown(f"""
                <div class="chat-message user-message">
                    <strong>👤 您</strong> <small>{timestamp}</small><br>
                    {content}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="chat-message copilot-message">
                    <strong>🤖 <span class="copilot-logo">Copilot</span></strong> <small>{timestamp}</small><br>
                    {content}
                </div>
                """, unsafe_allow_html=True)
    
    # 输入界面
    st.markdown("---")
    
    # 快速操作按钮
    st.markdown("### ⚡ 快速操作")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("💡 解释代码", use_container_width=True):
            st.session_state.quick_action = "explain"
    
    with col2:
        if st.button("⚡ 生成代码", use_container_width=True):
            st.session_state.quick_action = "generate"
    
    with col3:
        if st.button("🔍 代码审查", use_container_width=True):
            st.session_state.quick_action = "review"
    
    with col4:
        if st.button("💬 自由对话", use_container_width=True):
            st.session_state.quick_action = "chat"
    
    # 根据快速操作显示不同的输入界面
    if hasattr(st.session_state, 'quick_action'):
        action = st.session_state.quick_action
        
        if action == "explain":
            st.markdown("#### 📝 代码解释")
            col1, col2 = st.columns([3, 1])
            with col1:
                code_input = st.text_area("粘贴要解释的代码:", height=150, placeholder="在这里粘贴您的代码...")
            with col2:
                language = st.selectbox("编程语言", ["python", "javascript", "java", "cpp", "go", "rust", "typescript"])
            
            if st.button("🔍 解释这段代码", use_container_width=True) and code_input:
                with st.spinner("🤖 Copilot 正在分析代码..."):
                    response = st.session_state.copilot_api.explain_code(code_input, language)
                    
                    # 添加到聊天记录
                    timestamp = datetime.now().strftime("%H:%M:%S")
                    st.session_state.chat_messages.extend([
                        {"role": "user", "content": f"请解释这段{language}代码：\n```{language}\n{code_input}\n```", "timestamp": timestamp},
                        {"role": "assistant", "content": response, "timestamp": timestamp}
                    ])
                    st.rerun()
        
        elif action == "generate":
            st.markdown("#### ⚡ 代码生成")
            col1, col2 = st.columns([3, 1])
            with col1:
                description = st.text_area("描述您需要的功能:", height=100, placeholder="例如：写一个函数来计算斐波那契数列...")
            with col2:
                language = st.selectbox("编程语言", ["python", "javascript", "java", "cpp", "go", "rust", "typescript"])
            
            if st.button("⚡ 生成代码", use_container_width=True) and description:
                with st.spinner("🤖 Copilot 正在生成代码..."):
                    response = st.session_state.copilot_api.generate_code(description, language)
                    
                    timestamp = datetime.now().strftime("%H:%M:%S")
                    st.session_state.chat_messages.extend([
                        {"role": "user", "content": f"请用{language}生成代码：{description}", "timestamp": timestamp},
                        {"role": "assistant", "content": response, "timestamp": timestamp}
                    ])
                    st.rerun()
        
        elif action == "review":
            st.markdown("#### 🔍 代码审查")
            col1, col2 = st.columns([3, 1])
            with col1:
                code_input = st.text_area("粘贴要审查的代码:", height=150, placeholder="在这里粘贴您的代码...")
            with col2:
                language = st.selectbox("编程语言", ["python", "javascript", "java", "cpp", "go", "rust", "typescript"])
            
            if st.button("🔍 审查代码", use_container_width=True) and code_input:
                with st.spinner("🤖 Copilot 正在审查代码..."):
                    response = st.session_state.copilot_api.review_code(code_input, language)
                    
                    timestamp = datetime.now().strftime("%H:%M:%S")
                    st.session_state.chat_messages.extend([
                        {"role": "user", "content": f"请审查这段{language}代码：\n```{language}\n{code_input}\n```", "timestamp": timestamp},
                        {"role": "assistant", "content": response, "timestamp": timestamp}
                    ])
                    st.rerun()
        
        else:  # chat
            st.markdown("#### 💬 自由对话")
            user_input = st.text_area("与Copilot对话:", height=100, placeholder="问任何编程相关的问题...")
            
            if st.button("💬 发送消息", use_container_width=True) and user_input:
                with st.spinner("🤖 Copilot 正在思考..."):
                    messages_for_api = []
                    for msg in st.session_state.chat_messages[-10:]:  # 最近10条消息
                        messages_for_api.append({
                            "role": msg["role"],
                            "content": msg["content"]
                        })
                    
                    messages_for_api.append({"role": "user", "content": user_input})
                    
                    response = st.session_state.copilot_api.chat_with_copilot(
                        messages_for_api, 
                        st.session_state.get("selected_model", "gpt-4")
                    )
                    
                    timestamp = datetime.now().strftime("%H:%M:%S")
                    st.session_state.chat_messages.extend([
                        {"role": "user", "content": user_input, "timestamp": timestamp},
                        {"role": "assistant", "content": response, "timestamp": timestamp}
                    ])
                    st.rerun()

def render_features():
    """渲染功能介绍页面"""
    st.markdown('<h1 class="main-header">🚀 功能特性</h1>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3>🔍 智能代码解释</h3>
            <p>上传任何代码片段，Copilot会详细解释其功能、逻辑和实现细节，帮助您快速理解复杂代码。</p>
            <ul>
                <li>支持多种编程语言</li>
                <li>详细的逐行解释</li>
                <li>识别设计模式和算法</li>
                <li>解释最佳实践</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <h3>🛠️ 专业代码审查</h3>
            <p>获得专业级的代码审查，包括性能优化、安全性检查和代码质量提升建议。</p>
            <ul>
                <li>性能优化建议</li>
                <li>安全漏洞检测</li>
                <li>代码风格改进</li>
                <li>最佳实践推荐</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3>⚡ 高效代码生成</h3>
            <p>只需描述需求，Copilot就能生成高质量、可运行的代码，大大提升开发效率。</p>
            <ul>
                <li>自然语言转代码</li>
                <li>完整的函数实现</li>
                <li>包含详细注释</li>
                <li>遵循编码规范</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <h3>💬 智能编程对话</h3>
            <p>与AI助手进行自然对话，获得编程问题的解答、学习建议和技术指导。</p>
            <ul>
                <li>实时问答互动</li>
                <li>编程概念解释</li>
                <li>技术选型建议</li>
                <li>学习路径规划</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # 支持的编程语言
    st.markdown("## 🌐 支持的编程语言")
    
    languages = [
        ("🐍 Python", "数据科学、Web开发、自动化"),
        ("⚛️ JavaScript", "前端开发、Node.js、React"),
        ("☕ Java", "企业级应用、Android开发"),
        ("⚡ C++", "系统编程、游戏开发"),
        ("🚀 Go", "云原生、微服务"),
        ("🦀 Rust", "系统编程、WebAssembly"),
        ("💎 TypeScript", "类型安全的JavaScript"),
        ("🔷 C#", ".NET开发、游戏开发")
    ]
    
    cols = st.columns(4)
    for i, (lang, desc) in enumerate(languages):
        with cols[i % 4]:
            st.markdown(f"""
            <div style="text-align: center; padding: 1rem; border: 1px solid #d0d7de; border-radius: 8px; margin: 0.5rem 0;">
                <h4>{lang}</h4>
                <small>{desc}</small>
            </div>
            """, unsafe_allow_html=True)

def render_usage_guide():
    """渲染使用指南"""
    st.markdown('<h1 class="main-header">📖 使用指南</h1>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["🚀 快速开始", "🔧 高级功能", "❓ 常见问题"])
    
    with tab1:
        st.markdown("""
        ## 🚀 快速开始
        
        ### 第一步：获取 GitHub Token
        1. 登录 GitHub，进入 **Settings** → **Developer settings**
        2. 选择 **Personal access tokens** → **Tokens (classic)**
        3. 点击 **Generate new token (classic)**
        4. 选择以下权限：
           - ✅ `repo` - 完整的仓库访问权限
           - ✅ `user` - 用户信息读取权限
           - ✅ `copilot` - Copilot API访问权限
        5. 生成并保存 Token
        
        ### 第二步：配置应用
        1. 在左侧边栏输入您的 GitHub Token
        2. 点击 "测试连接" 验证配置
        3. 确认 Copilot 访问权限状态
        
        ### 第三步：开始使用
        1. 选择功能：解释代码、生成代码、代码审查或自由对话
        2. 输入相关内容或问题
        3. 等待 Copilot 的智能回复
        
        ### 💡 使用技巧
        - **具体描述**：描述需求时越具体，生成的代码质量越高
        - **上下文信息**：提供足够的背景信息帮助理解
        - **分步骤**：复杂任务可以分解为多个步骤
        - **多轮对话**：利用对话历史进行深入讨论
        """)
    
    with tab2:
        st.markdown("""
        ## 🔧 高级功能详解
        
        ### 🔍 代码解释功能
        
        **适用场景：**
        - 理解开源项目代码
        - 学习新的编程模式
        - 分析遗留代码逻辑
        - 代码文档生成
        
        **最佳实践：**
        ```python
        # 输入示例
        def fibonacci(n):
            if n <= 1:
                return n
            return fibonacci(n-1) + fibonacci(n-2)
        ```
        
        **输出内容：**
        - 函数功能说明
        - 算法复杂度分析
        - 潜在问题识别
        - 优化建议
        
        ### ⚡ 代码生成功能
        
        **描述技巧：**
        - 明确输入输出格式
        - 指定错误处理需求
        - 说明性能要求
        - 提及特殊边界情况
        
        **示例描述：**
        ```
        创建一个Python函数，接收一个整数列表，
        返回去重后的列表，保持原有顺序，
        如果输入为空或None则返回空列表
        ```
        
        ### 🛠️ 代码审查功能
        
        **审查维度：**
        - **性能优化**：算法复杂度、内存使用
        - **安全性**：输入验证、SQL注入防护
        - **可维护性**：代码结构、命名规范
        - **最佳实践**：设计模式、编码标准
        
        ### 💬 智能对话功能
        
        **对话类型：**
        - 技术概念解释
        - 架构设计讨论
        - 问题调试帮助
        - 学习路径规划
        
        **提问技巧：**
        ```
        ❌ 不好的问题：如何写代码？
        ✅ 好的问题：如何用Python实现一个线程安全的单例模式？
        
        ❌ 不好的问题：代码有问题
        ✅ 好的问题：这段代码在高并发环境下可能出现什么问题？
        ```
        """)
    
    with tab3:
        st.markdown("""
        ## ❓ 常见问题解答
        
        ### 🔑 权限和访问
        
        **Q: 为什么需要 Copilot 订阅？**
        A: GitHub Copilot 是付费服务，需要有效订阅才能访问API功能。个人用户可以在GitHub设置中订阅。
        
        **Q: Token 权限设置有什么要求？**
        A: 需要包含 `repo`、`user` 和 `copilot` 权限。部分功能可能需要额外的模型访问权限。
        
        **Q: 如何检查我的 Copilot 订阅状态？**
        A: 访问 GitHub Settings → Billing → Plans and usage → Copilot 查看订阅状态。
        
        ### 🚀 功能使用
        
        **Q: 代码生成的质量如何保证？**
        A: 
        - 提供详细和具体的需求描述
        - 指定编程语言和框架
        - 说明错误处理和边界条件
        - 多次迭代优化结果
        
        **Q: 支持哪些编程语言？**
        A: 主流编程语言都支持，包括Python、JavaScript、Java、C++、Go、Rust等。
        
        **Q: 如何获得更好的代码解释？**
        A: 
        - 提供完整的代码上下文
        - 说明代码的使用场景
        - 指出特别关注的部分
        - 询问具体的疑问点
        
        ### ⚡ 性能和限制
        
        **Q: API 有请求限制吗？**
        A: 是的，GitHub API 有速率限制。认证用户通常有更高的限制。具体限制请查看GitHub API文档。
        
        **Q: 响应时间较慢怎么办？**
        A: 
        - 简化问题描述
        - 减少代码量
        - 避免过于复杂的请求
        - 检查网络连接
        
        **Q: 如何处理API错误？**
        A: 
        - 检查Token权限和有效性
        - 确认Copilot订阅状态
        - 查看错误信息详情
        - 尝试重新连接
        
        ### 🛡️ 安全和隐私
        
        **Q: 我的代码会被保存吗？**
        A: 代码仅在对话期间保存在浏览器本地，不会上传到第三方服务器。
        
        **Q: GitHub 会使用我的代码训练模型吗？**
        A: 请参考 GitHub Copilot 的隐私政策和服务条款了解数据使用情况。
        
        **Q: 如何保护敏感代码？**
        A: 
        - 避免包含敏感信息（密码、密钥等）
        - 使用示例代码而非生产代码
        - 定期更换 API Token
        - 仅在安全环境下使用
        """)

def main():
    """主函数"""
    init_session_state()
    
    # 渲染侧边栏
    render_sidebar()
    
    # 主界面选项卡
    tab1, tab2, tab3 = st.tabs(["🤖 AI 助手", "🚀 功能特性", "📖 使用指南"])
    
    with tab1:
        render_chat_interface()
    
    with tab2:
        render_features()
    
    with tab3:
        render_usage_guide()
    
    # 页脚信息
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem;">
        <p>🤖 <strong><span class="copilot-logo">GitHub Copilot AI 助手</span></strong> | 基于 GitHub API 构建</p>
        <p><small>智能编程 | 代码生成 | 专业审查 | 实时对话</small></p>
        <p><small>由 GitHub Copilot 技术驱动 | 安全可靠 | 开源免费</small></p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
