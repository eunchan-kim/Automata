#-*- coding: utf-8 -*-
import sys
import Mealy_machine
reload(sys)
sys.setdefaultencoding('utf-8')

# chosung_Hangul_Automata.py
# Eunchan Kim (pavian48@gmail.com)

def hangul_combination(chosung, jungsung, jongsung):
  # ㄱ + -1 + -1 = ㄱ
  # ㄱ + ㅗ + o = 공
  # ㄱ + ㅗ + -1 = 고
  chosung_list = u"ㄱ,ㄲ,ㄴ,ㄷ,ㄸ,ㄹ,ㅁ,ㅂ,ㅃ,ㅅ,ㅆ,ㅇ,ㅈ,ㅉ,ㅊ,ㅋ,ㅌ,ㅍ,ㅎ".split(",")
  jungsung_list = u"ㅏ,ㅐ,ㅑ,ㅒ,ㅓ,ㅔ,ㅕ,ㅖ,ㅗ,ㅘ,ㅙ,ㅚ,ㅛ,ㅜ,ㅝ,ㅞ,ㅟ,ㅠ,ㅡ,ㅢ,ㅣ".split(",")
  jongsung_list = u"X,ㄱ,ㄲ,ㄳ,ㄴ,ㄵ,ㄶ,ㄷ,ㄹ,ㄺ,ㄻ,ㄼ,ㄽ,ㄾ,ㄿ,ㅀ,ㅁ,ㅂ,ㅄ,ㅅ,ㅆ,ㅇ,ㅈ,ㅊ,ㅋ,ㅌ,ㅍ,ㅎ".split(",")

  unicode_value = 0xac00
  if chosung != -1:
    unicode_value += 588 * chosung_list.index(chosung)
    if jungsung == -1:
      return chosung
    unicode_value += 28 * jungsung_list.index(jungsung)
    if jongsung == -1:
      return unichr(unicode_value)
    unicode_value += jongsung_list.index(jongsung)
    return unichr(unicode_value)

  elif jungsung != -1:
    return jungsung


class Hangul_Automata(Mealy_machine.Mealy_machine):
  def __init__(self, states, inputs, transitions, actions, initial_state):
    Mealy_machine.Mealy_machine.__init__(self, states, inputs, transitions, actions, initial_state)
    self.chosung = -1
    self.chosung2 = -1
    self.jungsung = -1
    self.jongsung = -1
    self.fixed_output = u""

  def init_chosung_jungsung_jongsung(self):
    self.chosung = -1
    self.chosung2 = -1
    self.jungsung = -1
    self.jongsung = -1

  def simulate(self, input):
    if input == "-":
      #print "backspace"
      if self.chosung2 != -1:
        self.fixed_output += hangul_combination(self.chosung, self.jungsung, self.jongsung)
        print self.fixed_output
        self.init_chosung_jungsung_jongsung()
        self.curr_state = self.initial_state
        return

      elif (self.chosung == -1 and self.chosung2 == -1 and self.jungsung == -1 and self.jongsung == -1):
        self.fixed_output = self.fixed_output[:-1]
        self.curr_state = self.initial_state
      else:
        self.init_chosung_jungsung_jongsung()
        self.curr_state = self.initial_state
      print self.fixed_output
      return

    if input in self.inputs:
      try:
        next_state = self.transitions[(self.curr_state, input)]
        todo = self.actions[(self.curr_state, input)]

        """
        print u"next state is " + next_state
        print "action is "
        print todo
        """

        todo(self, input)
        self.curr_state = next_state

      except KeyError:
        # go to deadstate, start again
        """
        print "KeyError, No match found"
        print self.curr_state
        print self.chosung
        print self.chosung2
        print self.jungsung
        print self.jongsung
        """

        if input in jaeum:
          # think it as first input of first automata
          self.fixed_output += hangul_combination(self.chosung, self.jungsung, self.jongsung)
          self.init_chosung_jungsung_jongsung()
          self.curr_state = self.initial_state
          self.simulate(input)
        else:
          if not(self.chosung == -1 and self.chosung2 == -1 and self.jungsung == -1 and self.jongsung == -1):
            # ex) 하 + ㅏ
            self.fixed_output += hangul_combination(self.chosung, self.jungsung, self.jongsung)
          self.fixed_output += input
          print self.fixed_output

          self.init_chosung_jungsung_jongsung()
          self.curr_state = self.initial_state

    else:
      print u"올바르지 않은 입력입니다"


