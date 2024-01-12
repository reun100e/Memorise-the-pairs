from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
import random
import json
import difflib

class Question:
    def __init__(self, text, correct_answer):
        self.text = text
        self.correct_answer = correct_answer
        self.user_choice = None

class QuizApp(App):
    def build(self):
        self.questions_dict = self.load_questions_from_program()
        self.asked_questions = set()
        self.remaining_questions = len(self.questions_dict) - len(self.asked_questions)
        self.score = 0

        self.question_list = []
        self.current_question_index = 0

        layout = BoxLayout(orientation='vertical')

        self.instruction_label = Label(text="Choose the correct option", font_size=12, bold=True, color=(1, 1, 1, 1))
        layout.add_widget(self.instruction_label)

        self.remaining_label = Label(text="", font_size=10, color=(1, 1, 1, 1))
        layout.add_widget(self.remaining_label)

        self.question_label = Label(text="", font_size=12, halign='left', color=(1, 1, 1, 1))
        layout.add_widget(self.question_label)

        self.choice_buttons = []
        for i in range(4):
            button = Button(text="", size=(30, 30), on_press=lambda instance, i=i: self.check_answer(i))
            layout.add_widget(button)
            self.choice_buttons.append(button)

        self.next_question_button = Button(text="Next Question", size=(150, 30), on_press=self.next_question)
        layout.add_widget(self.next_question_button)

        self.restart_button = Button(text="Restart Quiz", size=(150, 30), on_press=self.restart)
        layout.add_widget(self.restart_button)

        self.add_question_button = Button(text="Add New Question", size=(150, 30), on_press=self.add_new_question)
        layout.add_widget(self.add_question_button)

        scrollable_results_text = ScrollView(size=(300, 200), do_scroll_x=False)
        self.results_label = Label(text="", font_size=10, halign='center', valign='top', color=(1, 1, 1, 1))
        scrollable_results_text.add_widget(self.results_label)
        layout.add_widget(scrollable_results_text)

        # Use Clock to defer accessing ids until the build process is complete
        Clock.schedule_once(lambda dt: self.init_ui(layout), 0)
        Clock.schedule_once(lambda dt: self.randomize_questions(layout), 0)

        return layout

    def init_ui(self, dt=None):
        # Access ids here
        self.question_label.text = f"{self.question_order[self.current_question_index]}\n"

    def set_remaining_label(self):
        self.remaining_label.text = f"Remaining Questions: {self.remaining_questions}"

    def randomize_questions(self, layout):
        self.question_order = list(self.questions_dict.keys())
        random.shuffle(self.question_order)
        self.next_question(layout)

    def load_questions_from_program(self):
        try:
            with open('questions.json', 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def save_questions(self):
        with open('questions.json', 'w') as file:
            json.dump(self.questions_dict, file, indent=2)

    def generate_variations(self, existing_answers, correct_answer):
        variations = [correct_answer]

        for answer in existing_answers:
            if len(answer) == len(correct_answer):
                variations.append(answer)

            common_part = difflib.SequenceMatcher(None, answer, correct_answer).find_longest_match(0, len(answer), 0, len(correct_answer)).size
            if common_part > 2 and answer in existing_answers:
                variations.append(answer)

        return variations

    def quiz_mode(self, layout, dt):
        if self.current_question_index >= len(self.question_order):
            self.show_final_results()
            return

        question_text = self.question_order[self.current_question_index]
        correct_answer = self.questions_dict[question_text]

        existing_answers = list(self.questions_dict.values())
        answer_variations = self.generate_variations(existing_answers, correct_answer)

        choices = [correct_answer] + random.sample(answer_variations, min(3, len(answer_variations)))
        random.shuffle(choices)

        self.question_list.append(Question(question_text, correct_answer))

        layout.children[0].children[2].text = f"{question_text}\n"

        for i, button in enumerate(self.choice_buttons):
            button.text = str(choices[i])


    def check_answer(self, choice_index):
        if self.current_question_index >= len(self.question_list):
            return

        chosen_answer = self.choice_buttons[choice_index].text
        correct_answer = self.question_list[self.current_question_index].correct_answer

        self.question_list[self.current_question_index].user_choice = chosen_answer

        if chosen_answer == correct_answer:
            self.score += 1

        self.asked_questions.add(correct_answer)
        self.current_question_index += 1
        self.next_question()

    def next_question(self, instance=None):
        if not self.remaining_questions:
            self.show_final_results()
            return

        Clock.schedule_once(lambda dt: self.quiz_mode(self.root, dt), 0)

    def show_final_results(self):
        result_message = f"Quiz Complete. Your final score: {self.score}\n\n"
        result_message += "Results for each question:\n"

        for i, question in enumerate(self.question_list):
            result_message += f"\nQuestion {i + 1}:\n"
            result_message += f"  - Correct Answer: {question.correct_answer}\n"
            result_message += f"  - Your Choice: {question.user_choice}\n"

        self.results_label.text = result_message

    def add_new_question(self, instance):
        new_question_layout = BoxLayout(orientation='vertical')

        new_question_layout.add_widget(Label(text="New Question:"))
        new_question_entry = TextInput(width=50)
        new_question_layout.add_widget(new_question_entry)

        new_question_layout.add_widget(Label(text="Correct Answer:"))
        new_answer_entry = TextInput(width=50)
        new_question_layout.add_widget(new_answer_entry)

        new_question_window = BoxLayout(orientation='vertical')
        new_question_window.add_widget(new_question_layout)

        new_question_window.add_widget(Button(text="Add Question", on_press=lambda instance: self.submit_new_question(new_question_entry.text, new_answer_entry.text, new_question_window)))

        self.root.add_widget(new_question_window)  # Use self.root instead of self.root_window

    def submit_new_question(self, new_question, new_answer, new_question_window):
        if new_question and new_answer:
            self.questions_dict[new_question] = new_answer
            self.save_questions()
            new_question_window.parent.remove_widget(new_question_window)
            self.restart()
        else:
            # Handle the case where either the question or answer is not provided
            pass

    def restart(self, instance=None):
        self.asked_questions.clear()
        self.remaining_questions = len(self.questions_dict) - len(self.asked_questions)
        self.score = 0
        self.question_list = []
        self.current_question_index = 0

        self.results_label.text = ""

        Clock.schedule_once(lambda dt: self.randomize_questions(self.root, dt), 0)

if __name__ == "__main__":
    QuizApp().run()
