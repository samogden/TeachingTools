#!env python
import logging
import os
import shutil
import tempfile
import jinja2
import pypdf
import question
import argparse

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)


def parse_args():
  parser = argparse.ArgumentParser()
  parser.add_argument("--num_exams", default=1, type=int)
  parser.add_argument("--questions_file", default="questions.json")
  return parser.parse_args()


def generate_exam(questions_file="questions.json"):
  env = jinja2.Environment(
    loader=jinja2.FileSystemLoader("templates"),
    block_start_string='<BLOCK>',
    block_end_string='</BLOCK>',
    variable_start_string='<VAR>',
    variable_end_string='</VAR>',
    comment_start_string='<COMMENT>',
    comment_end_string='</COMMENT>',
  )
  
  question_set = question.QuestionSet(questions_file).questions
  question_set = sorted(
    question_set,
    key=lambda q: (-q.value, ["memory", "io"].index(q.subject))
  )
  
  def make_questions(*args, **kwargs):
    ## In this function we'll make the questions for the exam
    questions = [q.get_question() for q in question_set]
    
    return '\n\n'.join(questions)
  
  env.globals["generate_exam"] = make_questions
  template = env.get_template('exam_base.j2')
  
  rendered_output = template.render()
  return rendered_output


def main():
  args = parse_args()
  
  if os.path.exists("out"): shutil.rmtree("out")
  os.mkdir("out")
  
  for _ in range(args.num_exams):
    exam_text = generate_exam(questions_file=args.questions_file)
    with tempfile.NamedTemporaryFile('w') as tmp_tex:
    # with open("exam.tex", 'w') as tmp_tex:
      tmp_tex.write(exam_text)
      tmp_tex.flush()
      os.system(f"latexmk -pdf -output-directory={os.path.join(os.getcwd(), 'out')} {tmp_tex.name}")
      os.system(f"latexmk -c {tmp_tex.name} -output-directory={os.path.join(os.getcwd(), 'out')}")
  
  writer = pypdf.PdfWriter()
  for pdf_file in [os.path.join("out", f) for f in os.listdir("out") if f.endswith(".pdf")]:
    writer.append(pdf_file)
  
  writer.write("exam.pdf")
  #shutil.rmtree("out")


if __name__ == "__main__":
  main()