def jungsung_combination(jungsung1, jungsung2):
  if jungsung1 == u"ㅗ":
    if jungsung2 == u"ㅏ":
      return u"ㅘ"
    elif jungsung2 == u"ㅣ":
      return u"ㅚ"
    else:
      print "jungsung2 not match"
      return -1

  elif jungsung1 == u"ㅜ":
    if jungsung2 == u"ㅓ":
      return u"ㅝ"
    elif jungsung2 == u"ㅣ":
      return u"ㅟ"
    elif jungsung2 == u"ㅔ":
      return u"ㅞ"
    else:
      print "jungsung2 not match"
      return -1
  elif jungsung1 == u"ㅡ" and jungsung2 == u"ㅣ":
    return u"ㅢ"
  else:  
    print "jungsung combination error"
    return -1 

def jongsung_combination(jongsung1, jongsung2):
  # ㄳ ㄵ ㄶ ㄺ ㄻ ㄼ ㄽ ㄾ ㄿ ㅀ ㅄ
  # ex) ㄱ + ㅅ = ㄳ
  if jongsung1 == u"ㄱ" and jongsung2 == u"ㅅ":
    return u"ㄳ"
  if jongsung1 == u"ㄴ" and jongsung2 == u"ㅈ":
    return u"ㄵ"
  if jongsung1 == u"ㄴ" and jongsung2 == u"ㅎ":
    return u"ㄶ"
  if jongsung1 == u"ㄹ" and jongsung2 == u"ㄱ":
    return u"ㄺ"
  if jongsung1 == u"ㄹ" and jongsung2 == u"ㅁ":
    return u"ㄻ"
  if jongsung1 == u"ㄹ" and jongsung2 == u"ㅂ":
    return u"ㄼ"
  if jongsung1 == u"ㄹ" and jongsung2 == u"ㅅ":
    return u"ㄽ"
  if jongsung1 == u"ㄹ" and jongsung2 == u"ㅌ":
    return u"ㄾ"
  if jongsung1 == u"ㄹ" and jongsung2 == u"ㅍ":
    return u"ㄿ"
  if jongsung1 == u"ㄹ" and jongsung2 == u"ㅎ":
    return u"ㅀ"
  if jongsung1 == u"ㅂ" and jongsung2 == u"ㅅ":
    return u"ㅄ"  
  return -1

def jongsung_split(jongsung):
  # ㄳ ㄵ ㄶ ㄺ ㄻ ㄼ ㄽ ㄾ ㄿ ㅀ ㅄ
  # ㄳ = ㄱ + ㅅ
  if jongsung == u"ㄳ":
    return [u"ㄱ", u"ㅅ"]
  if jongsung == u"ㄵ":
    return [u"ㄴ", u"ㅈ"]
  if jongsung == u"ㄶ":
    return [u"ㄴ", u"ㅎ"]
  if jongsung == u"ㄺ":
    return [u"ㄹ", u"ㄱ"]
  if jongsung == u"ㄻ":
    return [u"ㄹ", u"ㅁ"]
  if jongsung == u"ㄼ":
    return [u"ㄹ", u"ㅂ"]
  if jongsung == u"ㄽ":
    return [u"ㄹ", u"ㅅ"]
  if jongsung == u"ㄾ":
    return [u"ㄹ", u"ㅌ"]
  if jongsung == u"ㄿ":
    return [u"ㄹ", u"ㅍ"]
  if jongsung == u"ㅀ":
    return [u"ㄹ", u"ㅎ"]
  if jongsung == u"ㅄ":
    return [u"ㅂ", u"ㅅ"]
  return -1

