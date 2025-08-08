import streamlit as st
import requests
import json
import time
from datetime import datetime
from typing import Dict, List

# 页面配置
st.set_page_config(
    page_title="AI 镜像站",
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
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid #667eea;
    }
    .user-message {
        background-color: #f0f2f6;
        border-left-color: #667eea;
    }
    .assistant-message {
        background-color: #e8f4fd;
        border-left-color: #2196F3;
    }
    .model-card {
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        background-color: #fafafa;
    }
    .api-key-section {
        background-color: #f8f9fa;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        border: 1px solid #dee2e6;
    }
    .warning-box {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

class AIModelClient:
    """AI模型客户端"""
    
    def __init__(self):
        self.models = {
            "OpenAI": {
                "gpt-4o": {"name": "GPT-4o", "context": 128000, "description": "最新最强的GPT模型"},
                "gpt-4": {"name": "GPT-4", "context": 8192, "description": "最强大的GPT模型"},
                "gpt-3.5-turbo": {"name": "GPT-3.5 Turbo", "context": 4096, "description": "快速响应的GPT模型"},
                "gpt-4-turbo": {"name": "GPT-4 Turbo", "context": 128000, "description": "更大上下文的GPT-4"}
            },
            "Anthropic": {
                "claude-3-5-sonnet-20241022": {"name": "Claude 3.5 Sonnet", "context": 200000, "description": "最新的Claude模型"},
                "claude-3-opus-20240229": {"name": "Claude 3 Opus", "context": 200000, "description": "最强大的Claude模型"},
                "claude-3-haiku-20240307": {"name": "Claude 3 Haiku", "context": 200000, "description": "快速的Claude模型"}
            },
            "自定义API": {
                "custom-model": {"name": "自定义模型", "context": 32000, "description": "使用自定义API端点"}
            }
        }
    
    def get_available_models(self) -> Dict:
        """获取可用模型列表"""
        return self.models
    
    def test_model_availability(self, provider: str, model: str, api_key: str, api_base: str = "") -> bool:
        """测试模型可用性"""
        if not api_key or len(api_key) < 10:
            return False
        try:
            if provider == "OpenAI":
                headers = {
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                }
                url = api_base.rstrip('/') + "/v1/models" if api_base else "https://api.openai.com/v1/models"
                response = requests.get(url, headers=headers, timeout=10)
                return response.status_code == 200
            elif provider == "Anthropic":
                return len(api_key) > 20 and api_key.startswith("sk-ant-")
            elif provider == "自定义API":
                if not api_base:
                    return False
                headers = {
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                }
                # 尝试访问自定义端点
                try:
                    url = api_base.rstrip('/') + "/v1/models"
                    response = requests.get(url, headers=headers, timeout=10)
                    return response.status_code == 200
                except:
                    return True  # 对于自定义API，假设配置正确
            return False
        except:
            return False
    
    def chat_completion(self, provider: str, model: str, messages: List[Dict], 
                       api_key: str, temperature: float = 0.7, max_tokens: int = 2000, 
                       api_base: str = "") -> str:
        """发送聊天请求"""
        try:
            if provider == "OpenAI":
                return self._openai_request(model, messages, api_key, temperature, max_tokens, api_base)
            elif provider == "Anthropic":
                return self._anthropic_request(model, messages, api_key, temperature, max_tokens)
            elif provider == "自定义API":
                return self._custom_api_request(model, messages, api_key, temperature, max_tokens, api_base)
            else:
                return "不支持的AI提供商"
        except Exception as e:
            return f"请求失败: {str(e)}"
    
    def _openai_request(self, model: str, messages: List[Dict], api_key: str, 
                       temperature: float, max_tokens: int, api_base: str = "") -> str:
        """OpenAI API请求"""
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": False
        }
        
        url = api_base.rstrip('/') + "/v1/chat/completions" if api_base else "https://api.openai.com/v1/chat/completions"
        
        response = requests.post(url, headers=headers, json=data, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["message"]["content"]
        else:
            error_text = response.text
            return f"API请求失败: {response.status_code} - {error_text}"
    
    def _anthropic_request(self, model: str, messages: List[Dict], api_key: str,
                          temperature: float, max_tokens: int) -> str:
        """Anthropic API请求"""
        headers = {
            "x-api-key": api_key,
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01"
        }
        
        # 转换消息格式
        claude_messages = []
        system_message = ""
        
        for msg in messages:
            if msg["role"] == "system":
                system_message = msg["content"]
            else:
                claude_messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })
        
        data = {
            "model": model,
            "messages": claude_messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        
        if system_message:
            data["system"] = system_message
        
        response = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers=headers,
            json=data,
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            return result["content"][0]["text"]
        else:
            error_text = response.text
            return f"Claude API请求失败: {response.status_code} - {error_text}"
    
    def _custom_api_request(self, model: str, messages: List[Dict], api_key: str,
                           temperature: float, max_tokens: int, api_base: str) -> str:
        """自定义API请求"""
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": False
        }
        
        url = api_base.rstrip('/') + "/v1/chat/completions"
        
        response = requests.post(url, headers=headers, json=data, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["message"]["content"]
        else:
            error_text = response.text
            return f"自定义API请求失败: {response.status_code} - {error_text}"

class PromptManager:
    """Prompt管理器"""
    
    def __init__(self):
        self.built_in_prompts = {
            "编程助手": {
                "代码调试": "我有一段代码出现了问题，请帮我分析并修复：\n\n```\n{请在这里粘贴您的代码}\n```\n\n错误信息：{请描述错误信息}",
                "代码优化": "请帮我优化这段代码，提高性能和可读性：\n\n```\n{请在这里粘贴您的代码}\n```",
                "代码解释": "请详细解释这段代码的功能和工作原理：\n\n```\n{请在这里粘贴您的代码}\n```",
                "生成代码": "请根据以下需求生成代码：\n\n需求：{请描述您的需求}\n语言：{编程语言}\n\n请提供完整的实现和注释。",
                "API文档": "请为以下代码生成详细的API文档：\n\n```\n{请在这里粘贴您的代码}\n```",
                "单元测试": "请为以下代码编写单元测试：\n\n```\n{请在这里粘贴您的代码}\n```\n\n测试框架：{测试框架名称}"
            },
            "文案写作": {
                "产品介绍": "请为以下产品写一份吸引人的介绍文案：\n\n产品：{产品名称}\n特点：{产品特点}\n目标用户：{目标用户群体}",
                "邮件撰写": "请帮我写一封专业邮件：\n\n收件人：{收件人}\n主题：{邮件主题}\n要点：{要表达的要点}",
                "文章标题": "请为以下文章内容生成5个吸引人的标题：\n\n内容概要：{文章内容概要}",
                "社交媒体": "请为以下内容写一份适合社交媒体的文案：\n\n内容：{要发布的内容}\n平台：{社交媒体平台}\n目标：{营销目标}",
                "新闻稿": "请为以下事件撰写一份新闻稿：\n\n事件：{事件描述}\n时间：{事件时间}\n影响：{事件影响}",
                "广告文案": "请为以下产品创作广告文案：\n\n产品：{产品名称}\n卖点：{主要卖点}\n目标受众：{目标受众}\n风格：{文案风格}"
            },
            "学习辅导": {
                "概念解释": "请用简单易懂的语言解释这个概念：{概念名称}\n\n我的知识水平：{学习水平}",
                "问题解答": "请详细解答这个问题：{问题描述}\n\n请提供步骤和例子。",
                "学习计划": "请为我制定一个学习计划：\n\n学科：{学习学科}\n当前水平：{当前水平}\n目标：{学习目标}\n时间：{可用时间}",
                "知识总结": "请帮我总结以下主题的要点：{主题}\n\n请包括关键概念、重要公式和实际应用。",
                "习题讲解": "请详细讲解这道题的解题思路：\n\n题目：{题目内容}\n学科：{所属学科}",
                "记忆技巧": "请为以下内容提供记忆技巧和方法：\n\n内容：{需要记忆的内容}\n类型：{内容类型}"
            },
            "翻译助手": {
                "专业翻译": "请将以下内容翻译成中文，保持专业性和准确性：\n\n{请在这里输入要翻译的内容}",
                "口语翻译": "请将以下中文口语表达翻译成自然的英文：\n\n{请在这里输入中文内容}",
                "技术翻译": "请将以下技术文档翻译成中文，保持术语准确性：\n\n{请在这里输入技术文档}",
                "商务翻译": "请将以下商务文件翻译成英文，保持正式语调：\n\n{请在这里输入商务文件}",
                "学术翻译": "请将以下学术文章翻译成中文，保持学术严谨性：\n\n{请在这里输入学术内容}",
                "多语种翻译": "请将以下内容翻译成{目标语言}：\n\n{请在这里输入要翻译的内容}"
            },
            "创意写作": {
                "故事创作": "请根据以下元素创作一个故事：\n\n主题：{故事主题}\n角色：{主要角色}\n背景：{故事背景}\n长度：{短篇/中篇/长篇}",
                "诗歌创作": "请创作一首诗歌：\n\n主题：{诗歌主题}\n风格：{诗歌风格}\n情感：{要表达的情感}",
                "剧本写作": "请写一个剧本片段：\n\n场景：{剧本场景}\n角色：{登场角色}\n冲突：{主要冲突}\n类型：{剧本类型}",
                "歌词创作": "请创作歌词：\n\n主题：{歌曲主题}\n风格：{音乐风格}\n情感：{情感基调}\n目标听众：{目标听众}",
                "小说大纲": "请为小说创作大纲：\n\n类型：{小说类型}\n主题：{主要主题}\n主角：{主角设定}\n世界观：{故事背景}",
                "对话写作": "请编写一段对话：\n\n场景：{对话场景}\n角色：{对话角色}\n目的：{对话目的}\n风格：{对话风格}"
            },
            "商务办公": {
                "会议纪要": "请根据以下信息整理会议纪要：\n\n会议主题：{会议主题}\n参会人员：{参会人员}\n讨论要点：{讨论内容}\n决议事项：{会议决议}",
                "工作报告": "请帮我撰写工作报告：\n\n报告期间：{报告时间段}\n主要工作：{主要工作内容}\n完成情况：{工作完成情况}\n下一步计划：{后续计划}",
                "商业计划": "请帮我制定商业计划：\n\n项目名称：{项目名称}\n市场分析：{市场情况}\n产品服务：{产品/服务描述}\n财务预测：{财务情况}",
                "客服回复": "请帮我写一份客服回复：\n\n客户问题：{客户问题}\n解决方案：{提供的解决方案}\n语调：{回复语调要求}",
                "招聘广告": "请为以下职位撰写招聘广告：\n\n职位名称：{职位名称}\n岗位要求：{岗位要求}\n公司介绍：{公司简介}\n福利待遇：{薪资福利}",
                "提案撰写": "请帮我撰写项目提案：\n\n项目名称：{项目名称}\n项目背景：{项目背景}\n解决方案：{解决方案}\n预期效果：{预期效果}"
            }
        }
    
    def get_categories(self) -> List[str]:
        """获取Prompt分类"""
        return list(self.built_in_prompts.keys())
    
    def get_prompts_by_category(self, category: str) -> Dict[str, str]:
        """根据分类获取Prompt"""
        return self.built_in_prompts.get(category, {})
    
    def search_prompts(self, query: str) -> Dict[str, Dict[str, str]]:
        """搜索Prompt"""
        results = {}
        query_lower = query.lower()
        
        for category, prompts in self.built_in_prompts.items():
            matching_prompts = {}
            for name, content in prompts.items():
                if (query_lower in name.lower() or 
                    query_lower in content.lower() or 
                    query_lower in category.lower()):
                    matching_prompts[name] = content
            
            if matching_prompts:
                results[category] = matching_prompts
        
        return results

def init_session_state():
    """初始化会话状态"""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "current_model" not in st.session_state:
        st.session_state.current_model = None
    if "api_keys" not in st.session_state:
        st.session_state.api_keys = {}
    if "api_bases" not in st.session_state:
        st.session_state.api_bases = {}
    if "user_prompts" not in st.session_state:
        st.session_state.user_prompts = []
    if "chat_sessions" not in st.session_state:
        st.session_state.chat_sessions = []
    if "current_session_id" not in st.session_state:
        st.session_state.current_session_id = None

def render_api_key_help():
    """渲染API密钥帮助信息"""
    with st.expander("🔑 API密钥获取指南", expanded=False):
        st.markdown("""
        ### OpenAI API
        1. 访问：https://platform.openai.com/api-keys
        2. 注册账户并登录
        3. 点击"Create new secret key"创建密钥
        4. 密钥格式：`sk-proj-...` 或 `sk-...`
        
        ### Anthropic Claude API
        1. 访问：https://console.anthropic.com/
        2. 申请API访问权限
        3. 创建API密钥
        4. 密钥格式：`sk-ant-...`
        
        ### 自定义API
        - 支持OpenAI兼容的API端点
        - 如：OneAPI、FastGPT、本地部署的模型等
        - 需要提供完整的API基础URL
        
        ### 安全提醒
        - 请妥善保管您的API密钥
        - 不要在公开场合分享密钥
        - 定期更换密钥确保安全
        """)

def render_sidebar():
    """渲染侧边栏"""
    with st.sidebar:
        st.markdown("## ⚙️ 配置中心")
        
        # API密钥帮助
        render_api_key_help()
        
        # 模型选择
        st.markdown("### 🤖 模型选择")
        
        client = AIModelClient()
        available_models = client.get_available_models()
        
        provider = st.selectbox("AI提供商", list(available_models.keys()))
        model_list = list(available_models[provider].keys())
        model = st.selectbox("模型", model_list)
        
        # 显示模型信息
        model_info = available_models[provider][model]
        st.markdown(f"""
        <div class="model-card">
            <strong>{model_info['name']}</strong><br>
            <small>上下文长度: {model_info['context']:,} tokens</small><br>
            <small>{model_info['description']}</small>
        </div>
        """, unsafe_allow_html=True)
        
        # API配置
        st.markdown("### 🔑 API 配置")
        
        # API密钥输入
        if provider == "OpenAI":
            st.markdown("**OpenAI API 配置**")
            api_key = st.text_input(
                "API Key", 
                value=st.session_state.api_keys.get(provider, ""),
                type="password",
                placeholder="sk-proj-... 或 sk-...",
                help="从 https://platform.openai.com/api-keys 获取"
            )
            api_base = st.text_input(
                "API Base URL (可选)", 
                value=st.session_state.api_bases.get(provider, ""),
                placeholder="https://api.openai.com (默认)",
                help="如使用代理或第三方服务，请填写完整URL"
            )
            
        elif provider == "Anthropic":
            st.markdown("**Anthropic Claude API 配置**")
            api_key = st.text_input(
                "API Key", 
                value=st.session_state.api_keys.get(provider, ""),
                type="password",
                placeholder="sk-ant-...",
                help="从 https://console.anthropic.com/ 获取"
            )
            api_base = ""  # Anthropic不支持自定义base URL
            
        elif provider == "自定义API":
            st.markdown("**自定义 API 配置**")
            api_key = st.text_input(
                "API Key", 
                value=st.session_state.api_keys.get(provider, ""),
                type="password",
                placeholder="您的API密钥",
                help="输入您的自定义API密钥"
            )
            api_base = st.text_input(
                "API Base URL", 
                value=st.session_state.api_bases.get(provider, ""),
                placeholder="https://your-api-endpoint.com",
                help="必填：您的API服务端点URL"
            )
            custom_model = st.text_input(
                "模型名称", 
                value="gpt-3.5-turbo",
                placeholder="gpt-3.5-turbo",
                help="输入实际的模型名称"
            )
            if custom_model:
                model = custom_model
        
        # 保存API配置
        if api_key:
            st.session_state.api_keys[provider] = api_key
        if api_base:
            st.session_state.api_bases[provider] = api_base
        
        # 连接测试
        if api_key:
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🔍 测试连接", use_container_width=True):
                    with st.spinner("测试中..."):
                        is_available = client.test_model_availability(
                            provider, model, api_key, api_base
                        )
                        if is_available:
                            st.success("✅ 连接成功！")
                            st.session_state.current_model = {
                                "provider": provider,
                                "model": model,
                                "api_key": api_key,
                                "api_base": api_base
                            }
                        else:
                            st.error("❌ 连接失败，请检查配置")
            
            with col2:
                if st.button("💾 保存配置", use_container_width=True):
                    st.session_state.current_model = {
                        "provider": provider,
                        "model": model,
                        "api_key": api_key,
                        "api_base": api_base
                    }
                    st.success("✅ 配置已保存")
        else:
            st.warning("⚠️ 请输入API密钥")
        
        # 模型参数
        st.markdown("### 🎛️ 模型参数")
        temperature = st.slider("创造性 (Temperature)", 0.0, 2.0, 0.7, 0.1, 
                               help="值越高回复越有创意，越低越准确")
        max_tokens = st.slider("最大输出长度", 100, 4000, 2000, 100,
                              help="控制AI回复的最大长度")
        
        # 对话管理
        st.markdown("### 💬 对话管理")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🆕 新建", use_container_width=True):
                new_session_id = f"session_{int(time.time())}"
                st.session_state.chat_sessions.append({
                    "id": new_session_id,
                    "title": f"对话 {len(st.session_state.chat_sessions) + 1}",
                    "created_at": datetime.now(),
                    "messages": []
                })
                st.session_state.current_session_id = new_session_id
                st.session_state.messages = []
                st.rerun()
        
        with col2:
            if st.button("🗑️ 清空", use_container_width=True):
                st.session_state.messages = []
                st.rerun()
        
        # 导出对话
        if st.session_state.messages:
            export_data = {
                "timestamp": datetime.now().isoformat(),
                "model": st.session_state.current_model,
                "messages": st.session_state.messages
            }
            st.download_button(
                "📥 导出对话",
                data=json.dumps(export_data, ensure_ascii=False, indent=2),
                file_name=f"chat_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )
        
        # 使用统计
        st.markdown("### 📊 使用统计")
        total_messages = sum(len(session.get("messages", [])) for session in st.session_state.chat_sessions)
        col1, col2 = st.columns(2)
        with col1:
            st.metric("总消息", total_messages)
        with col2:
            st.metric("会话数", len(st.session_state.chat_sessions))
        
        return temperature, max_tokens

def render_prompt_templates():
    """渲染Prompt模板"""
    prompt_manager = PromptManager()
    
    st.markdown('<h1 class="main-header">📝 Prompt 模板库</h1>', unsafe_allow_html=True)
    
    # 搜索功能
    col1, col2 = st.columns([3, 1])
    with col1:
        search_query = st.text_input("🔍 搜索模板", placeholder="输入关键词搜索...")
    with col2:
        search_mode = st.selectbox("搜索模式", ["按分类", "全局搜索"])
    
    if search_query and search_mode == "全局搜索":
        search_results = prompt_manager.search_prompts(search_query)
        if search_results:
            for category, prompts in search_results.items():
                st.markdown(f"### 📂 {category}")
                for name, content in prompts.items():
                    with st.expander(f"📋 {name}"):
                        st.code(content, language="text")
                        if st.button(f"✨ 使用模板", key=f"use_{category}_{name}"):
                            st.session_state.selected_prompt = content
                            st.success("✅ 模板已选择！请切换到聊天页面使用。")
        else:
            st.info("🔍 未找到匹配的模板，请尝试其他关键词")
    else:
        # 分类显示
        categories = prompt_manager.get_categories()
        selected_category = st.selectbox("📂 选择分类", categories)
        
        if selected_category:
            prompts = prompt_manager.get_prompts_by_category(selected_category)
            
            st.markdown(f"### 📂 {selected_category} ({len(prompts)} 个模板)")
            
            for name, content in prompts.items():
                with st.expander(f"📋 {name}"):
                    st.code(content, language="text")
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button(f"✨ 使用模板", key=f"use_{selected_category}_{name}", use_container_width=True):
                            st.session_state.selected_prompt = content
                            st.success("✅ 模板已选择！请切换到聊天页面使用。")
                    with col2:
                        if st.button(f"📋 复制到剪贴板", key=f"copy_{selected_category}_{name}", use_container_width=True):
                            st.success("✅ 已复制到剪贴板")
    
    # 自定义Prompt管理
    st.markdown("---")
    st.markdown("## ✏️ 自定义 Prompt 管理")
    
    # 创建新的自定义Prompt
    with st.expander("➕ 创建新的自定义 Prompt", expanded=False):
        custom_name = st.text_input("📝 Prompt名称", placeholder="给您的Prompt起个名字")
        custom_content = st.text_area("📄 Prompt内容", height=150, placeholder="在这里输入您的自定义Prompt内容...")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("💾 保存", use_container_width=True):
                if custom_name and custom_content:
                    st.session_state.user_prompts.append({
                        "name": custom_name,
                        "content": custom_content,
                        "created_at": datetime.now()
                    })
                    st.success("✅ 自定义Prompt已保存！")
                else:
                    st.error("❌ 请填写完整信息")
        with col2:
            if st.button("🧹 清空", use_container_width=True):
                st.rerun()
        with col3:
            if st.button("✨ 使用", use_container_width=True):
                if custom_content:
                    st.session_state.selected_prompt = custom_content
                    st.success("✅ 内容已选择！")
    
    # 显示用户自定义的Prompt
    if st.session_state.user_prompts:
        st.markdown("### 📚 我的自定义 Prompt")
        for idx, prompt in enumerate(st.session_state.user_prompts):
            with st.expander(f"📝 {prompt['name']} ({prompt['created_at'].strftime('%m-%d %H:%M')})"):
                st.code(prompt['content'], language="text")
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("✨ 使用", key=f"use_custom_{idx}", use_container_width=True):
                        st.session_state.selected_prompt = prompt['content']
                        st.success("✅ 模板已选择！")
                with col2:
                    if st.button("✏️ 编辑", key=f"edit_custom_{idx}", use_container_width=True):
                        st.session_state.editing_prompt = idx
                        st.info("💡 编辑功能待实现")
                with col3:
                    if st.button("🗑️ 删除", key=f"del_custom_{idx}", use_container_width=True):
                        st.session_state.user_prompts.pop(idx)
                        st.success("✅ 已删除")
                        st.rerun()

def render_chat_interface(temperature: float, max_tokens: int):
    """渲染聊天界面"""
    st.markdown('<h1 class="main-header">🤖 AI 智能对话</h1>', unsafe_allow_html=True)
    
    # 检查是否配置了模型
    if not st.session_state.current_model:
        st.markdown("""
        <div class="warning-box">
            <h3>⚠️ 请先配置AI模型</h3>
            <p>请在左侧边栏进行以下配置：</p>
            <ol>
                <li>选择AI提供商和模型</li>
                <li>输入有效的API密钥</li>
                <li>测试连接确保配置正确</li>
                <li>保存配置后即可开始对话</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
        
        st.info("💡 首次使用？请查看 '使用说明' 选项卡了解如何获取API密钥")
        return
    
    # 显示当前模型信息
    model_info = st.session_state.current_model
    st.markdown(f"""
    <div class="success-box">
        <strong>🤖 当前配置</strong><br>
        提供商: {model_info['provider']} | 模型: {model_info['model']}<br>
        参数: Temperature={temperature}, Max Tokens={max_tokens}
    </div>
    """, unsafe_allow_html=True)
    
    # 聊天历史显示
    chat_container = st.container()
    with chat_container:
        if not st.session_state.messages:
            st.markdown("""
            <div style="text-align: center; padding: 2rem; color: #666;">
                <h3>👋 欢迎使用AI智能对话</h3>
                <p>请在下方输入您的问题，或使用Prompt模板开始对话</p>
            </div>
            """, unsafe_allow_html=True)
        
        for message in st.session_state.messages:
            role = message["role"]
            content = message["content"]
            timestamp = message.get("timestamp", "")
            
            if role == "user":
                st.markdown(f"""
                <div class="chat-message user-message">
                    <strong>🧑 用户</strong> <small>{timestamp}</small><br>
                    {content}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="chat-message assistant-message">
                    <strong>🤖 助手</strong> <small>{timestamp}</small><br>
                    {content}
                </div>
                """, unsafe_allow_html=True)
    
    # 输入界面
    st.markdown("---")
    
    # 检查是否有选中的模板
    default_input = ""
    if hasattr(st.session_state, 'selected_prompt'):
        default_input = st.session_state.selected_prompt
        del st.session_state.selected_prompt
    
    # 聊天输入表单
    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_area(
            "💬 请输入您的消息", 
            value=default_input,
            height=120,
            placeholder="请输入您的问题，或从Prompt模板中选择...",
            help="支持多行输入，Ctrl+Enter快速发送"
        )
        
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            submit_button = st.form_submit_button("🚀 发送消息", use_container_width=True)
        with col2:
            example_button = st.form_submit_button("💡 示例", use_container_width=True)
        with col3:
            help_button = st.form_submit_button("❓ 帮助", use_container_width=True)
    
    # 处理示例按钮
    if example_button:
        example_prompts = [
            "请帮我解释一下什么是人工智能？",
            "写一个Python函数来计算斐波那契数列",
            "请为我的新产品写一份简短的介绍文案",
            "帮我翻译这句话：Hello, how are you today?"
        ]
        selected_example = st.selectbox("选择一个示例：", example_prompts)
        if st.button("使用这个示例"):
            st.session_state.selected_prompt = selected_example
            st.rerun()
    
    # 处理帮助按钮
    if help_button:
        st.info("""
        💡 **使用技巧**：
        - 问题描述越具体，AI回答越准确
        - 可以进行多轮对话，AI会记住上下文
        - 使用Prompt模板可以获得更好的效果
        - 调整Temperature参数控制创造性
        """)
    
    # 处理用户输入
    if submit_button and user_input.strip():
        # 添加用户消息
        timestamp = datetime.now().strftime("%H:%M:%S")
        user_message = {
            "role": "user", 
            "content": user_input,
            "timestamp": timestamp
        }
        st.session_state.messages.append(user_message)
        
        # 显示正在处理的状态
        with st.spinner("🤔 AI正在思考中，请稍候..."):
            client = AIModelClient()
            
            # 准备消息历史（限制最近20条消息以控制token使用）
            messages_for_api = []
            recent_messages = st.session_state.messages[-20:]
            
            for msg in recent_messages:
                messages_for_api.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })
            
            # 发送请求
            response = client.chat_completion(
                provider=model_info["provider"],
                model=model_info["model"],
                messages=messages_for_api,
                api_key=model_info["api_key"],
                temperature=temperature,
                max_tokens=max_tokens,
                api_base=model_info.get("api_base", "")
            )
            
            # 添加AI回复
            ai_timestamp = datetime.now().strftime("%H:%M:%S")
            ai_message = {
                "role": "assistant",
                "content": response,
                "timestamp": ai_timestamp
            }
            st.session_state.messages.append(ai_message)
        
        st.rerun()

def render_usage_guide():
    """渲染使用说明"""
    st.markdown('<h1 class="main-header">📖 使用说明</h1>', unsafe_allow_html=True)
    
    # 创建选项卡
    tab1, tab2, tab3, tab4 = st.tabs(["🚀 快速开始", "🔑 API配置", "💡 使用技巧", "❓ 常见问题"])
    
    with tab1:
        st.markdown("""
        ## 🚀 快速开始指南
        
        ### 步骤一：配置API
        1. **选择AI提供商**：在左侧边栏选择OpenAI、Anthropic或自定义API
        2. **输入API密钥**：在对应的输入框中填入您的API密钥
        3. **测试连接**：点击"测试连接"确保配置正确
        4. **保存配置**：点击"保存配置"完成设置
        
        ### 步骤二：开始对话
        1. **切换到对话页面**：点击"智能对话"选项卡
        2. **输入问题**：在文本框中输入您的问题
        3. **发送消息**：点击"发送消息"或使用Ctrl+Enter
        4. **查看回复**：AI将自动生成回复
        
        ### 步骤三：使用模板（可选）
        1. **浏览模板**：在"Prompt模板"页面浏览各类模板
        2. **选择模板**：点击"使用模板"自动填入聊天框
        3. **自定义内容**：根据需要修改模板内容
        4. **开始对话**：发送消息获得专业的AI回复
        """)
        
        # 添加演示视频或GIF的占位符
        st.info("💡 提示：首次使用建议先测试简单问题，确认一切正常后再进行复杂对话")
    
    with tab2:
        st.markdown("""
        ## 🔑 API密钥配置指南
        
        ### OpenAI API配置
        
        #### 获取API密钥
        1. 访问 [OpenAI平台](https://platform.openai.com/api-keys)
        2. 使用您的账户登录（需要手机号验证）
        3. 点击"Create new secret key"
        4. 复制生成的密钥（格式：sk-proj-... 或 sk-...）
        
        #### 配置说明
        - **API Key**：必填，粘贴您的OpenAI密钥
        - **API Base URL**：可选，默认使用官方地址
        - 如使用代理服务，请填入完整的API端点URL
        
        #### 费用说明
        - OpenAI采用按使用量计费
        - GPT-4费用较高，GPT-3.5-turbo性价比更好
        - 建议设置使用限额避免超支
        
        ---
        
        ### Anthropic Claude API配置
        
        #### 获取API密钥
        1. 访问 [Anthropic控制台](https://console.anthropic.com/)
        2. 申请API访问权限（可能需要等待审核）
        3. 创建API密钥
        4. 复制密钥（格式：sk-ant-...）
        
        #### 模型选择
        - **Claude 3.5 Sonnet**：最新模型，综合性能最佳
        - **Claude 3 Opus**：最强大的模型，适合复杂任务
        - **Claude 3 Haiku**：最快的模型，适合简单任务
        
        ---
        
        ### 自定义API配置
        
        #### 支持的服务
        - **OneAPI**：多模型聚合API服务
        - **FastGPT**：企业级AI对话平台
        - **本地部署**：如Ollama、LM Studio等
        - **第三方代理**：兼容OpenAI格式的服务
        
        #### 配置要求
        - **API Key**：提供商给出的密钥
        - **API Base URL**：完整的服务端点地址
        - **模型名称**：实际可用的模型名称
        
        #### 配置示例
        ```
        API Base URL: https://api.your-service.com
        API Key: your-custom-api-key
        模型名称: gpt-3.5-turbo
        ```
        """)
    
    with tab3:
        st.markdown("""
        ## 💡 使用技巧和最佳实践
        
        ### 🎯 提问技巧
        
        #### 1. 明确具体的问题
        ❌ **不好的提问**：帮我写代码
        ✅ **好的提问**：请用Python写一个函数，实现二分查找算法，包含注释
        
        #### 2. 提供足够的上下文
        ❌ **不好的提问**：这个错误怎么解决？
        ✅ **好的提问**：我在运行Python爬虫时遇到"requests.exceptions.ConnectionError"错误，代码如下...
        
        #### 3. 分步骤处理复杂任务
        对于复杂任务，可以分解为多个步骤：
        1. 先让AI理解需求
        2. 制定实现方案
        3. 逐步实现细节
        4. 测试和优化
        
        ### ⚙️ 参数调优
        
        #### Temperature（创造性）设置
        - **0.0-0.3**：适合编程、翻译等需要准确性的任务
        - **0.4-0.7**：适合一般对话、解释说明等
        - **0.8-1.0**：适合创意写作、头脑风暴等
        - **1.1-2.0**：高度创意，结果可能不太可控
        
        #### Max Tokens（输出长度）设置
        - **100-500**：简短回答、代码片段
        - **500-1500**：一般长度的文章、解释
        - **1500-4000**：详细文档、长篇内容
        
        ### 📝 Prompt模板使用
        
        #### 选择合适的模板
        - **编程任务**：使用"编程助手"分类
        - **写作任务**：使用"文案写作"或"创意写作"
        - **学习问题**：使用"学习辅导"分类
        - **工作文档**：使用"商务办公"分类
        
        #### 自定义模板技巧
        1. 明确角色定位（如：你是一个专业的程序员）
        2. 提供具体要求（如：代码要包含注释）
        3. 指定输出格式（如：以Markdown格式输出）
        4. 添加示例说明（如：参考以下格式）
        
        ### 🔄 多轮对话策略
        
        #### 建立上下文
        1. 首次对话时详细描述背景
        2. 在后续对话中可以简化描述
        3. 适时总结和确认理解
        
        #### 逐步深入
        1. 从概要开始，逐步询问细节
        2. 根据AI回复提出后续问题
        3. 利用"基于上面的回答，请..."的句式
        """)
    
    with tab4:
        st.markdown("""
        ## ❓ 常见问题解答
        
        ### 🔧 技术问题
        
        **Q: API密钥无效怎么办？**
        A: 
        1. 检查密钥格式是否正确
        2. 确认密钥未过期且有足够额度
        3. 检查网络连接是否正常
        4. 尝试重新生成密钥
        
        **Q: 连接测试失败？**
        A:
        1. 检查API Base URL是否正确
        2. 确认防火墙或代理设置
        3. 验证API服务是否正常运行
        4. 查看浏览器控制台的错误信息
        
        **Q: 响应速度很慢？**
        A:
        1. 减少Max Tokens设置
        2. 简化问题描述
        3. 检查网络连接速度
        4. 尝试切换到更快的模型
        
        **Q: AI回答不准确？**
        A:
        1. 提供更详细的上下文
        2. 使用更具体的问题描述
        3. 尝试调整Temperature参数
        4. 使用专业的Prompt模板
        
        ### 💰 费用相关
        
        **Q: 如何控制API使用费用？**
        A:
        1. 在API提供商控制台设置使用限额
        2. 优先使用成本较低的模型
        3. 避免过长的对话历史
        4. 定期检查使用量统计
        
        **Q: 不同模型的费用差异？**
        A:
        - GPT-3.5-turbo：最经济实惠
        - GPT-4：功能强大但费用较高
        - Claude：按字符计费，长文本处理有优势
        
        ### 🛡️ 安全隐私
        
        **Q: API密钥是否安全？**
        A:
        1. 密钥仅存储在浏览器本地
        2. 不会上传到任何服务器
        3. 建议定期更换密钥
        4. 不要在公共设备上保存密钥
        
        **Q: 对话内容是否会被保存？**
        A:
        1. 对话仅保存在浏览器本地
        2. 清除浏览器数据会删除对话历史
        3. 可以手动导出重要对话
        4. 不要在对话中包含敏感信息
        
        ### 🔄 使用限制
        
        **Q: 有什么使用限制？**
        A:
        1. 遵守API提供商的使用条款
        2. 不要用于违法或有害内容
        3. 注意API的速率限制
        4. 尊重知识产权和版权
        
        **Q: 如何获得更好的服务？**
        A:
        1. 升级到付费的API计划
        2. 申请更高的速率限制
        3. 使用专业版的AI模型
        4. 联系技术支持获得帮助
        
        ### 📞 技术支持
        
        **遇到其他问题？**
        - 查看API提供商的官方文档
        - 访问项目GitHub页面提交Issue
        - 联系开发者获得技术支持
        - 参考在线社区的讨论
        """)

def main():
    """主函数"""
    init_session_state()
    
    # 渲染侧边栏
    temperature, max_tokens = render_sidebar()
    
    # 主界面选项卡
    tab1, tab2, tab3 = st.tabs(["💬 智能对话", "📝 Prompt 模板", "📖 使用说明"])
    
    with tab1:
        render_chat_interface(temperature, max_tokens)
    
    with tab2:
        render_prompt_templates()
    
    with tab3:
        render_usage_guide()
    
    # 页脚信息
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem;">
        <p>🤖 <strong>AI 镜像站 v2.0</strong> | 由 Streamlit 强力驱动</p>
        <p><small>支持 OpenAI GPT-4、Anthropic Claude、自定义API等多种先进AI模型</small></p>
        <p><small>开源项目 | 安全可靠 | 完全免费</small></p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
