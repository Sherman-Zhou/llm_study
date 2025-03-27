import requests
import json
from typing import Dict, List

class DeepSeekAPIAgent:
    def __init__(self, api_key: str):
        """
        初始化 DeepSeek API Agent
        
        参数:
            api_key: 你的 DeepSeek API 密钥
        """
        self.api_key = api_key
        self.api_url = "https://api.deepseek.com/v1/chat/completions"  # 假设的API地址，请替换为真实地址
        self.conversation_history = []
        
        # 设置请求头
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def _call_api(self, messages: List[Dict]) -> str:
        """
        调用 DeepSeek API
        
        参数:
            messages: 对话消息列表
            
        返回:
            API 的响应内容
        """
        data = {
            "model": "deepseek-chat",  # 使用的模型
            "messages": messages,
            "temperature": 0.7,  # 控制随机性
            "max_tokens": 1000   # 最大返回token数
        }
        
        try:
            response = requests.post(
                self.api_url,
                headers=self.headers,
                data=json.dumps(data)
            )
            
            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"]
            else:
                return f"API请求失败，状态码: {response.status_code}, 错误: {response.text}"
        except Exception as e:
            return f"调用API时出错: {str(e)}"
    
    def chat(self, user_input: str) -> str:
        """
        与Agent对话
        
        参数:
            user_input: 用户输入文本
            
        返回:
            Agent的回复
        """
        # 添加用户消息到对话历史
        self.conversation_history.append({"role": "user", "content": user_input})
        
        # 调用API获取回复
        response = self._call_api(self.conversation_history)
        
        # 添加助手回复到对话历史
        self.conversation_history.append({"role": "assistant", "content": response})
        
        return response
    
    def reset_conversation(self):
        """重置对话历史"""
        self.conversation_history = []

# 使用示例
if __name__ == "__main__":
    # 替换为你的实际API密钥
    API_KEY = "your_api_key_here"
    
    agent = DeepSeekAPIAgent(API_KEY)
    
    print("DeepSeek API Agent 已启动，输入'退出'结束对话\n")
    
    while True:
        user_input = input("你: ")
        
        if user_input.lower() in ["退出", "exit", "quit", "bye", "再见"]:
            print("助手: 再见！")
            break
            
        response = agent.chat(user_input)
        print("助手:", response)
