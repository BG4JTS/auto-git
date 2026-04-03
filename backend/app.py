from flask import Flask, request, jsonify
from flask_cors import CORS
from github import Github
import os

app = Flask(__name__)
CORS(app)

# GitHub API认证 - 支持多种环境变量名称
def get_github_token():
    """获取GitHub Token，支持多种环境变量名称"""
    # 尝试不同的环境变量名称
    token_names = ['g_token', 'GITHUB_TOKEN', 'GH_TOKEN', 'GITHUB_ACCESS_TOKEN']
    
    for name in token_names:
        token = os.getenv(name)
        if token:
            print(f"Found GitHub token in environment variable: {name}")
            return token
    
    return None

github_token = get_github_token()
g = None

if github_token:
    try:
        g = Github(github_token)
        print("GitHub client initialized successfully")
    except Exception as e:
        print(f"Failed to initialize GitHub client: {e}")
else:
    print("Warning: No GitHub token found in environment variables")
    print("Available environment variables:", list(os.environ.keys()))

@app.route('/api/commit', methods=['POST'])
def create_commit():
    """创建GitHub提交"""
    try:
        if not g:
            return jsonify({'error': 'GitHub token not configured. Please set g_token environment variable.'}), 500
        
        data = request.json
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        repo_name = data.get('repo')
        file_path = data.get('file')
        content = data.get('content')
        commit_message = data.get('message', 'Auto commit from web interface')
        
        if not all([repo_name, file_path, content]):
            return jsonify({'error': 'Missing required parameters'}), 400
        
        repo = g.get_repo(repo_name)
        
        try:
            existing_file = repo.get_contents(file_path)
            repo.update_file(
                file_path,
                commit_message,
                content,
                existing_file.sha
            )
            action = 'updated'
        except:
            repo.create_file(
                file_path,
                commit_message,
                content
            )
            action = 'created'
        
        return jsonify({
            'success': True,
            'message': f'File {action} successfully',
            'repo': repo_name,
            'file': file_path
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/repos', methods=['GET'])
def get_repos():
    """获取用户的仓库列表"""
    try:
        if not g:
            return jsonify({'error': 'GitHub token not configured. Please set g_token environment variable.'}), 500
        
        user = g.get_user()
        repos = [{'name': repo.name, 'full_name': repo.full_name} for repo in user.get_repos()]
        return jsonify({'repos': repos})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health():
    """健康检查端点"""
    return jsonify({
        'status': 'ok',
        'github_token_configured': g is not None,
        'github_token_source': 'configured' if g else 'not configured'
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)