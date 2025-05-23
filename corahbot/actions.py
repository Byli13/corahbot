"""
Action handling for the bot
"""

import time
from typing import Optional
from airtest.core.api import exists, touch
from airtest.core.error import TargetNotFoundError
from corahbot.config import RETRY_LIMIT, STANDARD_PAUSE, LONG_PAUSE
from corahbot.logger import get_logger

log = get_logger(__name__)

class ActionHandler:
    """Handles all bot actions with retry logic and proper logging"""
    
    @staticmethod
    def safe_touch(template, pause: float = STANDARD_PAUSE, max_retries: int = RETRY_LIMIT) -> bool:
        """
        Safely attempt to touch a template on screen with retry logic
        
        Args:
            template: The Template object to look for and touch
            pause: Time to wait after successful touch
            max_retries: Maximum number of retry attempts
            
        Returns:
            bool: True if touch was successful, False otherwise
        """
        template_name = template.filename if hasattr(template, 'filename') else 'Unknown'
        
        for attempt in range(max_retries):
            if exists(template):
                try:
                    touch(template)
                    log.info(f"Successfully clicked on {template_name}")
                    time.sleep(pause)
                    return True
                except TargetNotFoundError:
                    log.warning(f"Touch failed for {template_name} - Attempt {attempt + 1}/{max_retries}")
            else:
                log.debug(f"Template {template_name} not found on screen - Attempt {attempt + 1}/{max_retries}")
            
            if attempt < max_retries - 1:  # Don't sleep after the last attempt
                time.sleep(0.2)  # Brief pause before retry
                
        log.error(f"Failed to touch {template_name} after {max_retries} attempts")
        return False

    def execute_sequence(self, template_manager, sequence_name: str) -> bool:
        """
        Execute a predefined sequence of actions
        
        Args:
            template_manager: Instance of TemplateManager
            sequence_name: Name of the sequence to execute
            
        Returns:
            bool: True if sequence completed successfully, False otherwise
        """
        if sequence_name == "town_sequence":
            log.info("Executing town sequence: Refill + Fight")
            
            # Define the sequence of actions with their respective pauses
            actions = [
                ("potion", STANDARD_PAUSE),
                ("max", STANDARD_PAUSE),
                ("refill", STANDARD_PAUSE),
                ("start", LONG_PAUSE),
                ("mob", STANDARD_PAUSE),
                ("attack", LONG_PAUSE)
            ]
            
            # Execute each action in sequence
            for template_key, pause in actions:
                template = template_manager.get(template_key)
                if template is None:
                    log.error(f"Missing template for {template_key}")
                    return False
                    
                if not self.safe_touch(template, pause=pause):
                    log.error(f"Town sequence failed at step: {template_key}")
                    return False
                    
            log.info("Town sequence completed successfully")
            return True
            
        elif sequence_name == "combat":
            template = template_manager.get("attack")
            if template is None:
                log.error("Missing attack template")
                return False
                
            return self.safe_touch(template, pause=0.3)
            
        else:
            log.error(f"Unknown sequence: {sequence_name}")
            return False

    def verify_screen(self, template_manager, screen_type: str) -> bool:
        """
        Verify if we're on a specific screen type
        
        Args:
            template_manager: Instance of TemplateManager
            screen_type: Type of screen to verify ('town' or 'combat')
            
        Returns:
            bool: True if we're on the specified screen, False otherwise
        """
        if screen_type == "town":
            return exists(template_manager.get("potion"))
        elif screen_type == "combat":
            return exists(template_manager.get("attack"))
        else:
            log.error(f"Unknown screen type: {screen_type}")
            return False
