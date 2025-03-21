### Project Setup Documentation

#### Installation of Required Libraries

To set up the project and install the necessary libraries, follow these steps:

1. **Create a virtual environment** (optional but recommended):
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

2. **Install the required libraries**:
   ```sh
   pip install -r requirements.txt
   ```

#### Running Tests

To run the tests, follow these steps:

1. **Run `pytest` with the `-v` option**:
   ```sh
   pytest -v
   ```

#### Configuring Test Parameters

To configure the test parameters, you need to modify the `TestConfig` class in the `config_data.py` file. Here are the parameters you need to set:

- **API Base URL**: The base URL for the API.
- **Points Type**: The type of points, either "network" or "vault".
- **Supported Receiver Types**: A list of supported receiver types.
- **Receiver Addresses**: A dictionary mapping receiver types to their respective addresses.
- **Block Number**: The block number to use for tests.

Example configuration in `config_data.py`:
```python
class TestConfig:
    API_BASE_URL = "https://partner.url/external/api/"  # The base URL for the API.
    POINTS_TYPE= "network"   # The type of points, either "network" or "vault".
    SUPPORTED_RECEIVER_TYPES = ["staker", "operator"]  # A list of supported receiver types. ["staker", "network", "operator"]
    RECEIVER_ADDRESSES = {
        "staker": "0xa5188f25C9F02870E78F7fAF5cf4E3D2ff307eaa",
        "network": "0x123xxx",
        "operator": "0x123xxx",
    }  # A addresses for each supported receiver type
    BLOCK_NUMBER = 21872694  # The block number to use for tests.
```

Make sure to update these parameters according to your specific requirements before running the tests.

## GitHub Action

This repository is also available as a GitHub Action that you can use in your CI/CD workflows.

### Usage

Add the following to your GitHub workflow file:

```yaml
jobs:
  test-external-points-api:
    runs-on: ubuntu-latest
    steps:
      - name: Run External Points API Tests
        uses: symbioticfi/external-points-api-test@v1
        with:
          api_base_url: "https://your-api-url.com/external/api/"
          points_type: "network"
          supported_receiver_types: "staker,operator"
          receiver_addresses: >-
            {
              "staker": "0xa5188f25C9F02870E78F7fAF5cf4E3D2ff307eaa",
              "operator": "0xb6188f25C9F02870E78F7fAF5cf4E3D2ff307bbc"
            }
          block_number: 21872694
```

### Inputs

| Input | Description | Required | Default |
|-------|-------------|----------|---------|
| `api_base_url` | The base URL for the External Points API | Yes | - |
| `points_type` | The type of points to test (network or vault) | No | `network` |
| `supported_receiver_types` | Comma-separated list of supported receiver types | No | `staker,operator` |
| `receiver_addresses` | JSON string of receiver addresses | Yes | - |
| `block_number` | The block number to use for tests | Yes | - |

### Example with GitHub Secrets

```yaml
jobs:
  test-external-points-api:
    runs-on: ubuntu-latest
    steps:
      - name: Run External Points API Tests
        uses: symbioticfi/external-points-api-test@main
        with:
          api_base_url: ${{ secrets.EXTERNAL_API_BASE_URL }}
          points_type: "network"
          supported_receiver_types: "staker,operator"
          receiver_addresses: >-
            {
              "staker": "${{ secrets.STAKER_ADDRESS }}",
              "operator": "${{ secrets.OPERATOR_ADDRESS }}"
            }
          block_number: ${{ secrets.TEST_BLOCK_NUMBER }}
```

### Scheduled Testing

You can also set up scheduled testing to regularly verify your API:

```yaml
name: External Points API Integration Test

on:
  schedule:
    - cron: '0 0 * * *'  # Run daily at midnight UTC
  workflow_dispatch:  # Allow manual triggers

jobs:
  test-external-points-api:
    runs-on: ubuntu-latest
    steps:
      - name: Run External Points API Tests
        uses: symbioticfi/external-points-api-test@main
        with:
          api_base_url: ${{ secrets.EXTERNAL_API_BASE_URL }}
          # ... other inputs
```