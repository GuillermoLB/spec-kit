# Feature: AWS SAM Serverless API Example

**Status**: Draft
**Owner**: spec-kit development team
**Last Updated**: 2026-01-17
**Priority**: Medium

## Purpose

Create a production-ready serverless REST API example using AWS SAM (Serverless Application Model) and Lambda that demonstrates spec-kit's api-development plugin in a serverless context. This example shows cloud-native patterns, infrastructure as code, and spec-driven development for serverless applications.

## Requirements

- [ ] Complete serverless API with AWS Lambda functions
- [ ] SAM template (template.yaml) for infrastructure as code
- [ ] DynamoDB table for data persistence
- [ ] API Gateway REST API configuration
- [ ] CRUD operations for user resources
- [ ] Local testing with SAM CLI (sam local)
- [ ] Feature specifications for each endpoint
- [ ] OpenAPI specification in specs/api/
- [ ] Comprehensive pytest test suite
- [ ] Deployment instructions for AWS
- [ ] Environment-specific configuration (dev, prod)
- [ ] CloudWatch logging integration

## User Stories

**As a** developer building serverless applications
**I want** a reference SAM project using spec-kit
**So that** I can see serverless best practices and spec-driven development

**As a** DevOps engineer
**I want** infrastructure as code examples
**So that** I can deploy consistent serverless applications

**As a** cloud architect
**I want** to see AWS serverless patterns
**So that** I can evaluate spec-kit for serverless projects

## Acceptance Criteria

1. **Given** I have AWS SAM CLI installed
   **When** I run `sam local start-api`
   **Then** the API runs locally and I can test all endpoints

2. **Given** I examine the specs/features/ directory
   **When** I read the specifications
   **Then** each spec describes a serverless endpoint with acceptance criteria

3. **Given** I want to deploy to AWS
   **When** I follow the deployment instructions
   **Then** the application deploys successfully to my AWS account

4. **Given** I run the test suite
   **When** I execute pytest
   **Then** all tests pass with mocked AWS services

5. **Given** I call an API endpoint
   **When** the request is processed
   **Then** logs appear in CloudWatch with proper structure

6. **Given** I compare infrastructure to specs
   **When** I review template.yaml
   **Then** the SAM template matches the architecture specifications

## Technical Details

### Architecture

**Serverless REST API with Lambda + DynamoDB:**

```
examples/serverless-api-sam/
├── CLAUDE.md
├── README.md
├── .claude/
│   └── skills/
│       └── api-development/
│           ├── SKILL.md
│           └── references/
│               ├── fastapi-endpoint.py
│               └── sam-template.yaml
├── template.yaml              # SAM CloudFormation template
├── samconfig.toml             # SAM deployment config
├── specs/
│   ├── features/
│   │   ├── create-user.md
│   │   ├── get-user.md
│   │   ├── list-users.md
│   │   ├── update-user.md
│   │   └── delete-user.md
│   ├── api/
│   │   └── users-api.yaml     # OpenAPI spec
│   └── architecture.md        # System architecture
├── src/
│   ├── __init__.py
│   ├── common/
│   │   ├── __init__.py
│   │   ├── responses.py       # Standard response formats
│   │   ├── validators.py      # Input validation
│   │   └── dynamodb.py        # DynamoDB client wrapper
│   └── functions/
│       ├── create_user/
│       │   ├── __init__.py
│       │   ├── app.py         # Lambda handler
│       │   └── requirements.txt
│       ├── get_user/
│       │   ├── __init__.py
│       │   └── app.py
│       ├── list_users/
│       │   ├── __init__.py
│       │   └── app.py
│       ├── update_user/
│       │   ├── __init__.py
│       │   └── app.py
│       └── delete_user/
│           ├── __init__.py
│           └── app.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py            # Pytest fixtures
│   ├── unit/
│   │   ├── test_create_user.py
│   │   ├── test_get_user.py
│   │   ├── test_list_users.py
│   │   ├── test_update_user.py
│   │   └── test_delete_user.py
│   └── integration/
│       └── test_api_flow.py   # End-to-end tests
├── events/                     # Test events for local testing
│   ├── create_user.json
│   ├── get_user.json
│   └── list_users.json
├── requirements.txt            # Dev dependencies
└── .gitignore
```

### AWS Resources (SAM Template)

**Infrastructure:**

| Resource | Type | Purpose |
|----------|------|---------|
| UsersTable | AWS::DynamoDB::Table | Store user data |
| UsersApi | AWS::Serverless::Api | API Gateway REST API |
| CreateUserFunction | AWS::Serverless::Function | POST /users handler |
| GetUserFunction | AWS::Serverless::Function | GET /users/{id} handler |
| ListUsersFunction | AWS::Serverless::Function | GET /users handler |
| UpdateUserFunction | AWS::Serverless::Function | PUT /users/{id} handler |
| DeleteUserFunction | AWS::Serverless::Function | DELETE /users/{id} handler |

