English | [简体中文](README_CN.md)  
# seekdb extension for cursor

Add seekdb database documentation to the `.cursor/rules` directory, enabling the Cursor AI assistant to understand seekdb database knowledge.

## Usage

### Add Documentation to Current Project

1. Open the command palette:
   - Windows/Linux: Press `Ctrl+Shift+P`
   - macOS: Press `Cmd+Shift+P`

2. Type and select the command:
   - Type "seekdb Docs" or "Add seekdb Docs"
   - Select the `Add seekdb Docs` command

3. The documentation will be automatically added to:
   - `.cursor/rules/seekdb-docs` directory (official documentation)
   - `.cursor/rules/seekdb.mdc` file (rule file)

### Remove Documentation from Current Project

1. Open the command palette (`Ctrl+Shift+P` or `Cmd+Shift+P`)

2. Type and select the command:
   - Type "Remove seekdb Docs"
   - Select the `Remove seekdb Docs` command

3. The documentation will be removed from:
   - `.cursor/rules/seekdb-docs` directory
   - `.cursor/rules/seekdb.mdc` file

## Working Modes

This extension supports **two working modes** with automatic fallback:

- **Remote Mode (Primary)**: Fetches documentation directly from GitHub Raw, always access the latest documentation
- **Local Mode (Fallback)**: Reads from local `.cursor/rules/seekdb-docs/` when GitHub is unreachable

The AI assistant detects network availability and switches modes seamlessly.

   
## Features

- Copy seekdb official documentation to the `.cursor/rules/seekdb-docs` directory in the current workspace
- Copy `seekdb.mdc` rule file to the `.cursor/rules` directory in the current workspace
- Support version management, only re-copy when documentation version is updated
- Support manual removal of copied documentation (removes both `.cursor/rules/seekdb-docs` and `.cursor/rules/seekdb.mdc`)



## Notes

- The extension does not automatically add documentation; you need to manually execute the command
- If the documentation already exists and the version is the same, it will skip adding

