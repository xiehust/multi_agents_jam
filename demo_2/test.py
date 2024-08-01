# import aiohttp
# import asyncio
# import boto3 
# from botocore.auth import SigV4Auth
# from botocore.awsrequest import AWSRequest

# endpoint_name= 'story-diffusion-inference-api-2024-07-31-09-12-26-010'
# async def async_invoke_endpoint(endpoint_name,payload):
#     client = boto3.client('sagemaker-runtime')
#     request = AWSRequest(
#         method='POST',
#         url=f'https://runtime.sagemaker.{client.meta.region_name}.amazonaws.com/endpoints/{endpoint_name}/invocations',
#             data=payload,
#         headers={'Content-Type':'application/json'})
                                
#     SigV4Auth(client._request_signer).add_auth(request)
#     async with aiohttp.ClientSession() as session:
#         async with session.post(reguest.url, data=request.data, headers=reguest.headers) as response:
#             result = await response.text()
#             print(f'Result: {result}')
# # Run the async function
# payload ='{"instances": [...]}'
# asyncio.run(async_invoke_endpoint(endpoint_name, payload))

import asyncio
import aiobotocore
from aiobotocore.session import get_session


async def async_invoke_endpoint(endpoint_name, body, content_type='application/json'):
    session = get_session()
    async with session.create_client('sagemaker-runtime') as client:
        response = await client.invoke_endpoint(
            EndpointName=endpoint_name,
            ContentType=content_type,
            Body=body
        )
        return await response['Body'].read()

async def async_invoke_endpoint_with_response_stream(endpoint_name, body, content_type='application/json'):
    session = get_session()
    async with session.create_client('sagemaker-runtime') as client:
        response = await client.invoke_endpoint_with_response_stream(
            EndpointName=endpoint_name,
            ContentType=content_type,
            Body=body
        )
        async for event in response['Body']:
            if event.get('PayloadPart'):
                yield event['PayloadPart']['Bytes'].decode('utf-8')
    
    
# 使用示例
async def main():
    endpoint_name = 'Qwen2-7B-Chat-2024-08-01-07-56-05-772'
    input_data = '{"inputs": "hello"}'
    
    result = await async_invoke_endpoint(endpoint_name, input_data)
    print(result.decode('utf-8'))
    
    async for chunk in async_invoke_endpoint_with_response_stream(endpoint_name, input_data):
        print("Received chunk:", chunk)

# 运行异步函数
asyncio.run(main())