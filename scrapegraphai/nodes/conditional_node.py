"""
Module for implementing the conditional node
"""
from typing import Optional, List
from .base_node import BaseNode

class ConditionalNode(BaseNode):
    """
    A node that determines the next step in the graph's execution flow based on 
    the presence and content of a specified key in the graph's state. It extends 
    the BaseNode by adding condition-based logic to the execution process.

    This node type is used to implement branching logic within the graph, allowing 
    for dynamic paths based on the data available in the current state.

    It is expected that exactly two edges are created out of this node.
    The first node is chosen for execution if the key exists and has a non-empty value,
    and the second node is chosen if the key does not exist or is empty.

    Attributes:
        key_name (str): The name of the key in the state to check for its presence.

    Args:
        key_name (str): The name of the key to check in the graph's state. This is 
                        used to determine the path the graph's execution should take.
        node_name (str, optional): The unique identifier name for the node. Defaults 
                                   to "ConditionalNode".

    """

    def __init__(self, 
                key_name: str,
                input: str,
                output: List[str],
                node_config: Optional[dict] = None,
                node_name: str = "ConditionalNode"):
        
        """
        Initializes an empty ConditionalNode.
        """

        # Initialize the BaseNode with the appropriate arguments
        super().__init__(node_name, "conditional_node", input, output, 2, node_config)
        
        # Store the key_name as an attribute
        self.key_name = key_name


    def execute(self, state: dict) -> dict:
        """
        Checks if the specified key is present in the state and decides the next node accordingly.

        Args:
            state (dict): The current state of the graph.

        Returns:
            str: The name of the next node to execute based on the presence of the key.
        """

        # Ensure exactly two edges are connected
        connected_nodes = self.get_connected_nodes()
        if len(connected_nodes) != 2:
            raise ValueError("ConditionalNode must have exactly two connected nodes.")

        # Check if the key exists and has a non-empty value
        value = state.get(self.key_name)
        if value:
            # Proceed to the first connected node
            next_node = connected_nodes[0]
        else:
            # Proceed to the second connected node
            next_node = connected_nodes[1]

        # Execute the next node with the current state
        return next_node.execute(state)
