import os
import json
import re
from langchain_core.output_parsers.base import BaseOutputParser
from langchain_core.runnables import RunnableLambda
from langchain_core.pydantic_v1 import BaseModel, Field
from json import JSONDecodeError
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, ToolMessage

def preprocess_answer_json(raw_text):
    content = raw_text.replace('\n', ' ')  # 移除换行符
    content = content.replace('\r', '')   # 移除回车符
    content = content.replace('\t', ' ')  # 替换制表符为空格
    
    # 处理转义字符
    content = content.replace('\\"', '"')  # 替换 \" 为 "
    content = content.replace('\\', '\\\\')  # 替换单个 \ 为 \\
    
    # 确保引号正确配对
    content = re.sub(r'(?<!\\)"', '\\"', content)  # 转义未转义的引号
    content = content.replace('\\"', '"')  # 恢复正确的引号
    return content
    


def dict_to_obj(json_str:dict, target:object):
    return target.parse_obj(json_str)


class CustJsonOuputParser(BaseOutputParser[str]): 
    verbose :bool = Field( default=True)

    def parse(self, text: str) -> str:
        if self.verbose:
            print(text)
        pattern = r"```json(.*?)```"
        match = re.search(pattern, text, re.DOTALL)
        if match:
            text = match.group(1)
        else:
            return {}    
        text = preprocess_answer_json(text)
        new_dict = json.loads(text)
        
        return new_dict

    @property
    def _type(self) -> str:
        return "cust_output_parser"

class TextOuputParser(BaseOutputParser[str]): 
    verbose :bool = Field( default=True)

    def parse(self, text: str) -> str:
        if self.verbose:
            print(text)
        pattern = r"<answer>(.*?)</answer>"
        match = re.search(pattern, text, re.DOTALL)
        if match:
            text = match.group(1)
            return text.strip()
        else:
            return ''

    @property
    def _type(self) -> str:
        return "TextOuputParser"
    
def convert_message_name(message:BaseMessage):
    if isinstance(message, AIMessage) and message.name:
        return AIMessage(content=f"{message.name} : {message.content}")
    elif isinstance(message, HumanMessage) and message.name:
        return HumanMessage(content=f"{message.name} : {message.content}")
    else:
        return message

##merge the continouse roles, and change sequences 
def reconstruct_to_claude_messages(messages):
    rec_messages = []
    for message in messages:
        message = convert_message_name(message)
        if rec_messages:
            if isinstance(rec_messages[0], AIMessage):
                rec_messages[0] = HumanMessage(content=rec_messages[0].content)
            last_msg = rec_messages[-1]
            last_role = 'assistant' if isinstance(last_msg,AIMessage) else 'user'
            current_role = 'assistant' if isinstance(message,AIMessage) else 'user'
            if last_role == current_role:
                last_msg_content = last_msg.content[-1]['text'] if isinstance(last_msg.content,list) else last_msg.content
                current_msg_content = message.content[-1]['text'] if isinstance(message.content, list) else message.content
                new_content = last_msg_content +"\n\n" + current_msg_content
                rec_messages[-1] = HumanMessage(content=new_content) if last_role == 'user' else AIMessage(content=new_content)
            else:
                rec_messages.append(message)
        else:
            rec_messages.append(message)
    return rec_messages

def swap_roles(messages, name: str):
    converted = []
    for message in messages:
        if isinstance(message, AIMessage) and message.name != name:
            message = HumanMessage(**message.dict(exclude={"type"}))
        converted.append(message)
    return  converted


