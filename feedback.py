import tkinter as tk
import os

def feedback_main():
    # Function to manage the feedback form's interactivity.
    def save_feedback():
        feedback_text = feedback_entry.get("1.0", "end-1c") 
        if feedback_text:
            # Create  "feedback" folder if it doesn't exist
            pathFeedback = "feedback"
            if not os.path.exists(pathFeedback):
                os.makedirs(pathFeedback)

            feedback_files = os.listdir(pathFeedback)
            file_name = f"{len(feedback_files) + 1}.txt"

            with open(os.path.join(pathFeedback, file_name), "w") as file:
                file.write(feedback_text)

            feedback_entry.delete("1.0", "end")
            feedback_confirmation.config(text="Thank you for your feedback, does help a bunch!")

    Feedback = tk.Tk()
    Feedback.title("Feedback")

    label = tk.Label(Feedback, text="Please tell us your experience:", font=("Arial", 16))
    label.pack(pady=10)

    feedback_entry = tk.Text(Feedback, width=40, height=10)
    feedback_entry.pack(padx=20, pady=5)

    submit_button = tk.Button(Feedback, text="Submit Feedback", command=save_feedback)
    submit_button.pack(pady=10)

    feedback_confirmation = tk.Label(Feedback, text="", font=("Arial", 12))
    feedback_confirmation.pack()
    Feedback.mainloop()
