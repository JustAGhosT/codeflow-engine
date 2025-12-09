import * as assert from 'assert';
import * as vscode from 'vscode';

suite('Extension Test Suite', () => {
  vscode.window.showInformationMessage('Start all tests.');

  test('Extension should be present', () => {
    assert.ok(vscode.extensions.getExtension('codeflow'));
  });

  test('Should activate', async () => {
    const extension = vscode.extensions.getExtension('codeflow');
    if (extension) {
      await extension.activate();
      assert.ok(extension.isActive);
    }
  });

  test('Should register commands', async () => {
    const commands = await vscode.commands.getCommands();
    const codeflowCommands = commands.filter(cmd => cmd.startsWith('codeflow.'));
    
    assert.ok(codeflowCommands.includes('codeflow.qualityCheck'));
    assert.ok(codeflowCommands.includes('codeflow.qualityCheckFile'));
    assert.ok(codeflowCommands.includes('codeflow.qualityCheckWorkspace'));
    assert.ok(codeflowCommands.includes('codeflow.fileSplit'));
    assert.ok(codeflowCommands.includes('codeflow.autoFix'));
    assert.ok(codeflowCommands.includes('codeflow.showDashboard'));
    assert.ok(codeflowCommands.includes('codeflow.configure'));
  });

  test('Should have configuration', () => {
    const config = vscode.workspace.getConfiguration('codeflow');
    assert.ok(config.has('enabled'));
    assert.ok(config.has('qualityMode'));
    assert.ok(config.has('autoFixEnabled'));
    assert.ok(config.has('showNotifications'));
    assert.ok(config.has('pythonPath'));
    assert.ok(config.has('maxFileSize'));
  });
});
