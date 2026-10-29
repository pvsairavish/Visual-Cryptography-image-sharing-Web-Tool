# 🔐 Visual Cryptography Tool for Secret Image Sharing

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.40+-FF4B4B)
![Flask](https://img.shields.io/badge/Flask-3.0+-black)
![OpenCV](https://img.shields.io/badge/OpenCV-4.10+-green)
![NumPy](https://img.shields.io/badge/NumPy-2.0+-orange)
![Security](https://img.shields.io/badge/Security-Visual%20Cryptography-red)
![Status](https://img.shields.io/badge/Status-Completed-success)

**Try the live application here:**

👉 [(https://visual-cryptography-image-sharing-web-tool-p3bjpgyjhlov4awdvvb.streamlit.app/)](https://visual-cryptography-image-sharing-web-tool-p3bjpgyjhlov4awdvvb.streamlit.app/)]

### 🛡️ Secure Image Encryption • Secret Sharing • Image Reconstruction

A lightweight **Visual Cryptography web application** that securely splits an image into two independent secret shares. The original image can only be reconstructed when both shares are combined.

---

## 🌟 Project Overview

**Visual Cryptography Tool** is a web-based security application developed using **Python, Flask, OpenCV, and NumPy**.

The system implements the concept of **Visual Secret Sharing**, where a confidential image is divided into two separate shares:

```text
                 🔐 SECRET IMAGE
                       │
                       ▼
              ┌─────────────────┐
              │ Visual           │
              │ Cryptography     │
              │ Encryption       │
              └─────────────────┘
                 │           │
                 ▼           ▼
            🖼️ Share 1    🖼️ Share 2
                 │           │
                 └─────┬─────┘
                       │
                       ▼
              🔓 RECONSTRUCTION
                       │
                       ▼
                🖼️ ORIGINAL IMAGE
```

Each individual share appears random and does not reveal the complete secret image. The original image becomes visible only when **both shares are combined**.

---

## 🎯 Project Objectives

The main objectives of this project are:

- 🔐 Protect confidential images using visual cryptography
- 🖼️ Split a secret image into multiple shares
- 🛡️ Prevent a single share from revealing the complete image
- 🔄 Reconstruct the original image using both shares
- 🌐 Provide a simple web interface for encryption and decryption
- 📥 Allow users to download encrypted shares and reconstructed images
- ⚡ Provide a lightweight solution suitable for academic and practical security applications

---

## ✨ Key Features

| Feature | Description |
|---|---|
| 📤 Image Upload | Upload images through the web interface |
| 🔐 Image Encryption | Generate two secret shares from the input image |
| 🖼️ Secret Sharing | Store the image information across two independent shares |
| 🔓 Image Reconstruction | Combine both shares to recover the secret image |
| 💾 Download Shares | Download generated encrypted shares |
| 📥 Download Output | Download the reconstructed image |
| 🌐 Web Interface | Simple Flask-based interface |
| ⚡ Lightweight | Uses efficient image and matrix operations |
| 📱 Responsive UI | HTML, CSS and Bootstrap-based interface |

---

## 🧠 How Visual Cryptography Works

The system follows a simple **Encrypt → Share → Reconstruct** workflow.

### 1️⃣ Upload

The user uploads a confidential image through the Flask web application.

```text
User
 │
 ▼
📤 Upload Image
```

### 2️⃣ Encryption

The uploaded image is processed using OpenCV and NumPy.

The system generates:

- **Share 1**
- **Share 2**

```text
             Original Image
                    │
                    ▼
             🔐 Encryption
              /           \
             /             \
            ▼               ▼
       🖼️ Share 1      🖼️ Share 2
```

### 3️⃣ Individual Shares

Each share is designed to look like random/noise information.

A single share should not provide the complete secret.

```text
Share 1 → ❌ Cannot reveal complete image

Share 2 → ❌ Cannot reveal complete image
```

### 4️⃣ Reconstruction

When both shares are combined using the reconstruction process:

```text
Share 1
   +
Share 2
   │
   ▼
🔓 Reconstruction
   │
   ▼
Original Image
```

The secret image is recovered.

---

## 🏗️ System Architecture

```text
                 ┌─────────────────────┐
                 │       User          │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │   Flask Web UI      │
                 └──────────┬──────────┘
                            │
                ┌───────────┴───────────┐
                ▼                       ▼
        📤 Upload Image          🔓 Upload Shares
                │                       │
                ▼                       ▼
        ┌───────────────┐       ┌────────────────┐
        │ OpenCV /      │       │ Reconstruction │
        │ NumPy         │       │ Module         │
        └───────┬───────┘       └───────┬────────┘
                │                       │
                ▼                       ▼
        🔐 Share Generation       🖼️ Reconstructed
                │                    Image
          ┌─────┴─────┐
          ▼           ▼
      Share 1       Share 2
```

---

## 🛠️ Technology Stack

### Backend

- **Python 3**
- **Flask**
- **OpenCV**
- **NumPy**

### Frontend

- **HTML5**
- **CSS3**
- **Bootstrap**
- **Jinja2**

### Image Processing

- OpenCV image reading and writing
- NumPy matrix and pixel operations
- Image transformation and reconstruction

---

## 📂 Project Structure

```text
Visual-Cryptography-Tool/
│
├── streamlit_app.py      # Streamlit v2.0 Web Application (Obsidian Cyber Studio)
├── cns.py                # Automated launcher (opens Streamlit in default browser)
├── run_streamlit.bat     # Windows 1-click batch launcher
├── app.py                # Legacy Flask backend server
├── requirements.txt      # Python dependencies
│
├── .streamlit/
│   └── config.toml       # Streamlit dark theme configuration
│
├── templates/            # Flask Jinja2 HTML templates
│   ├── base.html
│   ├── index.html
│   ├── encrypt.html
│   ├── decrypt.html
│   ├── login.html
│   └── signup.html
│
├── static/
│   ├── style.css         # Custom CSS styling
│   ├── uploads/          # Sample / uploaded images
│   └── shares/           # Generated cryptographic shares
│
├── .gitignore            # Git exclusions (venv, db, temp files)
└── README.md             # Project documentation
```

> Adjust the folder names above if your actual repository structure is different.

---

## 🔄 Complete Workflow

```text
┌──────────────┐
│ Upload Image │
└──────┬───────┘
       │
       ▼
┌────────────────────┐
│ Image Preprocessing│
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│ Secret Share       │
│ Generation         │
└─────────┬──────────┘
          │
     ┌────┴────┐
     ▼         ▼
 Share 1     Share 2
     │         │
     └────┬────┘
          │
          ▼
┌────────────────────┐
│ Share Combination  │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│ Reconstructed      │
│ Secret Image       │
└────────────────────┘
```

---

## 🔐 Security Concept

The core idea is based on **secret sharing**.

Instead of storing or transferring one complete confidential image, the system divides the information between two shares.

### Without both shares

```text
Share 1 → 🔒 Incomplete information
Share 2 → 🔒 Incomplete information
```

### With both shares

```text
Share 1 + Share 2
       ↓
  🔓 Secret Image
```

This provides a basic form of **distributed access control**, because access to the complete image requires possession of both shares.

---

## 💡 Example Use Case

### 🏫 Secure University Document Sharing

Suppose a university wants to protect confidential examination documents.

The university can divide the document into two shares:

```text
Confidential Exam Document
            │
            ▼
      Visual Cryptography
        /           \
       ▼             ▼
 Department A    Department B
   Share 1         Share 2
       \             /
        \           /
         ▼         ▼
        Combined
           │
           ▼
    Original Document
```

Department A alone cannot reconstruct the complete document.

Department B alone cannot reconstruct the complete document.

Only when both departments provide their shares can the document be reconstructed.

---

## 🌍 Potential Applications

### 🏛️ Government

Secure distribution of classified maps, documents and images between departments.

### 🏦 Banking

Protection of sensitive scanned documents, cheque images and financial records.

### 🏥 Healthcare

Controlled sharing of medical images and confidential diagnostic documents.

### 🪖 Defense

Distributed protection of confidential maps, mission-related images and strategic information.

### 🎓 Education

Secure distribution of examination papers, answer scripts and academic documents.

### 🔑 Authentication

Visual secret sharing can be incorporated into image-based authentication and verification systems.

---

## 📊 Input & Output

### Input

```text
🖼️ Secret Image
```

### Encryption Output

```text
🔐 Share 1
🔐 Share 2
```

### Decryption Output

```text
🔓 Reconstructed Image
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone <repo-url>
cd Visual-Cryptography-Tool
```

### 2️⃣ Create a Virtual Environment

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install flask==3.0.3
pip install opencv-python==4.10.0
pip install numpy==2.0.1
```

### 4️⃣ Start the Application

#### Option A: Run with Streamlit (Interactive Modern Web App)
```bash
streamlit run streamlit_app.py
```
*Or on Windows, simply double-click `run_streamlit.bat`!*

#### Option B: Run with Flask
```bash
python app.py
```

### 5️⃣ Open in Browser

- **Streamlit App:** `http://localhost:8501`
- **Flask App:** `http://127.0.0.1:5000`

---

## 📦 Requirements

Example `requirements.txt`:

```text
Flask==3.0.3
opencv-python==4.10.0
numpy==2.0.1
```

---

## 🖥️ How to Use

### 🔐 Encryption

1. Open the application.
2. Select an image.
3. Upload the image.
4. Click **Encrypt**.
5. The system generates two secret shares.
6. Download **Share 1** and **Share 2**.

### 🔓 Decryption

1. Open the decryption section.
2. Upload Share 1.
3. Upload Share 2.
4. Click **Decrypt / Reconstruct**.
5. The system combines both shares.
6. View or download the reconstructed image.

---

## ⚠️ Limitations

Although the system demonstrates the concept of visual cryptography effectively, it has some limitations:

- Works best with **binary or grayscale images**.
- Color-image support may have reduced reconstruction quality depending on the implementation.
- Image reconstruction can introduce quality loss.
- Both shares are required for successful reconstruction.
- The basic two-share scheme does not provide threshold-based sharing such as **2-of-3** or **3-of-5**.
- The Flask application is intended primarily as an academic/prototype implementation and requires additional hardening for production deployment.

---

## 🚀 Future Enhancements

The project can be extended with:

- 🔹 Support for high-quality color images
- 🔹 **(k, n) threshold visual cryptography**
- 🔹 More than two secret shares
- 🔹 AES + Visual Cryptography hybrid encryption
- 🔹 Password-protected shares
- 🔹 QR-code-based share distribution
- 🔹 User authentication and authorization
- 🔹 Secure cloud storage
- 🔹 Digital signatures for share verification
- 🔹 Share integrity validation
- 🔹 Docker-based deployment
- 🔹 Cloud deployment using AWS/Azure
- 🔹 Improved reconstruction quality
- 🔹 Audit logs for secure access tracking

---

## 🔬 Security Considerations

For a real-world deployment, additional security mechanisms should be considered.

The current project demonstrates the **visual secret-sharing concept**, but it should not automatically be considered a complete cryptographic security system.

Production implementations should additionally consider:

- Secure file storage
- HTTPS
- Authentication and authorization
- Access control
- Secure deletion of uploaded files
- File-type validation
- File-size limits
- Malware scanning
- Cryptographic integrity checks
- Secure session management

---

## 📸 Demo Screenshots

Add screenshots of your application here:

```text
📷 Upload Interface

📷 Encryption Result

📷 Generated Share 1

📷 Generated Share 2

📷 Decryption Interface

📷 Reconstructed Image
```

Example Markdown:

```markdown
![Upload Page](screenshots/upload.png)

![Encryption Result](screenshots/encryption.png)

![Decryption Result](screenshots/decryption.png)
```

---

## 🎓 Academic Relevance

This project demonstrates practical concepts from:

- 🔐 Cryptography
- 🛡️ Information Security
- 🖼️ Digital Image Processing
- 🧮 Matrix Operations
- 🌐 Web Application Development
- 🐍 Python Programming
- 🔄 Secret Sharing
- 🔒 Distributed Access Control

---

## 👨‍💻 Author

### **Punati Venkata Sai Ravish**

AI & Machine Learning | Data Analytics | Software Development

---

## ⭐ Project Highlights

> 🔐 **Split the secret.**  
> 🛡️ **Protect each share.**  
> 🔓 **Reconstruct only with both.**

If you find this project useful, consider giving the repository a ⭐.

---

## 📄 License

This project is intended for **educational, academic, and research purposes**.
