"""
Minimal test script to diagnose CrewAI integration test issues.
"""

from pathlib import Path
import sys


# Add project root to Python path
project_root = str(Path(__file__).parent.parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)


def test_import_codeflow_crew():
    """Test if we can import CodeFlowCrew."""
    from codeflow_engine.agents.crew import CodeFlowCrew

    assert CodeFlowCrew is not None


def test_instantiate_codeflow_crew():
    """Test if we can instantiate CodeFlowCrew."""
    from codeflow_engine.agents.crew import CodeFlowCrew

    crew = CodeFlowCrew(llm_model="gpt-4")
    assert crew is not None


if __name__ == "__main__":
    import_result = test_import_codeflow_crew()
    instantiate_result = False
    if import_result:
        instantiate_result = test_instantiate_codeflow_crew()

    if import_result and instantiate_result:
        sys.exit(0)
    else:
        sys.exit(1)
