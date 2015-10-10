#-*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class Mealy_machine:
  def __init__(self, states, inputs, transitions, actions, initial_state):
    self.states = states
    self.inputs = inputs
    self.transitions = transitions
    self.actions = actions
    self.initial_state = initial_state
    self.curr_state = self.initial_state

  def simulate(self, input):
    if input in self.inputs:
      next_state = self.transitions[(self.curr_state, input)]
      self.actions[(self.curr_state, input)](self, input)

