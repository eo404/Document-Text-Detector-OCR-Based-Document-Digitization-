import cv2
import pytesseract
from pytesseract import Output
import time
import matplotlib.pyplot as plt
from fpdf import FPDF
import os
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

# --- IMPORTANT: If on Windows, uncomment and update the path to your Tesseract executable ---
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class DocumentDigitizer:
    def __init__(self, image_path):
        self.image_path = image_path
        self.img_color = cv2.imread(image_path)
        if self.img_color is None:
            raise ValueError("Image not found. Please check the path.")
        self.img_gray = cv2.cvtColor(self.img_color, cv2.COLOR_BGR2GRAY)
        self.results = {}

    def technique_1_otsu(self):
        """Technique 1: Gaussian Blur + Global Otsu's Thresholding"""
        start_time = time.time()
        
        # CGIP Algorithm: Gaussian Blur for noise reduction
        blurred = cv2.GaussianBlur(self.img_gray, (5, 5), 0)
        # CGIP Algorithm: Otsu's Thresholding
        _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        process_time = time.time() - start_time
        return thresh, process_time

    def technique_2_adaptive_morph(self):
        """Technique 2: Adaptive Thresholding + Morphological Closing"""
        start_time = time.time()
        
        # CGIP Algorithm: Median Blur (better for salt & pepper noise)
        blurred = cv2.medianBlur(self.img_gray, 3)
        # CGIP Algorithm: Adaptive Thresholding
        thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                       cv2.THRESH_BINARY, 11, 2)
        
        # CGIP Algorithm: Morphological Operations (Closing to fill small holes in text)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
        morph = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        
        process_time = time.time() - start_time
        return morph, process_time

    def extract_text_and_metrics(self, processed_img, method_name):
        """Runs OCR, calculates average confidence (accuracy), and records time."""
        start_time = time.time()
        
        # Extract dictionary data for confidence scores
        ocr_data = pytesseract.image_to_data(processed_img, output_type=Output.DICT)
        text = pytesseract.image_to_string(processed_img)
        
        ocr_time = time.time() - start_time
        
        # Calculate average confidence for recognized words
        confidences = [int(conf) for conf in ocr_data['conf'] if int(conf) != -1]
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0
        
        self.results[method_name] = {
            'text': text,
            'confidence': avg_confidence,
            'ocr_time': ocr_time
        }
        return text

    def generate_pdf(self, text, output_filename="Output_Document.pdf"):
        """Converts extracted text to a formatted PDF."""
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        
        # Clean text to prevent FPDF unicode errors
        safe_text = text.encode('latin-1', 'replace').decode('latin-1')
        
        pdf.multi_cell(0, 10, safe_text)
        pdf.output(output_filename)
        print(f"\n[SUCCESS] PDF saved as {output_filename}")

    def visualize_and_compare(self, img1, time1, img2, time2):
        """Generates the required visualization and performance analysis."""
        fig, axs = plt.subplots(2, 2, figsize=(12, 10))
        fig.suptitle('CGIP Project: Document Image Enhancement & OCR', fontsize=16)

        # 1. Visual Comparison
        axs[0, 0].imshow(cv2.cvtColor(self.img_color, cv2.COLOR_BGR2RGB))
        axs[0, 0].set_title("Original Image")
        axs[0, 0].axis('off')

        axs[0, 1].imshow(img1, cmap='gray')
        axs[0, 1].set_title(f"Tech 1: Otsu Thresholding\nPrep Time: {time1:.4f}s")
        axs[0, 1].axis('off')

        axs[1, 0].imshow(img2, cmap='gray')
        axs[1, 0].set_title(f"Tech 2: Adaptive + Morph\nPrep Time: {time2:.4f}s")
        axs[1, 0].axis('off')

        # 2. Performance Analysis (Accuracy/Confidence Chart)
        methods = ['Otsu', 'Adaptive+Morph']
        confidences = [self.results['Otsu']['confidence'], self.results['Adaptive']['confidence']]
        
        axs[1, 1].bar(methods, confidences, color=['blue', 'green'])
        axs[1, 1].set_title("OCR Confidence (Accuracy %)")
        axs[1, 1].set_ylim(0, 100)
        for i, v in enumerate(confidences):
            axs[1, 1].text(i, v + 2, f"{v:.1f}%", ha='center')

        plt.tight_layout()
        plt.savefig("Performance_Analysis.png")
        plt.show()

    def process_document(self, show_visualization=True):
        """Runs the complete OCR pipeline and returns the best detected text."""
        img_otsu, time_otsu = self.technique_1_otsu()
        img_adapt, time_adapt = self.technique_2_adaptive_morph()

        text_otsu = self.extract_text_and_metrics(img_otsu, 'Otsu')
        text_adapt = self.extract_text_and_metrics(img_adapt, 'Adaptive')

        best_method = 'Adaptive' if self.results['Adaptive']['confidence'] > self.results['Otsu']['confidence'] else 'Otsu'
        best_text = text_adapt if best_method == 'Adaptive' else text_otsu

        pdf_name = f"{os.path.splitext(os.path.basename(self.image_path))[0]}_OCR_Output.pdf"
        pdf_path = os.path.join(os.path.dirname(self.image_path), pdf_name)
        self.generate_pdf(best_text, pdf_path)

        if show_visualization:
            self.visualize_and_compare(img_otsu, time_otsu, img_adapt, time_adapt)

        return {
            'best_text': best_text,
            'best_method': best_method,
            'pdf_path': pdf_path,
            'prep_times': {
                'Otsu': time_otsu,
                'Adaptive': time_adapt
            },
            'results': self.results
        }


class DocumentDigitizerUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Document Text Detector")
        self.root.geometry("760x620")
        self.root.resizable(False, False)

        self.selected_file = tk.StringVar()
        self.status_text = tk.StringVar(value="Choose an image to begin OCR processing.")

        self._build_layout()

    def _build_layout(self):
        container = tk.Frame(self.root, padx=20, pady=20)
        container.pack(fill='both', expand=True)

        title = tk.Label(container, text="Document Text Detector", font=("Arial", 18, "bold"))
        title.pack(anchor='w')

        subtitle = tk.Label(
            container,
            text="Upload an image and run the same Otsu vs Adaptive OCR comparison pipeline.",
            font=("Arial", 10)
        )
        subtitle.pack(anchor='w', pady=(4, 18))

        file_frame = tk.Frame(container)
        file_frame.pack(fill='x', pady=(0, 12))

        file_entry = tk.Entry(file_frame, textvariable=self.selected_file, font=("Arial", 10))
        file_entry.pack(side='left', fill='x', expand=True)

        browse_button = tk.Button(file_frame, text="Browse", width=12, command=self.browse_file)
        browse_button.pack(side='left', padx=(10, 0))

        process_button = tk.Button(container, text="Detect Text", width=18, command=self.process_selected_file)
        process_button.pack(anchor='w', pady=(0, 12))

        status_label = tk.Label(container, textvariable=self.status_text, fg="blue", justify='left', anchor='w')
        status_label.pack(fill='x', pady=(0, 12))

        metrics_frame = tk.LabelFrame(container, text="Performance Analysis", padx=10, pady=10)
        metrics_frame.pack(fill='x', pady=(0, 12))

        self.metrics_label = tk.Label(metrics_frame, text="No file processed yet.", justify='left', anchor='w')
        self.metrics_label.pack(fill='x')

        text_frame = tk.LabelFrame(container, text="Extracted Text", padx=10, pady=10)
        text_frame.pack(fill='both', expand=True)

        self.text_output = scrolledtext.ScrolledText(text_frame, wrap='word', font=("Consolas", 10))
        self.text_output.pack(fill='both', expand=True)

    def browse_file(self):
        file_path = filedialog.askopenfilename(
            title="Select an image",
            filetypes=[
                ("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.tif;*.tiff"),
                ("All Files", "*.*")
            ]
        )
        if file_path:
            self.selected_file.set(file_path)
            self.status_text.set("Image selected. Click 'Detect Text' to run OCR.")

    def process_selected_file(self):
        image_path = self.selected_file.get().strip()
        if not image_path:
            messagebox.showwarning("No file selected", "Please choose an image file first.")
            return

        try:
            self.status_text.set("Processing image and extracting text...")
            self.root.update_idletasks()

            app = DocumentDigitizer(image_path)
            analysis = app.process_document(show_visualization=True)

            self.text_output.delete('1.0', tk.END)
            self.text_output.insert(tk.END, analysis['best_text'].strip() or "No text detected.")

            results = analysis['results']
            self.metrics_label.config(
                text=(
                    f"Best Method: {analysis['best_method']}\n"
                    f"Technique 1 (Otsu)     -> Confidence: {results['Otsu']['confidence']:.2f}% | "
                    f"OCR Time: {results['Otsu']['ocr_time']:.2f}s | Prep Time: {analysis['prep_times']['Otsu']:.4f}s\n"
                    f"Technique 2 (Adaptive) -> Confidence: {results['Adaptive']['confidence']:.2f}% | "
                    f"OCR Time: {results['Adaptive']['ocr_time']:.2f}s | Prep Time: {analysis['prep_times']['Adaptive']:.4f}s\n"
                    f"PDF Saved To: {analysis['pdf_path']}"
                )
            )
            self.status_text.set("OCR processing completed successfully.")
        except Exception as error:
            self.status_text.set("Processing failed.")
            messagebox.showerror("Processing Error", str(error))

    def run(self):
        self.root.mainloop()

# ==========================================
# Execution Block
# ==========================================
if __name__ == "__main__":
    DocumentDigitizerUI().run()