# Bot Management

PyMedplum provides comprehensive support for managing Medplum Bots, including deploying bot code, saving source code, and executing bots.

## Overview

Medplum Bots are serverless functions that run as AWS Lambda functions within the Medplum infrastructure. They can be triggered by various events and are written in TypeScript/JavaScript.

PyMedplum's bot management features allow you to:

- **Create and manage bots** with full CRUD operations
- **Deploy bot code** to AWS Lambda using the `$deploy` operation
- **Save source code** to Bot resources for version control
- **Execute bots** with custom input data
- **Combine operations** for streamlined workflows

## Bot Runtime Requirements

**IMPORTANT:** For bots to execute successfully, you must specify a `runtime_version` when creating the bot. Without this, deployment and execution will fail with an "Unsupported bot runtime" error.

Medplum supports two runtime versions:

- **`awslambda`**: Runs bots on AWS Lambda (most common)
- **`vmcontext`**: Runs bots in a VM context (advanced use cases)

### Creating Bots with Runtime

Always specify the runtime version when creating a bot:

```python
from pymedplum import MedplumClient

client = MedplumClient(base_url="https://api.medplum.com")
client.authenticate()

# Create bot with AWS Lambda runtime (required for execution!)
bot = client.create_bot(
    name="My Bot",
    description="Processes patient data",
    runtime_version="awslambda"  # This is required!
)
```

Without `runtime_version`, your bot will be created but cannot be deployed or executed.

## Installation

Bot management is built directly into the `MedplumClient`:

```python
from pymedplum import MedplumClient

client = MedplumClient(base_url="https://api.medplum.com")
client.authenticate()

# All bot methods are available on the client
client.create_bot(...)
client.deploy_bot(...)
client.execute_bot(...)
```

## Basic Usage

### Deploying a Bot

Deploy compiled JavaScript code to a bot:

```python
from pymedplum import MedplumClient

# Initialize client and authenticate
client = MedplumClient(base_url="https://api.medplum.com")
client.authenticate()

# Read your compiled bot code
with open("dist/my-bot.js") as f:
    compiled_code = f.read()

# Deploy the bot
result = client.deploy_bot(
    bot_id="your-bot-id-here",
    code=compiled_code,
    filename="index.js"  # optional, defaults to "index.js"
)

print(f"Bot deployed: {result}")
```

### Saving Bot Source Code

Save TypeScript source code to a Bot resource:

```python
# Read your bot source code
with open("src/my-bot.ts") as f:
    source_code = f.read()

# Save the source code to the Bot resource
updated_bot = client.save_bot_code(
    bot_id="your-bot-id-here",
    source_code=source_code
)

print(f"Source code saved to bot: {updated_bot['id']}")
```

### Save and Deploy in One Step

For convenience, you can save source code and deploy compiled code together:

```python
# Read both source and compiled code
with open("src/my-bot.ts") as f:
    source_code = f.read()

with open("dist/my-bot.js") as f:
    compiled_code = f.read()

# Save and deploy
bot, deploy_result = client.save_and_deploy_bot(
    bot_id="your-bot-id-here",
    source_code=source_code,
    compiled_code=compiled_code
)

print(f"Bot updated: {bot['id']}")
print(f"Deployment result: {deploy_result}")
```

### Executing a Bot

Execute a deployed bot with custom input data:

```python
# Execute the bot
result = client.execute_bot(
    bot_id="your-bot-id-here",
    input_data={
        "resourceType": "Parameters",
        "parameter": [
            {
                "name": "patientId",
                "valueString": "patient-123"
            }
        ]
    }
)

print(f"Bot execution result: {result}")
```

## Async Support

All bot management methods are available on `AsyncMedplumClient`:

```python
from pymedplum import AsyncMedplumClient

async with AsyncMedplumClient(base_url="https://api.medplum.com") as client:
    await client.authenticate()

    # Deploy bot asynchronously
    with open("dist/my-bot.js") as f:
        compiled_code = f.read()

    result = await client.deploy_bot(
        bot_id="your-bot-id-here",
        code=compiled_code
    )

    # Execute bot asynchronously
    exec_result = await client.execute_bot(
        bot_id="your-bot-id-here",
        input_data={"resourceType": "Parameters", "parameter": []}
    )
```

## Complete Workflow Example

Here's a complete example showing how to create, deploy, and execute a bot:

```python
from pymedplum import MedplumClient

# Initialize and authenticate
client = MedplumClient(base_url="https://api.medplum.com")
client.authenticate()

# Create a new Bot resource
bot = client.create_bot(
    name="My Custom Bot",
    description="A bot that processes patient data",
    runtime_version="awslambda"
)
bot_id = bot["id"]

# TypeScript source code
source_code = """
export async function handler(medplum, event) {
  const { input } = event;
  console.log('Processing input:', input);

  // Your bot logic here
  const result = {
    resourceType: 'Parameters',
    parameter: [{
      name: 'status',
      valueString: 'success'
    }]
  };

  return result;
}
"""

# Compiled JavaScript code
compiled_code = """
exports.handler = async function(medplum, event) {
  const { input } = event;
  console.log('Processing input:', input);

  const result = {
    resourceType: 'Parameters',
    parameter: [{
      name: 'status',
      valueString: 'success'
    }]
  };

  return result;
};
"""

# Save and deploy
bot, deploy_result = client.save_and_deploy_bot(
    bot_id=bot_id,
    source_code=source_code,
    compiled_code=compiled_code
)

print(f"✓ Bot {bot_id} deployed successfully")

# Execute the bot
result = client.execute_bot(
    bot_id=bot_id,
    input_data={
        "resourceType": "Parameters",
        "parameter": [
            {
                "name": "input",
                "valueString": "test data"
            }
        ]
    }
)

print(f"✓ Bot execution result: {result}")
```

