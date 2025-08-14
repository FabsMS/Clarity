# Clarity

**Clarity** é uma extensão para **Visual Studio Code** desenvolvida com o propósito de analisar o código-fonte de um projeto e gerar documentação clara e estruturada, como um `README.md` completo, diretamente dentro do editor.

O objetivo é facilitar a compreensão do projeto, reduzir o tempo gasto com documentação manual e manter as informações sempre atualizadas.

---

## ✨ Como Funciona

1.  **Análise de Código:** Identifica os pontos-chave do projeto, como funções, classes, dependências e a estrutura geral.
2.  **Agente Inteligente:** Utiliza um agente em Python para processar e interpretar o código-fonte.
3.  **Geração de Documentação:** Emprega um segundo agente para redigir um `README.md` com base nas informações coletadas.
4.  **Integração com VS Code:** Permite executar a análise e gerar a documentação com poucos cliques ou atalhos.
5.  **Suporte a Linguagens:** Foco inicial em projetos **JavaScript/TypeScript/Python/Java**, com uma arquitetura expansível para outras linguagens.

---

## 🛠️ Tecnologias Utilizadas

* **Python:** Responsável pela lógica de análise do código e geração de conteúdo.
* **TypeScript/JavaScript (Node.js):** Implementa a interface da extensão e a integração com o VS Code.
* **APIs do Visual Studio Code:** Utilizadas para manipular o ambiente e interagir com os arquivos do usuário.

---

## 📋 Requisitos

Antes de começar, garanta que você possui:

* **[Python](https://www.python.org/downloads/)** instalado.
* **[Node.js](https://nodejs.org/en/)** (versão LTS recomendada).
* **[Visual Studio Code](https://code.visualstudio.com/)** instalado.

---

## 🚀 Como Rodar a Extensão

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/FabsMS/Clarity.git](https://github.com/FabsMS/Clarity.git)
    cd Clarity
    ```

2.  **Instale as dependências:**
    ```bash
    npm install
    ```

3.  **Execute em modo de desenvolvimento:**
    * Abra o projeto no **Visual Studio Code**.
    * Pressione `F5` para abrir uma nova janela do VS Code com a extensão **Clarity** ativa.
    * Na nova janela, use o atalho `Ctrl+Shift+P` (ou `Cmd+Shift+P` no macOS), procure por **"Gerar Documentação com Clarity"** e execute o comando.

---

## 📂 Estrutura do Repositório

```text
Clarity/
├── .vscode/                   # Configurações e scripts de desenvolvimento da extensão
├── python/                    # Código do agente de análise em Python
├── src/                       # Código-fonte da extensão (TypeScript/JavaScript)
├── .gitignore                 # Arquivos e diretórios ignorados pelo Git
├── CHANGELOG.md               # Registro de alterações
├── package.json               # Configurações do Node.js e dependências
├── README.md                  # Este arquivo
├── tsconfig.json              # Configuração do compilador TypeScript
└── vsc-extension-quickstart.md # Guia rápido do VS Code

---

## 📜 Resumo Rápido

| Item         | Descrição                                                       |
| :----------- | :-------------------------------------------------------------- |
| **Projeto** | Extensão para VS Code para geração automatizada de documentação |
| **Frontend** | VS Code com TypeScript/JavaScript (`src/`)                      |
| **Backend** | Agente em Python (`python/`)                                    |
| **Requisitos** | Python + Node.js                                                |
| **Execução** | `npm install` → Abrir no VS Code → Pressionar `F5`                |