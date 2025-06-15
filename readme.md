
# Teacher Portal

## Repository

GitHub Repository: [https://github.com/rajatrawal/teacher](https://github.com/rajatrawal/teacher)  
Live Demo: [https://teacher-bpae.onrender.com/](https://teacher-bpae.onrender.com/)



## Run Locally

### 1. Clone the Repository

```bash
git clone https://github.com/rajatrawal/teacher.git
cd teacher
````

### 2. Create Virtual Environment & Install Requirements

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Run Migrations

```bash
python manage.py migrate
```


### 5. Start Development Server

```bash
python manage.py runserver
```

Open `http://127.0.0.1:8000/` in  browser.

---



## Testing

```bash
python manage.py test
```



