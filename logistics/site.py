import requests
from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()
client = OpenAI()
def  query_self_openai(llm_q):
    template = f"""你是java专家，请回答以下问题：
            {llm_q}
            请给出详细的代码实现。"""
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": template}],
            temperature=0,
            stream=False
        )
        answer = response.choices[0].message.content.strip() if response.choices else "无法提供答案"
        print(f"完整回答: {answer}")
        return answer
    except Exception as e:
        print(f"API调用失败: {e}")
        return "无法提供答案"



def query_company_openai(llm_q):
    # 设置请求头
    headers = {
        'Content-Type': 'application/json;charset=utf-8',
        'Authorization': 'fa2abdc3-ad1e-48c4-8c0f-750f45251dc4'
    }
    template = f"""
            {llm_q}
            """
    message = [{
        "role": "user",
        "content": template
    }]

    body = {
        "model": "glm-4-plus",
        "temperature": float(0),
        "top_p": float(1),
        "messages" : message
    }
    response = requests.post('http://gpt-proxy.jd.com/v1/chat/completions', headers=headers, json=body, stream=True)
    status_code = response.status_code
    response_body = response.json()

    print(f"Status Code: {status_code}")
    print(f"Response Body: {response_body['choices'][0]['message']['content']}")



if __name__ == "__main__":
    query_company_openai("请用java实现一个hello word")