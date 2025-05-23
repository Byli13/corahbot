"""
Template management for visual recognition
"""

import os
from typing import Dict, Optional
from airtest.core.api import Template
from corahbot.config import IMG_DIR, THRESH_DEFAULT, THRESH_ATTACK
from corahbot.logger import get_logger

log = get_logger(__name__)

class TemplateManager:
    """Manages the loading and access of image templates used for recognition"""
    
    def __init__(self):
        self.templates: Dict[str, Template] = {}
        self._load_templates()
    
    def _load_templates(self) -> None:
        """Load all template images with their respective thresholds"""
        templates_config = {
            "potion": ("potionrefill.png", THRESH_DEFAULT),
            "max": ("max.png", THRESH_DEFAULT),
            "refill": ("refill.png", THRESH_DEFAULT),
            "start": ("startadventure.png", THRESH_DEFAULT),
            "mob": ("mob.png", THRESH_DEFAULT),
            "attack": ("attack.png", THRESH_ATTACK),
        }
        
        for key, (filename, threshold) in templates_config.items():
            full_path = os.path.join(IMG_DIR, filename)
            if not os.path.exists(full_path):
                log.critical(f"Template image not found: {full_path}")
                raise FileNotFoundError(f"Template image missing: {filename}")
                
            try:
                self.templates[key] = Template(full_path, threshold=threshold)
                log.debug(f"Loaded template: {key} from {filename}")
            except Exception as e:
                log.error(f"Failed to load template {key}: {str(e)}")
                raise
    
    def get(self, key: str) -> Optional[Template]:
        """
        Retrieve a template by its key
        
        Args:
            key: The identifier for the template
            
        Returns:
            Template object if found, None otherwise
        """
        template = self.templates.get(key)
        if template is None:
            log.warning(f"Template not found: {key}")
        return template
    
    def verify_all(self) -> bool:
        """
        Verify that all required templates are loaded
        
        Returns:
            bool: True if all templates are loaded, False otherwise
        """
        return all(template is not None for template in self.templates.values())