### API Endpoints

| Method | Path | Lambda Function | Description |
|--------|------|-----------------|-------------|
| POST | /users | CreateUserFunction | Create new user |
| GET | /users | ListUsersFunction | List all users (paginated) |
| GET | /users/{id} | GetUserFunction | Get single user |
| PUT | /users/{id} | UpdateUserFunction | Update user |
| DELETE | /users/{id} | DeleteUserFunction | Delete user |

### Data Model (DynamoDB)

**Users Table Schema:**

```python
{
    "id": "string (UUID, partition key)",
    "email": "string (required, unique via GSI)",
    "name": "string (required)",
    "created_at": "string (ISO 8601)",
    "updated_at": "string (ISO 8601)"
}
```

**Indexes:**
- Primary Key: `id` (partition key)
- GSI: `email-index` on `email` field

### Technology Stack

- **Runtime**: Python 3.11
- **Framework**: None (pure Lambda handlers) or FastAPI with Mangum adapter
- **Database**: DynamoDB
- **Infrastructure**: AWS SAM / CloudFormation
- **API Gateway**: REST API
- **Logging**: CloudWatch Logs
- **Testing**: pytest, moto (AWS mocking)

### SAM Template Structure

**Key Sections:**

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31

Globals:
  Function:
    Timeout: 10
    Runtime: python3.11
    Environment:
      Variables:
        USERS_TABLE: !Ref UsersTable
        LOG_LEVEL: INFO

Resources:
  UsersTable:
    Type: AWS::DynamoDB::Table
    Properties:
      AttributeDefinitions:
        - AttributeName: id
          AttributeType: S
        - AttributeName: email
          AttributeType: S
      KeySchema:
        - AttributeName: id
          KeyType: HASH
      GlobalSecondaryIndexes:
        - IndexName: email-index
          KeySchema:
            - AttributeName: email
              KeyType: HASH
          Projection:
            ProjectionType: ALL
      BillingMode: PAY_PER_REQUEST

  CreateUserFunction:
    Type: AWS::Serverless::Function
    Properties:
      CodeUri: src/functions/create_user/
      Handler: app.lambda_handler
      Policies:
        - DynamoDBCrudPolicy:
            TableName: !Ref UsersTable
      Events:
        CreateUser:
          Type: Api
          Properties:
            Path: /users
            Method: post
            RestApiId: !Ref UsersApi

Outputs:
  UsersApi:
    Description: "API Gateway endpoint URL"
    Value: !Sub "https://${UsersApi}.execute-api.${AWS::Region}.amazonaws.com/Prod/"
  UsersTableName:
    Description: "DynamoDB table name"
    Value: !Ref UsersTable
```

### Lambda Handler Pattern

```python
# src/functions/create_user/app.py
import json
import boto3
import os
from uuid import uuid4
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['USERS_TABLE'])

def lambda_handler(event, context):
    """
    Create new user in DynamoDB.

    Event: API Gateway proxy request
    Returns: API Gateway proxy response
    """
    try:
        body = json.loads(event['body'])

        # Validate required fields
        if 'email' not in body or 'name' not in body:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'email and name are required'})
            }

        # Create user
        user_id = str(uuid4())
        timestamp = datetime.utcnow().isoformat()

        user = {
            'id': user_id,
            'email': body['email'],
            'name': body['name'],
            'created_at': timestamp,
            'updated_at': timestamp
        }

        table.put_item(Item=user)

        return {
            'statusCode': 201,
            'body': json.dumps(user),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            }
        }

    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Internal server error'})
        }
```

### Local Development

**Commands:**

```bash
# Build functions
sam build

# Start local API
sam local start-api

# Invoke single function
sam local invoke CreateUserFunction --event events/create_user.json

# Run tests
pytest tests/ -v
```

### Deployment

**Commands:**

```bash
# Deploy to AWS (first time)
sam deploy --guided

# Deploy updates
sam deploy

# Tail logs
sam logs -n CreateUserFunction --tail

