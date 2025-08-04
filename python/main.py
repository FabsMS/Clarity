import sys
import os
import json
import io

# Garante encoding UTF-8 na saída padrão (Windows)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from agents import Create_Crew
from functions import MultiLanguageCodeAnalyzer  # ✅ Importa seu analisador inteligente

EXTENSIONS_PERMITIDAS = ('.py', '.js', '.ts', '.jsx', '.tsx', '.java')


def find_package_json_path(search_path):
    for root, dirs, files in os.walk(search_path):
        for d in ['node_modules', '.git', 'dist', 'build', '__pycache__']:
            if d in dirs:
                dirs.remove(d)
        if 'package.json' in files:
            return os.path.join(root, 'package.json')
    return None


def get_all_relevant_files(project_path):
    arquivos = []
    for root, dirs, files in os.walk(project_path):
        if any(x in root for x in ['node_modules', '.git', 'dist', 'build', '__pycache__']):
            continue
        for file in files:
            if file.endswith(EXTENSIONS_PERMITIDAS) and not file.startswith('test'):
                arquivos.append(os.path.join(root, file))
    return arquivos


if __name__ == "__main__":
    try:
        if len(sys.argv) > 1:
            project_path_arg = sys.argv[1]

            if not os.path.isdir(project_path_arg):
                raise FileNotFoundError(f"O caminho fornecido não é um diretório válido: {project_path_arg}")

            package_json_path = find_package_json_path(project_path_arg)
            actual_project_path = os.path.dirname(package_json_path) if package_json_path else project_path_arg

            arquivos_para_analisar = get_all_relevant_files(actual_project_path)

            if not arquivos_para_analisar:
                raise FileNotFoundError("Nenhum arquivo de código relevante encontrado para análise.")

            # ✅ Análise real do projeto com sua ferramenta
            analyzer = MultiLanguageCodeAnalyzer()
            analysis_result = analyzer.analyze_project(actual_project_path)
            resumo = analyzer.summarize_analysis(analysis_result)

            # ✅ Chamada ao agente com conteúdo útil
            crew_manager = Create_Crew()
            agent_result = crew_manager.generate_documentation(resumo)  # 🔄 Aqui o prompt foi alimentado com o resumo real

            # Determina o conteúdo do README com segurança
            if hasattr(agent_result, 'output'):
                readme_content = agent_result.output
            elif isinstance(agent_result, dict):
                readme_content = agent_result.get("output") or str(agent_result)
            elif hasattr(agent_result, "to_json"):
                readme_content = agent_result.to_json()
            elif hasattr(agent_result, "dict"):
                readme_content = agent_result.dict().get("result")
            else:
                readme_content = str(agent_result)

            if not readme_content:
                raise ValueError("O agente não conseguiu gerar o conteúdo do README.")

            readme_file_path = os.path.join(actual_project_path, 'README-CLARITY.md')
            with open(readme_file_path, 'w', encoding='utf-8') as f:
                f.write(readme_content)

            # ✅ Única saída padrão
            print(json.dumps({
                "success": True,
                "message": f"README gerado com sucesso em: {readme_file_path}",
                "readme_path": readme_file_path
            }))

        else:
            raise ValueError("Nenhum caminho de projeto foi fornecido como argumento.")

    except Exception as e:
        print(json.dumps({
            "error": "Erro ao executar o script.",
            "error_type": type(e).__name__,
            "error_message": str(e)
        }), file=sys.stderr)
        sys.exit(1)
