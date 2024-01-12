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
        self.master.title("Quiz App")
        self.set_window_size()
        self.set_color_scheme()

        self.instruction_label = tk.Label(self.master, text="Choose the correct option", font=("Arial", 12, "bold"), bg=self.background_color, fg=self.headline_color)
        self.instruction_label.pack(pady=5)

        self.remaining_label = tk.Label(self.master, text="", font=("Arial", 10), bg=self.background_color, fg=self.paragraph_color)
        self.remaining_label.pack()

        self.question_label = tk.Label(self.master, text="", font=("Arial", 12), wraplength=380, justify='left', bg=self.background_color, fg=self.paragraph_color)
        self.question_label.pack(pady=5, padx=5)

        self.choice_buttons = []
        for i in range(4):
            button = tk.Button(self.master, text="", width=30, height=1, command=lambda i=i: self.check_answer(i), bg=self.button_bg_color, fg=self.button_text_color)
            button.pack(pady=3)
            self.choice_buttons.append(button)

        self.next_question_button = tk.Button(self.master, text="Next Question", width=15, height=1, command=self.next_question, bg=self.button_bg_color, fg=self.button_text_color)
        self.next_question_button.pack(side="left", padx=5)

        self.restart_button = tk.Button(self.master, text="Restart Quiz", width=15, height=1, command=self.restart, bg=self.button_bg_color, fg=self.button_text_color)
        self.restart_button.pack(side="left", padx=5)

        self.add_question_button = tk.Button(self.master, text="Add New Question", width=15, height=1, command=self.add_new_question, bg=self.button_bg_color, fg=self.button_text_color)
        self.add_question_button.pack(side="left", padx=5)

        self.scrollable_results_text = tk.Text(self.master, wrap="word", width=50, height=10, font=("Arial", 10), bd=0, highlightthickness=0,  bg=self.background_color, fg=self.paragraph_color)
        self.scrollable_results_text.tag_configure("center", justify='center')

        self.scrollable_results_text.pack(side="left", pady=20, padx=5)

        # scrollbar = tk.Scrollbar(self.master, command=self.scrollable_results_text.yview)
        # scrollbar.pack(side="right", fill="y")
        # self.scrollable_results_text.config(yscrollcommand=scrollbar.set)

        window_width = self.master.winfo_reqwidth()
        window_height = self.master.winfo_reqheight()
        text_width = self.scrollable_results_text.winfo_reqwidth()
        text_height = self.scrollable_results_text.winfo_reqheight()
        x_position = (window_width - text_width) + 170
        y_position = window_height - text_height + 280

        self.scrollable_results_text.place(x=x_position, y=y_position)

        self.next_question_button.place(x=x_position+260, y=y_position-40)
        self.restart_button.place(x=x_position+125, y=y_position-40)
        self.add_question_button.place(x=x_position-10, y=y_position-40)

    def set_window_size(self):
        self.master.geometry("400x500+300+300")

    def set_color_scheme(self):
        self.background_color = "#004643"
        self.headline_color = "#fffffe"
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
            if len(answer) == len(correct_answer):
                variations.append(answer)

            common_part = difflib.SequenceMatcher(None, answer, correct_answer).find_longest_match(0, len(answer), 0, len(correct_answer)).size
            if common_part > 2 and answer in existing_answers:
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
            button.config(text=str(choices[i]))

    def check_answer(self, choice_index):
        if self.current_question_index >= len(self.question_list):
            return

        chosen_answer = self.choice_buttons[choice_index].cget("text")
        correct_answer = self.question_list[self.current_question_index].correct_answer

        self.question_list[self.current_question_index].user_choice = chosen_answer

        if chosen_answer == correct_answer:
            self.score += 1

        self.asked_questions.add(correct_answer)
        self.current_question_index += 1
        self.next_question()

    def next_question(self):
        if not self.remaining_questions:
            self.show_final_results()
            return

        self.quiz_mode()

    def show_final_results(self):
        result_message = f"Quiz Complete. Your final score: {self.score}\n\n"
        result_message += "Results for each question:\n"

        for i, question in enumerate(self.question_list):
            result_message += f"\nQuestion {i + 1}:\n"
            result_message += f"  - Correct Answer: {question.correct_answer}\n"
            result_message += f"  - Your Choice: {question.user_choice}\n"

        self.scrollable_results_text.insert(tk.END, result_message, "center")

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
    root.mainloop()

if __name__ == "__main__":
    main()
