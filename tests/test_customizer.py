"""Unit tests for resume template management and customization"""

import pytest
from pathlib import Path
from src.customizer.template_manager import TemplateManager, ResumeTemplate, template_manager
from src.customizer import ResumeCustomizer

# Create a test customizer instance
test_customizer = ResumeCustomizer(output_dir="tests/output/resumes")


class TestTemplateManager:
    """Test suite for TemplateManager"""

    def test_list_templates(self):
        """Test listing available templates"""
        templates = template_manager.list_templates()
        
        assert isinstance(templates, dict)
        assert len(templates) >= 4
        assert "resume_consultant.md" in templates
        assert "resume_solution_architect.md" in templates
        assert "resume_data_engineer.md" in templates
        assert "resume_fde.md" in templates

    def test_template_registry_structure(self):
        """Test that templates have required metadata"""
        templates = template_manager.list_templates()
        
        for filename, template in templates.items():
            assert isinstance(template, ResumeTemplate)
            assert template.filename == filename
            assert isinstance(template.name, str)
            assert isinstance(template.target_roles, list)
            assert len(template.target_roles) > 0
            assert isinstance(template.description, str)
            assert isinstance(template.keywords, list)
            assert len(template.keywords) > 0

    def test_recommend_templates_by_job_title(self):
        """Test template recommendations based on job title"""
        recommendations = template_manager.recommend_templates("Consultant", "")
        
        assert len(recommendations) > 0
        # Should recommend consultant template first
        assert "Consultant" in recommendations[0].target_roles

    def test_recommend_templates_by_keywords(self):
        """Test template recommendations based on job description keywords"""
        job_desc = "Big data pipeline development using Spark and Hadoop"
        recommendations = template_manager.recommend_templates("Engineer", job_desc)
        
        assert len(recommendations) > 0
        # Should recommend data engineer template
        assert "Data Engineer" in recommendations[0].target_roles

    def test_recommend_templates_full_stack(self):
        """Test template recommendations for full-stack developer"""
        job_desc = "Full-stack React and Node.js development, TypeScript experience required"
        recommendations = template_manager.recommend_templates("Developer", job_desc)
        
        assert len(recommendations) > 0
        # Should recommend full-stack/frontend template
        assert any("Frontend" in t.name or "Full Stack" in t.name for t in recommendations)

    def test_recommend_templates_ranking(self):
        """Test that templates are ranked by relevance"""
        recommendations = template_manager.recommend_templates(
            "Solution Architect",
            "Enterprise architecture design patterns microservices"
        )
        
        assert len(recommendations) >= 1
        # First should be most relevant
        assert "Solution Architect" in recommendations[0].target_roles

    def test_get_template_path(self):
        """Test getting template path"""
        path = template_manager.get_template_path("resume_consultant.md")
        
        assert isinstance(path, Path)
        # File should exist
        assert path.exists()

    def test_get_template_path_invalid(self):
        """Test that invalid template raises error"""
        with pytest.raises(FileNotFoundError):
            template_manager.get_template_path("nonexistent.md")

    def test_load_template(self):
        """Test loading template content"""
        content = template_manager.load_template("resume_consultant.md")
        
        assert isinstance(content, str)
        assert len(content) > 0
        # Should have markdown
        assert "#" in content or "*" in content

    def test_load_template_all(self):
        """Test loading all templates"""
        templates = template_manager.list_templates()
        
        for filename in templates.keys():
            content = template_manager.load_template(filename)
            assert len(content) > 0
            assert isinstance(content, str)

    def test_validate_template_valid(self):
        """Test template validation for valid template"""
        is_valid = template_manager.validate_template("resume_consultant.md")
        assert is_valid is True

    def test_validate_template_invalid(self):
        """Test template validation for invalid template"""
        is_valid = template_manager.validate_template("nonexistent.md")
        assert is_valid is False

    def test_get_all_template_info(self):
        """Test template info formatting"""
        info = template_manager.get_all_template_info()
        
        assert isinstance(info, str)
        assert "Consultant" in info
        assert "Solution Architect" in info
        assert "Data Engineer" in info


class TestResumeCustomizer:
    """Test suite for ResumeCustomizer"""

    def test_customizer_init(self):
        """Test customizer initialization"""
        customizer = ResumeCustomizer()
        
        assert customizer.output_dir.exists()
        assert customizer.output_dir.is_dir()

    def test_select_template_with_user_preference(self):
        """Test template selection with user preference"""
        selected = test_customizer.select_template_for_job(
            "Any Job",
            "",
            user_preference="resume_consultant.md"
        )
        
        assert selected == "resume_consultant.md"

    def test_select_template_consultant_role(self):
        """Test template selection for consultant role"""
        selected = test_customizer.select_template_for_job(
            "Management Consultant",
            "Lead consulting projects"
        )
        
        assert "consultant" in selected.lower()

    def test_select_template_architect_role(self):
        """Test template selection for architect role"""
        selected = test_customizer.select_template_for_job(
            "Solution Architect",
            "Design enterprise solutions with microservices"
        )
        
        assert "architect" in selected.lower()

    def test_select_template_data_role(self):
        """Test template selection for data engineer role"""
        selected = test_customizer.select_template_for_job(
            "Data Engineer",
            "Build data pipelines with Spark and Hadoop"
        )
        
        assert "data" in selected.lower()

    def test_generate_output_path(self):
        """Test output path generation"""
        path = test_customizer.generate_output_path(
            "Acme Corp",
            "Senior Engineer",
            "resume_consultant.md"
        )
        
        assert isinstance(path, Path)
        assert "acme_corp" in str(path).lower()
        assert "senior_engineer" in str(path).lower()
        assert path.parent.exists()

    def test_load_template_for_customization(self):
        """Test loading template for customization"""
        content = test_customizer.load_template_for_customization("resume_consultant.md")
        
        assert isinstance(content, str)
        assert len(content) > 0

    def test_customize_resume_dry_run(self):
        """Test resume customization in dry-run mode"""
        result = test_customizer.customize_resume(
            "resume_consultant.md",
            "Management Consultant",
            "Lead strategic initiatives",
            "Acme Corp",
            dry_run=True
        )
        
        assert isinstance(result, dict)
        assert result["template_name"] == "resume_consultant.md"
        assert result["job_title"] == "Management Consultant"
        assert result["company"] == "Acme Corp"
        assert result["status"] == "ready_for_ai_processing"
        assert "output_path" in result
        assert "template_content" in result

    def test_customize_resume_multiple_templates(self):
        """Test customization with different templates"""
        templates = template_manager.list_templates().keys()
        
        for template in templates:
            result = test_customizer.customize_resume(
                template,
                "Test Role",
                "Test description",
                "Test Company",
                dry_run=True
            )
            
            assert result["template_name"] == template
            assert "output_path" in result

    def test_get_template_for_application_specific(self):
        """Test getting template for specific application"""
        content = test_customizer.get_template_for_application(
            1,
            template_name="resume_consultant.md"
        )
        
        assert isinstance(content, str)
        assert len(content) > 0

    def test_get_template_for_application_default(self):
        """Test getting default template for application"""
        content = test_customizer.get_template_for_application(1)
        
        assert isinstance(content, str)
        assert len(content) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
