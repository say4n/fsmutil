"""Finite State Machines

author - Sayan Goswami
email - goswami[dot]sayan47[at]gmail[dot]com
"""

import matplotlib.pyplot as plt
import networkx as nx
import os, errno
from networkx.drawing.nx_agraph import to_agraph
from string import ascii_uppercase


from constants import FSM_OUTPUT_DIR, FSM_OUTPUT_FORMAT, FSM_OUTPUT_PROGRAM, DEBUG


class FSM:
    def __init__(self, sequence):
        self.sequence = self._validate(sequence)
        self.graph = nx.MultiDiGraph()

        self.num_states = None

        # graph options
        self.graph_options = {
        'font_color': 'white',
        'width': 2,
        'label': f"FSM for {self.sequence}"
        }

        # make output dir
        try:
            os.makedirs(FSM_OUTPUT_DIR)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

    def _validate(self, sequence):
        if not (set(sequence) == set("01") or set(sequence) == set("0") or set(sequence) == set("1")):
            raise Exception(f"Parse error: Invalid binary sequence `{sequence}`")
        else:
            return sequence

    def _build_fsm(self):
        raise NotImplementedError("`build_fsm` not implemented")

    def render_fsm(self):
        pos = nx.nx_agraph.graphviz_layout(self.graph)
        edge_labels = nx.get_edge_attributes(self.graph, 'seq')

        nx.draw(self.graph,
                pos,
                arrows=True,
                with_labels=True,
                **self.graph_options)

        A = to_agraph(self.graph)

        file_name = f"fsm_for_{self.sequence}"
        file_name = ".".join([file_name, FSM_OUTPUT_FORMAT])

        file_path = os.path.join(FSM_OUTPUT_DIR, file_name)

        A.draw(path=file_path, format=FSM_OUTPUT_FORMAT, prog=FSM_OUTPUT_PROGRAM)

    def graph_to_dot(self):
        pass

    def get_state_name(self, num, alphabet=ascii_uppercase):
        """Number to state name
        Base 26 encoding
        """
        if num == 0:
            return alphabet[0]
        arr = []
        base = len(alphabet)
        
        while num:
            num, rem = divmod(num, base)
            arr.append(alphabet[rem])
        arr.reverse()

        return ''.join(arr)

    def get_state_matching_pattern(self, pattern):
        """Given a `pattern`, find a state that expects it"""
        for i in range(len(pattern)):
            pattern_to_match = pattern[i:]

            if DEBUG: print(f"Matching pattern: {pattern_to_match}")
        
            for state in range(self.num_states-1, -1, -1):
                expected_pattern = self.sequence[:state]

                if expected_pattern == pattern_to_match:
                    if DEBUG: print(f"Found match, next state: {self.get_state_name(state)}")
                    return self.get_state_name(state)

        return None