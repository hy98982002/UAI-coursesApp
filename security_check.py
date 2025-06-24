#!/usr/bin/env python3
"""
安全检查脚本 - 符合Codex安全规范
检测项目中的硬编码敏感信息
"""

import os
import re
import sys
from pathlib import Path

class SecurityChecker:
    def __init__(self):
        self.sensitive_patterns = [
            r'MYSQL_PASSWORD\s*=\s*[\'"][^\'"]*[\'"]',
            r'SECRET_KEY\s*=\s*[\'"]django-insecure[^\'"]*[\'"]',
            r'mysql://[^/]+:[^@]+@[^/]+',
            r'dbconn\.sealosbja\.site',
            r'4mhpzmwn',
            r'password\s*=\s*[\'"][^\'"]{6,}[\'"]',
            r'host\s*=\s*[\'"]dbconn\.[^\'"]*[\'"]',
        ]
        
        self.exclude_files = {
            '.env', '.env.example', '.gitignore', 'security_check.py',
            '__pycache__', '.git', 'node_modules', 'venv', '.specstory'
        }
        
        self.exclude_extensions = {'.pyc', '.log', '.png', '.jpg', '.gif', '.md'}
        
    def scan_file(self, file_path):
        """扫描单个文件"""
        violations = []
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
            for line_num, line in enumerate(content.split('\n'), 1):
                for pattern in self.sensitive_patterns:
                    if re.search(pattern, line, re.IGNORECASE):
                        violations.append({
                            'file': file_path,
                            'line': line_num,
                            'content': line.strip(),
                            'pattern': pattern
                        })
        except Exception as e:
            print(f"⚠️  无法读取文件 {file_path}: {e}")
            
        return violations
    
    def scan_project(self):
        """扫描整个项目"""
        violations = []
        
        for root, dirs, files in os.walk('.'):
            # 排除目录
            dirs[:] = [d for d in dirs if d not in self.exclude_files]
            
            for file in files:
                # 排除文件
                if file in self.exclude_files:
                    continue
                
                file_path = Path(root) / file
                if file_path.suffix in self.exclude_extensions:
                    continue
                
                violations.extend(self.scan_file(file_path))
        
        return violations
    
    def generate_report(self, violations):
        """生成安全报告"""
        print("🔒 UAI项目安全检查报告")
        print("=" * 50)
        
        if not violations:
            print("✅ 未发现硬编码敏感信息")
            print("🎉 项目符合Codex安全规范")
            return True
        
        print(f"❌ 发现 {len(violations)} 个安全问题:")
        print()
        
        for i, violation in enumerate(violations, 1):
            print(f"问题 {i}:")
            print(f"  📄 文件: {violation['file']}")
            print(f"  📍 行号: {violation['line']}")
            print(f"  🔍 内容: {violation['content'][:100]}...")
            print(f"  🚨 模式: {violation['pattern']}")
            print()
        
        print("🛡️  修复建议:")
        print("1. 将所有敏感信息移至 .env 文件")
        print("2. 使用 os.getenv() 或环境变量")
        print("3. 确保 .env 文件在 .gitignore 中")
        print("4. 删除代码中的硬编码凭据")
        
        return False

def main():
    print("🚀 启动安全检查...")
    checker = SecurityChecker()
    violations = checker.scan_project()
    
    is_secure = checker.generate_report(violations)
    
    if not is_secure:
        print("\n⚠️  请修复上述安全问题后再提交代码")
        sys.exit(1)
    else:
        print("\n✅ 安全检查通过！")
        sys.exit(0)

if __name__ == "__main__":
    main() 