def f1_1(automata, input):
  # ㅎ = ㅎ
  automata.chosung = input
  print automata.fixed_output + automata.chosung

def f2_1(automata, input):
  # ㅎ + ㅡ = 흐
  automata.jungsung = input
  print automata.fixed_output + hangul_combination(automata.chosung, automata.jungsung, -1)

def f2_2(automata, input):
  # 흐 + ㅣ = 희
  automata.jungsung = jungsung_combination(automata.jungsung, input)
  print automata.fixed_output + hangul_combination(automata.chosung, automata.jungsung, -1)

def f3_1(automata, input):
  # 흐 + ㄱ = 흐ㄱ
  first_print = hangul_combination(automata.chosung, automata.jungsung, -1)
  automata.chosung2 = input
  print automata.fixed_output + first_print + automata.chosung2

def f3_2(automata, input):
  # 흐ㄹ + ㄱ = 흘ㄱ
  automata.jongsung = automata.chosung2
  automata.chosung2 = input
  first_print = hangul_combination(automata.chosung, automata.jungsung, automata.jongsung)
  second_print = automata.chosung2
  print automata.fixed_output + first_print + second_print

def f3_3(automata, input):
  # 가 + ㄸ = 가ㄸ
  first_print = hangul_combination(automata.chosung, automata.jungsung, -1)
  automata.chosung = input
  print automata.fixed_output + first_print + automata.chosung

def f4_1(automata, input):
  # 흐ㄴ + ㅣ = 흐니
  automata.fixed_output += hangul_combination(automata.chosung, automata.jungsung, -1)
  automata.chosung = automata.chosung2
  automata.chosung2 = -1
  automata.jungsung = input
  print automata.fixed_output + hangul_combination(automata.chosung, automata.jungsung, -1)

def f4_2(automata, input):
  # 가ㅂ + ㅂ = 갑ㅂ
  automata.jongsung = automata.chosung2
  automata.fixed_output += hangul_combination(automata.chosung, automata.jungsung, automata.jongsung)
  automata.init_chosung_jungsung_jongsung()

  automata.chosung = input
  print automata.fixed_output + automata.chosung

def f4_3(automata, input):
  # 흘ㄱ + ㅣ = 흘기
  automata.fixed_output += hangul_combination(automata.chosung, automata.jungsung, automata.jongsung)
  automata.chosung = automata.chosung2
  automata.jungsung = input
  automata.jongsung = -1
  automata.chosung2 = -1

  print automata.fixed_output + hangul_combination(automata.chosung, automata.jungsung, -1)


def f4_4(automata, input):
  # 달ㄱ + ㄲ = 닭ㄲ
  automata.jongsung = jongsung_combination(automata.jongsung, automata.chosung2)
  automata.fixed_output += hangul_combination(automata.chosung, automata.jungsung, automata.jongsung)
  automata.init_chosung_jungsung_jongsung()
  automata.chosung = input
  print automata.fixed_output + automata.chosung

  
jaeum = u"ㄱㄴㄷㄹㅁㅂㅅㅇㅈㅊㅋㅌㅍㅎㄲㄸㅃㅆㅉ"
moeum = u"ㅏㅑㅐㅒㅓㅕㅔㅖㅗㅛㅜㅠㅡㅣ"
actions = {}
transitions = {}

for char in jaeum:
  actions[(u"초", char)] = f1_1
  actions[(u"ㅗ", char)] = f3_1
  actions[(u"ㅜ", char)] = f3_1
  actions[(u"중1", char)] = f3_1
  actions[(u"중2", char)] = f3_1
  actions[(u"ㄱ", char)] = f4_2
  actions[(u"ㄴ", char)] = f4_2
  actions[(u"ㄹ", char)] = f4_2
  actions[(u"받1", char)] = f4_4
  actions[(u"받2", char)] = f4_2

