# Passos para instalação

- Clonar o repositório
- Criar um ambiente virtual do Python (`python -m venv .venv`)
- Ative o ambiente virtual (`source .venv/bin/activate`)
- Instale os pacotes do repositório (`pip install -r requirements.txt`)
- Rode o migrate inicial (`python ./manage.py migrate`)
- Crie o usuário inicial (`python ./manage.py createsuperuser`)
- Rode o servidor (`python ./manage.py runserver`)