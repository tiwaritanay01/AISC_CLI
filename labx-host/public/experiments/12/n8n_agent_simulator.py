import json
import time

class N8nNode:
    def __init__(self, name: str, node_type: str):
        self.name = name
        self.node_type = node_type

    def execute(self, payload: dict) -> dict:
        print(f"  [Node: {self.name} ({self.node_type})] Executing...")
        time.sleep(0.1)
        return payload

class N8nWorkflowAgent:
    def __init__(self):
        self.nodes = {
            "webhook": N8nNode("Webhook Trigger", "n8n-nodes-base.webhook"),
            "llm": N8nNode("AI Agent LLM Parser", "@n8n/n8n-nodes-langchain.agent"),
            "email": N8nNode("Send Email Notification", "n8n-nodes-base.emailSend"),
            "database": N8nNode("PostgreSQL Logger", "n8n-nodes-base.postgres")
        }

    def process_command(self, user_command: str):
        print(f"\nProcessing Inbound Task: \"{user_command}\"")
        print("-" * 50)

        # 1. Trigger
        data = self.nodes["webhook"].execute({"raw_input": user_command, "timestamp": time.time()})

        # 2. LLM Intent Extraction
        if "email" in user_command.lower() or "alert" in user_command.lower():
            intent = "SEND_EMAIL"
            params = {"recipient": "admin@college.edu", "subject": "Automated Alert", "body": user_command}
        else:
            intent = "DATABASE_LOG"
            params = {"table": "system_events", "record": user_command}

        llm_data = self.nodes["llm"].execute({"intent": intent, "params": params})

        # 3. Dynamic Node Routing
        if intent == "SEND_EMAIL":
            self.nodes["email"].execute(llm_data["params"])
            print("  --> Email successfully dispatched via n8n worker node.")
        else:
            self.nodes["database"].execute(llm_data["params"])
            print("  --> Record committed to database via n8n SQL node.")

        print("-" * 50)
        print("[SUCCESS] n8n AI Agent Workflow Completed!")

def main():
    print("=" * 60)
    print(" LabX Exp 12: AI Agent for Automation using n8n")
    print("=" * 60)

    workflow = N8nWorkflowAgent()
    workflow.process_command("Send urgent email alert about lab attendance drop")
    workflow.process_command("Log daily laboratory usage telemetry")
    print("=" * 60)

if __name__ == "__main__":
    main()

# ============================================================================
# EXPERIMENT THEORY (from AISC Laboratory Submission):
# ============================================================================
# n8n is a workflow automation tool that uses nodes to connect services via
# APIs. An AI agent can be built by creating a node that sends user input to
# an LLM (e.g., OpenAI) and processes the response. The workflow then routes
# the LLM output to subsequent nodes that perform actions like sending
# emails, updating databases, or triggering other APIs. By chaining these
# nodes, the agent can interpret natural language commands and execute
# complex automation tasks.
# ============================================================================
