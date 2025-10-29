from bedrock_agentcore_starter_toolkit import Runtime
from boto3.session import Session
import time

boto_session = Session()
region = boto_session.region_name


agentcore_runtime = Runtime()

response = agentcore_runtime.configure(
    entrypoint="strands_claude_streaming.py",
    auto_create_execution_role=True,
    auto_create_ecr=True,
    requirements_file="requirements.txt",
    region=region,
    agent_name="strands_claude_streaming"
)

launch_result = agentcore_runtime.launch()

status_response = agentcore_runtime.status()
status = status_response.endpoint['status']
end_status = ['READY', 'CREATE_FAILED', 'DELETE_FAILED', 'UPDATE_FAILED']
while status not in end_status:
    time.sleep(10)
    status_response = agentcore_runtime.status()
    status = status_response.endpoint['status']
    print(status)

time.sleep(30)
invoke_response = agentcore_runtime.invoke({
    "prompt":
    "give me a detailed response of why people are going crazy with artificial inteligence"
})