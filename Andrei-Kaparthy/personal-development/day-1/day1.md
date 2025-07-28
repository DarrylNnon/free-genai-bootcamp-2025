**Day 1 (Mon)**:  
  - Enroll in ExamPro GenAI Bootcamp  
  - Learn LLM fundamentals: tokens, temperature, context windows  
  - Create accounts: OpenAI, HuggingFace, GitHub, AWS/GCP


## LLM-fundamentals

intro to Large Lnaguage Models with Andrej Kaparthy (AI expert- ai tech lead at tesla)

## youtube video use to learn this introduction:

https://youtu.be/zjkBMFhNj_g?si=AldODDoOTlq84Gw8

# What is a Large Lnaguage Model (LLM)?

Think of LLMs as mostly inscrutable artifacts, develop correspondingly sophisticated evaluations

A llm is just 2 files and this hypothetical directorie.

For example working with a specific example of llama-2-70b ( this a llm release by openAI)

![alt text](image.png)

The llma is just 2 files:
-   the parameters
-   the run

# the two steps in llm: 1 Pretraining

pre-training stage is about alarge quantity of text but potentially low quality because it just comes from the internet and there's tens of or hundreds of terabyte Tech off it and it's not all very high quality but in this second stage we prefer quality over quantity so we may have many fewer documents for example 100,000 but all these documents now are
conversations and they should be very high quality conversations and fundamentally people create them based on abling instructions so we swap out.

pre-training is about knowledge and fine tuning is about alignment.

# Summary: HOW TO TRAIN YOUR CHATGPT

<img width="628" height="376" alt="image" src="https://github.com/user-attachments/assets/52960471-e5c5-4bc5-a5e7-7172188d89fa" />

After finetuning i have an assistant:

<img width="415" height="304" alt="image" src="https://github.com/user-attachments/assets/afd591be-31ed-4e0b-a766-740a4fead2b5" />

# The second kind of label: comparisons

<img width="628" height="351" alt="image" src="https://github.com/user-attachments/assets/3d641209-3dcd-41d4-8989-491d57c8d579" />

<img width="580" height="324" alt="image" src="https://github.com/user-attachments/assets/2f451121-5a11-48cc-b16f-0b2a6c3374fa" />


# LLM leaderboard from "chatbot Arena"

<img width="598" height="324" alt="image" src="https://github.com/user-attachments/assets/a91d23e2-adbe-413a-91df-42b432133852" />


# LLM Scaling Laws

<img width="463" height="351" alt="image" src="https://github.com/user-attachments/assets/af5ac6bc-9b0d-4512-8556-ce13973a04e4" />



It is often easier to compare answer instead of writing Answer.


# trinaing the assistant

<img width="665" height="358" alt="image" src="https://github.com/user-attachments/assets/c012d87c-5a1a-49a3-89aa-e8530663ebf9" />

-  Postraining


# RAG (retrieval augmented generation

when you upload files there's something called retrieval augmented generation where
chpt can actually like reference chunks of that text in those files and use that when it creates responses so it's it's
kind of like an equivalent of browsing but instead of browsing the internet Chach can browse the files that you
upload and it can use them as a reference information for creating its answers um so today these are the kinds



## LLM OS

<img width="680" height="376" alt="image" src="https://github.com/user-attachments/assets/15dcd9d7-fda6-42da-be5c-f359ae1ce7a5" />


<img width="645" height="368" alt="image" src="https://github.com/user-attachments/assets/2e94d818-0d86-46d0-b684-2751ff59e57c" />


## LLM Security

challenges in the original operating system stack we're going to have new security challenges that are specific to
large language models so I want to show some of those challenges by example to demonstrate  kind of like the ongoing
uh c and mouse games that are going to be present in this new Computing Paradigm so the first example.

<img width="496" height="305" alt="image" src="https://github.com/user-attachments/assets/e5687982-2d6f-438d-b12f-8aa1520dead3" />


-  Jailbreak

  fooling chatgpt with a different approach by using my grand-mother so chatgpt can give me the solution to use the poison.

  <img width="477" height="178" alt="image" src="https://github.com/user-attachments/assets/4de0847c-c9f5-4571-a6f4-085abb68c454" />


-  Prompt injection
  a prompt injection attack

<img width="466" height="329" alt="image" src="https://github.com/user-attachments/assets/09667e57-c158-4be9-b214-dbf0730c10cf" />

<img width="421" height="345" alt="image" src="https://github.com/user-attachments/assets/9597ec13-b488-45eb-9150-e4fc724e329c" />


- Data poisoning / Backdoor attack

  <img width="649" height="378" alt="image" src="https://github.com/user-attachments/assets/c498877e-a9ab-4c45-9ae6-449a709f3133" />



# Slides as PDF: [https://drive.google.com/file/d/1pxx_... (42MB)](https://www.youtube.com/redirect?event=video_description&redir_token=QUFFLUhqbDA1MjBLeXhNRERyUEMwWFY0YXUyMEl3WUFmd3xBQ3Jtc0traXE1cG5hTzhBY0NrWU1pZUYxWkZQOGhZNzQxR1VNRXplTFhMX1NNVC1OMktxdU9ObkZlYWVEUzM5ZTZOaGFsQ01zYTNseHM3aE1WdkFINEh1bGF5OWtITDBoaGU1ZTRUQ2ExSFBNYmRLN3IyR293TQ&q=https%3A%2F%2Fdrive.google.com%2Ffile%2Fd%2F1pxx_ZI7O-Nwl7ZLNk5hI3WzAsTLwvNU7%2Fview%3Fusp%3Dshare_link&v=zjkBMFhNj_g)

# Slides. as Keynote: [https://drive.google.com/file/d/1FPUp... (140MB)](https://www.youtube.com/redirect?event=video_description&redir_token=QUFFLUhqbDA1MjBLeXhNRERyUEMwWFY0YXUyMEl3WUFmd3xBQ3Jtc0traXE1cG5hTzhBY0NrWU1pZUYxWkZQOGhZNzQxR1VNRXplTFhMX1NNVC1OMktxdU9ObkZlYWVEUzM5ZTZOaGFsQ01zYTNseHM3aE1WdkFINEh1bGF5OWtITDBoaGU1ZTRUQ2ExSFBNYmRLN3IyR293TQ&q=https%3A%2F%2Fdrive.google.com%2Ffile%2Fd%2F1pxx_ZI7O-Nwl7ZLNk5hI3WzAsTLwvNU7%2Fview%3Fusp%3Dshare_link&v=zjkBMFhNj_g)
