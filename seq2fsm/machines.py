"""Finite State Machines

author - Sayan Goswami
email - goswami[dot]sayan47[at]gmail[dot]com
"""

from fsm import FSM
from constants import DEBUG


class MooreMachine(FSM):
    """Moore Machine"""
    def __init__(self, sequence):
        super().__init__(sequence, f"Moore Machine to detect `{sequence}`")

        self.num_states = len(self.sequence) + 1
        self.file_name = f"moore_fsm_for_{self.sequence}"

        # Build the fsm
        self._build_fsm()

        # Graph built
        self.built = True

    def _get_node_output(self, state):
        return "0" if state != self.num_states - 1 else "1"

    def _get_state_label(self, state):
        name = self.get_state_name(state)
        output = self._get_node_output(state)

        return f"{name}/{output}"

    def _build_fsm(self):
        # Add nodes
        for state in range(self.num_states):
            self.graph.add_node(self._get_state_label(state))

        # Add edges
        for state in range(self.num_states):
            # Sequence till now
            prev_seq = self.sequence[:state]
            # Positive
            positive = self.sequence[state-1]
            # Negative
            negative = "0" if positive == "1" else "1"

            if DEBUG: print(f"prev_seq: {prev_seq}, positive: {positive}, negative: {negative}")

            src = state
            src_node = self._get_state_label(src)
            dst = None
            dst_node = None

            # Positive edge
            dst = self.get_state_matching_pattern(prev_seq + positive)
            dst_node = self._get_state_label(dst)
            self.graph.add_edge(src_node, dst_node, label=positive)

            # Negative edge
            dst = self.get_state_matching_pattern(prev_seq + negative)
            dst_node = self._get_state_label(dst)
            self.graph.add_edge(src_node, dst_node, label=negative)


class MealyMachine(FSM):
    """Mealy Machine"""
    def __init__(self, sequence):
        super().__init__(sequence, f"Mealy Machine to detect `{sequence}`")

        self.num_states = len(self.sequence)
        self.file_name = f"mealy_fsm_for_{self.sequence}"

        # Build the fsm
        self._build_fsm()

        # Graph built
        self.built = True

    def _get_edge_output(self, state, positive):
        if state == self.num_states-1 and positive:
            return True
        else:
            return False

    def _get_edge_label(self, label, state, positive):
        output = int(self._get_edge_output(state, positive))

        return f"{label}/{output}"

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
            positive = self.sequence[state]
            # Negative
            negative = "0" if positive == "1" else "1"

            if DEBUG: print(f"prev_seq: {prev_seq}, positive: {positive}, negative: {negative}")

            src = self.get_state_name(state)
            dst = None

            # Positive edge
            dst = self.get_state_matching_pattern(prev_seq + positive)
            dst_node = self.get_state_name(dst)
            self.graph.add_edge(src, dst_node, label=self._get_edge_label(positive, state, positive=True))

            # Negative edge
            dst = self.get_state_matching_pattern(prev_seq + negative)
            dst_node = self.get_state_name(dst)
            self.graph.add_edge(src, dst_node, label=self._get_edge_label(negative, state, positive=False))


