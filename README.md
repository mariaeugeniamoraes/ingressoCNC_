<p align="center"> <img src="docs/Nautico.png" alt="Banner Náutico Ingressos" width="100%"> </p> <h1 align="center">🎟️ Náutico Ingressos</h1> <p align="center"> <img src="https://img.shields.io/badge/HTML5-E34F26?logo=html5&logoColor=white" alt="HTML5"> <img src="https://img.shields.io/badge/CSS3-1572B6?logo=css3&logoColor=white" alt="CSS3"> <img src="https://img.shields.io/badge/JavaScript-F7DF1E?logo=javascript&logoColor=black" alt="JavaScript"> <img src="https://img.shields.io/badge/Django-092E20?logo=django&logoColor=white" alt="Django"> <img src="https://img.shields.io/badge/MySQL-4479A1?logo=mysql&logoColor=white" alt="MySQL"> </p>


# 🎟️ Náutico Ingressos

Sistema web para compra de ingressos dos jogos do **Clube Náutico Capibaribe**, desenvolvido como projeto pessoal.

> ⚠️ **Aviso:** este é um projeto pessoal e de estudo, sem qualquer vínculo oficial com o Clube Náutico Capibaribe. Nenhuma venda real é realizada.

---

## 📋 Sumário

- [Sobre o projeto](#-sobre-o-projeto)
- [Funcionalidades](#-funcionalidades)
- [Tecnologias](#-tecnologias)
- [Pré-requisitos](#-pré-requisitos)
- [Como rodar o projeto](#-como-rodar-o-projeto)
- [Estrutura de pastas](#-estrutura-de-pastas)
- [Capturas de tela](#-capturas-de-tela)
- [Próximos passos](#-próximos-passos)
- [Autor](#-autor)
- [Licença](#-licença)

---

## 💡 Sobre o projeto

O **Náutico Ingressos** simula uma plataforma de venda de ingressos para os jogos do Timbu nos Aflitos. O torcedor pode ver os próximos jogos, escolher o setor do estádio, selecionar a quantidade de ingressos e finalizar a compra.

O objetivo do projeto é praticar o desenvolvimento web completo (front-end, back-end e banco de dados) em um contexto real e divertido.

---

## ✨ Funcionalidades

- [x] Cadastro e login de usuários
- [x] Listagem dos próximos jogos
- [x] Escolha de setor e quantidade de ingressos
- [x] Carrinho de compras
- [ ] Pagamento simulado
- [ ] Histórico de compras do usuário
- [ ] Painel administrativo para cadastrar jogos e setores
- [ ] Geração de ingresso com QR Code

> Marque com `[x]` o que já está pronto e ajuste a lista conforme o projeto evoluir.

---

## 🛠️ Tecnologias

**Front-end**
- HTML5
- CSS3
- JavaScript

**Back-end**
- Python 3
- Django

**Banco de dados**
- MySQL

---

## ✅ Pré-requisitos

Antes de começar, você precisa ter instalado:

- [Python 3.10+](https://www.python.org/downloads/)
- [MySQL 8+](https://dev.mysql.com/downloads/)
- [Git](https://git-scm.com/)

---

## 🚀 Como rodar o projeto

```bash
# 1. Clone o repositório
git clone https://github.com/SEU-USUARIO/nautico-ingressos.git
cd nautico-ingressos

# 2. Crie e ative um ambiente virtual
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/macOS
source venv/bin/activate

# 3. Instale as dependências
pip install -r requirements.txt
```

**4. Crie o banco de dados no MySQL:**

```sql
CREATE DATABASE nautico_ingressos CHARACTER SET utf8mb4;
```

**5. Configure a conexão** no arquivo `settings.py` (ou em um arquivo `.env`):

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'nautico_ingressos',
        'USER': 'seu_usuario',
        'PASSWORD': 'sua_senha',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

```bash
# 6. Rode as migrações
python manage.py migrate

# 7. (Opcional) Crie um superusuário para acessar o admin
python manage.py createsuperuser

# 8. Inicie o servidor
python manage.py runserver
```

Acesse em: **http://127.0.0.1:8000/**

---

## 📁 Estrutura de pastas

```
nautico-ingressos/
├── manage.py
├── requirements.txt
├── README.md
├── nautico_ingressos/     # Configurações do projeto Django
│   ├── settings.py
│   └── urls.py
├── ingressos/             # App principal
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── templates/
└── static/
    ├── css/
    ├── js/
    └── img/
```

> Ajuste essa árvore para refletir a estrutura real do seu repositório.

---

## 🖼️ Capturas de tela

| Página inicial | Escolha de setor |
|:---:|:---:|
| ![Home](docs/home.png) | ![Setores](docs/setores.png) |

> Salve os prints em uma pasta `docs/` e atualize os caminhos acima.

---

## 🔭 Próximos passos

- Integração com um gateway de pagamento em modo de teste
- Envio de ingresso por e-mail
- Versão responsiva otimizada para celular
- Testes automatizados

---

## 👨‍💻 Autores

**Daniel Bezerra**
Estudante de Ciência da Computação na CESAR School


[![GitHub](https://github.com/DanielBezerraCNC)
[![LinkedIn](www.linkedin.com/in/danielsantanabezerra)


**Maria Eugênia**
[![GitHub](https://github.com/mariaeugeniamoraes)
[![LinkedIn](www.linkedin.com/in/maria-eugenia-moraes)


---

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

<p align="center">Feito com ❤️ para o maior do mundo!🔴⚪</p>
