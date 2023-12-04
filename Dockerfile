FROM python:3.9

WORKDIR /backend

COPY . /backend
RUN pip install --no-cache-dir -r backend/requirements.txt

RUN apt-get update && apt-get install -y \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgl1-mesa-glx \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir \
    opencv-python \
    torch \
    torchvision \
    pymupdf \
    frontend \
    tools \
    plotly
	
RUN python backend/blizniaki_app/manage.py migrate
	
RUN rm -rf /tmp/* /var/tmp/* /usr/share/man /usr/share/doc /usr/share/doc-base

EXPOSE 8000

CMD ["python", "backend/blizniaki_app/manage.py", "runserver", "0.0.0.0:8000"]
