import boto3
import json
from IPython.display import Markdown, display

agent_arn = launch_result.agent_arn

agentcore_client = boto3.client(
    'bedrock-agentcore',
    region_name=region
)

# For streaming responses, we need to handle the EventStream
boto3_response = agentcore_client.invoke_agent_runtime(
    agentRuntimeArn=agent_arn,
    qualifier="DEFAULT",
    payload=json.dumps({"prompt": "How much is 2+1"})
)

# Check if the response is streaming
if "text/event-stream" in boto3_response.get("contentType", ""):
    print("Processing streaming response with boto3:")
    content = []
    for line in boto3_response["response"].iter_lines(chunk_size=1):
        if line:
            line = line.decode("utf-8")
            if line.startswith("data: "):
                data = line[6:].replace('"', '')  # Remove "data: " prefix
                print(f"Received streaming chunk: {data}")
                content.append(data.replace('"', ''))

    # Display the complete streamed response
    full_response = " ".join(content)
    display(Markdown(full_response))
else:
    # Handle non-streaming response
    try:
        events = []
        for event in boto3_response.get("response", []):
            events.append(event)
    except Exception as e:
        events = [f"Error reading EventStream: {e}"]

    if events:
        try:
            response_data = json.loads(events[0].decode("utf-8"))
            display(Markdown(response_data))
        except:
            print(f"Raw response: {events[0]}")