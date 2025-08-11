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
- **Interface:** Aplicativo Web (FrameWord Django)

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

