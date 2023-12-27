import customtkinter
import json
from difflib import get_close_matches
import os

def LOAD_KNOWLEDGE_BASE(FILE_PATH: str):
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, 'r') as file:
            DATA = json.load(file)
    else:
        DATA = {"Questions": []}
        with open(FILE_PATH, 'w') as file:
            json.dump(DATA, file, indent=2)
    return DATA
def save_knowledge_base(FILE_PATH: str, DATA: dict):
    with open(FILE_PATH, 'w') as file:
        json.dump(DATA, file, indent=2)
def find_best_match(user_Question: str, Questions: list) -> str or None:
	matches = get_close_matches(user_Question, Questions, n=1, cutoff=0.6)
	return matches[0] if matches else None
def get_answer_for_Question(Question: str, knowledge_base: dict) -> str or None:
    for q in knowledge_base["Questions"]:
        if q["Question"] == Question:
            return q["answer"]
    return None
def Luancher(message):
    knowledge_base: dict = LOAD_KNOWLEDGE_BASE('knowledge_base.json')
    while True:
        user_input: str = message
        if user_input.lower() == 'quit':
            break
        best_match: str | None = find_best_match(user_input, [q["Question"] for q in knowledge_base["Questions"]])
        if best_match:
            answer: str = get_answer_for_Question(best_match, knowledge_base)
            return answer
        else:
            print("Bot: I don't know the answer. Can you teach me?")
            root = customtkinter.CTk()
            root.geometry('200x50+100+30')
            root.title("LTOOL")
            bb = customtkinter.CTkEntry(root)
            bb.pack()
            def new_answers():
                if bb.get().lower() != 'skip':
                    knowledge_base["Questions"].append({"Question": user_input, "answer": bb.get()})
                    save_knowledge_base('knowledge_base.json', knowledge_base)
                    print("Bot: Thank you! I've learned something new.")
                    root.destroy()
            btn = customtkinter.CTkButton(root, text=" ارسال ", command=new_answers)
            
            btn.pack()
            def NBind(event):
                new_answers()
            root.bind('<Return>', NBind)
            root.mainloop()
            
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        def botReply():
            Question = QuestionField.get()
            Question = Question.capitalize()                                                         
            textarea.insert(customtkinter.END, 'YOU: ' + Question + '\n')
            textarea.insert(customtkinter.END, 'BOT: ' + str(Luancher(message=Question)) + '\n')
            QuestionField.delete(0, customtkinter.END)
        def TBind(event):
            botReply()
        
        self.title("U8SEF - ZPT")
        self.geometry('500x570+100+30')
        centerFrame = customtkinter.CTkFrame(self, width=500, height=570)
        centerFrame.pack()
        scrollbar = customtkinter.CTkScrollbar(centerFrame)
        scrollbar.pack(side=customtkinter.RIGHT)
        textarea = customtkinter.CTkTextbox(centerFrame, font=('Parastoo', 20, 'bold'), height=400, yscrollcommand=scrollbar.set, wrap='word', width=500)
        textarea.pack(side=customtkinter.LEFT)
        scrollbar.configure(command=textarea.yview)
        QuestionField = customtkinter.CTkEntry(self,height=50, font=('Parastoo', 20, 'bold'))
        QuestionField.pack(pady=15, fill=customtkinter.X)
        askButton = customtkinter.CTkButton(self, text=" ارسال ", width=80, height=40, command=botReply)
        askButton.pack()
        self.bind('<Return>', TBind)

app = App()
app.mainloop()
