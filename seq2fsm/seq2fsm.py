"""Finite State Machine

author - Sayan Goswami
email - goswami[dot]sayan47[at]gmail[dot]com
"""

from machines import MooreMachine, MealyMachine


seq = input("Enter binary input sequnce to detect : ")

mooreFSM = MooreMachine(seq)
mooreFSM.render_fsm(save_dot=True)

mealyFSM = MealyMachine(seq)
mealyFSM.render_fsm(save_dot=True)
