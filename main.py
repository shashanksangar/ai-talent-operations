"""
AI Talent Operations - Main orchestration module

This module provides the framework for operational efficiency workflows
combining multiple specialized AI agents for recruiting operations.
"""

import os
import yaml
import logging
import importlib.util
from datetime import datetime
from typing import Dict, List, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class OperationsOrchestrator:
    """
    Main orchestrator for AI Talent operations workflows.

    Manages the flow and integration of specialized agents:
    - Scheduling Agent: Interview coordination with thumb rules
    - Model Mapping Agent: AI model analysis and researcher profiling
    - Sourcing Agent: Candidate discovery
    - Matching Agent: Candidate-job matching
    - Outreach Agent: Automated communication
    """

    def __init__(self, config_path: str = "config.yaml"):
        """
        Initialize the Operations Orchestrator.

        Args:
            config_path: Path to the configuration YAML file
        """
        self.config = self._load_config(config_path)
        self.scheduling_enabled = self.config.get('operations', {}).get('scheduling_agent', {}).get('enabled', False)
        self.model_mapping_enabled = self.config.get('operations', {}).get('model_mapping_agent', {}).get('enabled', False)
        self.sourcing_enabled = self.config.get('operations', {}).get('sourcing_agent', {}).get('enabled', False)
        self.matching_enabled = self.config.get('operations', {}).get('matching_agent', {}).get('enabled', False)
        self.outreach_enabled = self.config.get('operations', {}).get('outreach_agent', {}).get('enabled', False)

        # Initialize agent modules (will be loaded dynamically)
        self.scheduling_agent = None
        self.model_mapping_agent = None

        logger.info("Operations Orchestrator initialized")

    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from YAML file."""
        if not os.path.exists(config_path):
            logger.error(f"Config file not found: {config_path}")
            return {}

        with open(config_path, 'r') as f:
            return yaml.safe_load(f)

    def _load_scheduling_agent(self):
        """Dynamically load the scheduling agent from separate repository."""
        if self.scheduling_agent is not None:
            return self.scheduling_agent

        try:
            # Try to import from local development path first
            scheduling_path = os.path.join(os.path.dirname(__file__), '..', 'ai-talent-scheduling-agent', 'scheduling_agent.py')
            if os.path.exists(scheduling_path):
                spec = importlib.util.spec_from_file_location("scheduling_agent", scheduling_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                self.scheduling_agent = module.SchedulingAgent()
                logger.info("Loaded scheduling agent from local path")
            else:
                # Try to import as installed package
                from ai_talent_scheduling_agent.scheduling_agent import SchedulingAgent
                self.scheduling_agent = SchedulingAgent()
                logger.info("Loaded scheduling agent from package")

        except ImportError as e:
            logger.error(f"Failed to load scheduling agent: {e}")
            raise ImportError("Scheduling agent not available. Please ensure ai-talent-scheduling-agent is installed or available locally.")

        return self.scheduling_agent

    def _load_model_mapping_agent(self):
        """Dynamically load the model mapping agent from separate repository."""
        if self.model_mapping_agent is not None:
            return self.model_mapping_agent

        try:
            # Try to import from local development path first
            mapping_path = os.path.join(os.path.dirname(__file__), '..', 'ai-talent-model-mapping-agent', 'model_mapping_agent.py')
            if os.path.exists(mapping_path):
                spec = importlib.util.spec_from_file_location("model_mapping_agent", mapping_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                self.model_mapping_agent = module.ModelMappingAgent()
                logger.info("Loaded model mapping agent from local path")
            else:
                # Try to import as installed package
                from ai_talent_model_mapping_agent.model_mapping_agent import ModelMappingAgent
                self.model_mapping_agent = ModelMappingAgent()
                logger.info("Loaded model mapping agent from package")

        except ImportError as e:
            logger.error(f"Failed to load model mapping agent: {e}")
            raise ImportError("Model mapping agent not available. Please ensure ai-talent-model-mapping-agent is installed or available locally.")

        return self.model_mapping_agent
    
    def run_sourcing_workflow(self, search_query: str) -> Optional[List[Dict]]:
        """
        Execute the sourcing workflow.
        
        Args:
            search_query: Query to search for candidates
            
        Returns:
            List of discovered candidates or None if disabled
        """
        if not self.sourcing_enabled:
            logger.warning("Sourcing Agent is not enabled")
            return None
        
        logger.info(f"Starting sourcing workflow with query: {search_query}")
        # Workflow implementation will be added with first project
        pass
    
    def run_matching_workflow(self, candidates: List[Dict], position: Dict) -> Optional[List[Dict]]:
        """
        Execute the matching workflow.
        
        Args:
            candidates: List of candidates to evaluate
            position: Position specification
            
        Returns:
            List of scored and ranked candidates or None if disabled
        """
        if not self.matching_enabled:
            logger.warning("Matching Agent is not enabled")
            return None
        
        logger.info(f"Starting matching workflow for {len(candidates)} candidates")
        # Workflow implementation will be added with first project
        pass
    
    def run_outreach_workflow(self, candidates: List[Dict], position: Dict) -> Optional[List[Dict]]:
        """
        Execute the outreach workflow.
        
        Args:
            candidates: List of candidates to reach out to
            position: Position specification
            
        Returns:
            List of generated messages or None if disabled
        """
        if not self.outreach_enabled:
            logger.warning("Outreach Agent is not enabled")
            return None
        
        logger.info(f"Starting outreach workflow for {len(candidates)} candidates")
        # Workflow implementation will be added with first project
        pass
    
    def run_scheduling_workflow(self, interviewer_name: str = None, candidate: str = None,
                               role: str = None, date_str: str = None) -> Optional[Dict]:
        """
        Execute the scheduling workflow.

        Args:
            interviewer_name: Name of interviewer (optional)
            candidate: Candidate name (optional)
            role: Role being interviewed for (optional)
            date_str: Interview date (optional)

        Returns:
            Scheduling results or None if workflow fails
        """
        if not self.scheduling_enabled:
            logger.warning("Scheduling Agent is not enabled")
            return {
                "status": "disabled",
                "message": "Scheduling agent is not enabled in configuration"
            }

        try:
            # Load scheduling agent dynamically
            agent = self._load_scheduling_agent()

            logger.info("Starting scheduling workflow")

            # If all parameters provided, attempt to schedule
            if all([interviewer_name, candidate, role, date_str]):
                success, message = agent.schedule_interview(
                    interviewer_name, candidate, role, date_str
                )

                if success:
                    logger.info(f"Scheduling successful: {message}")
                    return {
                        "status": "success",
                        "message": message,
                        "scheduled_interviews": len(agent.scheduled_interviews)
                    }
                else:
                    logger.error(f"Scheduling failed: {message}")
                    return {
                        "status": "failed",
                        "message": message
                    }

            # Otherwise, return availability information
            summary = agent.get_schedule_summary()
            available_today = agent.get_available_interviewers(
                datetime.now().strftime("%Y-%m-%d")
            )

            return {
                "status": "info",
                "summary": summary,
                "available_today": available_today
            }

        except Exception as e:
            logger.error(f"Scheduling workflow failed: {e}")
            return {
                "status": "error",
                "message": str(e)
            }
    
    def run_model_mapping_workflow(self, model_name: str) -> Optional[Dict]:
        """
        Execute the model mapping workflow.

        Args:
            model_name: Name of the AI model to map

        Returns:
            Model mapping results or None if workflow fails
        """
        if not self.model_mapping_enabled:
            logger.warning("Model Mapping Agent is not enabled")
            return {
                "status": "disabled",
                "message": "Model mapping agent is not enabled in configuration"
            }

        try:
            # Load model mapping agent dynamically
            agent = self._load_model_mapping_agent()

            logger.info(f"Starting model mapping workflow for: {model_name}")

            # Map the model
            result = agent.map_model(model_name)

            if result:
                # Save the mapping
                agent.save_mapping(result)

                logger.info(f"Model mapping successful: {model_name}")
                return {
                    "status": "success",
                    "model_name": result.name,
                    "technical_summary": result.technical_summary,
                    "paper_title": result.paper_title,
                    "authors_count": len(result.authors),
                    "first_author": result.authors[0].name if result.authors else None,
                    "categories": result.categories,
                    "paper_url": result.paper_url
                }
            else:
                logger.warning(f"Model mapping failed: {model_name}")
                return {
                    "status": "not_found",
                    "model_name": model_name,
                    "message": "Model not found in academic databases"
                }

        except Exception as e:
            logger.error(f"Model mapping workflow failed: {e}")
            return {
                "status": "error",
                "message": str(e)
            }
    
    def run_full_pipeline(self, search_query: str, position: Dict) -> Optional[Dict]:
        """
        Run the complete end-to-end pipeline.
        
        Flow: Sourcing → Matching → Outreach
        
        Args:
            search_query: Initial search query
            position: Target position specification
            
        Returns:
            Complete pipeline results or None if any step fails
        """
        logger.info("Starting full recruitment pipeline")
        
        # TODO: Implement full pipeline orchestration
        # 1. Source candidates
        # 2. Match candidates to position
        # 3. Generate outreach messages
        # 4. Export results
        
        pass


def main():
    """Entry point for operations orchestrator."""
    orchestrator = OperationsOrchestrator()
    logger.info("AI Talent Operations ready for workflow execution")


if __name__ == "__main__":
    main()
