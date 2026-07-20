"""
Skills Registry for CoCo Agent Skills.
Parses SKILL.md files, loads frontmatter metadata, and binds skill handlers.
"""
import os
import re
import yaml
from typing import Dict, Any, List

class SkillsRegistry:
    def __init__(self, skills_dir: str = "skills"):
        self.skills_dir = skills_dir
        self.skills: Dict[str, Dict[str, Any]] = {}
        self.load_skills()

    def load_skills(self):
        """Scans skills directory and parses SKILL.md files."""
        if not os.path.exists(self.skills_dir):
            return

        for folder in os.listdir(self.skills_dir):
            folder_path = os.path.join(self.skills_dir, folder)
            skill_md_path = os.path.join(folder_path, "SKILL.md")
            
            if os.path.isdir(folder_path) and os.path.exists(skill_md_path):
                skill_info = self._parse_skill_md(skill_md_path)
                skill_info["path"] = folder_path
                self.skills[skill_info.get("name", folder)] = skill_info

    def _parse_skill_md(self, filepath: str) -> Dict[str, Any]:
        """Extracts YAML frontmatter and markdown body from SKILL.md."""
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        frontmatter_match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", content, re.DOTALL)
        if frontmatter_match:
            yaml_text = frontmatter_match.group(1)
            markdown_body = frontmatter_match.group(2)
            metadata = yaml.safe_load(yaml_text) or {}
            metadata["documentation"] = markdown_body.strip()
            return metadata
        else:
            return {"name": os.path.basename(os.path.dirname(filepath)), "documentation": content}

    def list_skills(self) -> List[Dict[str, Any]]:
        """Returns summary list of all registered skills."""
        return [
            {
                "name": name,
                "description": info.get("description", ""),
                "version": info.get("version", "1.0.0"),
                "category": info.get("category", "General"),
                "tags": info.get("tags", [])
            }
            for name, info in self.skills.items()
        ]

    def get_skill(self, name: str) -> Dict[str, Any]:
        return self.skills.get(name, {})

if __name__ == "__main__":
    registry = SkillsRegistry()
    print("Registered CoCo Skills:", registry.list_skills())
