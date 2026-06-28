# SmartOCR 🔍

An intelligent OCR (Optical Character Recognition) system powered by Google Gemini AI for extracting text from images and PDF documents.

🌐 Live Demo

🔗 Try SmartOCR: https://your-deployment-link.com

Demo Features:

- Upload image or PDF files
- AI-powered text extraction using Google Gemini
- View extracted text instantly
- Store results in the database


## 📋 Features

- **AI-Powered OCR**: Utilizes Google's Gemini AI for accurate text extraction
- **Multi-Format Support**: Process both images and PDF documents
- **Database Storage**: Stores extracted text and metadata in SQLite database
- **Web Interface**: User-friendly HTML interface for uploading and processing documents
- **Meter Reading Detection**: Specialized OCR for utility meter readings
- **Batch Processing**: Handle multiple documents efficiently

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Google Cloud account with Gemini API access
- pip (Python package installer)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Sudhasri-ui/smartOCR.git
   cd smartOCR
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - Linux/Mac:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up Google Cloud credentials**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select existing one
   - Enable the Gemini API
   - Create a service account
   - Download the JSON key file
   - Save it as `google_key.json` in the project root directory

6. **Configure environment variables** (optional)
   - Create a `.env` file in the project root
   - Add your configuration settings

## 📖 Usage

### Running the Application

```bash
python main.py
```

### Using the Web Interface

1. Open your browser and navigate to the local server (check terminal for URL)
2. Upload an image or PDF document
3. Click "Process" to extract text
4. View and download the extracted text

### Using Individual Modules

**Image OCR:**
```python
from gemini_ocr import process_image

result = process_image("path/to/image.jpg")
print(result)
```

**PDF Processing:**
```python
from pdf_reader import extract_text_from_pdf

text = extract_text_from_pdf("path/to/document.pdf")
print(text)
```

**Meter Reading:**
```python
from vision_ocr import read_meter

reading = read_meter("path/to/meter_image.jpg")
print(reading)
```

## 📁 Project Structure

```
smartOCR/
├── main.py                 # Main application entry point
├── gemini_ocr.py          # Gemini AI OCR implementation
├── gemini_structure.py    # Structured data extraction
├── pdf_reader.py          # PDF text extraction
├── vision_ocr.py          # Computer vision OCR utilities
├── ocr_utils.py           # OCR helper functions
├── llm_client.py          # LLM client wrapper
├── database.py            # Database operations
├── templates/             # HTML templates
│   ├── table.html
│   └── upload.html
├── uploads/               # Uploaded files directory
├── google_key.json        # Google Cloud credentials (not in repo)
├── .gitignore            # Git ignore file
├── requirements.txt       # Python dependencies
└── README.md             # Project documentation
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
GOOGLE_APPLICATION_CREDENTIALS=google_key.json
DATABASE_PATH=meter_readings.db
UPLOAD_FOLDER=uploads
```

## 📊 Database Schema

The application uses SQLite to store:
- Extracted text content
- Document metadata
- Processing timestamps
- Meter readings (if applicable)

## 🛠️ Technologies Used

- **Python 3.x** - Core programming language
- **Google Gemini AI** - Advanced OCR and text extraction
- **SQLite** - Lightweight database
- **Flask/FastAPI** - Web framework (based on your implementation)
- **HTML/CSS** - Frontend interface

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/improvement`)
3. Make your changes
4. Commit your changes (`git commit -am 'Add new feature'`)
5. Push to the branch (`git push origin feature/improvement`)
6. Create a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Important Notes

- **Never commit `google_key.json`** to version control
- Keep your API keys secure and private
- The `.gitignore` file is configured to exclude sensitive files

## 🐛 Troubleshooting

### Common Issues

**Issue: API Authentication Error**
- Ensure `google_key.json` is in the project root
- Verify the service account has proper permissions

**Issue: Module Not Found**
- Activate the virtual environment
- Run `pip install -r requirements.txt`

**Issue: Database Lock Error**
- Close any programs accessing the database
- Restart the application

## 📧 Contact

For questions or support, please open an issue on GitHub.

## 🙏 Acknowledgments

- Google Gemini AI for powerful OCR capabilities
- Open-source community for excellent Python libraries

---

**Made with ❤️ by Sudhasri**
