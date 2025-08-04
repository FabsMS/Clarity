import * as vscode from 'vscode';
import { spawn } from 'child_process';
import * as path from 'path';

export function activate(context: vscode.ExtensionContext) {
	const disposable = vscode.commands.registerCommand('fabsms-clarity.generateDocumentation', async () => {
		const workspaceFolders = vscode.workspace.workspaceFolders;
		if (!workspaceFolders) {
			vscode.window.showErrorMessage('Nenhuma pasta aberta no VSCode.');
			return;
		}
		const projectPath = workspaceFolders[0].uri.fsPath;

		const pythonScript = path.join(context.extensionPath, 'python', 'main.py');
		const pythonPath = path.join(context.extensionPath, '.venv', 'Scripts', 'python.exe');

		await vscode.window.withProgress({
			location: vscode.ProgressLocation.Notification,
			title: "Gerando documentação. Aguarde...",
			cancellable: false
		}, async () => {
			return new Promise<void>((resolve, reject) => {
				console.log(`🔄 Executando script Python:\npython "${pythonScript}" "${projectPath}"`);

				const pythonProcess = spawn(pythonPath, [pythonScript, projectPath]);

				let stdout = '';
				let stderr = '';

				pythonProcess.stdout.on('data', (data) => {
					stdout += data.toString();
				});

				pythonProcess.stderr.on('data', (data) => {
					stderr += data.toString();
				});

				pythonProcess.on('error', (err) => {
					console.error('❌ ERRO AO INICIAR SCRIPT PYTHON');
					console.error(err);
					vscode.window.showErrorMessage(`Falha ao iniciar o script Python: ${err.message}`);
					reject();
				});

				pythonProcess.on('close', (code) => {
					if (code !== 0) {
						console.error('❌ ERRO AO EXECUTAR SCRIPT PYTHON');
						console.error(`Código de saída: ${code}`);
						console.error(stderr);
						vscode.window.showErrorMessage(`Erro ao executar script (código: ${code}). Veja o console para detalhes.`);
						return reject();
					}

					try {
						const matches = [...stdout.matchAll(/\{[\s\S]*?\}/g)];
						if (!matches || matches.length === 0) throw new Error("Nenhum JSON válido encontrado na saída do script Python.");

						// Usa o último JSON válido encontrado
						const result = JSON.parse(matches[matches.length - 1][0]);

						if (result.error) {
							vscode.window.showErrorMessage(result.error);
						} else if (result.success) {
							vscode.window.showInformationMessage(result.message, 'Abrir README')
								.then(selection => {
									if (selection === 'Abrir README') {
										const readmeUri = vscode.Uri.file(result.readme_path);
										vscode.workspace.openTextDocument(readmeUri).then(doc => {
											vscode.window.showTextDocument(doc);
										});
									}
								});
						}
						resolve();
					} catch (e) {
						console.error('--- ERRO AO PROCESSAR SAÍDA JSON DO PYTHON ---');
						console.error('Saída (stdout):', stdout);
						console.error('Erro de parsing:', e);
						vscode.window.showErrorMessage('Falha ao processar a resposta do script Python. Veja o Debug Console.');
						reject();
					}
				});
			});
		});
	});

	context.subscriptions.push(disposable);
}
