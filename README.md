## Proyek Analisis Data: Bike Sharing Dataset

### Setup Environment - Anaconda
conda create --name main-ds python=3.9
conda activate main-ds
pip install -r requirements.txt

### Setup Environment - Shell/Terminal
mkdir proyek_analisis_data
cd proyek_analisis_data
pipenv install
pipenv shell
pip install -r requirements.txt

### Run streamlit app
#### Pastikan bahwa saat menggunakan command di bawah, Anda berada di direktori SUBMISSION dan BUKAN di dalam folder DASHBOARD. Direktori SUBMISSION berada 1 tingkat di atas folder DASHBOARD.
streamlit run dashboard/dashboard.py
