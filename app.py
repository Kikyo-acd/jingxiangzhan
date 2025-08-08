import streamlit as st
import requests
import json
import time
from datetime import datetime
from typing import Dict, List, Optional

# 页面配置
st.set_page_config(
    page_title="GitHub API 工具站",
    page_icon="🐙",
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
        background: linear-gradient(90deg, #f97316 0%, #dc2626 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .repo-card {
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        background-color: #fafafa;
        border-left: 4px solid #f97316;
    }
    .user-card {
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        background-color: #f0f9ff;
        border-left: 4px solid #0ea5e9;
    }
    .issue-card {
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        background-color: #f0fdf4;
        border-left: 4px solid #22c55e;
    }
    .stat-card {
        background-color: #f8fafc;
        border-radius: 8px;
        padding: 1.5rem;
        text-align: center;
        border: 1px solid #e2e8f0;
    }
    .api-info {
        background-color: #fef3c7;
        border: 1px solid #f59e0b;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

class GitHubAPI:
    """GitHub API 客户端"""
    
    def __init__(self, token: str):
        self.token = token
        self.base_url = "https://api.github.com"
        self.headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json"
        }
    
    def test_connection(self) -> bool:
        """测试GitHub API连接"""
        try:
            response = requests.get(f"{self.base_url}/user", headers=self.headers, timeout=10)
            return response.status_code == 200
        except:
            return False
    
    def get_user_info(self, username: str = None) -> Dict:
        """获取用户信息"""
        try:
            url = f"{self.base_url}/user" if not username else f"{self.base_url}/users/{username}"
            response = requests.get(url, headers=self.headers, timeout=10)
            if response.status_code == 200:
                return response.json()
            return {}
        except:
            return {}
    
    def search_repositories(self, query: str, sort: str = "stars", order: str = "desc", per_page: int = 10) -> List[Dict]:
        """搜索仓库"""
        try:
            params = {
                "q": query,
                "sort": sort,
                "order": order,
                "per_page": per_page
            }
            response = requests.get(f"{self.base_url}/search/repositories", 
                                  headers=self.headers, params=params, timeout=10)
            if response.status_code == 200:
                return response.json().get("items", [])
            return []
        except:
            return []
    
    def get_user_repos(self, username: str = None, sort: str = "updated", per_page: int = 10) -> List[Dict]:
        """获取用户仓库"""
        try:
            if username:
                url = f"{self.base_url}/users/{username}/repos"
            else:
                url = f"{self.base_url}/user/repos"
            
            params = {
                "sort": sort,
                "per_page": per_page,
                "type": "all"
            }
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            if response.status_code == 200:
                return response.json()
            return []
        except:
            return []
    
    def get_repo_issues(self, owner: str, repo: str, state: str = "open", per_page: int = 10) -> List[Dict]:
        """获取仓库Issues"""
        try:
            params = {
                "state": state,
                "per_page": per_page
            }
            response = requests.get(f"{self.base_url}/repos/{owner}/{repo}/issues", 
                                  headers=self.headers, params=params, timeout=10)
            if response.status_code == 200:
                return response.json()
            return []
        except:
            return []
    
    def get_repo_stats(self, owner: str, repo: str) -> Dict:
        """获取仓库统计信息"""
        try:
            response = requests.get(f"{self.base_url}/repos/{owner}/{repo}", 
                                  headers=self.headers, timeout=10)
            if response.status_code == 200:
                return response.json()
            return {}
        except:
            return {}
    
    def search_users(self, query: str, per_page: int = 10) -> List[Dict]:
        """搜索用户"""
        try:
            params = {
                "q": query,
                "per_page": per_page
            }
            response = requests.get(f"{self.base_url}/search/users", 
                                  headers=self.headers, params=params, timeout=10)
            if response.status_code == 200:
                return response.json().get("items", [])
            return []
        except:
            return []
    
    def get_trending_repos(self, language: str = "", period: str = "daily") -> List[Dict]:
        """获取趋势仓库（通过搜索API模拟）"""
        try:
            # 使用搜索API获取最近创建的热门仓库
            date_filter = "2024-01-01"  # 可以动态调整
            query = f"created:>{date_filter}"
            if language:
                query += f" language:{language}"
            
            params = {
                "q": query,
                "sort": "stars",
                "order": "desc",
                "per_page": 10
            }
            response = requests.get(f"{self.base_url}/search/repositories", 
                                  headers=self.headers, params=params, timeout=10)
            if response.status_code == 200:
                return response.json().get("items", [])
            return []
        except:
            return []

def init_session_state():
    """初始化会话状态"""
    if "github_token" not in st.session_state:
        st.session_state.github_token = ""
    if "github_api" not in st.session_state:
        st.session_state.github_api = None
    if "search_history" not in st.session_state:
        st.session_state.search_history = []

def render_sidebar():
    """渲染侧边栏"""
    with st.sidebar:
        st.markdown("## ⚙️ GitHub API 配置")
        
        # GitHub API Token 配置
        st.markdown("### 🔑 API Token")
        
        # Token 输入
        github_token = st.text_input(
            "GitHub API Token",
            value=st.session_state.github_token,
            type="password",
            placeholder="ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
            help="输入您的 GitHub Personal Access Token"
        )
        
        if github_token:
            st.session_state.github_token = github_token
            
            # 测试连接
            if st.button("🔍 测试连接"):
                with st.spinner("测试连接中..."):
                    api = GitHubAPI(github_token)
                    if api.test_connection():
                        st.success("✅ 连接成功！")
                        st.session_state.github_api = api
                        
                        # 显示当前用户信息
                        user_info = api.get_user_info()
                        if user_info:
                            st.markdown(f"""
                            **当前用户：** {user_info.get('login', 'Unknown')}  
                            **剩余请求：** API限制检查中...
                            """)
                    else:
                        st.error("❌ 连接失败，请检查Token")
                        st.session_state.github_api = None
        else:
            st.warning("⚠️ 请输入 GitHub API Token")
        
        # 搜索历史
        if st.session_state.search_history:
            st.markdown("### 📝 搜索历史")
            for i, search in enumerate(st.session_state.search_history[-5:]):
                if st.button(f"🔄 {search}", key=f"history_{i}"):
                    st.session_state.current_search = search

def format_number(num):
    """格式化数字显示"""
    if num >= 1000000:
        return f"{num/1000000:.1f}M"
    elif num >= 1000:
        return f"{num/1000:.1f}K"
    else:
        return str(num)

def render_repo_card(repo: Dict):
    """渲染仓库卡片"""
    language = repo.get('language', 'Unknown')
    stars = repo.get('stargazers_count', 0)
    forks = repo.get('forks_count', 0)
    description = repo.get('description', '无描述')
    
    st.markdown(f"""
    <div class="repo-card">
        <h4><a href="{repo['html_url']}" target="_blank">📦 {repo['full_name']}</a></h4>
        <p>{description}</p>
        <div style="display: flex; gap: 15px; margin-top: 10px;">
            <span>⭐ {format_number(stars)}</span>
            <span>🍴 {format_number(forks)}</span>
            <span>💻 {language}</span>
            <span>📅 {repo.get('updated_at', '')[:10]}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_user_card(user: Dict):
    """渲染用户卡片"""
    st.markdown(f"""
    <div class="user-card">
        <div style="display: flex; align-items: center; gap: 15px;">
            <img src="{user.get('avatar_url', '')}" width="60" style="border-radius: 50%;">
            <div>
                <h4><a href="{user['html_url']}" target="_blank">👤 {user['login']}</a></h4>
                <p>{user.get('bio', '无简介')}</p>
                <div style="display: flex; gap: 15px;">
                    <span>📍 {user.get('location', '未知')}</span>
                    <span>👥 {user.get('followers', 0)} followers</span>
                    <span>📦 {user.get('public_repos', 0)} repos</span>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_repo_explorer():
    """渲染仓库探索页面"""
    st.markdown('<h1 class="main-header">🔍 仓库探索</h1>', unsafe_allow_html=True)
    
    if not st.session_state.github_api:
        st.warning("⚠️ 请先在侧边栏配置 GitHub API Token")
        return
    
    api = st.session_state.github_api
    
    # 搜索界面
    col1, col2, col3 = st.columns([3, 1, 1])
    
    with col1:
        search_query = st.text_input("🔍 搜索仓库", placeholder="输入关键词搜索仓库...")
    
    with col2:
        sort_by = st.selectbox("排序方式", ["stars", "forks", "updated"], 
                              format_func=lambda x: {"stars": "⭐ 星标", "forks": "🍴 分叉", "updated": "📅 更新"}[x])
    
    with col3:
        per_page = st.selectbox("每页显示", [5, 10, 20, 30], index=1)
    
    # 高级搜索选项
    with st.expander("🔧 高级搜索选项"):
        col1, col2, col3 = st.columns(3)
        with col1:
            language_filter = st.text_input("编程语言", placeholder="如：Python, JavaScript")
        with col2:
            stars_filter = st.text_input("星标数量", placeholder="如：>100, 50..200")
        with col3:
            created_filter = st.text_input("创建时间", placeholder="如：>2023-01-01")
    
    # 执行搜索
    if search_query:
        # 构建搜索查询
        full_query = search_query
        if language_filter:
            full_query += f" language:{language_filter}"
        if stars_filter:
            full_query += f" stars:{stars_filter}"
        if created_filter:
            full_query += f" created:{created_filter}"
        
        # 添加到搜索历史
        if full_query not in st.session_state.search_history:
            st.session_state.search_history.append(full_query)
        
        with st.spinner("🔍 搜索中..."):
            repos = api.search_repositories(full_query, sort=sort_by, per_page=per_page)
        
        if repos:
            st.success(f"✅ 找到 {len(repos)} 个仓库")
            
            for repo in repos:
                render_repo_card(repo)
        else:
            st.info("📭 未找到匹配的仓库，请尝试其他关键词")
    
    # 热门仓库推荐
    st.markdown("## 🔥 热门仓库推荐")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🐍 Python 热门项目", use_container_width=True):
            with st.spinner("加载中..."):
                python_repos = api.get_trending_repos("python")
                for repo in python_repos[:5]:
                    render_repo_card(repo)
    
    with col2:
        if st.button("⚛️ JavaScript 热门项目", use_container_width=True):
            with st.spinner("加载中..."):
                js_repos = api.get_trending_repos("javascript")
                for repo in js_repos[:5]:
                    render_repo_card(repo)

def render_user_explorer():
    """渲染用户探索页面"""
    st.markdown('<h1 class="main-header">👥 用户探索</h1>', unsafe_allow_html=True)
    
    if not st.session_state.github_api:
        st.warning("⚠️ 请先在侧边栏配置 GitHub API Token")
        return
    
    api = st.session_state.github_api
    
    # 用户搜索
    col1, col2 = st.columns([3, 1])
    
    with col1:
        username_query = st.text_input("🔍 搜索用户", placeholder="输入用户名或关键词...")
    
    with col2:
        search_type = st.selectbox("搜索类型", ["搜索用户", "查看特定用户"])
    
    if username_query:
        if search_type == "搜索用户":
            with st.spinner("🔍 搜索中..."):
                users = api.search_users(username_query)
            
            if users:
                st.success(f"✅ 找到 {len(users)} 个用户")
                for user in users:
                    render_user_card(user)
            else:
                st.info("📭 未找到匹配的用户")
        
        else:  # 查看特定用户
            with st.spinner("📋 加载用户信息..."):
                user_info = api.get_user_info(username_query)
            
            if user_info:
                # 用户详细信息
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    st.image(user_info.get('avatar_url', ''), width=200)
                
                with col2:
                    st.markdown(f"## {user_info.get('name', user_info['login'])}")
                    st.markdown(f"**用户名：** @{user_info['login']}")
                    st.markdown(f"**简介：** {user_info.get('bio', '无简介')}")
                    st.markdown(f"**位置：** {user_info.get('location', '未知')}")
                    st.markdown(f"**公司：** {user_info.get('company', '未知')}")
                    st.markdown(f"**网站：** {user_info.get('blog', '无')}")
                    st.markdown(f"**加入时间：** {user_info.get('created_at', '')[:10]}")
                
                # 统计信息
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.markdown(f"""
                    <div class="stat-card">
                        <h3>{user_info.get('public_repos', 0)}</h3>
                        <p>公开仓库</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                    <div class="stat-card">
                        <h3>{user_info.get('followers', 0)}</h3>
                        <p>关注者</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    st.markdown(f"""
                    <div class="stat-card">
                        <h3>{user_info.get('following', 0)}</h3>
                        <p>关注中</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col4:
                    st.markdown(f"""
                    <div class="stat-card">
                        <h3>{user_info.get('public_gists', 0)}</h3>
                        <p>公开Gist</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # 用户仓库
                st.markdown("## 📦 用户仓库")
                user_repos = api.get_user_repos(username_query, per_page=10)
                
                if user_repos:
                    for repo in user_repos:
                        render_repo_card(repo)
                else:
                    st.info("📭 该用户没有公开仓库")
            
            else:
                st.error("❌ 用户不存在或无法访问")

def render_my_dashboard():
    """渲染我的仪表板"""
    st.markdown('<h1 class="main-header">📊 我的 GitHub 仪表板</h1>', unsafe_allow_html=True)
    
    if not st.session_state.github_api:
        st.warning("⚠️ 请先在侧边栏配置 GitHub API Token")
        return
    
    api = st.session_state.github_api
    
    # 获取当前用户信息
    with st.spinner("📋 加载个人信息..."):
        user_info = api.get_user_info()
    
    if not user_info:
        st.error("❌ 无法获取用户信息，请检查API Token权限")
        return
    
    # 用户基本信息
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.image(user_info.get('avatar_url', ''), width=200)
    
    with col2:
        st.markdown(f"## 👋 你好，{user_info.get('name', user_info['login'])}！")
        st.markdown(f"**用户名：** @{user_info['login']}")
        st.markdown(f"**简介：** {user_info.get('bio', '无简介')}")
        st.markdown(f"**位置：** {user_info.get('location', '未知')}")
        st.markdown(f"**GitHub 会员：** {user_info.get('created_at', '')[:10]} 加入")
    
    # 统计概览
    st.markdown("## 📈 统计概览")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <h2>{user_info.get('public_repos', 0)}</h2>
            <p>📦 公开仓库</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <h2>{user_info.get('followers', 0)}</h2>
            <p>👥 关注者</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="stat-card">
            <h2>{user_info.get('following', 0)}</h2>
            <p>👤 关注中</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="stat-card">
            <h2>{user_info.get('public_gists', 0)}</h2>
            <p>📝 公开Gist</p>
        </div>
        """, unsafe_allow_html=True)
    
    # 我的仓库
    st.markdown("## 📦 我的仓库")
    
    sort_option = st.selectbox("排序方式", 
                              ["updated", "created", "pushed", "full_name"],
                              format_func=lambda x: {
                                  "updated": "📅 最近更新",
                                  "created": "🆕 创建时间", 
                                  "pushed": "🔄 最近推送",
                                  "full_name": "📝 名称"
                              }[x])
    
    with st.spinner("📋 加载仓库列表..."):
        my_repos = api.get_user_repos(sort=sort_option, per_page=20)
    
    if my_repos:
        for repo in my_repos:
            render_repo_card(repo)
    else:
        st.info("📭 您还没有公开仓库")

def render_usage_guide():
    """渲染使用说明"""
    st.markdown('<h1 class="main-header">📖 使用说明</h1>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["🚀 快速开始", "🔧 功能介绍", "❓ 常见问题"])
    
    with tab1:
        st.markdown("""
        ## 🚀 快速开始指南
        
        ### 第一步：获取 GitHub API Token
        1. 登录您的 GitHub 账户
        2. 点击右上角头像 → Settings
        3. 左侧菜单选择 "Developer settings"
        4. 选择 "Personal access tokens" → "Tokens (classic)"
        5. 点击 "Generate new token (classic)"
        6. 填写 Token 描述，选择过期时间
        7. 勾选以下权限：
           - ✅ `public_repo` - 访问公开仓库
           - ✅ `user` - 访问用户信息
           - ✅ `repo` - 访问私有仓库（可选）
        8. 点击 "Generate token" 并保存生成的 token
        
        ### 第二步：配置应用
        1. 在左侧边栏找到 "GitHub API 配置"
        2. 将复制的 token 粘贴到输入框
        3. 点击 "测试连接" 确保配置正确
        4. 看到 "连接成功" 提示即可使用
        
        ### 第三步：开始探索
        - 🔍 **仓库探索**：搜索和发现有趣的开源项目
        - 👥 **用户探索**：查找和了解其他开发者
        - 📊 **我的仪表板**：查看您的GitHub统计和仓库
        """)
        
        st.markdown("""
        <div class="api-info">
            <h4>💡 小提示</h4>
            <p>• GitHub API 每小时有请求限制，认证用户可以请求5000次</p>
            <p>• Token 请妥善保管，不要分享给他人</p>
            <p>• 建议定期更换 Token 确保账户安全</p>
        </div>
        """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown("""
        ## 🔧 功能介绍
        
        ### 🔍 仓库探索功能
        
        #### 基础搜索
        - **关键词搜索**：输入项目名称、描述中的关键词
        - **排序选项**：按星标数、分叉数、更新时间排序
        - **结果数量**：可选择每页显示的仓库数量
        
        #### 高级搜索
        - **编程语言过滤**：如 `Python`、`JavaScript`
        - **星标数过滤**：如 `>100`、`50..200`
        - **创建时间过滤**：如 `>2023-01-01`
        
        #### 搜索示例
        ```
        基础搜索：machine learning
        语言过滤：web scraping language:python
        星标过滤：todo app stars:>50
        时间过滤：react created:>2023-01-01
        组合搜索：ai tools language:python stars:>100
        ```
        
        ### 👥 用户探索功能
        
        #### 用户搜索
        - 按用户名或关键词搜索开发者
        - 查看用户的基本信息和统计数据
        - 浏览用户的公开仓库
        
        #### 用户详情
        - 个人资料信息（头像、简介、位置等）
        - 统计数据（仓库数、关注者、关注中）
        - 仓库列表（按更新时间排序）
        
        ### 📊 个人仪表板
        
        #### 个人统计
        - 公开仓库数量
        - 关注者和关注中的数量
        - 公开 Gist 数量
        - GitHub 加入时间
        
        #### 仓库管理
        - 查看所有个人仓库
        - 多种排序方式（更新时间、创建时间等）
        - 仓库详细信息（星标、分叉、语言等）
        """)
    
    with tab3:
        st.markdown("""
        ## ❓ 常见问题解答
        
        ### 🔑 Token 相关问题
        
        **Q: 为什么需要 GitHub API Token？**
        A: GitHub API 对未认证用户有严格的请求限制（每小时60次），使用 Token 可以增加到5000次，并且可以访问私有仓库等更多功能。
        
        **Q: Token 权限应该如何选择？**
        A: 
        - `public_repo`：必需，用于访问公开仓库
        - `user`：推荐，用于获取用户信息
        - `repo`：可选，如需访问私有仓库
        
        **Q: Token 安全吗？**
        A: 本应用仅在浏览器本地使用 Token，不会上传到任何服务器。但请定期更换 Token 确保安全。
        
        ### 🔍 搜索相关问题
        
        **Q: 为什么搜索结果很少？**
        A: GitHub API 对搜索结果有限制，尝试使用更具体的关键词或高级搜索过滤条件。
        
        **Q: 如何搜索特定类型的项目？**
        A: 使用高级搜索功能，可以按编程语言、星标数量、创建时间等条件过滤。
        
        **Q: 搜索历史在哪里？**
        A: 最近的5次搜索会显示在左侧边栏的"搜索历史"中，点击可以快速重复搜索。
        
        ### ⚡ 性能相关问题
        
        **Q: 为什么有时候加载很慢？**
        A: 
        1. 网络连接问题
        2. GitHub API 响应较慢
        3. 达到 API 请求限制
        
        **Q: 如何查看 API 使用情况？**
        A: GitHub 在每个 API 响应中包含剩余请求次数信息，可以在浏览器开发者工具中查看。
        
        **Q: API 限制如何计算？**
        A: 
        - 认证用户：5000 请求/小时
        - 搜索 API：30 请求/分钟
        - 限制按小时重置
        
        ### 🛠️ 技术支持
        
        **遇到其他问题？**
        - 查看 GitHub API 官方文档
        - 检查网络连接和防火墙设置
        - 确认 Token 权限是否足够
        - 查看浏览器控制台的错误信息
        
        **联系方式**
        - GitHub Issues: 在项目仓库提交问题
        - 官方文档: https://docs.github.com/en/rest
        """)

def main():
    """主函数"""
    init_session_state()
    
    # 渲染侧边栏
    render_sidebar()
    
    # 主界面选项卡
    tab1, tab2, tab3, tab4 = st.tabs(["🔍 仓库探索", "👥 用户探索", "📊 我的仪表板", "📖 使用说明"])
    
    with tab1:
        render_repo_explorer()
    
    with tab2:
        render_user_explorer()
    
    with tab3:
        render_my_dashboard()
    
    with tab4:
        render_usage_guide()
    
    # 页脚信息
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem;">
        <p>🐙 <strong>GitHub API 工具站</strong> | 基于 Streamlit 构建</p>
        <p><small>探索开源世界 | 发现优质项目 | 连接开发者社区</small></p>
        <p><small>安全可靠 | 完全开源 | 本地运行</small></p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
