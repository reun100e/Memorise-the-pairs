# -*- coding: utf-8 -*-
import tkinter as tk
import random
import json
import difflib

class Question:
    def __init__(self, text, correct_answer):
        self.text = text
        self.correct_answer = correct_answer
        self.user_choice = None

class QuizApp:
    def __init__(self, master):
        self.master = master
        self.setup_ui()

        self.questions_dict = self.load_questions_from_program()
        self.asked_questions = set()
        self.remaining_questions = len(self.questions_dict) - len(self.asked_questions)
        self.score = 0

        self.question_list = []
        self.current_question_index = 0

        self.randomize_questions()

    def randomize_questions(self):
        self.question_order = list(self.questions_dict.keys())
        random.shuffle(self.question_order)
        self.next_question()

    def setup_ui(self):
        self.master.title("Memorise-the-pairs Quiz! - by Dr. Aghosh")
        self.set_window_size()
        # self.master.iconbitmap("path_to_icon.ico")
        self.set_color_scheme()

        self.instruction_label = tk.Label(self.master, text="Choose the correct option", font=("Arial", 12, "bold"), bg=self.background_color, fg=self.button_bg_color)
        self.instruction_label.pack(pady=5)

        self.remaining_label = tk.Label(self.master, text="", font=("Arial", 12, "bold"), bg=self.background_color, fg=self.paragraph_color)
        self.remaining_label.pack()

        self.question_label = tk.Label(self.master, text="", font=("Arial", 18, "bold"), wraplength=480, justify='left', bg=self.background_color, fg=self.paragraph_color)
        self.question_label.pack(pady=5, padx=5)

        self.choice_buttons = []
        for i in range(4):
            button = tk.Button(self.master, text="", font=("Calibri", 12, "bold"), width=50, height=2, command=lambda i=i: self.check_answer(i), bg=self.button_bg_color, fg=self.button_text_color)
            button.pack(pady=10)
            self.choice_buttons.append(button)

        self.restart_button = tk.Button(self.master, text="Restart Quiz", font=("Arial", 12), width=15, height=1, command=self.restart, bg=self.paragraph_color, fg=self.button_text_color)
        self.restart_button.pack(pady=15)

        self.add_question_button = tk.Button(self.master, text="Add New Question", font=("Arial", 12), width=15, height=1, command=self.add_new_question, bg=self.paragraph_color, fg=self.button_text_color)
        self.add_question_button.pack(pady=15)

        self.scrollable_results_text = tk.Text(self.master, wrap="word", width=70, height=100, font=("Arial", 10), bd=0, highlightthickness=0,  bg=self.background_color, fg=self.paragraph_color)
        self.scrollable_results_text.tag_configure("center", justify='center')

        self.scrollable_results_text.pack(pady=20, padx=5)

    def set_window_size(self):
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()

        # Calculate the width based on the desired height (9:16 aspect ratio)
        desired_height = int(screen_height * 0.9)
        desired_width = int(desired_height * 9 / 16)

        x_position = (screen_width - desired_width) // 2
        y_position = (screen_height - desired_height) // 2

        self.master.geometry(f"{desired_width}x{desired_height}+{x_position}+{y_position}")

    def set_color_scheme(self):
        self.background_color = "#004643"
        self.paragraph_color = "#abd1c6"
        self.button_bg_color = "#f9bc60"
        self.button_text_color = "#001e1d"

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
            if answer != correct_answer and answer not in variations:
                # Avoid adding duplicate options
                common_part = difflib.SequenceMatcher(None, answer, correct_answer).find_longest_match(0, len(answer), 0, len(correct_answer)).size
                if common_part > 2:
                    variations.append(answer)

        return variations

    def quiz_mode(self):
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

        self.question_label.config(text=f"{question_text}\n")

        for i, button in enumerate(self.choice_buttons):
            if i < len(choices):
                button.config(text=str(choices[i]))
            else:
                button.config(text="")  # Set the text to an empty string for extra buttons

    def check_answer(self, choice_index):
        if self.current_question_index >= len(self.question_list):
            return

        chosen_answer = self.choice_buttons[choice_index].cget("text")
        correct_answer = self.question_list[self.current_question_index].correct_answer

        self.question_list[self.current_question_index].user_choice = chosen_answer

        feedback = f"Question {self.current_question_index + 1}:\n"

        if chosen_answer == correct_answer:
            self.score += 1
            feedback += f"CORRECT!\n"
        else:
            feedback += F"WRONG\n"

        feedback += f"{self.question_order[self.current_question_index]}\n"
        feedback += f"  - Your Answer: {chosen_answer}\n"
        feedback += f"  - Correct Answer: {correct_answer}\n"
        feedback += f"\n"

        current_content = self.scrollable_results_text.get(1.0, tk.END)
        new_content = feedback + current_content
        self.scrollable_results_text.delete(1.0, tk.END)
        self.scrollable_results_text.insert(tk.END, new_content, "center")

        self.asked_questions.add(correct_answer)
        self.current_question_index += 1
        self.remaining_questions -= 1
        self.next_question()

    def next_question(self):
        if not self.remaining_questions:
            self.show_final_results()
            return

        self.quiz_mode()

    def show_final_results(self):
        result_message = f"Quiz Complete. Your final score: {self.score}\n\n"
        result_message += "Results for each question:\n"

        current_content = self.scrollable_results_text.get(1.0, tk.END)
        new_content = result_message + current_content
        self.scrollable_results_text.delete(1.0, tk.END)
        self.scrollable_results_text.insert(tk.END, new_content, "center")

    def add_new_question(self):
        new_question_window = tk.Toplevel(self.master)
        new_question_window.title("Add New Question")

        tk.Label(new_question_window, text="New Question:").pack()
        new_question_entry = tk.Entry(new_question_window, width=50)
        new_question_entry.pack(pady=5)

        tk.Label(new_question_window, text="Correct Answer:").pack()
        new_answer_entry = tk.Entry(new_question_window, width=50)
        new_answer_entry.pack(pady=5)

        tk.Button(new_question_window, text="Add Question", command=lambda: self.submit_new_question(new_question_entry.get(), new_answer_entry.get(), new_question_window)).pack(pady=10)

    def submit_new_question(self, new_question, new_answer, new_question_window):
        if new_question and new_answer:
            self.questions_dict[new_question] = new_answer
            self.save_questions()
            new_question_window.destroy()
            self.restart()
        else:
            tk.messagebox.showerror("Error", "Both question and answer must be provided.")

    def restart(self):
        self.asked_questions.clear()
        self.remaining_questions = len(self.questions_dict) - len(self.asked_questions)
        self.score = 0
        self.question_list = []
        self.current_question_index = 0

        self.scrollable_results_text.delete(1.0, tk.END)

        self.randomize_questions()


def main():
    root = tk.Tk()
    app = QuizApp(root)
    root.configure(bg=app.background_color)
    # root.attributes('-fullscreen', True)  # Start in fullscreen mode
    # root.bind('<Escape>', lambda event: root.attributes('-fullscreen', False))  # Press Escape to exit fullscreen
    root.mainloop()

if __name__ == "__main__":
    main()
