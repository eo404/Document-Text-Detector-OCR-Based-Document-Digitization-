# 📄 Document Text Detector (OCR-Based Document Digitization)

A Python-based **OCR Document Digitization System** that extracts text from images and converts it into a clean digital document (PDF).
The project applies **image preprocessing techniques** to improve OCR accuracy and compares their performance.

This project was developed as part of a **Computer Graphics & Image Processing (CGIP)** implementation.

---

# 🚀 Features

* 📷 Upload an image containing printed text
* 🔍 Image preprocessing for better OCR accuracy
* ⚙️ Comparison of two image processing techniques
* 📊 OCR confidence and performance analysis
* 📄 Automatic PDF generation of extracted text
* 🖥️ Simple GUI interface built with Tkinter
* 📈 Visualization of preprocessing techniques and accuracy comparison

---

# 🧠 Image Processing Techniques Used

### 1️⃣ Technique 1: Otsu Thresholding

* Gaussian Blur (noise reduction)
* Global Otsu Thresholding

### 2️⃣ Technique 2: Adaptive Thresholding + Morphology

* Median Blur
* Adaptive Gaussian Thresholding
* Morphological Closing

The system automatically **selects the technique with the highest OCR confidence**.

---

# 🛠️ Technologies Used

* Python
* OpenCV
* Tesseract OCR
* Tkinter (GUI)
* Matplotlib
* FPDF
* Pytesseract


---

# ⚙️ Installation

## 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/your-repository-name.git
cd your-repository-name
```

---

## 2️⃣ Create Virtual Environment

```bash
python -m venv venv
```

Activate it:

### Windows

```
venv\Scripts\activate
```

### Mac/Linux

```
source venv/bin/activate
```

---

## 3️⃣ Install Dependencies

```
pip install -r requirements.txt
```

---

## 4️⃣ Install Tesseract OCR

Download from:

```
https://github.com/tesseract-ocr/tesseract
```

If using **Windows**, update the path in the code:

```
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

---

# ▶️ Running the Application

Run the program:

```
python main.py
```

Steps:

1. Select an image containing text.
2. Click **Detect Text**.
3. The system processes the image.
4. Extracted text is displayed.
5. A **PDF document is automatically generated**.

---

# 📊 Output

The system generates:

* Extracted text in the GUI
* Digitized **PDF document**
* **Performance comparison chart**
* OCR confidence analysis

---

# 🎯 Applications

* Document digitization
* OCR research
* Academic CGIP projects
* Scanned document processing
* Text extraction from images

---

# 👨‍💻 Contributors

* Eldho Reji

---

# 📜 License

This project is for **educational and research purposes**.

---

⭐ If you found this project helpful, consider giving it a **star** on GitHub!
