#!/usr/bin/env python3
"""
Git提交前安全检查脚本
确保不会意外提交敏感信息到GitHub
"""

import os
import re
import sys
from pathlib import Path

class SecurityChecker:
    """安全检查器"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.errors = []
        self.warnings = []
        
        # 敏感信息模式
        self.sensitive_patterns = [
            r'SECRET_KEY\s*=\s*["\'](?!your-secret-key-here)[^"\']{10,}["\']',
            r'MYSQL_PASSWORD\s*=\s*["\'](?!your-database-password)[^"\']+["\']',
            r'password\s*[=:]\s*["\'](?!test123456|your-database-password)[^"\']{6,}["\']',
            r'api_key\s*[=:]\s*["\'][^"\']{10,}["\']',
            # 排除localhost和常见示例域名的实际主机名
            r'(?!localhost|127\.0\.0\.1|your-)[a-zA-Z0-9-]+\.[a-zA-Z0-9.-]+\.(?:site|com|net|org):\d+',
        ]
        
        # 需要检查的文件扩展名
        self.check_extensions = {'.py', '.js', '.ts', '.vue', '.json', '.md', '.txt', '.yml', '.yaml'}
        
        # 应该忽略的文件和目录
        self.ignore_patterns = {
            '.git', '__pycache__', 'node_modules', 'venv', 'env',
            '.env*', '*.log', 'logs', '.cursor', '.idea', '.vscode',
            '.specstory', 'dist', 'build', 'test_', 'Postman_Collection'
        }
    
    def should_ignore(self, path):
        """检查是否应该忽略该路径"""
        path_str = str(path)
        for pattern in self.ignore_patterns:
            if pattern in path_str:
                return True
        return False
    
    def check_file(self, file_path):
        """检查单个文件"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
                for pattern in self.sensitive_patterns:
                    matches = re.finditer(pattern, content, re.IGNORECASE)
                    for match in matches:
                        line_num = content[:match.start()].count('\n') + 1
                        self.errors.append(f"🚨 敏感信息发现: {file_path}:{line_num}")
                        self.errors.append(f"   内容: {match.group()}")
                        
        except Exception as e:
            self.warnings.append(f"⚠️  无法读取文件 {file_path}: {e}")
    
    def check_env_files(self):
        """检查是否有.env文件被意外包含"""
        env_files = []
        for root, dirs, files in os.walk(self.project_root):
            for file in files:
                if file.startswith('.env'):
                    file_path = Path(root) / file
                    if not self.should_ignore(file_path):
                        env_files.append(file_path)
        
        if env_files:
            self.errors.append("🚨 发现.env文件可能被包含在Git中:")
            for env_file in env_files:
                self.errors.append(f"   {env_file}")
            self.errors.append("   建议: 确保这些文件在.gitignore中")
    
    def check_gitignore(self):
        """检查.gitignore配置"""
        gitignore_path = self.project_root / '.gitignore'
        if not gitignore_path.exists():
            self.errors.append("🚨 缺少.gitignore文件")
            return
            
        with open(gitignore_path, 'r', encoding='utf-8') as f:
            gitignore_content = f.read()
            
        required_entries = ['.env', 'venv/', '__pycache__/', '*.log']
        missing_entries = []
        
        for entry in required_entries:
            if entry not in gitignore_content:
                missing_entries.append(entry)
        
        if missing_entries:
            self.warnings.append("⚠️  .gitignore中缺少建议的条目:")
            for entry in missing_entries:
                self.warnings.append(f"   {entry}")
    
    def scan_project(self):
        """扫描整个项目"""
        print("🔍 开始安全检查...")
        
        # 检查.gitignore
        self.check_gitignore()
        
        # 检查.env文件
        self.check_env_files()
        
        # 扫描所有相关文件
        scanned_files = 0
        for root, dirs, files in os.walk(self.project_root):
            # 跳过忽略的目录
            dirs[:] = [d for d in dirs if not any(pattern in d for pattern in self.ignore_patterns)]
            
            for file in files:
                file_path = Path(root) / file
                
                if self.should_ignore(file_path):
                    continue
                    
                if file_path.suffix in self.check_extensions:
                    self.check_file(file_path)
                    scanned_files += 1
        
        print(f"📊 已扫描 {scanned_files} 个文件")
        
        # 输出结果
        if self.errors:
            print("\n❌ 发现安全问题:")
            for error in self.errors:
                print(error)
        
        if self.warnings:
            print("\n⚠️  警告:")
            for warning in self.warnings:
                print(warning)
        
        if not self.errors and not self.warnings:
            print("\n✅ 安全检查通过！可以安全提交到Git。")
        
        return len(self.errors) == 0

def main():
    """主函数"""
    print("🛡️  UAI项目安全检查工具")
    print("=" * 50)
    
    checker = SecurityChecker()
    is_safe = checker.scan_project()
    
    if not is_safe:
        print("\n🚫 检测到安全问题，请修复后再提交！")
        print("\n💡 修复建议:")
        print("1. 确保所有敏感信息都在.env文件中")
        print("2. 确保.env文件在.gitignore中")
        print("3. 不要在代码中硬编码密码、密钥等敏感信息")
        print("4. 使用环境变量替代硬编码配置")
        sys.exit(1)
    else:
        print("\n🎉 项目可以安全上传到GitHub！")
        sys.exit(0)

if __name__ == "__main__":
    main() 