# Delete stack
sam delete
```

### Security Considerations

- [ ] IAM least privilege policies (DynamoDB CRUD only)
- [ ] API Gateway throttling configured
- [ ] Input validation on all endpoints
- [ ] CORS properly configured
- [ ] CloudWatch logs encrypted
- [ ] No hardcoded credentials
- [ ] Environment variables for configuration

## Edge Cases & Error Handling

1. **Edge case**: Create user with duplicate email
   - **Handling**: Use DynamoDB conditional write, return 409 Conflict

2. **Edge case**: Get non-existent user
   - **Message**: "404 Not Found: User not found"
   - **Recovery**: Client checks user ID

3. **Error**: DynamoDB throttling
   - **Message**: "503 Service Unavailable: Database temporarily unavailable"
   - **Recovery**: Implement exponential backoff retry

4. **Edge case**: List users with no results
   - **Handling**: Return empty array with 200 OK

5. **Error**: Invalid JSON in request body
   - **Message**: "400 Bad Request: Invalid JSON"
   - **Recovery**: Client fixes JSON format

## Testing Strategy

### Unit Tests

- [ ] Test each Lambda handler with mocked DynamoDB
- [ ] Test input validation logic
- [ ] Test response formatting
- [ ] Test error handling paths

### Integration Tests

- [ ] Test full CRUD workflow
- [ ] Test with local DynamoDB (DynamoDB Local)
- [ ] Test API Gateway integration
- [ ] Test pagination

### Mocking with Moto

```python
import boto3
from moto import mock_dynamodb
import pytest

@mock_dynamodb
def test_create_user():
    # Setup mock DynamoDB
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.create_table(
        TableName='users-table',
        KeySchema=[{'AttributeName': 'id', 'KeyType': 'HASH'}],
        AttributeDefinitions=[{'AttributeName': 'id', 'AttributeType': 'S'}],
        BillingMode='PAY_PER_REQUEST'
    )

    # Test Lambda handler
    from src.functions.create_user.app import lambda_handler

    event = {
        'body': json.dumps({'email': 'test@example.com', 'name': 'Test User'})
    }

    response = lambda_handler(event, {})
    assert response['statusCode'] == 201
```

### Test Coverage Goals

- Minimum 80% code coverage
- 100% coverage on handler entry points
- All error paths tested

### Manual Testing Checklist

- [ ] Deploy to AWS dev account
- [ ] Create user via API Gateway
- [ ] List users
- [ ] Get single user
- [ ] Update user
- [ ] Delete user
- [ ] Test with invalid data
- [ ] Check CloudWatch logs

## Dependencies

- **Blocked by**: documentation-improvements, testing-infrastructure
- **Blocks**: None
- **Related**: example-fastapi-todo (CRUD patterns), plugin-cicd (deployment automation)

## Implementation Notes

### Decisions Made

- 2026-01-17 - Use DynamoDB (serverless-native, no server management)
- 2026-01-17 - Pure Lambda handlers (no FastAPI initially for simplicity)
- 2026-01-17 - REST API (not HTTP API) for feature completeness
- 2026-01-17 - Python 3.11 (latest stable Lambda runtime)
- 2026-01-17 - Separate function per endpoint (better isolation)
- 2026-01-17 - GSI on email for uniqueness checks

### Environment Configuration

**samconfig.toml:**

```toml
[default.deploy.parameters]
stack_name = "spec-kit-users-api"
s3_bucket = "spec-kit-sam-deployments"
s3_prefix = "users-api"
region = "us-east-1"
capabilities = "CAPABILITY_IAM"
parameter_overrides = "Environment=dev"
```

### README Content

The example README should include:

1. **Overview** - Serverless API with SAM
2. **Architecture** - Diagram of Lambda + API Gateway + DynamoDB
3. **Prerequisites** - AWS account, SAM CLI, Python 3.11
4. **Local Development** - sam build, sam local commands
5. **Deployment** - Step-by-step AWS deployment
6. **Testing** - Unit and integration tests
7. **Costs** - AWS pricing estimates
8. **Spec-Driven Workflow** - How specs guided infrastructure design
9. **Cleanup** - How to delete resources

### Cost Estimates

**Monthly costs (low traffic):**
- Lambda: ~$0.20 (1M requests)
- DynamoDB: ~$1.25 (on-demand, 1GB storage)
- API Gateway: ~$3.50 (1M requests)
- **Total: ~$5/month** for development

## Verification

### Local Verification

```bash
cd examples/serverless-api-sam

# Build
sam build

# Start API locally
sam local start-api

# Test endpoint
curl -X POST http://localhost:3000/users \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","name":"Test User"}'
```

### AWS Deployment Verification

```bash
# Deploy
sam deploy --guided

# Get API URL from outputs
aws cloudformation describe-stacks \
  --stack-name spec-kit-users-api \
  --query 'Stacks[0].Outputs'

# Test deployed API
curl -X POST https://{api-id}.execute-api.us-east-1.amazonaws.com/Prod/users \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","name":"Test User"}'
```

### Test Verification

```bash
pytest tests/ -v --cov=src --cov-report=term-missing
```

## References

- API development plugin: [plugins/api-development/](../../plugins/api-development/)
- SAM template example: [plugins/api-development/templates/sam-template.yaml](../../plugins/api-development/templates/sam-template.yaml)
- AWS SAM docs: https://docs.aws.amazon.com/serverless-application-model/
- DynamoDB best practices: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/best-practices.html

---

**Template Version**: 1.0
**Last Updated**: 2026-01-17