## API Reference

### client.create_bot()

Create a new Bot resource.

**Parameters:**
- `name` (str): The name of the bot
- `description` (str, optional): Bot description
- `source_code` (str, optional): Initial source code
- `runtime_version` (str, optional): Runtime ("awslambda" or "vmcontext")
- `**kwargs`: Additional Bot resource properties

**Returns:** `dict[str, Any]` - The created Bot resource

### client.deploy_bot()

Deploy compiled bot code to AWS Lambda.

**Parameters:**
- `bot_id` (str): The ID of the Bot resource
- `code` (str): The compiled JavaScript code to deploy
- `filename` (str, optional): The filename for the bot code (default: "index.js")

**Returns:** `dict[str, Any]` - The response from the $deploy operation

### client.save_bot_code()

Save source code to a Bot resource's code property.

**Parameters:**
- `bot_id` (str): The ID of the Bot resource
- `source_code` (str): The source code to save (typically TypeScript)

**Returns:** `dict[str, Any]` - The updated Bot resource

### client.save_and_deploy_bot()

Save source code and deploy compiled code in one operation.

**Parameters:**
- `bot_id` (str): The ID of the Bot resource
- `source_code` (str): The source code to save
- `compiled_code` (str): The compiled JavaScript code to deploy
- `filename` (str, optional): The filename for the bot code (default: "index.js")

**Returns:** `tuple[dict[str, Any], dict[str, Any]]` - A tuple of (updated Bot resource, deploy response)

### client.execute_bot()

Execute a deployed bot.

**Parameters:**
- `bot_id` (str): The ID of the Bot to execute
- `input_data` (Any): Input data to pass to the bot
- `content_type` (str, optional): Content type (default: "application/json")

**Returns:** `dict[str, Any]` - Bot execution result

### client.read_bot()

Read a Bot resource by ID.

**Parameters:**
- `bot_id` (str): The ID of the Bot resource

**Returns:** `dict[str, Any]` - The Bot resource

### client.update_bot()

Update a Bot resource.

**Parameters:**
- `bot` (dict[str, Any]): The Bot resource with updates

**Returns:** `dict[str, Any]` - The updated Bot resource

### client.delete_bot()

Delete a Bot resource.

**Parameters:**
- `bot_id` (str): The ID of the Bot resource to delete

**Returns:** None

### client.list_bots()

List Bot resources with optional search parameters.

**Parameters:**
- `**search_params` (Any): Optional FHIR search parameters

**Returns:** `dict[str, Any]` - A Bundle of Bot resources

### Async Methods

All methods are available on `AsyncMedplumClient` and must be awaited:
- `await client.create_bot(...)`
- `await client.deploy_bot(...)`
- `await client.save_bot_code(...)`
- `await client.save_and_deploy_bot(...)`
- `await client.execute_bot(...)`
- `await client.read_bot(...)`
- `await client.update_bot(...)`
- `await client.delete_bot(...)`
- `await client.list_bots(...)`

## Best Practices

### 1. Version Control

Always save source code to the Bot resource for version control and auditing:

```python
# Good: Save source before deploying
client.save_and_deploy_bot(bot_id, source_code, compiled_code)

# Not recommended: Deploy without saving source
client.deploy_bot(bot_id, compiled_code)
```

### 2. Error Handling

Wrap bot operations in try-except blocks:

```python
try:
    result = client.deploy_bot(bot_id, compiled_code)
    print(f"Deployment successful: {result}")
except Exception as e:
    print(f"Deployment failed: {e}")
    # Handle error appropriately
```

### 3. Testing

Test bots locally before deploying:

```python
# Deploy to a test bot first
test_bot_id = "test-bot-id"
client.deploy_bot(test_bot_id, compiled_code)

# Execute and verify
result = client.execute_bot(test_bot_id, test_data)
assert result["parameter"][0]["valueString"] == "expected_value"

# Then deploy to production
client.deploy_bot(production_bot_id, compiled_code)
```

### 4. Deployment Timing

Note that bot deployments may take a moment to propagate:

```python
import time

# Deploy the bot
client.deploy_bot(bot_id, compiled_code)

# Wait a moment for deployment to complete
time.sleep(2)

# Then execute
result = client.execute_bot(bot_id, input_data)
```

## Comparison with Medplum CLI

PyMedplum's bot management features provide similar functionality to the Medplum CLI's `bot deploy` command, but within Python:

| Feature | Medplum CLI | PyMedplum |
|---------|------------|-----------|
| Deploy bot code | `npx medplum bot deploy <name>` | `client.deploy_bot(bot_id, code)` |
| Save source code | Handled automatically | `client.save_bot_code(bot_id, source)` |
| Execute bot | Via API calls | `client.execute_bot(bot_id, data)` |
| Language | Node.js/TypeScript | Python |
| Use case | CLI automation | Python applications |

Choose PyMedplum when:
- You're building Python applications
- You need programmatic bot management
- You want to integrate bot deployment into Python workflows

Choose Medplum CLI when:
- You're working primarily in Node.js/TypeScript
- You need `medplum.config.json` support
- You prefer command-line tools

## Related Documentation

- [Medplum Bots Documentation](https://www.medplum.com/docs/bots)
- [Bot Execution](https://www.medplum.com/docs/bots/bot-basics)
- [AWS Lambda Integration](https://www.medplum.com/docs/bots/bot-for-questionnaire-response)
