#!env python
from typing import List, Tuple, Dict, Type, Any

from src.question import Question, Answer

import random
import math

import logging

logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


class BitsAndBytes(Question):
  
  MIN_BITS = 3
  MAX_BITS = 49
  
  def __init__(self, name: str = None, value: float = 1.0, kind: Question.TOPIC = Question.TOPIC.MISC, *args, **kwargs):
    if name is None:
      name = self.__class__.__name__
    super().__init__(name, value, kind, *args, **kwargs)
    
    self.from_binary = None
    self.num_bits = None
    self.num_bytes = None
    self.answers = []
    
  def instantiate(self):
    self.from_binary = 0 == random.randint(0,1)
    self.num_bits = random.randint(self.MIN_BITS, self.MAX_BITS)
    self.num_bytes = int(math.pow(2, self.num_bits))
    
    if self.from_binary:
      self.answers = [Answer("num_bytes", self.num_bytes, Answer.AnswerKind.BLANK)]
    else:
      self.answers = [Answer("num_bits", self.num_bits, Answer.AnswerKind.BLANK)]
  
  def get_body_lines(self, *args, **kwargs) -> List[str]:
    lines = []
    
    lines = [
      f"Given that we have {self.num_bits if self.from_binary else self.num_bytes} {'bits' if self.from_binary else 'bytes'}, "
      f"how many {'bits' if not self.from_binary else 'bytes'} "
      f"{'do we need to address our memory' if not self.from_binary else 'of memory can be addressed'}?"
    ]
    
    lines.extend([
      "",
      f"{'Address space size' if self.from_binary else 'Number of bits in address'}: [{self.answers[0].key}] {'bits' if not self.from_binary else 'bytes'}"
    ])
    
    return lines
    
  def get_explanation_lines(self, *args, **kwargs) -> List[str]:
    explanation_lines = [
      "Remember that for these problems we use one of these two equations (which are equivalent)",
      "",
      r"- $log_{2}(\text{#bytes}) = \text{#bits}$",
      r"- $2^{(\text{#bits})} = \text{#bytes}$",
      "",
      "Therefore, we calculate:",
    ]
    
    if self.from_binary:
      explanation_lines.extend([
        f"\\( 2 ^ {{{self.num_bits}bits}} = \\textbf{{{self.num_bytes}}}bytes \\)"
      ])
    else:
      explanation_lines.extend([
        f"$log_{2}({self.num_bytes} \\text{{bytes}}) = \\textbf{{{self.num_bits}}}\\text{{bits}}$"
      ])
    
    return explanation_lines

  def get_answers(self, *args, **kwargs) -> Tuple[Answer.AnswerKind, List[Dict[str,Any]]]:
    return Answer.AnswerKind.BLANK, [a.get_for_canvas() for a in self.answers]
