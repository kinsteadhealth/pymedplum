"""Integration tests for bot execution and management.

Tests the bot functionality against a live Medplum server, including:
- CRUD operations (Create, Read, Update, Delete)
- Deploying bot code
- Saving bot source code
- Executing bots
"""

import os

import pytest

from pymedplum.client import MedplumClient


def test_bot_crud_operations(medplum_client: MedplumClient):
    """Test complete CRUD lifecycle for Bot resources."""
    # CREATE
    bot = medplum_client.create_bot(
        name="Test CRUD Bot",
        description="Integration test for CRUD operations",
        runtime_version="awslambda",
    )
    assert bot["resourceType"] == "Bot"
    assert bot["name"] == "Test CRUD Bot"
    assert "id" in bot
    bot_id = bot["id"]

    try:
        # READ
        read_result = medplum_client.read_bot(bot_id)
        assert read_result["id"] == bot_id
        assert read_result["name"] == "Test CRUD Bot"

        # UPDATE
        read_result["description"] = "Updated description"
        updated = medplum_client.update_bot(read_result)
        assert updated["description"] == "Updated description"
        assert updated["id"] == bot_id

        # LIST
        bots = medplum_client.list_bots(name="Test CRUD Bot")
        assert "entry" in bots
        found = any(e["resource"]["id"] == bot_id for e in bots.get("entry", []))
        assert found, f"Bot {bot_id} should be in list results"

    finally:
        # DELETE
        medplum_client.delete_bot(bot_id)

    # Verify deletion - expect 410 Gone error
    from pymedplum.exceptions import OperationOutcomeError

    with pytest.raises(OperationOutcomeError) as exc_info:
        medplum_client.read_bot(bot_id)
    # 410 Gone surfaces as OperationOutcomeError; the outcome itself is attached
    # on exc.outcome for inspection. We can't assert on HTTP status directly
    # without the response, so we assert the outcome shape instead.
    assert isinstance(exc_info.value.outcome, dict)


def test_save_bot_code(medplum_client: MedplumClient):
    """Test saving bot source code to a Bot resource."""
    bot = medplum_client.create_bot(
        name="Test Bot for Source Code",
        description="Integration test bot",
        runtime_version="awslambda",
    )
    bot_id = bot["id"]

    try:
        source_code = """
export async function handler(medplum, event) {
  console.log('Test bot executed');
  return { message: 'Hello from test bot' };
}
"""
        updated_bot = medplum_client.save_bot_code(bot_id, source_code)

        assert updated_bot["code"] == source_code
        assert "id" in updated_bot

    finally:
        medplum_client.delete_bot(bot_id)


def test_deploy_bot(medplum_client: MedplumClient):
    """Test deploying bot code using the $deploy operation."""
    bot = medplum_client.create_bot(
        name="Test Bot for Deployment",
        description="Integration test bot for deployment",
        runtime_version="awslambda",
    )
    bot_id = bot["id"]

    try:
        compiled_code = """
exports.handler = async function(medplum, event) {
  console.log('Test bot deployed and executed');
  return {
    resourceType: 'Parameters',
    parameter: [{
      name: 'result',
      valueString: 'Deployment successful'
    }]
  };
};
"""
        deploy_result = medplum_client.deploy_bot(bot_id, compiled_code)
        assert deploy_result is not None

    finally:
        medplum_client.delete_bot(bot_id)


def test_save_and_deploy_bot(medplum_client: MedplumClient):
    """Test the combined save and deploy operation."""
    bot = medplum_client.create_bot(
        name="Test Bot for Save and Deploy",
        description="Integration test bot for combined operation",
        runtime_version="awslambda",
    )
    bot_id = bot["id"]

    try:
        source_code = """
export async function handler(medplum, event) {
  return {
    resourceType: 'Parameters',
    parameter: [{ name: 'status', valueString: 'success' }]
  };
}
"""
        compiled_code = """
exports.handler = async function(medplum, event) {
  return {
    resourceType: 'Parameters',
    parameter: [{ name: 'status', valueString: 'success' }]
  };
};
"""
        updated_bot, deploy_result = medplum_client.save_and_deploy_bot(
            bot_id, source_code, compiled_code
        )

        assert updated_bot["code"] == source_code
        assert "id" in updated_bot
        assert deploy_result is not None

    finally:
        medplum_client.delete_bot(bot_id)


def test_execute_bot(medplum_client: MedplumClient):
    """Test executing a bot by its ID.

    The bot ID is specified via the MEDPLUM_TEST_BOT_ID environment variable in .env.
    If not set, the test is skipped. If set but the bot doesn't exist, the test fails.
    """
    # Get bot ID from environment (loaded via load_dotenv in conftest.py)
    bot_id = os.getenv("MEDPLUM_TEST_BOT_ID")

    if not bot_id:
        pytest.skip(
            "MEDPLUM_TEST_BOT_ID not set in .env file - skipping bot execution test"
        )

    # Verify the bot exists - if it doesn't, this should fail the test
    bot = medplum_client.read_bot(bot_id)
    assert bot["id"] == bot_id, f"Bot {bot_id} not found"

    # Attempt to execute the bot
    result = medplum_client.execute_bot(
        bot_id=bot_id,
        input_data={"resourceType": "Parameters", "parameter": []},
    )

    # If we get here, execution succeeded
    assert result is not None


def test_complete_bot_lifecycle(medplum_client: MedplumClient):
    """Test the complete bot lifecycle from creation to deletion."""
    bot = medplum_client.create_bot(
        name="Complete Lifecycle Bot",
        description="Testing complete lifecycle",
        runtime_version="awslambda",
    )
    bot_id = bot["id"]

    try:
        # Save source code
        source_code = """
export async function handler(medplum, event) {
  const input = event.input || {};
  return {
    resourceType: 'Parameters',
    parameter: [{
      name: 'output',
      valueString: 'Lifecycle test successful'
    }]
  };
}
"""
        bot = medplum_client.save_bot_code(bot_id, source_code)
        assert bot["code"] == source_code

        # Deploy compiled code
        compiled_code = """
exports.handler = async function(medplum, event) {
  const input = event.input || {};
  return {
    resourceType: 'Parameters',
    parameter: [{
      name: 'output',
      valueString: 'Lifecycle test successful'
    }]
  };
};
"""
        deploy_result = medplum_client.deploy_bot(bot_id, compiled_code)
        assert deploy_result is not None

        # Update bot
        bot["description"] = "Lifecycle test - updated"
        bot = medplum_client.update_bot(bot)
        assert bot["description"] == "Lifecycle test - updated"

    finally:
        medplum_client.delete_bot(bot_id)
