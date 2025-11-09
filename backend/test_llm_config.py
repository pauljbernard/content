"""
Test LLM Configuration System
"""
import requests
import json

BASE_URL = "http://localhost:8000/api/v1"
TEST_USER = {
    "email": "admin@hmhco.com",
    "password": "changeme"
}

def get_auth_token():
    """Login and get auth token."""
    response = requests.post(
        "http://localhost:8000/api/v1/auth/login",
        data={"username": TEST_USER["email"], "password": TEST_USER["password"]}
    )
    response.raise_for_status()
    return response.json()["access_token"]

def test_llm_config():
    """Test the LLM configuration workflow."""
    print("=" * 60)
    print("Testing LLM Configuration System")
    print("=" * 60)

    # Get auth token
    print("\n1. Authenticating...")
    token = get_auth_token()
    headers = {"Authorization": f"Bearer {token}"}
    print("   ✓ Authenticated")

    # Test 1: Create OpenAI provider
    print("\n2. Creating OpenAI provider...")
    provider_data = {
        "name": "openai",
        "display_name": "OpenAI",
        "description": "Official OpenAI API",
        "provider_type": "openai",
        "api_key": "sk-test-key-12345",
        "api_base_url": "https://api.openai.com/v1",
        "supports_chat": True,
        "supports_embeddings": True,
        "supports_function_calling": True,
        "supports_streaming": True,
        "requests_per_minute": 500,
        "tokens_per_minute": 100000,
    }

    response = requests.post(
        f"{BASE_URL}/llm-providers",
        headers=headers,
        json=provider_data
    )
    response.raise_for_status()
    provider = response.json()
    provider_id = provider["id"]

    print(f"   ✓ Provider created: {provider['display_name']}")
    print(f"     ID: {provider_id}")
    print(f"     API Key Masked: {provider['api_key_masked']}")

    # Test 2: List providers
    print("\n3. Listing all providers...")
    response = requests.get(f"{BASE_URL}/llm-providers", headers=headers)
    response.raise_for_status()
    providers = response.json()

    print(f"   ✓ Found {len(providers)} provider(s)")
    for p in providers:
        print(f"     - {p['display_name']} ({p['provider_type']})")

    # Test 3: Test provider connection
    print("\n4. Testing provider connection...")
    response = requests.post(
        f"{BASE_URL}/llm-providers/{provider_id}/test",
        headers=headers
    )
    if response.status_code == 200:
        result = response.json()
        print(f"   ✓ Connection test passed: {result['message']}")
    else:
        print(f"   ⚠ Connection test failed (expected - using test API key)")

    # Test 4: Create embedding model
    print("\n5. Creating embedding model...")
    model_data = {
        "provider_id": provider_id,
        "model_id": "text-embedding-3-small",
        "display_name": "Text Embedding 3 Small",
        "description": "OpenAI's text embedding model (1536 dimensions)",
        "model_type": "embedding",
        "context_window": 8191,
        "max_output_tokens": None,
        "supports_vision": False,
        "supports_json_mode": False,
        "supports_tools": False,
        "default_temperature": 0.0,
        "default_top_p": 1.0,
        "input_cost_per_1m": 0.02,
        "output_cost_per_1m": 0.0,
        "is_default_for_embeddings": True,
    }

    response = requests.post(
        f"{BASE_URL}/llm-models",
        headers=headers,
        json=model_data
    )
    response.raise_for_status()
    model = response.json()
    model_id = model["id"]

    print(f"   ✓ Model created: {model['display_name']}")
    print(f"     ID: {model_id}")
    print(f"     Model ID: {model['model_id']}")
    print(f"     Cost: ${model['input_cost_per_1m']}/1M tokens")

    # Test 5: Create chat model
    print("\n6. Creating chat model...")
    chat_model_data = {
        "provider_id": provider_id,
        "model_id": "gpt-4-turbo-preview",
        "display_name": "GPT-4 Turbo",
        "description": "OpenAI's most capable model",
        "model_type": "chat",
        "context_window": 128000,
        "max_output_tokens": 4096,
        "supports_vision": True,
        "supports_json_mode": True,
        "supports_tools": True,
        "default_temperature": 0.7,
        "default_top_p": 1.0,
        "default_max_tokens": 4096,
        "input_cost_per_1m": 10.0,
        "output_cost_per_1m": 30.0,
        "is_default_for_chat": True,
        "is_default_for_agents": True,
    }

    response = requests.post(
        f"{BASE_URL}/llm-models",
        headers=headers,
        json=chat_model_data
    )
    response.raise_for_status()
    chat_model = response.json()

    print(f"   ✓ Model created: {chat_model['display_name']}")
    print(f"     Context: {chat_model['context_window']:,} tokens")
    print(f"     Cost: ${chat_model['input_cost_per_1m']}/1M in, ${chat_model['output_cost_per_1m']}/1M out")

    # Test 6: List models
    print("\n7. Listing all models...")
    response = requests.get(f"{BASE_URL}/llm-models", headers=headers)
    response.raise_for_status()
    models = response.json()

    print(f"   ✓ Found {len(models)} model(s)")
    for m in models:
        default_flags = []
        if m.get("is_default_for_chat"):
            default_flags.append("chat")
        if m.get("is_default_for_embeddings"):
            default_flags.append("embeddings")
        if m.get("is_default_for_agents"):
            default_flags.append("agents")

        default_str = f" [default: {', '.join(default_flags)}]" if default_flags else ""
        print(f"     - {m['display_name']} ({m['model_type']}){default_str}")

    # Test 7: Get defaults
    print("\n8. Getting default models...")
    response = requests.get(f"{BASE_URL}/llm-defaults", headers=headers)
    response.raise_for_status()
    defaults = response.json()

    print("   ✓ Default models:")
    if defaults.get("chat"):
        print(f"     - Chat: {defaults['chat']['display_name']}")
    if defaults.get("embeddings"):
        print(f"     - Embeddings: {defaults['embeddings']['display_name']}")
    if defaults.get("agents"):
        print(f"     - Agents: {defaults['agents']['display_name']}")

    # Test 8: Update provider
    print("\n9. Updating provider...")
    update_data = {
        "description": "Official OpenAI API - Updated",
        "is_default": True,
    }

    response = requests.put(
        f"{BASE_URL}/llm-providers/{provider_id}",
        headers=headers,
        json=update_data
    )
    response.raise_for_status()
    updated_provider = response.json()

    print(f"   ✓ Provider updated")
    print(f"     Description: {updated_provider['description']}")
    print(f"     Is Default: {updated_provider['is_default']}")

    # Test 9: Delete models
    print("\n10. Cleaning up - deleting models...")
    for model in models:
        response = requests.delete(
            f"{BASE_URL}/llm-models/{model['id']}",
            headers=headers
        )
        response.raise_for_status()
        print(f"   ✓ Deleted model: {model['display_name']}")

    # Test 10: Delete provider
    print("\n11. Cleaning up - deleting provider...")
    response = requests.delete(
        f"{BASE_URL}/llm-providers/{provider_id}",
        headers=headers
    )
    response.raise_for_status()
    print(f"   ✓ Deleted provider: {provider['display_name']}")

    print("\n" + "=" * 60)
    print("All LLM Configuration Tests Passed!")
    print("=" * 60)

if __name__ == "__main__":
    try:
        test_llm_config()
    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
