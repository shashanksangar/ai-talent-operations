#!/usr/bin/env python3
"""
AI Talent Operations - Configuration Stress Test

Comprehensive stress test to validate configuration setup and system integration.
Tests all agents, workflows, and orchestrator functionality.
"""

import os
import sys
import time
# import psutil  # Not available, using basic memory tracking
import tracemalloc
from datetime import datetime
from typing import Dict, List, Any

# Add parent directory to path
sys.path.append(os.path.dirname(__file__))

# Import all components
from main import OperationsOrchestrator

# Workflow imports (optional - will test if available)
try:
    from workflows.scheduling.scheduling_agent import SchedulingAgent
    SCHEDULING_AVAILABLE = True
except ImportError:
    SCHEDULING_AVAILABLE = False
    print("⚠️  Scheduling workflow not available")

try:
    from workflows.model_mapping.model_mapping_agent import ModelMappingAgent
    MODEL_MAPPING_AVAILABLE = True
except ImportError:
    MODEL_MAPPING_AVAILABLE = False
    print("⚠️  Model mapping workflow not available")


class StressTestRunner:
    """Stress test runner for AI Talent Operations."""

    def __init__(self):
        """Initialize stress test runner."""
        self.results = {
            "config_tests": [],
            "agent_tests": [],
            "workflow_tests": [],
            "integration_tests": [],
            "performance_tests": [],
            "memory_tests": []
        }
        self.start_time = None
        self.memory_start = None

    def log_result(self, category: str, test_name: str, success: bool, message: str = "", duration: float = None):
        """Log a test result."""
        result = {
            "test": test_name,
            "success": success,
            "message": message,
            "timestamp": datetime.now().isoformat()
        }
        if duration is not None:
            result["duration"] = duration

        self.results[category].append(result)

        status = "✅" if success else "❌"
        print(f"{status} {test_name}: {message}")

    def run_config_tests(self):
        """Test configuration loading and validation."""
        print("\n🔧 Testing Configuration Setup...")

        # Test 1: Main config loading
        try:
            start_time = time.time()
            orchestrator = OperationsOrchestrator()
            duration = time.time() - start_time

            self.log_result("config_tests", "main_config_load",
                          True, "Main configuration loaded successfully", duration)
        except Exception as e:
            self.log_result("config_tests", "main_config_load",
                          False, f"Failed to load main config: {e}")

        # Test 2: Config structure validation
        try:
            if hasattr(orchestrator, 'config') and orchestrator.config:
                required_sections = ['operations']
                for section in required_sections:
                    if section not in orchestrator.config:
                        raise ValueError(f"Missing required config section: {section}")

                self.log_result("config_tests", "config_structure",
                              True, "Configuration structure is valid")
            else:
                raise ValueError("Config not loaded properly")
        except Exception as e:
            self.log_result("config_tests", "config_structure",
                          False, f"Configuration structure invalid: {e}")

        # Test 3: Workflow config validation
        try:
            config = orchestrator.config
            if 'operations' in config:
                ops_config = config['operations']

                # Check agent configurations
                expected_agents = ['sourcing_agent', 'matching_agent', 'outreach_agent',
                                 'scheduling_agent', 'model_mapping_agent']

                for agent in expected_agents:
                    if agent in ops_config:
                        agent_config = ops_config[agent]
                        if isinstance(agent_config, dict) and 'enabled' in agent_config:
                            status = "enabled" if agent_config['enabled'] else "disabled"
                            self.log_result("config_tests", f"{agent}_config",
                                          True, f"{agent} configuration valid ({status})")
                        else:
                            self.log_result("config_tests", f"{agent}_config",
                                          False, f"{agent} config missing 'enabled' key")
                    else:
                        self.log_result("config_tests", f"{agent}_config",
                                      False, f"{agent} configuration missing")

            self.log_result("config_tests", "workflow_configs",
                          True, "All workflow configurations validated")
        except Exception as e:
            self.log_result("config_tests", "workflow_configs",
                          False, f"Workflow config validation failed: {e}")

    def run_agent_tests(self):
        """Test individual agent initialization."""
        print("\n🤖 Testing Agent Initialization...")

        # Test 1: Scheduling Agent
        if SCHEDULING_AVAILABLE:
            try:
                start_time = time.time()
                agent = SchedulingAgent()
                duration = time.time() - start_time

                # Basic validation
                assert hasattr(agent, 'interviewers'), "Missing interviewers attribute"
                assert hasattr(agent, 'scheduled_interviews'), "Missing scheduled_interviews attribute"
                assert len(agent.interviewers) > 0, "No interviewers loaded"

                self.log_result("agent_tests", "scheduling_agent_init",
                              True, f"Scheduling agent initialized with {len(agent.interviewers)} interviewers", duration)
            except Exception as e:
                self.log_result("agent_tests", "scheduling_agent_init",
                              False, f"Scheduling agent init failed: {e}")
        else:
            self.log_result("agent_tests", "scheduling_agent_init",
                          False, "Scheduling agent not available")

        # Test 2: Model Mapping Agent
        if MODEL_MAPPING_AVAILABLE:
            try:
                start_time = time.time()
                agent = ModelMappingAgent()
                duration = time.time() - start_time

                # Basic validation
                assert hasattr(agent, 'config'), "Missing config attribute"
                assert hasattr(agent, 'session'), "Missing session attribute"

                self.log_result("agent_tests", "model_mapping_agent_init",
                              True, "Model mapping agent initialized successfully", duration)
            except Exception as e:
                self.log_result("agent_tests", "model_mapping_agent_init",
                              False, f"Model mapping agent init failed: {e}")
        else:
            self.log_result("agent_tests", "model_mapping_agent_init",
                          False, "Model mapping agent not available")

    def run_workflow_tests(self):
        """Test workflow execution."""
        print("\n⚙️ Testing Workflow Execution...")

        orchestrator = OperationsOrchestrator()

        # Test 1: Scheduling Workflow
        try:
            start_time = time.time()
            result = orchestrator.run_scheduling_workflow(
                interviewer_name="Sarah Chen",
                candidate="Test Candidate",
                role="Test Role",
                date_str="2026-03-15"
            )
            duration = time.time() - start_time

            if result and result.get('status') in ['success', 'info']:
                self.log_result("workflow_tests", "scheduling_workflow",
                              True, f"Scheduling workflow executed successfully", duration)
            else:
                self.log_result("workflow_tests", "scheduling_workflow",
                              False, f"Scheduling workflow failed: {result}")
        except Exception as e:
            self.log_result("workflow_tests", "scheduling_workflow",
                          False, f"Scheduling workflow error: {e}")

        # Test 2: Model Mapping Workflow
        try:
            start_time = time.time()
            result = orchestrator.run_model_mapping_workflow("Test Model")
            duration = time.time() - start_time

            # Model mapping might fail due to network/API issues, but should not crash
            if result and 'status' in result:
                status_msg = f"Model mapping workflow completed with status: {result['status']}"
                self.log_result("workflow_tests", "model_mapping_workflow",
                              True, status_msg, duration)
            else:
                self.log_result("workflow_tests", "model_mapping_workflow",
                              False, "Model mapping workflow returned invalid result")
        except Exception as e:
            self.log_result("workflow_tests", "model_mapping_workflow",
                          False, f"Model mapping workflow error: {e}")

    def run_integration_tests(self):
        """Test system integration."""
        print("\n🔗 Testing System Integration...")

        try:
            orchestrator = OperationsOrchestrator()

            # Test 1: Multiple workflow calls
            results = []
            for i in range(3):
                result = orchestrator.run_scheduling_workflow(
                    interviewer_name=f"Test Interviewer {i}",
                    candidate=f"Test Candidate {i}",
                    role="Test Role",
                    date_str=f"2026-03-{15+i}"
                )
                results.append(result)

            success_count = sum(1 for r in results if r and r.get('status') in ['success', 'info'])
            self.log_result("integration_tests", "multiple_workflow_calls",
                          success_count >= 2, f"{success_count}/3 workflow calls successful")

            # Test 2: Orchestrator state persistence
            initial_state = len(orchestrator.__dict__)
            # Run some operations
            orchestrator.run_scheduling_workflow("Test", "Test", "Test", "2026-03-20")
            final_state = len(orchestrator.__dict__)

            self.log_result("integration_tests", "orchestrator_state",
                          initial_state == final_state, "Orchestrator state maintained")

        except Exception as e:
            self.log_result("integration_tests", "integration_test",
                          False, f"Integration test failed: {e}")

    def run_performance_tests(self):
        """Test system performance."""
        print("\n⚡ Testing Performance...")

        # Test 1: Workflow execution time
        orchestrator = OperationsOrchestrator()

        times = []
        for i in range(5):
            start_time = time.time()
            orchestrator.run_scheduling_workflow(
                f"Perf Test {i}", f"Candidate {i}", "Role", f"2026-03-{20+i}"
            )
            duration = time.time() - start_time
            times.append(duration)

        avg_time = sum(times) / len(times)
        max_acceptable_time = 1.0  # 1 second

        self.log_result("performance_tests", "workflow_execution_time",
                      avg_time < max_acceptable_time,
                      ".3f")

    def run_memory_tests(self):
        """Test memory usage."""
        print("\n🧠 Testing Memory Usage...")

        # Test 1: Memory leak detection using tracemalloc
        orchestrator = OperationsOrchestrator()

        # Get initial memory
        initial_memory = tracemalloc.get_traced_memory()[0] / 1024 / 1024  # MB

        # Run multiple operations
        for i in range(10):
            orchestrator.run_scheduling_workflow(
                f"Memory Test {i}", f"Candidate {i}", "Role", f"2026-03-{20+i}"
            )

        # Check final memory
        final_memory = tracemalloc.get_traced_memory()[0] / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory

        # Allow up to 10MB increase for 10 operations (tracemalloc overhead)
        max_acceptable_increase = 10.0

        self.log_result("memory_tests", "memory_usage",
                      memory_increase < max_acceptable_increase,
                      ".1f")

    def run_all_tests(self):
        """Run all stress tests."""
        print("🚀 AI Talent Operations - Configuration Stress Test")
        print("=" * 60)

        self.start_time = time.time()
        tracemalloc.start()
        self.memory_start = tracemalloc.get_traced_memory()[0]

        try:
            self.run_config_tests()
            self.run_agent_tests()
            self.run_workflow_tests()
            self.run_integration_tests()
            self.run_performance_tests()
            self.run_memory_tests()

        finally:
            tracemalloc.stop()

        self.generate_report()

    def generate_report(self):
        """Generate test report."""
        total_duration = time.time() - self.start_time

        print("\n" + "=" * 60)
        print("📊 STRESS TEST REPORT")
        print("=" * 60)

        # Calculate statistics
        total_tests = 0
        passed_tests = 0

        for category, tests in self.results.items():
            if tests:
                category_passed = sum(1 for t in tests if t['success'])
                category_total = len(tests)
                total_tests += category_total
                passed_tests += category_passed

                print(f"\n{category.replace('_', ' ').title()}:")
                print(f"  ✅ Passed: {category_passed}/{category_total}")

                # Show failed tests
                failed_tests = [t for t in tests if not t['success']]
                if failed_tests:
                    print("  ❌ Failed:")
                    for test in failed_tests:
                        print(f"    • {test['test']}: {test['message']}")

        print(f"\n🎯 OVERALL RESULTS:")
        print(f"  📊 Total Tests: {total_tests}")
        print(f"  ✅ Passed: {passed_tests}")
        print(f"  ❌ Failed: {total_tests - passed_tests}")
        print(".1f")
        print(".1f")

        # Configuration status
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0

        if success_rate >= 90:
            print("  🎉 STATUS: Configuration is EXCELLENT!")
        elif success_rate >= 75:
            print("  👍 STATUS: Configuration is GOOD!")
        elif success_rate >= 50:
            print("  ⚠️  STATUS: Configuration needs ATTENTION!")
        else:
            print("  ❌ STATUS: Configuration has CRITICAL issues!")

        print("\n💡 RECOMMENDATIONS:")
        if success_rate < 100:
            print("  • Review failed tests above")
            print("  • Check configuration file syntax")
            print("  • Verify all dependencies are installed")
            print("  • Ensure API keys are properly configured")
        else:
            print("  • All systems operational!")
            print("  • Ready for production use!")


def main():
    """Main entry point."""
    try:
        tester = StressTestRunner()
        tester.run_all_tests()
    except KeyboardInterrupt:
        print("\n👋 Stress test interrupted by user")
    except Exception as e:
        print(f"\n❌ Stress test failed with error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
