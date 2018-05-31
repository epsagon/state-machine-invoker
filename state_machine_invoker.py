"""
Lambda handler used to invoke a State Machine.
Make sure to update STATE_MACHINE_NAME.
"""
import os
import json
import botocore.exceptions
import boto3

STATE_MACHINE_NAME = 'MyStateMachine'  # Update this to relevant State Machine name
STATE_MACHINE_ARN_ENV = 'CF_{0}'.format(STATE_MACHINE_NAME)

client = boto3.client('stepfunctions')


def run(event, context):
    if STATE_MACHINE_ARN_ENV not in os.environ:
        print(
            'Error: State Machine ARN environment variable {0!r} was not found'.format(
                STATE_MACHINE_ARN_ENV
            )
        )
        return

    try:
        response = client.start_execution(
            stateMachineArn=os.environ[STATE_MACHINE_ARN_ENV],
            name=str(context.aws_request_id),
            input=json.dumps(event)
        )
        print(
            'Started State Machine {0!r} successfully'.format(
                response['executionArn']
            )
        )
    except botocore.exceptions.ClientError as error:
        if error.response['Error']['Code'] == 'ExecutionAlreadyExists':
            # May happen if this lambda is retried
            print(
                'State Machine was not started because this execution already exists'
            )
        else:
            # Unexpected error
            raise