actions[(u"ㅗ", u"ㄸ")] = f3_3; actions[(u"ㅗ", u"ㅃ")] = f3_3; actions[(u"ㅗ", u"ㅉ")] = f3_3
actions[(u"ㅜ", u"ㄸ")] = f3_3; actions[(u"ㅜ", u"ㅃ")] = f3_3; actions[(u"ㅜ", u"ㅉ")] = f3_3
actions[(u"중1", u"ㄸ")] = f3_3; actions[(u"중1", u"ㅃ")] = f3_3; actions[(u"중1", u"ㅉ")] = f3_3
actions[(u"중2", u"ㄸ")] = f3_3; actions[(u"중2", u"ㅃ")] = f3_3; actions[(u"중2", u"ㅉ")] = f3_3
actions[(u"ㄱ", u"ㅅ")] = f3_2;
actions[(u"ㄴ", u"ㅈ")] = f3_2; actions[(u"ㄴ", u"ㅎ")] = f3_2
actions[(u"ㄹ", u"ㄱ")] = f3_2; actions[(u"ㄹ", u"ㅁ")] = f3_2; actions[(u"ㄹ", u"ㅂ")] = f3_2; actions[(u"ㄹ", u"ㅅ")] = f3_2;
actions[(u"ㄹ", u"ㅌ")] = f3_2; actions[(u"ㄹ", u"ㅍ")] = f3_2; actions[(u"ㄹ", u"ㅎ")] = f3_2


for char in moeum:
  actions[(u"중", char)] = f2_1
  actions[(u"ㄱ", char)] = f4_1
  actions[(u"ㄴ", char)] = f4_1
  actions[(u"ㄹ", char)] = f4_1
  actions[(u"받1", char)] = f4_3
  actions[(u"받2", char)] = f4_1

actions[(u"ㅗ", u"ㅏ")] = f2_2; actions[(u"ㅗ", u"ㅣ")] = f2_2
actions[(u"ㅜ", u"ㅓ")] = f2_2; actions[(u"ㅜ", u"ㅔ")] = f2_2; actions[(u"ㅜ", u"ㅣ")] = f2_2
actions[(u"중1", u"ㅣ")] = f2_2

for char in jaeum:
  transitions[(u"초", char)] = u"중"
  transitions[(u"ㅗ", char)] = u"받2"
  transitions[(u"ㅜ", char)] = u"받2"
  transitions[(u"중1", char)] = u"받2"
  transitions[(u"중2", char)] = u"받2"
  transitions[(u"ㄱ", char)] = u"중"
  transitions[(u"ㄴ", char)] = u"중"
  transitions[(u"ㄹ", char)] = u"중"
  transitions[(u"받1", char)] = u"중"
  transitions[(u"받2", char)] = u"중"

transitions[(u"ㅗ", u"ㄱ")] = u"ㄱ"; transitions[(u"ㅗ", u"ㄴ")] = u"ㄴ"; transitions[(u"ㅗ", u"ㄹ")] = u"ㄹ"; transitions[(u"ㅗ", u"ㅂ")] = u"ㄱ"
transitions[(u"ㅗ", u"ㄸ")] = u"중"; transitions[(u"ㅗ", u"ㅃ")] = u"중"; transitions[(u"ㅗ", u"ㅉ")] = u"중"
transitions[(u"ㅜ", u"ㄱ")] = u"ㄱ"; transitions[(u"ㅜ", u"ㄴ")] = u"ㄴ"; transitions[(u"ㅜ", u"ㄹ")] = u"ㄹ"; transitions[(u"ㅜ", u"ㅂ")] = u"ㄱ"
transitions[(u"ㅜ", u"ㄸ")] = u"중"; transitions[(u"ㅜ", u"ㅃ")] = u"중"; transitions[(u"ㅜ", u"ㅉ")] = u"중"
transitions[(u"중1", u"ㄱ")] = u"ㄱ"; transitions[(u"중1", u"ㄴ")] = u"ㄴ"; transitions[(u"중1", u"ㄹ")] = u"ㄹ"; transitions[(u"중1", u"ㅂ")] = u"ㄱ"
transitions[(u"중1", u"ㄸ")] = u"중"; transitions[(u"중1", u"ㅃ")] = u"중"; transitions[(u"중1", u"ㅉ")] = u"중"
transitions[(u"중2", u"ㄱ")] = u"ㄱ"; transitions[(u"중2", u"ㄴ")] = u"ㄴ"; transitions[(u"중2", u"ㄹ")] = u"ㄹ"; transitions[(u"중2", u"ㅂ")] = u"ㄱ"
transitions[(u"중2", u"ㄸ")] = u"중"; transitions[(u"중2", u"ㅃ")] = u"중"; transitions[(u"중2", u"ㅉ")] = u"중"
transitions[(u"ㄱ", u"ㅅ")] = u"받1"
transitions[(u"ㄴ", u"ㅈ")] = u"받1"; transitions[(u"ㄴ", u"ㅎ")] = u"받1"
transitions[(u"ㄹ", u"ㄱ")] = u"받1"; transitions[(u"ㄹ", u"ㅁ")] = u"받1"; transitions[(u"ㄹ", u"ㅂ")] = u"받1"; transitions[(u"ㄹ", u"ㅅ")] = u"받1"
transitions[(u"ㄹ", u"ㅌ")] = u"받1"; transitions[(u"ㄹ", u"ㅍ")] = u"받1"; transitions[(u"ㄹ", u"ㅎ")] = u"받1";


