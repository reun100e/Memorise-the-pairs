# Memorise-the-pairs
A small python program designed to help you revise and memorise two pieces of logically unrelated data by repeatition &amp; recollection (basically mugging up) in the form of a quiz. I hate this method of learning but is extremely usefull in very niche cases like learning the index of books or important dates and such.

<p align="center">
    <img width="420" src="https://i.imgur.com/dMNoTgd.png" alt="screenshot">
</p>

# What does it do?
- The program takes in and stores question answer pair in the form of json file like this: <br>
 ![image](https://github.com/reun100e/Memorise-the-pairs/assets/47780896/bd93beed-af25-4f91-a554-5552f5695739)
- On running the quiz, the program asks each question with four choices as answers after shuffling everything. The choices contain the correct answers and three others which are most similar to the correct answer.
- The buttons can be used to restart the quiz or Add entries to the .json file.
- After clicking on an option, the result is immediately shown in a text area below the buttons and the quiz moves to the next question. <br>
- Once, all the questions are answered, the quiz stops by showing the total number of answered correctly.
 ![image](https://github.com/reun100e/Memorise-the-pairs/assets/47780896/5fe477f6-d39b-4652-aca5-819e749431d9)
- Clicking on the Restart quiz button, shuffles the questions and restarts the quiz.

# How to use
## Option A: Download the latest release
1. This is the easiest. Just download the latest version from the [releases](https://github.com/reun100e/Memorise-the-pairs/releases).
```
NOTE: During download there might be antivirus alert. This is because there is an .exe file. I guarentee you the file you get from here does no harm.
```
3. Download the 'Memorise-the-pairs.exe + questions.json.zip' file
4. Extract it
5. Open 'questions.json' using any text editor
6. Add your questions to the json file. Save it & close
7. Run quiz.exe

## Option B: Build your own
Make sure you have [Python](https://www.python.org/) installed in your machine. You will also need Tkinder installed
```
pip install tk
```
Then,
### 1. Download or clone the repo
```
git clone https://github.com/reun100e/Memorise-the-pairs.git
```
### 2. Open questions.json and add your questions and answers
![image](https://github.com/reun100e/Memorise-the-pairs/assets/47780896/bd93beed-af25-4f91-a554-5552f5695739)
### 3. Go to the root directory and run the script
```
python quiz.py
```

# FAQ
### 1. How to delete a question or how to edit/modify a question or answer?
As of now, there is no such functionality to do that. So kindly open the questions.json file using any text or code editor. Make you edits and save it.
### 2. Does it run on Andorid or iOS?
Not directly as a standalone. This works on windows and is tested on windows only as of now. Any python environment can run this code if you build it yourself using the steps mentioned above. But i have not made any standalone application for Android or iOS.

# Contact
Dr. Aghosh B Prasad <br>
aghoshbprasad100@gmail.com
