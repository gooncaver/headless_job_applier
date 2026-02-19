"""Resume customization engine for tailoring templates to job descriptions"""

from pathlib import Path
from typing import Optional, Dict
from loguru import logger
from .template_manager import template_manager


class ResumeCustomizer:
    """Handle resume customization and PDF generation"""

    def __init__(self, output_dir: str = "output/resumes"):
        """Initialize resume customizer

        Args:
            output_dir: Directory to store customized resumes
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Initialized ResumeCustomizer with output directory: {self.output_dir}")

    def select_template_for_job(
        self,
        job_title: str,
        job_description: str = "",
        user_preference: Optional[str] = None
    ) -> str:
        """Select appropriate resume template for a job

        Args:
            job_title: Job title to match
            job_description: Job description for keyword matching
            user_preference: User-specified template (overrides recommendations)

        Returns:
            Selected template filename
        """
        if user_preference:
            logger.info(f"Using user-preferred template: {user_preference}")
            if template_manager.validate_template(user_preference):
                return user_preference
            else:
                logger.warning(f"User template invalid, falling back to recommendations")

        # Get top recommendation
        recommendations = template_manager.recommend_templates(job_title, job_description, top_n=1)
        if recommendations:
            selected = recommendations[0].filename
            logger.info(f"Selected template: {selected} for job '{job_title}'")
            return selected

        # Fallback to first available template
        templates = list(template_manager.list_templates().keys())
        logger.warning(f"No strong match found, using fallback template: {templates[0]}")
        return templates[0]

    def generate_output_path(self, company: str, job_title: str, template_name: str) -> Path:
        """Generate output path for customized resume

        Args:
            company: Company name
            job_title: Job title
            template_name: Template filename (without extension)

        Returns:
            Path to output file
        """
        # Extract template name without extension: resume_consultant.md -> consultant
        template_type = template_name.replace("resume_", "").replace(".md", "")

        # Create company-specific directory
        company_dir = self.output_dir / company.replace(" ", "_").lower()
        company_dir.mkdir(parents=True, exist_ok=True)

        # Filename: {company}_{job_title}_{template_type}.md
        safe_title = job_title.replace(" ", "_").replace("/", "_").lower()
        output_filename = f"{safe_title}_{template_type}.md"
        output_path = company_dir / output_filename

        logger.debug(f"Generated output path: {output_path}")
        return output_path

    def load_template_for_customization(self, template_name: str) -> str:
        """Load template content for customization

        Args:
            template_name: Template filename

        Returns:
            Template content

        Raises:
            FileNotFoundError: If template not found
        """
        return template_manager.load_template(template_name)

    def customize_resume(
        self,
        template_name: str,
        job_title: str,
        job_description: str,
        company: str,
        company_info: Optional[Dict] = None,
        dry_run: bool = False
    ) -> Dict:
        """Prepare resume for customization (Phase 2)

        This is a placeholder for Phase 2 resume customization using AI.
        Currently just validates inputs and prepares metadata.

        Args:
            template_name: Resume template to use
            job_title: Target job title
            job_description: Job description to tailor to
            company: Company name
            company_info: Optional company metadata
            dry_run: If True, don't write files

        Returns:
            Dictionary with customization metadata and paths
        """
        logger.info(f"Customizing resume for {company} - {job_title}")

        # Load template
        template_content = self.load_template_for_customization(template_name)

        # Generate output paths
        output_path = self.generate_output_path(company, job_title, template_name)

        result = {
            "template_name": template_name,
            "template_content": template_content,
            "job_title": job_title,
            "job_description": job_description,
            "company": company,
            "output_path": str(output_path),
            "status": "ready_for_ai_processing",  # Will be processed in Phase 2
        }

        if company_info:
            result["company_info"] = company_info

        if not dry_run:
            logger.info(f"Customization prepared: {output_path}")

        return result

    def get_template_for_application(self, application_id: int, template_name: Optional[str] = None) -> str:
        """Get template content for a specific application

        Args:
            application_id: Application ID
            template_name: Optional specific template name

        Returns:
            Template content
        """
        if template_name:
            return self.load_template_for_customization(template_name)

        # Default to latest template if not specified
        templates = list(template_manager.list_templates().keys())
        default_template = templates[0]
        logger.debug(f"Using default template for application {application_id}: {default_template}")
        return self.load_template_for_customization(default_template)


# Global instance
customizer = ResumeCustomizer()
