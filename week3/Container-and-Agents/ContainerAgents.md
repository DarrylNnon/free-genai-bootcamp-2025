### week 3 - CONTAINERS AND AGENTS

This week is focused on deepening our knowledge working with containerized GenAI workloads through OPEA and learning to build our own Agent that uses Agentic workflow.


OPEA MegaService Continued 
You’re tasked with attempting to expand your knowledge and construct your own Mega-service.

For example: 
Andrew returned back to the megaservice and fully troubleshooted why the handle_request was not working my stepping through all the code and the codebase and developing debugging techniques and made the original mega-service example working.

Andrew then went on to reimplement the MegaService from scratch with new understanding of the codebase and tried to swap out Ollama with vLLM. However it turned out vLLM introduced more technical uncertainty because the target model was not loading or might not be compatible. Attempting to debug vLLM in isolation was challenging because the OPEA Configuration is intended for a specific Intel configuration and Andrew could not in designated time resolve local hardware configuration.

Andrew instead decided to dive deep into the TTS service learning about the underlying model SpeakT5 and RVC-Boss/GPT-SoVITS, GPT-SoVITS is a voicecloning layer ontop of SpeakT5 which lack documentation, but Andrew was able to get a 10s voice cloning to work (with abysmal results). Andrew attempted 1m but it produced an empty voice clip and it would require stepping through the GPT-SoVITS which is not well documented, created by chinese research company with a very messy codebase. However this discovery leads Andrew to believe he might be able to produce a high quality synthetic voice if continued down this path.

Andrew did not complete integration into the megaservice.

Agents and Agentic Workflow
Implement an agent with Agentic workflow using an agent framework or from scratch

eg:
Andrew attempted to reimplement Goerge’s Vocab Song application in Windsurf and wrote a TechSpec to generate the app in a waterfall fashion. As per usual this approach lead significant troubleshooting since the app made several mistakes. Andrew could not get DuckDuckGo despite using the exact code that George used. This issue was due to Ratelimiting. Andrew implemented SerpAPI which had to be done manually because Claude Sonnet 3.5 kept producing incorrect results. Andrew implemented the agentic workflow without a framework and chose to use local models via LLM. However at a specific step the output kept returning blank. Andrew investigated and it appeared to be that the context window was set too small. After researching Andrew noticed that the code was hard coded for a very small context window of something like 2K and these models cloud handle 128K so he increased to the max size which resulted in there not being about Shared memory (generic memory). Andrew created a function to set the program to use a certain about of memory which would result in a token amount. Andrew had switch from Mistral 7B to Llama 3.2:3B because Mistral 7 was performing slow. Andrew did eventually realize he wasn’t utilizing GPUs and this was due to Ollama in WSL does not properly detect GPUs or iGPUs. Andrew researched and it appears that Ollama might have to be compiled to work on the WSL side. 

While Andrew did not finish his implementation of his Agent, he is confident he could get it working using managed serverless services and the domain knowledge gained was working with local LLMS.




### Week 3 Livestream - Containers and Agents with James Spurin
This week is containers and Agents with James Spurin specialist in cloud space, docker captain.

[diveinto.com](https://diveinto.com/p/home)


### GenAI Architecting (OPEA  -  Open Enterprise AI)

<img width="805" height="431" alt="image" src="https://github.com/user-attachments/assets/4c0b6f5b-601b-4990-9ea2-80cd6e757bd9" />

### DAG (Directed Acylic Graph)

DAG if a go be if be go d...is a continuous graph




