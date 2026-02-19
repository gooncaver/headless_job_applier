"""Resume template management for multi-template support"""

from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass
from loguru import logger
import re


@dataclass
class ResumeTemplate:
    """Represents a resume template with metadata"""
    filename: str
    name: str
    target_roles: List[str]  # e.g., ["Consultant", "Strategic Advisor"]
    description: str
    keywords: List[str]  # Keywords to match against job descriptions
    priority: int = 0  # Higher priority templates are recommended first


class TemplateManager:
    """Manage multiple resume templates and recommend appropriate ones"""

    # Template registry: filename -> (name, roles, description, keywords)
    TEMPLATE_REGISTRY: Dict[str, ResumeTemplate] = {
        "resume_consultant.md": ResumeTemplate(
            filename="resume_consultant.md",
            name="Consultant resume",
            target_roles=["Consultant", "Manager", "Business Analyst", "Strategic Advisor"],
            description="Business-focused resume emphasizing consulting projects, client engagement, and strategic initiatives",
            keywords=["consulting", "strategy", "client", "project management", "stakeholder", "business","advisory"],
            priority=3
        ),
        "resume_solution_architect.md": ResumeTemplate(
            filename="resume_solution_architect.md",
            name="Solution Architect resume",
            target_roles=["Solution Architect", "Enterprise Architect", "Tech Lead", "Senior Engineer"],
            description="Technical architecture-focused resume emphasizing system design, enterprise solutions, and technical leadership",
            keywords=["architecture", "system design", "enterprise", "solution", "infrastructure", "technical leadership"],
            priority=4
        ),
        "resume_data_engineer.md": ResumeTemplate(
            filename="resume_data_engineer.md",
            name="Data Engineer resume",
            target_roles=["Data Engineer", "Big Data Engineer", "ETL Developer", "Analytics Engineer"],
            description="Data-focused resume emphasizing data pipelines, big data technologies, and analytics infrastructure",
            keywords=["data engineer", "pipeline", "etl", "big data", "spark", "hadoop", "analytics", "data warehouse"],
            priority=2
        ),
        "resume_fde.md": ResumeTemplate(
            filename="resume_fde.md",
            name="Full-Stack/Frontend Developer resume",
            target_roles=["Full Stack Developer", "Frontend Engineer", "Web Developer", "Software Engineer"],
            description="Development-focused resume emphasizing full-stack capabilities, frontend frameworks, and application development",
            keywords=["developer", "frontend", "backend", "full-stack", "web", "react", "node", "typescript", "javascript"],
            priority=1
        ),
    }

    def __init__(self, input_dir: str = "input"):
        """Initialize template manager

        Args:
            input_dir: Path to input directory containing resume templates
        """
        self.input_dir = Path(input_dir)
        logger.info(f"Initializing TemplateManager with input directory: {self.input_dir}")

    def list_templates(self) -> Dict[str, ResumeTemplate]:
        """List all available resume templates

        Returns:
            Dictionary of template filename -> ResumeTemplate
        """
        return self.TEMPLATE_REGISTRY

    def get_template_path(self, template_name: str) -> Path:
        """Get full path to a template file

        Args:
            template_name: Template filename (e.g., 'resume_consultant.md')

        Returns:
            Full path to template file

        Raises:
            FileNotFoundError: If template doesn't exist
        """
        template_path = self.input_dir / template_name
        if not template_path.exists():
            raise FileNotFoundError(f"Template not found: {template_path}")
        logger.debug(f"Template path: {template_path}")
        return template_path

    def load_template(self, template_name: str) -> str:
        """Load template content

        Args:
            template_name: Template filename

        Returns:
            Template content as string

        Raises:
            FileNotFoundError: If template doesn't exist
        """
        template_path = self.get_template_path(template_name)
        try:
            content = template_path.read_text(encoding="utf-8")
            logger.info(f"Loaded template: {template_name} ({len(content)} bytes)")
            return content
        except Exception as e:
            logger.error(f"Failed to load template {template_name}: {e}")
            raise

    def recommend_templates(self, job_title: str, job_description: str = "", top_n: int = 3) -> List[ResumeTemplate]:
        """Recommend best matching templates based on job description

        Args:
            job_title: Job title from posting
            job_description: Job description text for keyword matching
            top_n: Number of recommendations to return

        Returns:
            List of ResumeTemplate sorted by match score (best first)
        """
        combined_text = f"{job_title} {job_description}".lower()
        recommendations = []

        for template in self.TEMPLATE_REGISTRY.values():
            score = 0

            # Check target roles (direct match in job title)
            for role in template.target_roles:
                if role.lower() in job_title.lower():
                    score += 10  # High priority for role match
                    break

            # Check keywords (match in description)
            keyword_matches = sum(1 for keyword in template.keywords if keyword in combined_text)
            score += keyword_matches * 2

            # Add template priority
            score += template.priority

            if score > 0:
                recommendations.append((template, score))

        # Sort by score descending and return top N
        recommendations.sort(key=lambda x: x[1], reverse=True)
        result = [template for template, _ in recommendations[:top_n]]

        logger.info(
            f"Recommended {len(result)} templates for job '{job_title}': "
            f"{[t.name for t in result]}"
        )
        return result

    def get_template_choice_prompt(self, job_title: str, job_description: str = "") -> str:
        """Generate user prompt for template selection with recommendations

        Args:
            job_title: Job title
            job_description: Job description

        Returns:
            Formatted prompt string for CLI display
        """
        recommendations = self.recommend_templates(job_title, job_description, top_n=2)

        prompt = f"\n📋 Recommended resume templates for '{job_title}':\n"

        for i, template in enumerate(recommendations, 1):
            prompt += f"\n{i}. {template.name}\n"
            prompt += f"   Target roles: {', '.join(template.target_roles)}\n"
            prompt += f"   {template.description}\n"

        # Add all available templates option
        prompt += f"\nAvailable templates:\n"
        for idx, (filename, template) in enumerate(self.TEMPLATE_REGISTRY.items(), 1):
            prompt += f"  {idx}. {template.name} ({filename})\n"

        return prompt

    def validate_template(self, template_name: str) -> bool:
        """Validate that a template exists and is readable

        Args:
            template_name: Template filename

        Returns:
            True if valid and readable, False otherwise
        """
        try:
            self.get_template_path(template_name)
            _ = self.load_template(template_name)
            return True
        except Exception as e:
            logger.warning(f"Template validation failed for {template_name}: {e}")
            return False

    def get_all_template_info(self) -> str:
        """Generate formatted info about all available templates

        Returns:
            Formatted string with template details
        """
        info = "\n📚 Available Resume Templates\n"
        info += "=" * 60 + "\n\n"

        for filename, template in sorted(self.TEMPLATE_REGISTRY.items()):
            info += f"📄 {template.name}\n"
            info += f"   File: {filename}\n"
            info += f"   Target Roles: {', '.join(template.target_roles)}\n"
            info += f"   Description: {template.description}\n"
            info += f"   Keywords: {', '.join(template.keywords)}\n"
            if template.priority:
                info += f"   Priority: {template.priority}\n"
            info += "\n"

        return info


# Global instance
template_manager = TemplateManager()
