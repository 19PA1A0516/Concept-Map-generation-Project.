import tkinter as tk
from tkinter import filedialog
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText

  

nltk.download('stopwords')
nltk.download('punkt')

class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

    def __str__(self):
        return str(self.value)

# function to insert a node into a binary search tree
def insert_node(root, node):
    if root is None:
        root = node
    else:
        if node.value < root.value:
            if root.left is None:
                root.left = node
            else:
                insert_node(root.left, node)
        else:
            if root.right is None:
                root.right = node
            else:
                insert_node(root.right, node)

root = tk.Tk()
root.withdraw()

# open a file dialog to choose a file
file_path = filedialog.askopenfilename(filetypes=[('All Files', '*.*')])

# read the file contents
with open(file_path, 'r') as file:
    text = file.read()

# remove stop words and punctuations

stop_words=stopwords.words('english')+['also']
words = word_tokenize(text.lower())
filtered_words = [word for word in words if word.isalpha() and word not in stop_words]
for word in filtered_words:
    if (word+"s" in filtered_words) or (word+"es" in filtered_words):
        for i in range(len(filtered_words)):
            if filtered_words[i] in [word+"s",word+"es"]:
                filtered_words[i]=word
# get most frequent words
fdist = FreqDist(filtered_words)
most_common_words = [word[0] for word in fdist.most_common()]

# build binary tree
root_node = Node(most_common_words[0])
for word in most_common_words[1:]:
    insert_node(root_node, Node(word))

# display text and tree
def draw_tree(node, x, y, dx, dy):
    if node:
        # draw current node
        canvas.create_oval(x - dx, y - dy, x + dx, y + dy, fill='white')
        canvas.create_text(x, y, text=node.value)

        # draw left child
        if node.left:
            x_left = x - dx * 2
            y_left = y + dy * 2
            canvas.create_line(x, y, x_left, y_left)
            draw_tree(node.left, x_left, y_left, dx // 2, dy)

        # draw right child
        if node.right:
            x_right = x + dx * 2
            y_right = y + dy * 2
            canvas.create_line(x, y, x_right, y_right)
            draw_tree(node.right, x_right, y_right, dx // 2, dy)

# display text and tree
window = tk.Tk()
window.geometry("800x600")

text_label = tk.Label(window, text="Input Text:", font=("Arial Bold", 14))
text_label.pack(pady=10)

text_box = ScrolledText(window, width=80, height=10)
text_box.pack(pady=10)

text_box.insert(tk.INSERT, text)

canvas_frame = ttk.Frame(window)
canvas_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

canvas = tk.Canvas(canvas_frame, width=800, height=600, bg='white')
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = ttk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=frame, anchor="nw")

draw_tree(root_node, 400, 100, 100, 80)

window.mainloop()
