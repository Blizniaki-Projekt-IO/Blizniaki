FROM python:3.9

WORKDIR /backend

# Skopiuj pliki projektu do katalogu roboczego
COPY . /backend
RUN pip install --no-cache-dir -r backend/requirements.txt

RUN apt-get update && apt-get install -y \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgl1-mesa-glx \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip install opencv-python torch torchvision fitz pymupdf frontend tools plotly

RUN python backend/blizniaki_app/manage.py migrate

EXPOSE 8000

CMD ["python", "backend/blizniaki_app/manage.py", "runserver", "0.0.0.0:8000"]