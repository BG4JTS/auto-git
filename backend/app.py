from flask import Flask, request, jsonify
from flask_cors import CORS
from github import Github
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

app = Flask(__name__)
CORS(app)  # 启用CORS，允许前端访问

# GitHub API认证
github_token = os.getenv('GITHUB_TOKEN')
if not github_token:
    raise ValueError('GITHUB_TOKEN environment variable is not set')

g = Github(github_token)

@app.route('/api/commit', methods=['POST'])
def create_commit():
    """创建GitHub提交"""
    try:
        data = request.json
        
        # 验证必要参数
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        repo_name = data.get('repo')
        file_path = data.get('file')
        content = data.get('content')
        commit_message = data.get('message', 'Auto commit from web interface')
        
        if not all([repo_name, file_path, content]):
            return jsonify({'error': 'Missing required parameters'}), 400
        
        # 获取仓库
        repo = g.get_repo(repo_name)
        
        # 尝试获取现有文件
        try:
            existing_file = repo.get_contents(file_path)
            # 更新文件
            repo.update_file(
                file_path,
                commit_message,
                content,
                existing_file.sha
            )
            action = 'updated'
        except:
            # 创建新文件
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
        user = g.get_user()
        repos = [{'name': repo.name, 'full_name': repo.full_name} for repo in user.get_repos()]
        return jsonify({'repos': repos})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)