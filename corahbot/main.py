"""
Main entry point for the CorahBot
"""

import time
import signal
import sys
from typing import Optional
from airtest.core.api import auto_setup
from corahbot.config import DEVICE, STANDARD_PAUSE
from corahbot.logger import get_logger
from corahbot.templates import TemplateManager
from corahbot.actions import ActionHandler

log = get_logger(__name__)

class CorahBot:
    """Main bot class that handles the game automation"""
    
    def __init__(self):
        self.running = False
        self.template_manager = TemplateManager()
        self.action_handler = ActionHandler()
        self._setup_signal_handlers()
        
    def _setup_signal_handlers(self):
        """Set up handlers for graceful shutdown"""
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
    def _signal_handler(self, signum: int, frame):
        """Handle shutdown signals"""
        log.info(f"Received signal {signum}. Initiating graceful shutdown...")
        self.running = False
        
    def start(self):
        """Start the bot's main loop"""
        try:
            # Initialize Airtest and device connection
            auto_setup(__file__, devices=[DEVICE])
            log.info("Bot started, ADB connection established")
            
            # Verify templates are loaded
            if not self.template_manager.verify_all():
                log.error("Failed to verify all templates")
                return
                
            self.running = True
            self._main_loop()
            
        except Exception as e:
            log.exception(f"Critical error occurred: {str(e)}")
        finally:
            self._cleanup()
            
    def stop(self):
        """Stop the bot's main loop"""
        self.running = False
        
    def _main_loop(self):
        """Main bot logic loop"""
        log.info("Starting main loop")
        
        while self.running:
            try:
                # Check if we're in town
                if self.action_handler.verify_screen(self.template_manager, "town"):
                    log.info("Town screen detected")
                    if not self.action_handler.execute_sequence(self.template_manager, "town_sequence"):
                        log.warning("Town sequence failed, will retry")
                        time.sleep(STANDARD_PAUSE)
                        continue
                
                # Check if we're in combat
                elif self.action_handler.verify_screen(self.template_manager, "combat"):
                    if not self.action_handler.execute_sequence(self.template_manager, "combat"):
                        log.warning("Combat action failed, will retry")
                        time.sleep(STANDARD_PAUSE)
                        continue
                
                # If neither screen is detected, wait briefly
                else:
                    time.sleep(STANDARD_PAUSE)
                    
            except Exception as e:
                log.error(f"Error in main loop: {str(e)}")
                time.sleep(STANDARD_PAUSE)
                
    def _cleanup(self):
        """Perform cleanup operations"""
        log.info("Cleaning up and shutting down...")
        # Add any necessary cleanup code here
        
def main():
    """Entry point for the bot"""
    bot = CorahBot()
    try:
        bot.start()
    except KeyboardInterrupt:
        log.info("Keyboard interrupt received")
    except Exception as e:
        log.exception(f"Unexpected error: {str(e)}")
    finally:
        bot.stop()
        sys.exit(0)

if __name__ == "__main__":
    main()
