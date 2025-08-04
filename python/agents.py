# Importações padrão
import os
from crewai import Agent, Task, Crew, Process
from functions import MultiLanguageCodeAnalyzer, ReadmeGeneratorTool
from dotenv import load_dotenv

# Carrega as variáveis do .env
load_dotenv()

# Importa LLM (Google Gemini via LiteLLM)
from langchain_community.chat_models import ChatLiteLLM

# Instancia o modelo Gemini com segurança
llm = ChatLiteLLM(
    model="gemini/gemini-1.5-flash-latest",
    temperature=0.7,
    api_key=os.getenv("GEMINI_API_KEY") 
)


class Create_Crew:
    def __init__(self):
        # Inicializa agentes e tarefas
        self.analyzer_agent = self.create_multi_language_analyzer_agent()
        self.writer_agent = self.create_readme_writer_agent()

        self.analysis_task = None  # será criado dinamicamente
        self.readme_task = None
        self.crew = None

    def create_multi_language_analyzer_agent(self):
        """Cria o agente responsável por analisar o código fonte"""
        analyzer_tool = MultiLanguageCodeAnalyzer()

        return Agent(
            role="Analista de Código Multilinguagem",
            goal="Analisar todos os arquivos de um projeto e extrair informações estruturadas",
            backstory="""Você é um especialista em análise de código com domínio em várias linguagens.
            Sua missão é gerar uma visão abrangente da estrutura e lógica do sistema analisado.""",
            tools=[analyzer_tool],
            verbose=True,
            allow_delegation=False,
            llm=llm
        )

    def create_readme_writer_agent(self):
        """Cria o agente responsável por escrever o README"""
        readme_tool = ReadmeGeneratorTool()

        return Agent(
            role="Redator de Documentação",
            goal="Gerar um README técnico, completo, claro e bem formatado",
            backstory="""Você é um expert em documentação técnica. Sua missão é criar README.md 
            de altíssima qualidade com base na análise profunda do sistema.""",
            tools=[readme_tool],
            verbose=True,
            allow_delegation=False,
            llm=llm
        )

    def create_analysis_task(self, files: list):
        """Cria a tarefa de análise de múltiplos arquivos"""
        lista_formatada = '\n'.join(f"- `{path}`" for path in files)

        return Task(
            description=f"""
            Analise todos os arquivos abaixo e extraia uma visão global do projeto:

            **Arquivos para análise:**
            {lista_formatada}

            Para cada arquivo, extraia:
            1. Linguagem utilizada
            2. Classes, funções, objetos e hooks
            3. Relações entre módulos/componentes
            4. Arquivo(s) de entrada do sistema
            5. Frameworks e bibliotecas utilizados
            6. Padrões arquiteturais visíveis (ex: MVC, Hooks, Modular, Services)
            7. Responsabilidades dos arquivos e pastas
            8. Fluxo de dados e execução

            Gere um relatório unificado que sirva como base para documentação.
            """,
            expected_output="Relatório técnico detalhado e estruturado com base nos arquivos analisados",
            agent=self.analyzer_agent
        )

    def create_readme_task(self):
        """Cria a tarefa de geração do README a partir da análise"""
        return Task(
            description="""
            Com base na análise completa do sistema, gere um README.md profissional contendo:

            1. **Título e descrição geral**
            2. **Badges relevantes (linguagens, status)**
            3. **Índice**
            4. **Instalação e configuração**
            5. **Como usar (com exemplos ou comandos)**
            6. **Principais funcionalidades e componentes**
            7. **Estrutura de pastas e módulos**
            8. **Fluxo de execução ou arquitetura**
            9. **Contribuição e testes**
            10. **Licença**

            Use Markdown corretamente e adapte o conteúdo conforme o tipo do projeto detectado.
            Evite inventar qualquer dado: use apenas o que foi realmente analisado.
            """,
            expected_output="README.md em Markdown completo, técnico e claro",
            agent=self.writer_agent,
            context=[self.analysis_task]
        )

    def _create_crew(self):
        """Monta o Crew com as tarefas e agentes"""
        return Crew(
            agents=[self.analyzer_agent, self.writer_agent],
            tasks=[self.analysis_task, self.readme_task],
            process=Process.sequential,
            verbose=True,
            llm=llm
        )

    def generate_documentation(self, files: list) -> dict:
        """Gatilho principal: gera documentação a partir de vários arquivos"""
        self.analysis_task = self.create_analysis_task(files)
        self.readme_task = self.create_readme_task()
        self.crew = self._create_crew()

        # Executa o crew
        resultado = self.crew.kickoff()

        # Verifica se o resultado é CrewOutput e extrai a saída Markdown
        if hasattr(resultado, "output"):
            readme_markdown = resultado.output
        elif isinstance(resultado, dict):
            readme_markdown = resultado.get("result") or str(resultado)
        elif hasattr(resultado, "to_json"):
            readme_markdown = resultado.to_json()
        elif hasattr(resultado, "dict"):
            readme_markdown = resultado.dict().get("result")
        else:
            readme_markdown = str(resultado)

        return {
            "status": "success",
            "arquivos_analisados": files,
            "output": readme_markdown 
        }