for char in [u"중", u"ㄱ", u"ㄴ", u"ㄹ", u"받1", u"받2"]:
  transitions[(char, u"ㅏ")] = u"중1"
  transitions[(char, u"ㅑ")] = u"중1"
  transitions[(char, u"ㅐ")] = u"중2"
  transitions[(char, u"ㅒ")] = u"중2"
  transitions[(char, u"ㅓ")] = u"중1"
  transitions[(char, u"ㅕ")] = u"중1"
  transitions[(char, u"ㅔ")] = u"중2"
  transitions[(char, u"ㅖ")] = u"중2"
  transitions[(char, u"ㅗ")] = u"ㅗ"
  transitions[(char, u"ㅛ")] = u"중2"
  transitions[(char, u"ㅜ")] = u"ㅜ"
  transitions[(char, u"ㅠ")] = u"중2"
  transitions[(char, u"ㅡ")] = u"중1"
  transitions[(char, u"ㅣ")] = u"중2"

transitions[(u"ㅗ", u"ㅏ")] = u"중1"
transitions[(u"ㅜ", u"ㅓ")] = u"중1"
transitions[(u"ㅜ", u"ㅔ")] = u"중2"
transitions[(u"ㅗ", u"ㅣ")] = u"중2"; transitions[(u"ㅜ", u"ㅣ")] = u"중2"; transitions[(u"중1", u"ㅣ")] = u"중2" #-> ㅏ + ㅣ  = ㅐ 인정

states = [u"초", u"중", u"ㅗ", u"ㅜ", u"중1", u"중2", u"ㄱ", u"ㄴ", u"ㄹ", u"받1", u"받2"]
inputs = u"ㅂ,ㅃ,ㅈ,ㅉ,ㄷ,ㄸ,ㄱ,ㄲ,ㅅ,ㅆ,ㅛ,ㅕ,ㅑ,ㅐ,ㅒ,ㅔ,ㅖ,ㅁ,ㄴ,ㅇ,ㄹ,ㅎ,ㅗ,ㅓ,ㅏ,ㅣ,ㅋ,ㅌ,ㅊ,ㅍ,ㅠ,ㅜ,ㅡ".split(",")


HA = Hangul_Automata(states, inputs, transitions, actions, u"초")

def main(hangul_automata):
  print u"사용법: 자음 혹은 모음을 입력한 후 엔터를 누르세요."
  print u"글자를 지우고 싶을 때는 '-'를 누르세요."
  print u"프로그램을 종료하고 싶을 때는 'q'를 입력해주세요."
  while(True):
    input = unicode(raw_input(u"입력값:"))
    if input == unicode("q"):
      break
    hangul_automata.simulate(input)
  print "종료"

main(HA)
