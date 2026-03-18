from pathlib import Path

import pytest
import yaml

from src.legal_agent import analyze_contract_text


def load_test_data_files():
    """Discover all test data files in the test_data folder."""
    test_data_dir = Path(__file__).parent / "test_data"
    if not test_data_dir.exists():
        pytest.skip(f"Test data directory not found: {test_data_dir}")

    files = list(test_data_dir.glob("*"))
    if not files:
        pytest.skip(f"No test files found in: {test_data_dir}")

    return files


@pytest.mark.parametrize("test_file", load_test_data_files())
@pytest.mark.asyncio
async def test_contract_analysis(test_file):
    """Test contract analysis for each test data file."""
    print(f"\n{'=' * 60}")
    print(f"Processing file: {test_file.name}")

    # Read the test file content
    text_content = test_file.read_text(encoding="utf-8")
    print(f"File size: {len(text_content)} characters")

    # Determine expected result from filename
    expected_is_contract = test_file.name.startswith("True")
    print(f"Expected is_contract: {expected_is_contract}")

    # Run the legal agent analysis
    print("Running legal agent analysis...")
    result = await analyze_contract_text(text_content)

    # Save output to YAML file
    output_file = test_file.with_suffix(".yaml")
    result_dict = result.model_dump() if hasattr(result, "model_dump") else result.dict()

    with open(output_file, "w", encoding="utf-8") as f:
        yaml.dump(result_dict, f, default_flow_style=False, allow_unicode=True)

    print(f"Analysis saved to: {output_file.name}")
    print(f"Actual is_contract: {result_dict.get('is_contract')}")

    # Validate the result
    assert result_dict.get("is_contract") == expected_is_contract, \
        f"Expected is_contract={expected_is_contract}, but got {result_dict.get('is_contract')}"

    print(f"✓ Test PASSED for {test_file.name}")
    print(f"{'=' * 60}")


# # Alternative implementation for pytest < 6.2 or without lazy_fixture
# def pytest_generate_tests(metafunc):
#     """Generate tests dynamically for each test data file."""
#     if "test_file" in metafunc.fixturenames:
#         test_data_dir = Path(metafunc.module.__file__).parent / "test_data"
#         if test_data_dir.exists():
#             test_files = list(test_data_dir.glob("*"))
#             if test_files:
#                 metafunc.parametrize("test_file", test_files)
