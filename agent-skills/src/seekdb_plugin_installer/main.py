#!/usr/bin/env python3
"""Main entry point for seekdb plugin installer."""

import sys
import shutil
from pathlib import Path
from typing import Dict, List

try:
    import questionary
except ImportError:
    print("Error: questionary is not installed. Please install it with: pip install questionary")
    sys.exit(1)


# Tool configurations: tool name -> skills directory path
TOOL_CONFIGS: Dict[str, str] = {
    "Claude Code": ".claude/skills",
    "Cursor": ".cursor/skills",
    "Codex": ".codex/skills",
    "OpenCode": ".opencode/skills",
    "GitHub Copilot": ".github/skills",
    "Qoder": ".qoder/skills",
    "Trae": ".trae/skills"
}

# Available skills to install
AVAILABLE_SKILLS = [
    "seekdb",
    "importing-to-seekdb",
    "querying-from-seekdb",
]


def get_package_skills_dir() -> Path:
    package_dir = Path(__file__).parent
    # After installation: skills/ in package
    if (package_dir / "skills").exists():
        return package_dir / "skills"
    # During development: project root skills/ (package is in src/seekdb_plugin_installer/)
    root_skills = package_dir.parent.parent / "skills"
    if root_skills.exists():
        return root_skills
    raise FileNotFoundError("Skills directory not found")


def get_tool_skills_path(tool_name: str, project_root: Path) -> Path:
    """Get the full path to the skills directory for a given tool."""
    skills_dir_name = TOOL_CONFIGS.get(tool_name)
    if not skills_dir_name:
        raise ValueError(f"Unknown tool: {tool_name}")
    
    return project_root / skills_dir_name


def copy_skill(source_skill_dir: Path, target_skills_dir: Path, skill_name: str) -> bool:
    """Copy a skill directory to the target location."""
    target_skill_dir = target_skills_dir / skill_name
    
    try:
        # Remove existing skill if it exists
        if target_skill_dir.exists():
            shutil.rmtree(target_skill_dir)
        
        # Create parent directory if it doesn't exist
        target_skills_dir.mkdir(parents=True, exist_ok=True)
        
        # Copy the skill directory
        shutil.copytree(source_skill_dir, target_skill_dir)
        
        return True
    except Exception as e:
        print(f"Error copying skill {skill_name}: {e}")
        return False


def install_skills(tools: List[str], skills: List[str], project_root: Path) -> None:
    """Install selected skills to selected tools."""
    package_skills_dir = get_package_skills_dir()
    
    if not package_skills_dir.exists():
        print(f"Error: Skills directory not found at {package_skills_dir}")
        print("Please ensure the package is properly installed.")
        sys.exit(1)
    
    print(f"\n📦 Skills source: {package_skills_dir}")
    print(f"📁 Project root: {project_root}\n")
    
    for tool in tools:
        tool_skills_path = get_tool_skills_path(tool, project_root)
        print(f"🔧 Installing to {tool} ({tool_skills_path})...")
        
        for skill in skills:
            source_skill_dir = package_skills_dir / skill
            if not source_skill_dir.exists():
                print(f"  ⚠️  Skill '{skill}' not found, skipping...")
                continue
            
            if copy_skill(source_skill_dir, tool_skills_path, skill):
                print(f"  ✅ Installed '{skill}'")
            else:
                print(f"  ❌ Failed to install '{skill}'")
        
        print()


def main():
    """Main entry point for the installer."""
    try:
        print("🚀 seekdb Agent Skills Installer")
        print("=" * 50)
        
        # Find project root
        project_root = Path.cwd()
        print(f"📁 project root: {project_root}")
        
        # Ask user to confirm or change project root
        try:
            confirm_root = questionary.confirm(
                f"Install skills to this directory?",
                default=True
            ).ask()
        except KeyboardInterrupt:
            print("\n\nInstallation cancelled by user.")
            sys.exit(0)
        
        if not confirm_root:
            print("Installation cancelled.")
            sys.exit(0)
        
        # Select tools
        print("\n📋 Select tool to install to:")
        try:
            selected_tool = questionary.select(
                "Select one tool (use ↑↓ to navigate, Enter to confirm, Ctrl+C to cancel):",
                choices=list(TOOL_CONFIGS.keys())
            ).ask()
        except KeyboardInterrupt:
            print("\n\nInstallation cancelled by user.")
            sys.exit(0)
        
        if not selected_tool:
            print("No tool selected. Exiting.")
            sys.exit(0)
        selected_tools = [selected_tool]
        
        # Select skills
        print("\n📦 Select skills to install:")
        try:
            selected_skills = questionary.checkbox(
                "Select skills (use ↑↓ to navigate, Space to select, Enter to confirm, Ctrl+C to cancel):",
                choices=AVAILABLE_SKILLS,
                default="seekdb",  # Select all by default
                instruction="(Select multiple with Space)"
            ).ask()
        except KeyboardInterrupt:
            print("\n\nInstallation cancelled by user.")
            sys.exit(0)
        
        if not selected_skills:
            print("No skills selected. Exiting.")
            sys.exit(0)
        
        # Installation summary
        print("\n📝 Installation Summary:")
        print(f"  Tools: {', '.join(selected_tools)}")
        print(f"  Skills: {', '.join(selected_skills)}")
        print(f"  Project root: {project_root}")
        
        # Install skills
        install_skills(selected_tools, selected_skills, project_root)
        
        print("✨ Installation complete")
        print("\n💡 Please verify the skills are available in your tool's skill directory")
    except KeyboardInterrupt:
        print("\n\nInstallation cancelled by user.")
        sys.exit(0)

if __name__ == "__main__":
    main()
