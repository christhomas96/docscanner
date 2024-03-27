import tkinter as tk
from tkinter import filedialog, messagebox
from transformers import pipeline

# Initialize the model
nlp = pipeline("document-question-answering", model="impira/layoutlm-document-qa")

# Function to upload document
def upload_document():
    global uploaded_document
    file_path = filedialog.askopenfilename()
    if file_path:
        uploaded_document = file_path
        file_label.config(text=f"Uploaded: {file_path.split('/')[-1]}")


# Function to process question
def process_question():
    if uploaded_document:
        try:
            response = nlp(uploaded_document, question_entry.get())
            # Check if the response is a list and extract the first answer
            if isinstance(response, list) and response:
                answer = response[0]['answer']  # Take the answer from the first element
                score = response[0]['score']
                answer_text.set(f"Answer: {answer} (confidence: {score:.2f})")
            else:
                messagebox.showinfo("Unexpected Response", f"Received unexpected response format: {response}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
    else:
        messagebox.showinfo("No Document", "Please upload a document first.")

# Create the main window
root = tk.Tk()
root.title("Document QA Interface")
root.geometry("500x300")

# Upload button and label
upload_button = tk.Button(root, text="Upload Document", command=upload_document)
upload_button.pack(pady=10)
file_label = tk.Label(root, text="No document uploaded")
file_label.pack()

# Question entry and label
tk.Label(root, text="Enter your question:").pack(pady=(20,0))
question_entry = tk.Entry(root, width=50)
question_entry.pack(pady=5)

# Process button
process_button = tk.Button(root, text="Process Question", command=process_question)
process_button.pack(pady=10)

# Answer display
answer_text = tk.StringVar()
answer_label = tk.Label(root, textvariable=answer_text)
answer_label.pack(pady=10)

# Run the application
root.mainloop()
