
from finite_state_machine import FSM
from kpc import KPC
from charlie import Charlie
from keypad import Keypad

keypad = Keypad()
charlie = Charlie()

kpc = KPC(keypad, charlie, "TDT4113-PLAB-2/Group-projects/Project5_Keypad/python")
fsm = FSM(kpc)

fsm.main()
