# Sistema de Emissão de Folha de Ponto

## 📌 Descrição
O **Sistema de Emissão de Folha de Ponto** é uma aplicação desenvolvida na Liguagem Python conjuntamente com Framework Django e concebido para automatizar e simplificar o processo de emissão do folhas de ponto de servidores públicos.  


> 🆓 Este projeto é **público**. Use, modifique e adapte conforme a sua necessidade.

## 🚀 Funcionalidades
- Abandone o uso de malas diretas do MS Word.
- Cadastros Gerais: Carreiras, Funções, Áreas, Cargos, Servidores, Afastamentos e etc.
- Emissão da Folha de Ponto: Imprima direto ou Exporte para PDF, customização da Folha para Servidores afastados.
- Dashboard da Distribuição de Servidores por Careiras, Se Em PGD?, Se Afastado?, Tipo (Efetivo ou Contratato).

## 🛠️ Tecnologias Utilizadas
- **Linguagens:** Python, HTML, CSS e Javascript
- **Banco de Dados:** MySQL 
- **Interface:** Aplicativo Web (Framework Django)

## 📂 Estrutura do Projeto

folhadeponto/
├── controladores/ # Lógica e regras de negócio
├── utilitarios/ # Funções auxiliares
├── media/ # Arquivos enviados pelos usuários
├── migrations/ # Arquivos de migração do banco de dados
├── static/ # Arquivos estáticos (CSS, JS, imagens)
├── templates/ # Templates HTML
├── init.py
├── admin.py
├── apps.py
├── models.py
├── pipeline.py
├── signals.py
├── tests.py
├── urls.py
└── views.py

# View Login/Cadastro de Instituição
1. Login
<img width="1876" height="925" alt="image" src="https://github.com/user-attachments/assets/714a0786-b329-4d84-87a8-9c5eecf8372f" />
2. Cadastro de Instituição
<img width="1876" height="925" alt="image" src="https://github.com/user-attachments/assets/7afec24b-e949-45ed-9bc3-2d95f5e33954" />

# View Dashboard
<img width="1836" height="917" alt="image" src="https://github.com/user-attachments/assets/0d72b2a3-e4cf-4432-a4ba-7e1448262f2a" />

# View Servidores
<img width="1876" height="925" alt="image" src="https://github.com/user-attachments/assets/d7a42690-e040-4a51-8724-a766370e03b3" />

# View Folhas
1. Folhas de Ponto Criadas do Setor
<img width="1876" height="925" alt="image" src="https://github.com/user-attachments/assets/1e4207de-bd37-4f3c-860f-68f72bb760e6" />

2. Cria Folha de Ponto para o Setor
<img width="1876" height="925" alt="image" src="https://github.com/user-attachments/assets/b34db6e1-ce9b-4a49-83d0-383f296c8c6d" />

3. Impressão da Folha de Ponto
<img width="1918" height="1021" alt="image" src="https://github.com/user-attachments/assets/9bc445d7-1bf5-41f4-9df9-db16d02f6ab0" />

4. Folha de Ponto quando servidor está afastado
<img width="1915" height="954" alt="image" src="https://github.com/user-attachments/assets/1c4fa1b9-a7b4-4f90-a235-fae8c9a052d1" />




