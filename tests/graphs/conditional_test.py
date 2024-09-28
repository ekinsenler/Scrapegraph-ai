"""
Module for testing the ConditionalNode
"""
import pytest
from scrapegraphai.nodes.conditional_node import ConditionalNode
from scrapegraphai.nodes.base_node import BaseNode

@pytest.fixture
def graph_config():
    """
    Configuration for the graph
    """
    return {}

class MockNode(BaseNode):
    def __init__(self, result: str):
        super().__init__()
        self.result = result

    def execute(self, state: dict):
        """
        Simulates the execution of a node.
        
        Args:
            state (dict): The current state of the graph.
        
        Returns:
            dict: A result dict indicating which node was executed.
        """
        return {"result": self.result}

def test_conditional_node(graph_config: dict):
    """
    Test the ConditionalNode
    """
    # Create two mock nodes
    true_node = MockNode(result="True Node Executed")
    false_node = MockNode(result="False Node Executed")

    # Create the ConditionalNode that checks for "test_key"
    conditional_node = ConditionalNode(key_name="test_key")

    # Manually connect the two mock nodes to the conditional node
    conditional_node.add_edge(true_node)  # First edge is the "true" node
    conditional_node.add_edge(false_node)  # Second edge is the "false" node

    # Test 1: Key exists with a non-empty value
    state_with_key = {"test_key": "some_value"}
    result_with_key = conditional_node.execute(state_with_key)
    assert result_with_key == {"result": "True Node Executed"}, "Failed when key exists with a value"

    # Test 2: Key does not exist
    state_without_key = {}
    result_without_key = conditional_node.execute(state_without_key)
    assert result_without_key == {"result": "False Node Executed"}, "Failed when key is missing"

    # Test 3: Key exists but is empty
    state_empty_key = {"test_key": ""}
    result_empty_key = conditional_node.execute(state_empty_key)
    assert result_empty_key == {"result": "False Node Executed"}, "Failed when key is empty"

