# GitHub 自动提交工具

这是一个使用网页界面控制的GitHub自动提交工具，允许用户通过浏览器直接编辑文件并提交到GitHub仓库。

## 功能特点

- 通过网页界面选择GitHub仓库
- 编辑文件内容并提交到GitHub
- 支持创建新文件和更新现有文件
- 实时显示操作结果

## 技术栈

- **后端**: Python Flask
- **前端**: HTML, JavaScript, Bootstrap
- **API**: GitHub API (PyGithub)

## 快速开始

### 1. 生成GitHub个人访问令牌

1. 访问 [GitHub Settings > Tokens](https://github.com/settings/tokens)
2. 点击 "Generate new token"
3. 选择 "Generate new token (classic)"
4. 输入令牌名称，选择有效期
5. 勾选 `repo` 权限
6. 点击 "Generate token"
7. 复制生成的令牌

### 2. 配置环境变量

#### 本地开发环境
1. 打开 `backend/.env` 文件
2. 将 `your_github_token_here` 替换为你的GitHub令牌

#### 生产环境（使用GitHub Secrets）
1. 访问你的GitHub仓库页面
2. 点击 "Settings" > "Secrets and variables" > "Actions"
3. 点击 "New repository secret"
4. 名称输入 `g_token`
5. 值粘贴你的GitHub令牌
6. 点击 "Add secret"

### 3. 使用GitHub Dependabot Secrets

GitHub Dependabot Secrets 可以用于：
1. **CI/CD 工作流**：在 `.github/workflows` 中使用 `${{ secrets.g_token }}` 访问
2. ** Dependabot 自动更新**：Dependabot 会自动使用这些secrets进行依赖更新
3. **安全扫描**：确保敏感信息不会被泄露

### 4. 启动后端服务

```bash
# 进入backend目录
cd backend

# 激活虚拟环境
venv\Scripts\Activate.ps1

# 启动Flask应用
python app.py
```

服务将在 `http://localhost:5000` 运行

### 5. 访问前端页面

打开浏览器，访问 `frontend/index.html` 文件

## 项目结构

```
├── backend/           # 后端代码
│   ├── app.py         # Flask应用主文件
│   ├── venv/          # Python虚拟环境
│   └── .env           # 环境变量配置
├── frontend/          # 前端代码
│   └── index.html     # 网页界面
├── config/            # 配置文件
├── utils/             # 工具函数
└── README.md          # 项目说明
```

## 使用说明

1. 在浏览器中打开前端页面
2. 选择要操作的GitHub仓库
3. 输入文件路径（例如：README.md）
4. 编辑文件内容
5. 输入提交信息
6. 点击 "提交到 GitHub" 按钮
7. 查看操作结果

## 注意事项

- 确保你的GitHub令牌具有 `repo` 权限
- 确保后端服务正在运行
- 支持的文件大小取决于GitHub API的限制
- 提交操作可能需要几秒钟时间，请耐心等待

## 故障排除

### 后端服务无法启动

- 检查Python是否安装
- 检查虚拟环境是否正确创建
- 检查依赖是否安装完整
- 检查GitHub令牌是否正确配置

### 前端无法加载仓库列表

- 检查后端服务是否正在运行
- 检查GitHub令牌是否有效
- 检查网络连接

### 提交失败

- 检查仓库权限
- 检查文件路径是否正确
- 检查GitHub令牌权限
- 检查网络连接

## 许可证

MIT License