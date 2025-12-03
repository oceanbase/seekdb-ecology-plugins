import * as vscode from 'vscode';
import * as fs from 'fs';
import * as path from 'path';

/**
 * Recursively copy directory
 */
async function copyDirectory(src: string, dest: string): Promise<void> {
    // Ensure destination directory exists
    if (!fs.existsSync(dest)) {
        fs.mkdirSync(dest, { recursive: true });
    }

    const entries = fs.readdirSync(src, { withFileTypes: true });

    for (const entry of entries) {
        const srcPath = path.join(src, entry.name);
        const destPath = path.join(dest, entry.name);

        if (entry.isDirectory()) {
            // Recursively copy subdirectories
            await copyDirectory(srcPath, destPath);
        } else {
            // Copy file
            fs.copyFileSync(srcPath, destPath);
        }
    }
}

/**
 * Recursively delete directory
 */
function deleteDirectory(dirPath: string): void {
    if (!fs.existsSync(dirPath)) {
        return;
    }

    const entries = fs.readdirSync(dirPath, { withFileTypes: true });

    for (const entry of entries) {
        const fullPath = path.join(dirPath, entry.name);
        if (entry.isDirectory()) {
            // Recursively delete subdirectories
            deleteDirectory(fullPath);
        } else {
            // Delete file
            fs.unlinkSync(fullPath);
        }
    }

    // Delete empty directory
    fs.rmdirSync(dirPath);
}

/**
 * Get extension version from package.json
 */
function getExtensionVersion(context: vscode.ExtensionContext): string | null {
    try {
        const packageJsonPath = path.join(context.extensionPath, 'package.json');
        if (!fs.existsSync(packageJsonPath)) {
            return null;
        }
        const packageJson = JSON.parse(fs.readFileSync(packageJsonPath, 'utf-8'));
        return packageJson.version || null;
    } catch (error) {
        console.error('Error reading package.json:', error);
        return null;
    }
}

/**
 * Read version from version file
 */
function readVersionFile(versionFilePath: string): string | null {
    try {
        if (!fs.existsSync(versionFilePath)) {
            return null;
        }
        return fs.readFileSync(versionFilePath, 'utf-8').trim();
    } catch (error) {
        console.error('Error reading version file:', error);
        return null;
    }
}

/**
 * Write version to version file
 */
function writeVersionFile(versionFilePath: string, version: string): void {
    try {
        const dir = path.dirname(versionFilePath);
        if (!fs.existsSync(dir)) {
            fs.mkdirSync(dir, { recursive: true });
        }
        fs.writeFileSync(versionFilePath, version, 'utf-8');
    } catch (error) {
        console.error('Error writing version file:', error);
    }
}

/**
 * Remove seekdb-docs from workspace .cursor/rules directory
 * Also remove seekdb.mdc from .cursor/rules directory
 * @param silent If true, don't show any UI messages (useful for uninstall)
 */
async function removeSeekdbDocsFromRules(silent: boolean = false) {
    try {
        // Get workspace root directory
        const workspaceFolders = vscode.workspace.workspaceFolders;
        if (!workspaceFolders || workspaceFolders.length === 0) {
            if (!silent) {
                vscode.window.showWarningMessage('No workspace folder is open');
            }
            return;
        }

        const workspaceRoot = workspaceFolders[0].uri.fsPath;
        const rulesDir = path.join(workspaceRoot, '.cursor', 'rules');
        const seekdbDocsTargetPath = path.join(rulesDir, 'seekdb-docs');
        const seekdbMdcTargetPath = path.join(rulesDir, 'seekdb.mdc');

        let removedItems = [];

        // Check and delete seekdb-docs directory
        if (fs.existsSync(seekdbDocsTargetPath)) {
            deleteDirectory(seekdbDocsTargetPath);
            removedItems.push('seekdb-docs from .cursor/rules');
            console.log(`Deleted directory: ${seekdbDocsTargetPath}`);
        }

        // Check and delete seekdb.mdc file
        if (fs.existsSync(seekdbMdcTargetPath)) {
            fs.unlinkSync(seekdbMdcTargetPath);
            removedItems.push('seekdb.mdc from .cursor/rules');
            console.log(`Deleted file: ${seekdbMdcTargetPath}`);
        }

        if (removedItems.length === 0) {
            if (!silent) {
                vscode.window.showInformationMessage('Seekdb documentation not found in .cursor/rules directory');
            }
            return;
        }

        if (!silent) {
            vscode.window.showInformationMessage(`Seekdb documentation successfully removed: ${removedItems.join(', ')}`);
        }
    } catch (error) {
        const errorMessage = error instanceof Error ? error.message : String(error);
        if (!silent) {
            vscode.window.showErrorMessage(`Error removing documentation: ${errorMessage}`);
        }
        console.error(`Error removing documentation: ${errorMessage}`);
    }
}

/**
 * Copy seekdb.mdc to workspace .cursor/rules directory
 */
