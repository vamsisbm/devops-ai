import boto3
from flask import Flask, request, jsonify
app = Flask(__name__)
bedrock_agent_runtime = boto3.client('bedrock-agent-runtime', region_name='us-east-2')
KB_ID = 'YOUR_KNOWLEDGE_BASE_ID'
MODEL_ARN = 'arn:aws:bedrock:us-east-2::foundation-model/anthropic.claude-3-5-sonnet-20241022-v2:0'

@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({'status': 'ok'}), 200

@app.route('/invocations', methods=['POST'])
def invoke():
    body = request.get_json(force=True)
    query = body.get('query', body.get('inputText', ''))
    response = bedrock_agent_runtime.retrieve_and_generate(
        input={'text': query},
        retrieveAndGenerateConfiguration={'type': 'KNOWLEDGE_BASE',
            'knowledgeBaseConfiguration': {'knowledgeBaseId': KB_ID, 'modelArn': MODEL_ARN}})
    return jsonify({'answer': response['output']['text']}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
