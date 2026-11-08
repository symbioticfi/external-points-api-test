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

The pagination check compares complete records, including `receiver_type` and,
for network points, `network_address`. Records with equal points, receiver
addresses, and vault addresses can still be distinct.

To run the pagination regression tests offline, without contacting the configured
partner API:

```sh
python -m pytest -q tests/test_pagination_identity.py
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