# 1. Usa uma imagem oficial do Python, versão enxuta (slim) para ser leve
FROM python:3.10-slim

# 2. Define a pasta de trabalho dentro do contêiner
WORKDIR /app

# 3. Copia apenas o arquivo de requisitos primeiro (Otimização de cache do Docker)
COPY requirements.txt .

# 4. Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copia o código fonte para dentro do contêiner
# Nota: O arquivo .env e a pasta venv serão ignorados graças ao arquivo .dockerignore
COPY src/ ./src/

# 6. Comando padrão que será executado quando o contêiner ligar
CMD ["python", "-m", "src.main"]