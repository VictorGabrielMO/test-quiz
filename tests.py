import pytest
from model import Question


def test_create_question():
    question = Question(title='q1')
    assert question.id != None

def test_create_multiple_questions():
    question1 = Question(title='q1')
    question2 = Question(title='q2')
    assert question1.id != question2.id

def test_create_question_with_invalid_title():
    with pytest.raises(Exception):
        Question(title='')
    with pytest.raises(Exception):
        Question(title='a'*201)
    with pytest.raises(Exception):
        Question(title='a'*500)

def test_create_question_with_valid_points():
    question = Question(title='q1', points=1)
    assert question.points == 1
    question = Question(title='q1', points=100)
    assert question.points == 100

def test_create_question_with_invalida_points():
    with pytest.raises(Exception):
        Question(title='a', points=-20)
    with pytest.raises(Exception):
        Question(title='a', points= 1000)

def test_create_choice():
    question = Question(title='q1')
    
    question.add_choice('a', False)

    choice = question.choices[0]
    assert len(question.choices) == 1
    assert choice.text == 'a'
    assert not choice.is_correct

def test_creates_choices_and_removes_by_id():
    question = Question(title='q1')
    
    choice_1 = question.add_choice('a', False)
    choice_2 = question.add_choice('b', True)
    
    question.remove_choice_by_id(choice_2.id)
    
    assert len(question.choices) == 1
    assert question.choices[0].id == choice_1.id
    assert question.choices[0].id != choice_2.id
    assert len(set(question.choices)) == len(question.choices)

def test_create_remove_create_choices_by_id():
    question = Question(title='Q1')
    
    question.add_choice('a', False)
    choice_2 = question.add_choice('b', True)
    choice_3 = question.add_choice('c', True)
    question.add_choice('d', False)
    question.add_choice('e', True)
    question.add_choice('f', True)
    
    question.remove_choice_by_id(choice_2.id)
    question.remove_choice_by_id(choice_3.id)
    
    question.add_choice('g', True)
    question.add_choice('h', True)
    
    assert len(question.choices) == 6
    assert len(set(question.choices)) == len(question.choices)

def test_remove_unexisting_choice():
    question = Question(title='Q1')
    
    question.add_choice('a', False)
    choice_2 = question.add_choice('b', True)
    
    question.remove_choice_by_id(choice_2.id)
    with pytest.raises(Exception):
        question.remove_choice_by_id(choice_2.id)

def test_remove_all_choices():
    question = Question(title='Question 1')
    
    question.add_choice('a', False)
    question.add_choice('b', True)
    question.add_choice('c', True)
    question.add_choice('d', False)
    question.add_choice('e', True)
    question.add_choice('f', True)
    
    question.remove_all_choices()
    
    assert len(question.choices) == 0

def test_correct_selected_choices_with_multiple_right_choices():
    question = Question(title='Question-1', max_selections=3)
    
    choice_1_right = question.add_choice('a', True)
    question.add_choice('b', True)
    choice_2_right = question.add_choice('c', True)
    choice_3_wrong = question.add_choice('d', False)
    question.add_choice('e', False)
    question.add_choice('f', True)
    
    choices_input = [choice_1_right.id, choice_2_right.id, choice_3_wrong.id]
    selected_choices = question.correct_selected_choices(choices_input)
    
    assert len(selected_choices) == 2
    assert choice_1_right.id in selected_choices
    assert choice_2_right.id in selected_choices
    assert len(set(selected_choices)) == len(selected_choices)

def test_correct_selected_choices_with_only_false_choices():
    question = Question(title='Question_2', max_selections=3)
    
    q1 = question.add_choice('a', False)
    q2 = question.add_choice('b', False)
    question.add_choice('c', False)
    q4 = question.add_choice('d', False)
    question.add_choice('e', False)
    question.add_choice('f', False)
    
    
    choices_input = [q1, q2, q4]
    selected_choices = question.correct_selected_choices(choices_input)
    
    assert len(selected_choices) == 0
    
def test_correct_selected_choices_with_input_bigger_than_max():
    question = Question(title='Question_2')
    
    q1 = question.add_choice('a', False)
    q2 = question.add_choice('b', False)
    q3 = question.add_choice('c', True)
    q4 = question.add_choice('d', False)
    question.add_choice('e', False)
    question.add_choice('f', False)
    
    choices_input = [q1, q2, q3, q4]
    with pytest.raises(Exception):
        question.correct_selected_choices(choices_input)

def test_set_correct_choices_with_single_correct_choice():
    question = Question(title='Question_2', max_selections=1)
    
    q1 = question.add_choice('a', False)
    q2 = question.add_choice('b', False)
    q3 = question.add_choice('c', False)
    q4 = question.add_choice('d', False)
    
    question.set_correct_choices([q3.id])
    
    assert len(set(question.choices)) == len(question.choices)
    
    right_choices = 0
    for choice in question.choices:
        if choice.is_correct:
            right_choices += 1
    assert right_choices == 1
    
def test_initialized_and_set_correct_choices():
    question = Question(title='Quest-2')
    
    q1 = question.add_choice('a', False)
    q2 = question.add_choice('b', True)
    q3 = question.add_choice('c', False)
    q4 = question.add_choice('d', False)
    
    question.set_correct_choices([q3.id])
    
    assert len(set(question.choices)) == len(question.choices)
    
    right_choices = 0
    for choice in question.choices:
        if choice.is_correct:
            right_choices += 1
    assert right_choices == 2