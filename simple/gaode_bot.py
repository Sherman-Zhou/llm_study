# 导入必要的库和模块
import openai
import os
from math import *
from icecream import ic
import json
import requests
import logging
# 设置日志记录配置
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 加载环境变量
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

# 初始化OpenAI API密钥和模型
openai.api_key = os.getenv('OPENAI_API_KEY')
openai.api_base = os.getenv('OPENAI_API_URL')
model = os.getenv('MODEL')
amap_key = os.getenv('GAODE_MAP_API_KEY')

# 通过高德地图API获取地点的经纬度坐标
# 用于查询某个地点的地理坐标。
def get_location_coordinate(location, city="长沙"):
    """    
    根据地点和城市名称，使用高德地图API查询并返回该地点的坐标。 
           
    参数:    
    location (str): 地点名称。    
    city (str): 城市名称，默认为“长沙”。       
     
    返回:    
    dict: 包含地点坐标信息的字典，如果没有找到则返回None。    
    """    
    url = f"https://restapi.amap.com/v5/place/text?key={amap_key}&keywords={location}&region={city}"    
    ic(url)    
    r = requests.get(url)    
    result = r.json()    
    if "pois" in result and result["pois"]:        
        return result["pois"][0]
    return None

# 通过高德地图API查询给定坐标附近的兴趣点（POIs）
#用于查询地理坐标附近的某些信息（取决于用户输入的Keyword）
#这是用的高德地图的开放接口，在使用本例之前，你需要先去高德地图开放接口的官网(https://console.amap.com/dev/key/app)申请一个key，免费的。这里就不过多介绍了。
def search_nearby_pois(longitude, latitude, keyword):
    """    
    根据给定的经纬度和关键词，使用高德地图API查询并返回附近的兴趣点信息。   
         
    参数:    
    longitude (str): 经度。    
    latitude (str): 纬度。    
    keyword (str): 查询关键词。      
      
    返回:    
    str: 包含查询结果的字符串，如果没有找到则返回空字符串。    
    """    
    url = f"https://restapi.amap.com/v5/place/around?key={amap_key}&keywords={keyword}&location={longitude},{latitude}"    
    ic(url)    
    r = requests.get(url)    
    result = r.json()    
    ans = ""    
    if "pois" in result and result["pois"]:      
        for i in range(min(3, len(result["pois"]))):       
            name = result["pois"][i]["name"]            
            address = result["pois"][i]["address"]            
            distance = result["pois"][i]["distance"]            
            ans += f"{name}\n{address}\n距离：{distance}米\n\n"    
    return ans

# 使用OpenAI API完成聊天对话
def get_completion(messages, model=model):
    """    
    根据输入的消息列表，使用OpenAI API生成并返回聊天对话的回复。  
          
    参数:    
    messages (list): 消息列表，包含系统的和用户的对话内容。    
    model (str): 使用的OpenAI模型，默认为环境变量中的MODEL。   
        
    返回:    
    dict: 包含OpenAI生成的回复信息的字典。    
    """    
    response = openai.ChatCompletion.create(
        model=model,        
        messages=messages,        
        temperature=0,  # 模型输出的随机性，0 表示随机性最小        
        seed=1024,  # 随机种子保持不变，temperature 和 prompt 不变的情况下，输出就会不变        
        tool_choice="auto",  # 默认值，由系统自动决定，返回function call还是返回文字回复        
        tools=[{      
            "type": "function",            
            "function": {           
            
                "name": "get_location_coordinate",                
                "description": "根据POI名称，获得POI的经纬度坐标",                
                "parameters": {                
                    "type": "object",                    
                    "properties": {                        
                        "location": {                        
                            "type": "string",                            
                            "description": "POI名称，必须是中文",                        
                        },                        
                        "city": {                         
                            "type": "string",                            
                            "description": "POI所在的城市名，必须是中文",                        
                        }                    
                    },                    
                    "required": ["location", "city"],                
                }            
            }        
       },       
            {            
            "type": "function",            
            "function": {                
                "name": "search_nearby_pois",                
                "description": "搜索给定坐标附近的poi",                
                "parameters": {               
                    "type": "object",                    
                    "properties": {                    
                        "longitude": {                       
                            "type": "string",                            
                            "description": "中心点的经度",                        
                        },                        
                        "latitude": {                       
                            "type": "string",                            
                            "description": "中心点的纬度",                        
                        },                        
                        "keyword": {                         
                            "type": "string",                            
                            "description": "目标poi的关键字",                        
                        }                    
                    },                    
                    "required": ["longitude", "latitude", "keyword"],                
                }            
            }        
        }],    
    )    
    return response.choices[0].message

# 处理工具函数调用
def handle_tool_call(response, messages):
    """    
    处理聊天对话中的工具函数调用，根据调用的函数名称和参数执行相应的操作，并将结果添加到消息列表中。        
    
    参数:    
    response (dict): 包含工具函数调用信息的响应字典。    
    messages (list): 消息列表，用于添加工具函数的调用结果。    
    """    
    if response.tool_calls is not None:    
        for tool_call in response.tool_calls:       
            try:           
                args = json.loads(tool_call.function.arguments)            
            except json.JSONDecodeError:           
                logging.error("解析工具函数参数失败")                
                continue  # 跳过当前循环            
            logging.info(f"调用: {tool_call.function.name}")            
            try:           
                if tool_call.function.name == "get_location_coordinate":               
                    result = get_location_coordinate(**args)                
                elif tool_call.function.name == "search_nearby_pois":               
                    result = search_nearby_pois(**args)            
            except Exception as e:             
                logging.error(f"调用 {tool_call.function.name} 出错: {e}")                
                continue  # 跳过当前循环            
            logging.info("函数返回: ")            
            logging.info(result)            
            messages.append({          
                "tool_call_id": tool_call.id,                
                "role": "tool",                
                "name": tool_call.function.name,                
                "content": str(result)            
            })

# 测试聊天对话流程
def test_promopt():
    """    
    测试聊天助手的功能，模拟用户查询长沙证券大厦附近的咖啡店。    
    """    
    prompt = "长沙证券大厦附近的咖啡"    
    messages = [    
        {"role": "system", "content": "你是一个地图通，你可以找到任何地址。"},        
        {"role": "user", "content": prompt}    
    ]    
    
    try:  
        response = get_completion(messages)    
    except Exception as e:   
        logging.error(f"获取初始响应失败: {e}")        
        return    

    # 处理初始响应    
    if response.content is None:   
        response.content = "null"    
    messages.append(response)    
    
    logging.info("=====GPT回复=====")    
    logging.info(response)    
    
    while True:   
        handle_tool_call(response, messages)        
        
        # 检查是否还有更多响应        
        try:        
            response = get_completion(messages)        
        except Exception as e:       
            logging.error(f"获取后续响应失败: {e}")            
            break        
        if response.content is None:     
            response.content = "null"            
            messages.append(response)        
        if not hasattr(response,'tool_calls'):  # 如果没有tool_calls属性，则表示没有更多响应            
            break    
    logging.info("=====最终回复=====")    
    logging.info(response.content)

# 主程序入口
if __name__ == '__main__':
    test_promopt()
