import os
import fitz  # PyMuPDF
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from PIL import Image


# --- Main function ---
def pdf_to_images(pdf_path, output_dir, progress_callback=None):
    doc = fitz.open(pdf_path)
    os.makedirs(output_dir, exist_ok=True)

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        pix = page.get_pixmap(dpi=300)
        output_path = os.path.join(output_dir, f"page_{page_num + 1:03}.png")
        pix.save(output_path)
        if progress_callback:
            progress_callback(page_num + 1, len(doc))

    return len(doc)


# --- User interface ---
def run_app():
    def select_pdf():
        file_path = filedialog.askopenfilename(
            title="Wybierz plik PDF", filetypes=[("PDF Files", "*.pdf")]
        )
        if file_path:
            pdf_entry.delete(0, tk.END)
            pdf_entry.insert(0, file_path)

    def select_output_dir():
        dir_path = filedialog.askdirectory(title="Wybierz folder docelowy")
        if dir_path:
            output_entry.delete(0, tk.END)
            output_entry.insert(0, dir_path)

    def update_progress(current, total):
        progress_bar["maximum"] = total
        progress_bar["value"] = current
        root.update_idletasks()

    def process():
        pdf_path = pdf_entry.get()
        output_dir = output_entry.get()

        if not os.path.isfile(pdf_path):
            messagebox.showerror("Błąd", "Niepoprawna ścieżka do pliku PDF.")
            return

        if not os.path.isdir(output_dir):
            messagebox.showerror("Błąd", "Niepoprawna ścieżka do folderu.")
            return

        try:
            progress_bar["value"] = 0
            total = pdf_to_images(
                pdf_path, output_dir, progress_callback=update_progress
            )
            # Show info and wait for user to press OK
            messagebox.showinfo("Sukces", f"Zapisano {total} stron jako obrazy.")
            # Reset fields and progress bar for next conversion
            pdf_entry.delete(0, tk.END)
            output_entry.delete(0, tk.END)
            progress_bar["value"] = 0
        except Exception as e:
            messagebox.showerror("Błąd", str(e))
            progress_bar["value"] = 0

    root = tk.Tk()
    root.title("PDF do obrazów")
    root.geometry("600x300")
    root.resizable(True, True)

    tk.Label(root, text="Plik PDF:").pack(pady=(10, 0))
    pdf_entry = tk.Entry(root, width=60)
    pdf_entry.pack()
    tk.Button(root, text="Wybierz PDF", command=select_pdf, cursor="hand2").pack(
        pady=(0, 10)
    )

    tk.Label(root, text="Folder wyjściowy:").pack()
    output_entry = tk.Entry(root, width=60)
    output_entry.pack()
    tk.Button(
        root, text="Wybierz folder", command=select_output_dir, cursor="hand2"
    ).pack(pady=(0, 10))

    tk.Button(
        root, text="Zapisz strony jako obrazy", command=process, cursor="hand2"
    ).pack(pady=10)

    # Progress bar
    progress_bar = ttk.Progressbar(
        root, orient="horizontal", length=500, mode="determinate"
    )
    progress_bar.pack(pady=(10, 10))

    root.mainloop()


if __name__ == "__main__":
    run_app()
