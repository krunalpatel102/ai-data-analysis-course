# Use an official lightweight Python image.
FROM python:3.9-slim

# Set environment variables to make Python behave in a Docker container
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Install JupyterLab and any optional extensions like MyST-NB
RUN pip install jupyterlab jupyterlab_myst

# Copy the rest of your application's code
COPY . /app

# Expose port 8888 to access Jupyter
EXPOSE 8888

# Run JupyterLab
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--NotebookApp.token=''", "--allow-root"]
