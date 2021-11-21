import json
import os
import time

from google.cloud import workflows_v1beta
from google.cloud.workflows import executions_v1beta
from google.cloud.workflows.executions_v1beta.types import executions


def trigger_imageprocessing_workflow(event, context):
    # TODO: Get project name programatically?
    project = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project:
        raise Exception('GOOGLE_CLOUD_PROJECT env var is required.')

    return trigger_workflow(project, 'europe-west4', 'imageprocessing', event)


def trigger_workflow(project, location, workflow, data):
    execution_client = executions_v1beta.ExecutionsClient()
    workflows_client = workflows_v1beta.WorkflowsClient()

    # Execute the workflow.
    request = {
        "parent": workflows_client.workflow_path(project, location, workflow),
        "execution": {
            "argument": json.dumps({"bucket": data["bucket"], "name": data["name"]})
        }
    }
    response = execution_client.create_execution(request=request)
    print(f"created execution: {response.name}")

    # Wait for execution to finish, then print results.
    execution_finished = False
    backoff_delay = 1  # Start wait with delay of 1 second
    print('poll for result...')
    while not execution_finished:
        execution = execution_client.get_execution(request={"name": response.name})
        execution_finished = execution.state != executions.Execution.State.ACTIVE

        # If we haven't seen the result yet, wait a second.
        if not execution_finished:
            print('- waiting for results...')
            time.sleep(backoff_delay)
            # Increase delay exponentially, to a max of 60 s
            backoff_delay = min(60, 2 * backoff_delay)
        else:
            print(f'execution finished with state: {execution.state.name}')
            print(execution.result)
            return execution.result


if __name__ == "__main__":
    storage_event = {
        "bucket": "imageprocessing-upload",
        "name": "dogs.png"
    }
    trigger_imageprocessing_workflow(storage_event, {})
