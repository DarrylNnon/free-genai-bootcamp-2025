 # 🚀 Day 22: Mastery Plan for MLOps & AI Infrastructure
 
 This guide goes beyond the initial overview. It provides a hands-on project for each core concept. Your goal is to build each one. By doing so, you will gain the practical experience needed to master, explain, and teach these technologies.
 
 ---
 
 ## 1. AWS Bedrock: The Intelligent SIEM Alert Enricher
 
 **Goal:** Move from simply calling a model to integrating it into a real-time security workflow. We will build a serverless function that automatically enriches security alerts.
 
 ### The Concept (To Explain)
 AWS Bedrock is a fully managed service that provides access to a variety of high-performing foundation models (FMs) through a single, unified API.
 *   **Why it matters:** It abstracts away the complexity of hosting and scaling models. You get a serverless, pay-per-use experience with built-in AWS security and integration (IAM, CloudTrail).
 *   **Architectural Choice:** Choose Bedrock when you want to leverage best-in-class proprietary (like Anthropic's Claude) or open-source models without managing any infrastructure. It's ideal for building model-agile applications where you can swap FMs with minimal code changes.
 
 ### The Mastery Project (To Implement)
 **Workflow:** AWS Security Hub Finding → Amazon EventBridge → AWS Lambda → **AWS Bedrock** → Slack Notification.
 
 1.  **Trigger:** An AWS Security Hub finding is generated (you can do this manually for testing).
 2.  **Routing:** An EventBridge rule is configured to listen for Security Hub findings and trigger a specific Lambda function.
 3.  **Enrichment (The Core Logic):** The Lambda function receives the finding's JSON data. It then calls Bedrock with a detailed prompt.
 4.  **Notification:** The Lambda takes the human-readable response from Bedrock and posts it to a Slack channel.
 
 ### Code Deep Dive (Lambda Function)
 
 ```python
 # enrich_security_finding.py
 import boto3
 import json
 import os
 import urllib3
 
 # Initialize clients outside the handler for performance
 bedrock_runtime = boto3.client(service_name='bedrock-runtime', region_name='us-east-1')
 SLACK_WEBHOOK_URL = os.environ['SLACK_WEBHOOK_URL']
 http = urllib3.PoolManager()
 
 def generate_enrichment_prompt(finding_json):
     """Creates a detailed prompt for the LLM."""
     return f"""
     You are a senior DevSecOps analyst. Your task is to analyze the following AWS Security Hub finding and provide a concise, actionable summary for a development team on Slack.
 
     The summary must include:
     1.  **What Happened:** A one-sentence summary of the finding.
     2.  **Business Risk:** Explain the potential impact in simple terms (e.g., "data exposure," "unauthorized access").
     3.  **Suggested Action:** A clear, concrete next step for the developer to take.
 
     Security Hub Finding:
     ```json
     {json.dumps(finding_json, indent=2)}
     ```
     """
 
 def lambda_handler(event, context):
     """Lambda handler to enrich a security finding and post to Slack."""
     try:
         finding = event['detail']['findings'][0]
         prompt = generate_enrichment_prompt(finding)
 
         # Bedrock API call (using Claude 3 Sonnet)
         payload = {
             "anthropic_version": "bedrock-2023-05-31",
             "max_tokens": 1024,
             "messages": [{"role": "user", "content": [{"type": "text", "text": prompt}]}]
         }
         
         response = bedrock_runtime.invoke_model(
             body=json.dumps(payload),
             modelId='anthropic.claude-3-sonnet-20240229-v1:0'
         )
         
         response_body = json.loads(response.get('body').read())
         enriched_text = response_body['content'][0]['text']
 
         # Post to Slack
         slack_message = {
             "text": f"🚨 New Security Finding: *{finding['Title']}*\n\n{enriched_text}"
         }
         
         encoded_msg = json.dumps(slack_message).encode('utf-8')
         resp = http.request('POST', SLACK_WEBHOOK_URL, body=encoded_msg)
         
         return {"statusCode": 200, "body": "Alert sent to Slack."}
 
     except Exception as e:
         print(f"Error: {e}")
         # Optionally, post error to a different Slack channel
         return {"statusCode": 500, "body": "An error occurred."}
 
 ```
 
 ### The Impact (To Teach)
 "Instead of just getting a raw JSON alert, developers get a clear, prioritized explanation of the risk and what to do next, right in Slack. This automates the first 15 minutes of a security analyst's job for every single alert, drastically reducing Mean Time to Acknowledgment (MTTA)."
 
 ---
 
 ## 2. SageMaker JumpStart: The Private PII & Secrets Scanner
 
 **Goal:** Deploy a private, open-source model and use it for a sensitive task that cannot leave your cloud environment: scanning proprietary code for secrets.
 
 ### The Concept (To Explain)
 SageMaker JumpStart is an accelerator for AWS's full ML platform, SageMaker. It lets you deploy pre-trained open-source models (like Llama, Mistral, CodeLlama) to a dedicated, private endpoint in your VPC with just a few clicks or lines of code.
 *   **Why it matters:** It gives you the privacy and security of a self-hosted model without the complexity of building custom Docker containers. Your data never leaves your environment to be processed by a third-party API.
 *   **Architectural Choice:** Choose JumpStart when data residency and privacy are paramount, or when you need to fine-tune an open-source model on your own private data to create a specialized expert model.
 
 ### The Mastery Project (To Implement)
 **Workflow:** Local Python Script → **SageMaker Endpoint (with CodeLlama)** → Analysis Result.
 
 1.  **Deployment (Setup):** Use a Python script with the SageMaker SDK to deploy a model like `huggingface-llm-codellama-7b` from JumpStart to a real-time endpoint.
 2.  **Scanning (Execution):** Create a command-line tool (`scan_file.py`) that takes a file path as an argument.
 3.  **Invocation:** The tool reads the file's content and invokes the private SageMaker endpoint with a prompt designed for secret detection.
 4.  **Cleanup:** The deployment script should also include a function to delete the endpoint to manage costs.
 
 ### Code Deep Dive (Deployment & Scanning Scripts)
 
 **`deploy_scanner.py` (Run this once to set up the infrastructure)**
 ```python
 from sagemaker.jumpstart.model import JumpStartModel
 
 def deploy_and_get_endpoint():
     """Deploys a CodeLlama model and returns the predictor object."""
     # This model is great for code-related tasks.
     model_id = "huggingface-llm-codellama-7b"
     model = JumpStartModel(model_id=model_id)
     
     # This can take 10-15 minutes as it provisions EC2 instances.
     predictor = model.deploy() 
     print(f"Endpoint '{predictor.endpoint_name}' deployed successfully.")
     return predictor
 
 def cleanup(predictor):
     """Deletes the SageMaker endpoint to stop incurring costs."""
     predictor.delete_endpoint()
     print(f"Endpoint '{predictor.endpoint_name}' deleted.")
 
 if __name__ == '__main__':
     # Example usage:
     predictor = deploy_and_get_endpoint()
     # ... keep the endpoint name to use in the scanner script ...
     print(f"Endpoint Name: {predictor.endpoint_name}")
     # To clean up:
     # from sagemaker.predictor import Predictor
     # predictor_to_delete = Predictor("endpoint-name-from-above")
     # cleanup(predictor_to_delete)
 ```
 
 **`scan_file.py` (The actual tool)**
 ```python
 import boto3
 import json
 import sys
 
 # You would get this from the output of the deployment script
 ENDPOINT_NAME = "your-sagemaker-endpoint-name" 
 sagemaker_runtime = boto3.client("sagemaker-runtime")
 
 def scan_for_secrets(file_content):
     """Invokes the SageMaker endpoint to scan for secrets."""
     prompt = f"""
     Analyze the following code snippet. Does it contain any secrets like API keys, private keys, or passwords?
     Answer with a JSON object containing two keys: "has_secret" (boolean) and "explanation" (string).
 
     Code:
     ```
     {file_content}
     ```
     """
     payload = {"inputs": prompt, "parameters": {"max_new_tokens": 200}}
     
     response = sagemaker_runtime.invoke_endpoint(
         EndpointName=ENDPOINT_NAME,
         ContentType="application/json",
         Body=json.dumps(payload),
     )
     
     result = json.loads(response["Body"].read().decode())
     # The actual output structure can vary by model, inspect it first.
     return result[0]['generated_text']
 
 if __name__ == "__main__":
     if len(sys.argv) != 2:
         print("Usage: python scan_file.py <path_to_file>")
         sys.exit(1)
     
     file_path = sys.argv[1]
     with open(file_path, 'r') as f:
         content = f.read()
     
     analysis = scan_for_secrets(content)
     print("--- Scan Result ---")
     print(analysis)
 ```
 
 ### The Impact (To Teach)
 "We've built a security tool that can be safely run on our most sensitive internal source code. By hosting the model ourselves with JumpStart, we get powerful AI analysis with the guarantee that our proprietary data never leaves our AWS account. This is how you build AI tools for high-trust environments."
 
 ---
 
 ## 3. LangChain: The CVE Explainer with Live Web Context
 
 **Goal:** Go beyond a simple prompt-and-response. Build a multi-step "chain" that fetches live data from the web to answer a question, demonstrating Retrieval-Augmented Generation (RAG).
 
 ### The Concept (To Explain)
 LangChain is an open-source framework for building applications with LLMs. It provides standardized components (Prompts, Models, Retrievers, Output Parsers) and a way to "chain" them together into complex workflows using the LangChain Expression Language (LCEL `|`).
 *   **Why it matters:** It provides the "plumbing" for LLM applications. Instead of writing boilerplate code to connect your LLM to a vector database or a search API, you use LangChain's standard interfaces. This makes your code more modular, readable, and maintainable.
 *   **Architectural Choice:** Use LangChain when your application requires more than a single LLM call. It excels at RAG, agentic workflows (tool use), and managing conversational memory.
 
 ### The Mastery Project (To Implement)
 **Workflow:** User Input (CVE ID) → **LangChain Chain (Search → Load → Split → Store → Retrieve → Generate)** → Final Answer.
 
 1.  **Tool Use:** The chain will first use a search tool (like Tavily Search) to find relevant URLs for the given CVE.
 2.  **RAG Pipeline:** It will then load the content from those URLs, split it into chunks, embed them, and store them in a temporary in-memory vector store (FAISS).
 3.  **Generation:** Finally, it will use the user's original question to retrieve the most relevant chunks from the vector store and pass them to an LLM to generate a final, context-aware answer.
 
 ### Code Deep Dive (Runnable Python Script)
 
 ```python
 # cve_explainer.py
 # pip install langchain langchain-openai langchain-community beautifulsoup4 faiss-cpu tavily-python
 import os
 from langchain_openai import ChatOpenAI, OpenAIEmbeddings
 from langchain_community.document_loaders import WebBaseLoader
 from langchain_community.vectorstores import FAISS
 from langchain_text_splitters import RecursiveCharacterTextSplitter
 from langchain.chains import create_retrieval_chain
 from langchain.chains.combine_documents import create_stuff_documents_chain
 from langchain_core.prompts import ChatPromptTemplate
 from langchain_community.tools.tavily_search import TavilySearchResults
 
 # Set API keys
 os.environ["OPENAI_API_KEY"] = "sk-..."
 os.environ["TAVILY_API_KEY"] = "tvly-..."
 
 # 1. Set up the search tool to find relevant URLs
 search = TavilySearchResults(k=3) # Get top 3 results
 
 # 2. Set up the RAG chain
 llm = ChatOpenAI(model="gpt-3.5-turbo")
 prompt = ChatPromptTemplate.from_template("""Answer the following question based only on the provided context. Provide a detailed explanation and suggest mitigations.
 
 <context>
 {context}
 </context>
 
 Question: {input}""")
 
 document_chain = create_stuff_documents_chain(llm, prompt)
 
 # 3. The main function that orchestrates the flow
 def explain_cve(cve_id: str):
     print(f"--- Searching for information on {cve_id} ---")
     search_results = search.invoke(cve_id)
     urls = [res["url"] for res in search_results]
     print(f"Found URLs: {urls}")
 
     print("--- Loading and processing content ---")
     loader = WebBaseLoader(urls)
     docs = loader.load()
     
     text_splitter = RecursiveCharacterTextSplitter()
     documents = text_splitter.split_documents(docs)
     
     embeddings = OpenAIEmbeddings()
     vector = FAISS.from_documents(documents, embeddings)
     
     retriever = vector.as_retriever()
     retrieval_chain = create_retrieval_chain(retriever, document_chain)
     
     print("--- Generating final answer ---")
     response = retrieval_chain.invoke({"input": f"Explain the risk and mitigation for {cve_id}"})
     
     return response["answer"]
 
 if __name__ == "__main__":
     cve = "CVE-2024-21626" # Leaky Vessels Docker escape
     answer = explain_cve(cve)
     print("\n--- Final Report ---")
     print(answer)
 ```
 
 ### The Impact (To Teach)
 "We've built a security research assistant that provides up-to-the-minute analysis on vulnerabilities. By using LangChain to orchestrate a RAG pipeline that pulls live web data, our tool's answers are current and contextually rich, unlike a standard LLM which might have outdated knowledge. This is how you build LLM systems that reason with fresh information."
 
 ---
 
 ## 4. LangGraph: The Automated Terraform Auditor Agent
 
 **Goal:** Build a true "agent" that can operate in a loop, making decisions and using tools to achieve a goal. We will build an agent that scans, attempts to fix, and re-scans Terraform code until it's secure.
 
 ### The Concept (To Explain)
 LangGraph is a library for building stateful, multi-actor applications with LLMs. It extends LangChain's linear chains into cyclical graphs.
 *   **Why it matters:** It allows you to build agents that can reason, loop, and make decisions. Instead of a fixed sequence, the agent can choose its next action based on the current state of the problem. This is essential for complex tasks that require iteration, like automated debugging or incident response.
 *   **Architectural Choice:** Use LangGraph when you need to build an agent that can use multiple tools in a non-linear fashion. If your workflow can be described as a flowchart with decision points and loops, LangGraph is the right tool.
 
 ### The Mastery Project (To Implement)
 **Workflow:** A cyclical graph where the agent: **Scans** Terraform → **Decides** if fixes are needed → **Suggests Fixes** → **Re-scans** → **Reports**.
 
 1.  **State:** Define a state object that holds the Terraform code, scan results, and a loop counter.
 2.  **Nodes (Tools):** Create functions for each step: `scan_code`, `suggest_fix`, `generate_report`.
 3.  **Edges (Logic):** Create a conditional edge that checks the output of the `scan_code` node. If there are issues, it routes to `suggest_fix`. If not, it routes to `generate_report` to end the process. The graph will loop from `suggest_fix` back to `scan_code`.
 
 ### Code Deep Dive (Conceptual Agent)
 
 ```python
 # terraform_auditor_agent.py
 # pip install langgraph langchain langchain-openai
 import os
 from typing import TypedDict, List
 from langgraph.graph import StateGraph, END
 from langchain_openai import ChatOpenAI
 
 os.environ["OPENAI_API_KEY"] = "sk-..."
 
 # --- 1. Define Agent State ---
 class AgentState(TypedDict):
     terraform_code: str
     scan_results: List[str]
     iterations: int
     max_iterations: int
 
 # --- 2. Define Tools (Nodes) ---
 llm = ChatOpenAI(model="gpt-4-turbo")
 
 def scan_code(state: AgentState) -> AgentState:
     print(f"\n--- Iteration {state['iterations']}: Scanning Code ---")
     # In a real project, this would run `tfsec` or another scanner.
     # We'll mock it by calling an LLM to act as a scanner.
     prompt = f"You are a Terraform security scanner. Find issues in this code. If none, say 'No issues found.'.\n\n{state['terraform_code']}"
     response = llm.invoke(prompt).content
     print(f"Scan result: {response}")
     if "No issues found" in response:
         state['scan_results'] = []
     else:
         state['scan_results'] = [response]
     state['iterations'] += 1
     return state
 
 def suggest_fix(state: AgentState) -> AgentState:
     print("--- Suggesting a Fix ---")
     prompt = f"You are a DevSecOps expert. Fix the security issues in this Terraform code. Only output the corrected code block.\n\nIssues:\n{state['scan_results'][0]}\n\nCode:\n{state['terraform_code']}"
     corrected_code = llm.invoke(prompt).content
     state['terraform_code'] = corrected_code
     return state
 
 # --- 3. Define Logic (Conditional Edge) ---
 def should_continue(state: AgentState) -> str:
     if state['iterations'] >= state['max_iterations']:
         print("--- Max iterations reached. END. ---")
         return "end"
     if not state['scan_results']:
         print("--- No more issues found. END. ---")
         return "end"
     else:
         return "continue"
 
 # --- 4. Build the Graph ---
 workflow = StateGraph(AgentState)
 workflow.add_node("scanner", scan_code)
 workflow.add_node("fixer", suggest_fix)
 workflow.set_entry_point("scanner")
 workflow.add_conditional_edges(
     "scanner",
     should_continue,
     {"continue": "fixer", "end": END}
 )
 workflow.add_edge("fixer", "scanner")
 app = workflow.compile()
 
 # --- 5. Run the Agent ---
 initial_code = """
 resource "aws_s3_bucket" "insecure" {
   bucket = "my-public-bucket-for-testing"
   acl    = "public-read"
 }
 """
 
 final_state = app.invoke({
     "terraform_code": initial_code,
     "iterations": 0,
     "max_iterations": 3
 })
 
 print("\n--- Final Audited Code ---")
 print(final_state['terraform_code'])
 ```
 
 ### The Impact (To Teach)
 "We've built an autonomous agent that acts like a junior DevSecOps engineer. It doesn't just find problems; it actively tries to fix them and verifies its own work in a loop. This LangGraph agent demonstrates a powerful pattern for automation, where the AI can iterate on a problem until it reaches a successful state, just like a human would."
 
 ---
 
 By completing these four projects, you will have a deep, practical understanding of the modern GenAI stack, from managed APIs to private models and complex agentic workflows. You are now ready.