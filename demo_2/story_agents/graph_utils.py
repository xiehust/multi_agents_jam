import operator
from typing import Annotated, Sequence,Dict,Optional,Any,TypedDict,List
from langchain_core.pydantic_v1 import ValidationError
from langchain_core.messages import AIMessage, BaseMessage
from json import JSONDecodeError

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    env_var: Optional[Annotated[Dict[str, Any], operator.ior]]
    

def get_final_state_env_var(steps:List[Any],node_name:str):
    answer = None
    for s in steps:
        for k in list(s.keys()):
            if k == node_name:
                answer = s[node_name]['env_var']
    return answer

async def retry_call(chain,args: Dict[str,Any],times:int=5):
    """
      Retry mechanism to ensure the success rate of final json output 
    """
    try:
        content = await chain.ainvoke(args)
        return content
    except JSONDecodeError as e:
        if times:
            print(f'JSONDecodeError, retry again [{times}]')
            return await retry_call(chain,args,times=times-1)
        else:
            raise(JSONDecodeError(e))
    except ValidationError as e:
        print(e)
        if times:
            print(f'ValidationError, retry again [{times}]')
            return await retry_call(chain,args,times=times-1)
        else:
            raise(ValidationError(e))