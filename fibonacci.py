import tkinter as tk

def fibonacci(n):
    fib_sequence = []
    a, b = 0, 1
    for _ in range(n):
        fib_sequence.append(a)
        a, b = b, a + b
    return fib_sequence

def generate_fibonacci():
    try:
        limit = int(entry.get())
        if limit <= 0:
            result_label.config(text="Please enter a positive number.")
            return
        result = fibonacci(limit)
        result_label.config(text=f"Fibonacci Sequence: {result}")
    except ValueError:
        result_label.config(text="Please enter a valid number.")

# Create window
window = tk.Tk()
window.title("Fibonacci Generator")
window.geometry("300x200")

# Input field
tk.Label(window, text="Enter number of terms:").pack(pady=5)
entry = tk.Entry(window)
entry.pack(pady=5)

# Generate button
tk.Button(window, text="Generate", command=generate_fibonacci).pack(pady=5)

# Result label
result_label = tk.Label(window, text="Sequence will appear here.")
result_label.pack(pady=10)

# Start the app
window.mainloop()