async function copySeekdbMdcToRules(context: vscode.ExtensionContext) {
    try {
        // Get workspace root directory
        const workspaceFolders = vscode.workspace.workspaceFolders;
        if (!workspaceFolders || workspaceFolders.length === 0) {
            vscode.window.showWarningMessage('No workspace folder is open');
            return;
        }

        const workspaceRoot = workspaceFolders[0].uri.fsPath;
        const rulesDir = path.join(workspaceRoot, '.cursor', 'rules');

        // Get extension's seekdb.mdc file path
        const extensionPath = context.extensionPath;
        const seekdbMdcSourcePath = path.join(extensionPath, 'src', 'seekdb.mdc');
        const seekdbMdcTargetPath = path.join(rulesDir, 'seekdb.mdc');

        // Check if source file exists
        if (!fs.existsSync(seekdbMdcSourcePath)) {
            console.warn(`seekdb.mdc file not found: ${seekdbMdcSourcePath}`);
            return;
        }

        // Ensure destination directory exists
        if (!fs.existsSync(rulesDir)) {
            fs.mkdirSync(rulesDir, { recursive: true });
        }

        // Copy file
        fs.copyFileSync(seekdbMdcSourcePath, seekdbMdcTargetPath);
        
        console.log(`Copied seekdb.mdc from ${seekdbMdcSourcePath} to ${seekdbMdcTargetPath}`);
    } catch (error) {
        const errorMessage = error instanceof Error ? error.message : String(error);
        vscode.window.showErrorMessage(`Error copying seekdb.mdc: ${errorMessage}`);
        console.error('Error copying seekdb.mdc:', error);
    }
}

/**
 * Copy seekdb-docs to workspace .cursor/rules directory
 * Only copy when version is different or target directory does not exist
 */
async function copyOfficialDocsToRules(context: vscode.ExtensionContext) {
    try {
        // Get workspace root directory
        const workspaceFolders = vscode.workspace.workspaceFolders;
        if (!workspaceFolders || workspaceFolders.length === 0) {
            vscode.window.showWarningMessage('No workspace folder is open');
            return;
        }

        const workspaceRoot = workspaceFolders[0].uri.fsPath;
        const rulesDir = path.join(workspaceRoot, '.cursor', 'rules');

        // Get extension's seekdb-docs directory path
        const extensionPath = context.extensionPath;
        const seekdbDocsPath = path.join(extensionPath, 'src', 'seekdb-docs');

        // Check if source directory exists
        if (!fs.existsSync(seekdbDocsPath)) {
            console.warn(`seekdb-docs directory not found: ${seekdbDocsPath}`);
            return;
        }

        // Get current extension version
        const currentVersion = getExtensionVersion(context);
        if (!currentVersion) {
            console.warn('Unable to read extension version, skipping version check');
            // Fallback to old behavior: check if directory exists
            const seekdbDocsTargetPath = path.join(rulesDir, 'seekdb-docs');
            if (fs.existsSync(seekdbDocsTargetPath)) {
                console.log(`.cursor/rules/seekdb-docs already exists, skipping copy`);
                return;
            }
        } else {
            // Check version file
            const seekdbDocsTargetPath = path.join(rulesDir, 'seekdb-docs');
            const versionFilePath = path.join(seekdbDocsTargetPath, '.version');
            const existingVersion = readVersionFile(versionFilePath);

            // If version matches, skip copying
            if (existingVersion === currentVersion) {
                console.log(`.cursor/rules/seekdb-docs already exists with version ${currentVersion}, skipping copy`);
                return;
            }

            // If directory exists but version is different, delete it first
            if (fs.existsSync(seekdbDocsTargetPath)) {
                console.log(`Version mismatch (existing: ${existingVersion || 'unknown'}, current: ${currentVersion}), updating...`);
                deleteDirectory(seekdbDocsTargetPath);
            }
        }

        // Copy directory to seekdb-docs subdirectory
        const seekdbDocsTargetPath = path.join(rulesDir, 'seekdb-docs');
        await copyDirectory(seekdbDocsPath, seekdbDocsTargetPath);
        
        // Write version file after copying
        if (currentVersion) {
            const versionFilePath = path.join(seekdbDocsTargetPath, '.version');
            writeVersionFile(versionFilePath, currentVersion);
        }
        
        console.log(`Copied documentation from ${seekdbDocsPath} to ${seekdbDocsTargetPath}`);
        
        // Also copy seekdb.mdc to .cursor/rules directory
        await copySeekdbMdcToRules(context);
        
        // Prompt user to reload window to ensure rules are loaded
        const reloadAction = await vscode.window.showInformationMessage(
            'Seekdb documentation successfully added. Please reload the window to apply the changes.',
            'Reload Window'
        );
        if (reloadAction === 'Reload Window') {
            vscode.commands.executeCommand('workbench.action.reloadWindow');
        }
    } catch (error) {
        const errorMessage = error instanceof Error ? error.message : String(error);
        vscode.window.showErrorMessage(`Error copying documentation: ${errorMessage}`);
        console.error('Error copying documentation:', error);
    }
}

export function activate(context: vscode.ExtensionContext) {
    console.log('Seekdb Docs for Cursor extension is now active!');

    // Register command to copy documentation
    const copyCommand = vscode.commands.registerCommand('seekdb-docs.copyToRules', () => {
        copyOfficialDocsToRules(context);
    });
    context.subscriptions.push(copyCommand);

    // Register command to remove documentation
    const removeCommand = vscode.commands.registerCommand('seekdb-docs.removeFromRules', () => {
        removeSeekdbDocsFromRules();
    });
    context.subscriptions.push(removeCommand);
}

export async function deactivate() {
    // Note: We don't automatically cleanup files here because:
    // 1. deactivate() is called on window reload, which would incorrectly delete files
    // 2. Extension uninstall may not call deactivate()
    // Users can manually remove files using the 'seekdb-docs.removeFromRules' command if needed
}

