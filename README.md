# 🎓 Student Performance Analyzer

A **Python-based data analysis and visualization system** that helps teachers analyze student academic performance.
The application processes student marks, generates grades, ranks students, provides AI-based feedback, and visualizes performance through an interactive **Streamlit dashboard**.

---

# 🚀 Features

## 📊 Academic Analysis

* Calculates **mid exam score using weighted average**
* Computes **total marks automatically**
* Assigns **grades (A, B, C, D, F)**
* Determines **pass / fail percentage**
* Generates **student rankings**

## 📈 Data Visualization

* Interactive **bar charts**
* **Grade distribution pie charts**
* **Subject performance comparison**
* **Class analytics dashboard**

## 🧠 AI Feedback

Automatically generates **performance feedback** for each student.

Examples:

* Excellent performance
* Very good understanding
* Good but needs improvement
* Needs serious improvement
* At risk of failing

## 🔍 Student Search

* Search students instantly by **name**

## ⚠ Risk Detection

* Automatically identifies **failing students**

## 📥 Report Generation

Download reports easily:

* **Excel report**
* **PDF summary report**

## 🏫 Multi-Class Comparison

* Upload multiple class datasets
* Compare class averages
* Identify the **best performing class**

## 🔐 Secure Login

Teacher login system for accessing the dashboard.

Default credentials:

Username

```
teacher
```

Password

```
1234
```

---

# 🛠 Technologies Used

* **Python**
* **Streamlit** – interactive dashboard
* **Pandas** – data processing
* **Plotly** – interactive visualizations
* **Matplotlib** – additional data visualization
* **ReportLab** – PDF report generation
* **OpenPyXL** – Excel file export

---

# 📂 Project Structure

```
student-performance-analyzer
│
├── analysis.py          # Main Streamlit dashboard application
├── students.csv         # Sample student dataset
├── requirements.txt     # Required Python libraries
└── README.md            # Project documentation
```

---

# 📥 Installation

Clone the repository

```bash
git clone https://github.com/yourusername/student-performance-analyzer.git
```

Navigate to the project directory

```bash
cd student-performance-analyzer
```

Install required dependencies

```bash
pip install -r requirements.txt
```

---

# ▶ Run the Application

Start the Streamlit dashboard

```bash
streamlit run analysis.py
```

The application will automatically open in your browser.

---

# 📄 Input File Format

The uploaded **CSV or Excel file** should contain the following columns:

| Name  | Assignment | Mid1 | Mid2 | Semester |
| ----- | ---------- | ---- | ---- | -------- |
| John  | 15         | 20   | 18   | 40       |
| Sarah | 18         | 19   | 20   | 42       |
| Rahul | 14         | 17   | 16   | 35       |

---

# 📊 Example Output

The system generates:

* 📊 Student ranking table
* 📈 Class performance statistics
* 📉 Subject performance charts
* 🥧 Grade distribution pie chart
* 🧠 AI student feedback
* 🏆 Top 5 student list
* 📥 Downloadable Excel and PDF reports

---

# 🎯 Use Cases

* Teacher performance analysis
* Academic data visualization
* Student grading automation
* Educational analytics projects
* Data science learning projects

---

# 📌 Future Improvements

* Student login portal
* Email report generation
* Machine learning grade prediction
* Database integration
* Attendance analytics
* Institution-level dashboards

---

# 🤝 Contributing

Contributions are welcome.

1. Fork the repository
2. Create a new feature branch
3. Commit your changes
4. Submit a pull request

---

# 📄 License

This project is open-source and available under the **MIT License**.

---

# ⭐ Support

If you like this project, consider giving it a **star ⭐ on GitHub** to support development.
