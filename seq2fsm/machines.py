"""Finite State Machines

author - Sayan Goswami
email - goswami[dot]sayan47[at]gmail[dot]com
"""

from fsm import FSM
from constants import DEBUG

class MooreMachine(FSM):
    """Moore Machine"""
    def __init__(self, sequence):
        super().__init__(sequence)

        self.num_states = len(self.sequence) + 1

        # Build the fsm
        self._build_fsm()

    def _build_fsm(self):
        # Add nodes
        for state in range(self.num_states):
            node = self.get_state_name(state)
            self.graph.add_node(node)

        # Add edges
        for state in range(self.num_states):
            # Sequence till now
            prev_seq = self.sequence[:state]
            # Positive
            positive = self.sequence[state-1]
            # Negative
            negative = "0" if self.sequence[state-1] == "1" else "1"

            if DEBUG: print(f"prev_seq: {prev_seq}, positive: {positive}, negative: {negative}")

            src = self.get_state_name(state)
            dst = None

            # Positive edge
            dst = self.get_state_matching_pattern(prev_seq + positive)
            if dst is None: dst = self.get_state_name(0)
            self.graph.add_edge(src, dst, label=positive)

            # Negative edge
            dst = self.get_state_matching_pattern(prev_seq + negative)
            if dst is None: dst = self.get_state_name(0)
            self.graph.add_edge(src, dst, label=negative)


class MealyMachine(FSM):
    """Mealy Machine"""
    def __init__(self, sequence):
        super().__init__(sequence)

        self.num_states = len(self.sequence)

        # Build the fsm
        self._build_fsm()

    def _build_fsm(self):
        pass
