 # 🧱 Day 22: MLOps & AI Infrastructure Engineer Mode
 
 Welcome to Week 4. The focus now shifts from building individual AI-powered tools to understanding the platforms and frameworks that run them at scale. Today is about learning the "what" and "why" behind major AI/ML platforms and the libraries that orchestrate them. We'll use the few-shot technique, where each "shot" is a concept, a real-world use case, and an implementation example.
 
 ---
 
 ### Shot 1: AWS Bedrock (The "Easy Button" for Foundation Models)
 
 *   **What it is:** Think of AWS Bedrock as an API gateway for a curated set of powerful foundation models (FMs) from providers like Anthropic (Claude), AI21 Labs (Jurassic), Cohere, and Amazon (Titan). You don't host the models; you access them through a single, unified AWS API.
 
 *   **Real-World DevSecOps Use Case:** Your threat modeling bot from Week 3 uses a specific model. What if a new, more powerful model is released? With Bedrock, you can switch models with a one-line code change instead of re-architecting your application for a new API. This allows you to build a "model-agile" application, abstracting away the specific model provider.
 
 *   **Implementation Example (Python/Boto3):**
 
 ```python
 import boto3
 import json
 
 # Note: It's best practice to initialize clients outside the handler in a real Lambda
 bedrock_runtime = boto3.client(service_name='bedrock-runtime', region_name='us-east-1')
 
 def get_security_insight(prompt, model_id):
     """
     Gets a security insight from a specified Bedrock model.
     Notice how the core logic is the same, only the model_id and payload structure change.
     """
     if "anthropic.claude" in model_id:
         # Payload for Anthropic Claude 3 Sonnet
         payload = {
             "anthropic_version": "bedrock-2023-05-31",
             "max_tokens": 1024,
             "messages": [{"role": "user", "content": [{"type": "text", "text": prompt}]}]
         }
     elif "amazon.titan" in model_id:
         # Payload for Amazon Titan
         payload = {
             "inputText": prompt,
             "textGenerationConfig": {
                 "maxTokenCount": 1024,
                 "temperature": 0.7,
                 "topP": 1
             }
         }
     else:
         raise ValueError(f"Unsupported model_id: {model_id}")
 
     response = bedrock_runtime.invoke_model(
         body=json.dumps(payload),
         modelId=model_id,
         contentType='application/json',
         accept='application/json'
     )
     
     response_body = json.loads(response.get('body').read())
 
     if "anthropic.claude" in model_id:
         return response_body['content'][0]['text']
     elif "amazon.titan" in model_id:
         return response_body.get('results')[0].get('outputText')
 
 # --- You can now easily switch models ---
 
 cve_summary_prompt = "Summarize the risk of CVE-2021-44228 in simple terms for a developer."
 
 # Get insight from Claude 3 Sonnet
 claude_insight = get_security_insight(cve_summary_prompt, 'anthropic.claude-3-sonnet-20240229-v1:0')
 print(f"--- Claude's Insight ---\n{claude_insight}\n")
 
 # Get insight from Titan
 titan_insight = get_security_insight(cve_summary_prompt, 'amazon.titan-text-express-v1')
 print(f"--- Titan's Insight ---\n{titan_insight}")
 ```
 
 ---
 
 ### Shot 2: SageMaker JumpStart (The "Quick Start" for Custom & Open-Source Models)
 
 *   **What it is:** SageMaker is AWS's full-featured, end-to-end ML platform. JumpStart is its accelerator. It provides a catalog of pre-trained, open-source models (like Llama 3 or Mistral) that you can deploy to a dedicated, private SageMaker endpoint with a few clicks or a simple SDK call. You can also use it to fine-tune these models on your own data.
 
 *   **Real-World DevSecOps Use Case:** You need a specialized model to detect secrets in source code. Instead of building one from scratch, you find a pre-trained model on JumpStart that's good at code analysis. You deploy it to a SageMaker endpoint, giving you a private, high-performance API for your CI/CD pipeline to call, ensuring your proprietary code never leaves your AWS environment.
 
 *   **Implementation Example (Conceptual Python/SageMaker SDK):**
 
 ```python
 from sagemaker.jumpstart.model import JumpStartModel
 
 # 1. Choose a pre-trained model from the JumpStart catalog
 # This is a hypothetical model for demonstration
 model_id = "huggingface-llm-codellama-7b" 
 
 # 2. Deploy the model to a SageMaker endpoint
 # This single line provisions the necessary infrastructure and deploys the model container.
 model = JumpStartModel(model_id=model_id)
 predictor = model.deploy()
 
 # 3. You now have a private endpoint to call for inference
 code_snippet = 'aws_access_key = "AKIA..."'
 response = predictor.predict({"inputs": f"Does the following code contain a secret? -> {code_snippet}"})
 
 print(response)
 
 # 4. Remember to clean up the endpoint to avoid ongoing costs
 predictor.delete_endpoint()
 ```
 
 ---
 
 ### Shot 3: Vertex AI (The "Google Cloud Equivalent")
 
 *   **What it is:** Vertex AI is Google Cloud's unified MLOps platform, analogous to SageMaker. It offers a "Model Garden" (similar to JumpStart) for deploying foundation models and a full suite of tools for the entire ML lifecycle: data labeling, training, tuning, and serving.
 
 *   **Real-World DevSecOps Use Case:** Your organization operates in a multi-cloud environment. A new project on Google Cloud needs a security log analyzer. You use Vertex AI to deploy Google's own "Gemini" model to a private endpoint. You then build a Cloud Function (the GCP equivalent of Lambda) that triggers on new logs in Cloud Logging, calls the Gemini endpoint for analysis, and reports the findings. The principles are the same as on AWS, just with different service names.
 
 ---
 
 ### Shot 4: LangChain (The "Orchestration Framework" for LLMs)
 
 *   **What it is:** LangChain is an open-source Python/JS framework that makes it easier to build complex applications powered by LLMs. It's the "glue" that connects an LLM to other data sources or tools. Its core concept is the "Chain," which allows you to combine multiple components in a sequence.
 
 *   **Real-World DevSecOps Use Case:** You want to build a bot that explains a security vulnerability. A simple prompt isn't enough because the LLM needs up-to-date context. You use LangChain to create a `RetrievalQA` chain. This chain takes a user's query (e.g., "CVE-2024-12345"), retrieves relevant documents from your private knowledge base (a vector database), and then passes those documents along with the original query to the LLM.
 
 *   **Implementation Example (Python/LangChain):**
 
 ```python
 # This example requires installing:
 # pip install langchain langchain-openai beautifulsoup4 faiss-cpu
 
 from langchain_community.document_loaders import WebBaseLoader
 from langchain_community.vectorstores import FAISS
 from langchain_openai import OpenAIEmbeddings, ChatOpenAI
 from langchain_text_splitters import RecursiveCharacterTextSplitter
 from langchain.chains.combine_documents import create_stuff_documents_chain
 from langchain_core.prompts import ChatPromptTemplate
 from langchain.chains import create_retrieval_chain
 
 # 1. Load data from a source (e.g., a blog post about a CVE)
 loader = WebBaseLoader("https://www.wiz.io/blog/cve-2024-21626-runc-process-exploit-leaky-vessels-docker-escape")
 docs = loader.load()
 
 # 2. Create embeddings and store in a vector database (in-memory FAISS)
 embeddings = OpenAIEmbeddings()
 text_splitter = RecursiveCharacterTextSplitter()
 documents = text_splitter.split_documents(docs)
 vector = FAISS.from_documents(documents, embeddings)
 
 # 3. Create a prompt template
 prompt = ChatPromptTemplate.from_template("""Answer the following question based only on the provided context:
 
 <context>
 {context}
 </context>
 
 Question: {input}""")
 
 # 4. Create the chain
 llm = ChatOpenAI()
 document_chain = create_stuff_documents_chain(llm, prompt)
 retrieval_chain = create_retrieval_chain(vector.as_retriever(), document_chain)
 
 # 5. Invoke the chain
 response = retrieval_chain.invoke({"input": "What is the root cause of CVE-2024-21626?"})
 print(response["answer"])
 ```
 
 ---
 
 ### Shot 5: LangGraph (The "Stateful Agent Builder")
 
 *   **What it is:** LangGraph is an extension of LangChain designed for building complex, stateful agents. While LangChain is great for predefined sequences (chains), LangGraph allows you to define workflows as cyclical graphs. This is crucial for agents that need to make decisions, use tools, and loop until a problem is solved.
 
 *   **Real-World DevSecOps Use Case:** You want to build an automated incident response agent. When an alert comes in, the agent needs to decide what to do. Should it first enrich the alert by looking up an IP address? Or should it immediately try to isolate the affected host? LangGraph allows you to build an agent that can reason about the state of the incident and choose the next best action from a set of available tools, even calling multiple tools in a loop.
 
 *   **Implementation Example (Conceptual Python/LangGraph):**
 
 ```python
 # This is a conceptual example to illustrate the graph structure.
 # It requires installing: pip install langchain langgraph
 
 from typing import TypedDict, Annotated
 from langgraph.graph import StateGraph, END
 
 # 1. Define the state of your agent
 class AgentState(TypedDict):
     alert_details: str
     ip_info: str
     is_host_isolated: bool
     final_report: str
 
 # 2. Define the tools (as functions)
 def lookup_ip(state):
     print("TOOL: Looking up IP...")
     # In a real scenario, this would call an API
     state['ip_info'] = "IP is from a known malicious source."
     return state
 
 def isolate_host(state):
     print("TOOL: Isolating host...")
     state['is_host_isolated'] = True
     return state
 
 def decide_next_step(state):
     print("AGENT: Deciding next step...")
     if not state.get('ip_info'):
         return "lookup_ip"
     elif not state.get('is_host_isolated'):
         return "isolate_host"
     else:
         return "generate_report"
 
 def generate_report(state):
     print("AGENT: Generating final report...")
     state['final_report'] = f"Incident handled. Alert: {state['alert_details']}. IP Info: {state['ip_info']}. Host Isolated: {state['is_host_isolated']}"
     return state
 
 # 3. Build the graph
 workflow = StateGraph(AgentState)
 workflow.add_node("lookup_ip", lookup_ip)
 workflow.add_node("isolate_host", isolate_host)
 workflow.add_node("generate_report", generate_report)
 
 # 4. Define the edges and conditional logic
 workflow.add_conditional_edges(
     "decide_next_step",
     decide_next_step,
     {
         "lookup_ip": "lookup_ip",
         "isolate_host": "isolate_host",
         "generate_report": "generate_report"
     }
 )
 workflow.add_edge('lookup_ip', 'decide_next_step')
 workflow.add_edge('isolate_host', 'decide_next_step')
 workflow.add_edge('generate_report', END)
 workflow.set_entry_point("decide_next_step")
 
 # 5. Compile and run the agent
 app = workflow.compile()
 initial_state = {"alert_details": "Suspicious login from 1.2.3.4", "is_host_isolated": False}
 final_state = app.invoke(initial_state)
 
 print("\n--- Final Report ---")
 print(final_state['final_report'])
 ```
 
 ## Day 22 Conclusion
 
 Today, you've surveyed the landscape of AI infrastructure and orchestration. You've learned that:
 *   **Bedrock** is for easily consuming various foundation models via a single API.
 *   **SageMaker JumpStart** and **Vertex AI** are for deploying and managing your own private, scalable model endpoints.
 *   **LangChain** is the glue for creating sequences of LLM calls and tool usage.
 *   **LangGraph** is the next step, enabling you to build stateful, intelligent agents that can reason and loop.
 
 With these mental models, you are now equipped to make architectural decisions for building robust, scalable, and powerful GenAI DevSecOps applications.