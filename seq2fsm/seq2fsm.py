"""Finite State Machine

author - Sayan Goswami
email - goswami[dot]sayan47[at]gmail[dot]com
"""

from machines import MooreMachine, MealyMachine


seq = input("Enter binary input sequnce to detect : ")

myFSM = MealyMachine(seq)
myFSM.render_fsm()

