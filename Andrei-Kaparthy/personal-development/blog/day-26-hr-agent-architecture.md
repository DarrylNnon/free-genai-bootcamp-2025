# 🏛️ Day 26: The Billion-Dollar Architecture - An Autonomous HR AI Platform

Yesterday, we defined the vision for an AI-native HR company. Today, as the founding engineer, we build the blueprint. An idea is worth nothing without execution, and a billion-dollar company is built on a billion-dollar architecture.

This isn't just a plan for an app; it's the design for a scalable, intelligent system of agents.

## Core Architectural Principles

1.  **Serverless-First:** We don't manage servers. We manage services. This gives us infinite scalability, pay-per-use cost efficiency, and lets a small team operate a massive platform. The core will be AWS Lambda, API Gateway, DynamoDB, and S3.
2.  **Event-Driven & Decoupled:** Services do not call each other directly. They communicate asynchronously by publishing and subscribing to events via **Amazon EventBridge**. This makes the system resilient, extensible, and allows for complex, emergent behaviors.
3.  **AI-Native, Not AI-Adjacent:** AI is not a feature bolted on top; it's the core logic. We will use managed AI services like **Amazon Bedrock** to access best-in-class models without the operational overhead of hosting them.
4.  **Agentic Design:** Each core business capability (sourcing, matching, scheduling) is designed as a semi-autonomous agent with a clear goal, the ability to perceive its environment, and the tools to take action.

---

## The High-Level Architecture

Below is the conceptual diagram of our platform. It's composed of several key domains, each containing one or more microservices.

```mermaid
graph TD
    subgraph User Experience
        WebApp[Next.js on AWS Amplify]
    end

    subgraph API Layer
        API_Gateway[API Gateway]
        Cognito[Amazon Cognito]
    end

    subgraph Core Services (Microservices)
        ProfileSvc[Profile Service <br/>(Lambda + DynamoDB)]
        JobSourcingAgent[Job Sourcing Agent <br/>(Lambda + S3)]
        MatchingAgent[Matching Agent <br/>(Lambda + Bedrock + OpenSearch)]
        ContentAgent[Content Generation Agent <br/>(Lambda + Bedrock)]
        ApplicationAgent[Application Agent <br/>(Fargate + Playwright)]
        SchedulingAgent[Scheduling Agent <br/>(Step Functions + Lambda)]
    end

    subgraph Data & AI Layer
        DynamoDB[(DynamoDB <br/> Structured Data)]
        S3[(S3 <br/> Unstructured Data, CVs, Job Postings)]
        OpenSearch[(Amazon OpenSearch <br/> Vector Search)]
        Bedrock[Amazon Bedrock <br/> (Claude 3, Titan)]
    end

    subgraph Central Nervous System
        EventBridge[Amazon EventBridge]
    end

    WebApp --> API_Gateway
    API_Gateway --> Cognito
    API_Gateway --> ProfileSvc
    API_Gateway --> ContentAgent
    API_Gateway --> SchedulingAgent

    ProfileSvc -- Publishes Events --> EventBridge
    JobSourcingAgent -- Publishes Events --> EventBridge

    EventBridge -- Triggers --> MatchingAgent
    EventBridge -- Triggers --> SchedulingAgent

    MatchingAgent --> Bedrock
    MatchingAgent --> OpenSearch
    ContentAgent --> Bedrock
    ApplicationAgent --> Bedrock
    SchedulingAgent -- Interacts with --> ExternalAPIs[Google/Outlook Calendar APIs]

```

### Component Breakdown

1.  **User Experience (AWS Amplify):**
    *   A single Next.js web application serves both candidates and recruiters. Amplify handles the CI/CD, hosting, and scaling of the frontend seamlessly.

2.  **API & Identity (API Gateway + Cognito):**
    *   **Amazon Cognito** provides secure user registration, authentication, and profile management for candidates and recruiters.
    *   **API Gateway** exposes our backend services as a RESTful API. It integrates with Cognito for authorization, ensuring only authenticated users can access their data.

3.  **The Agentic Core (Microservices):**
    *   **Profile Service (Lambda + DynamoDB):** Manages the core data for candidates (skills, experience, career goals) and recruiters (company info, open roles).
    *   **Job Sourcing Agent (Scheduled Lambda + S3):** Runs on a schedule to scrape public job boards and company career pages. It dumps the raw HTML/JSON into an S3 bucket and publishes a `JobPostingFound` event to EventBridge.
    *   **Matching Agent (Lambda + Bedrock + OpenSearch):**
        *   Listens for `JobPostingFound` and `CandidateProfileUpdated` events.
        *   When triggered, it uses an embedding model via **Bedrock** to convert job descriptions and candidate profiles into vectors.
        *   It stores these vectors in **Amazon OpenSearch Serverless**, which acts as our vector database.
        *   It queries OpenSearch to find the top-k matches and publishes a `PotentialMatchFound` event.
    *   **Content Generation Agent (Lambda + Bedrock):**
        *   Provides synchronous API endpoints for on-demand content.
        *   `POST /cv/generate`: Takes a job ID and candidate ID, pulls the necessary data, and uses a powerful model in **Bedrock** (e.g., Claude 3) with a sophisticated prompt to generate a tailored CV.
        *   `POST /message/draft`: Does the same for generating personalized outreach messages.
    *   **Application Agent (Fargate + Playwright):**
        *   This is for the "AI-Fill" feature. Since browser automation can be long-running and resource-intensive, it runs as a containerized task on **AWS Fargate**, not Lambda.
        *   It receives a job application URL and candidate data, then uses a headless browser (via Playwright) to navigate the page and fill out the form fields.
    *   **Scheduling Agent (AWS Step Functions + Lambda):**
        *   The most complex agent. It's modeled as a state machine using **AWS Step Functions** to handle the multi-step, long-running process of scheduling an interview.
        *   **Workflow:** `GetAvailabilities` (calls Google/Outlook Calendar APIs via Lambda) → `ProposeTimes` (sends email via SES) → `WaitForResponse` (pauses the workflow) → `ConfirmBooking` (calls Calendar API again). Step Functions manage the state, retries, and waiting periods perfectly.

4.  **Central Nervous System (Amazon EventBridge):**
    *   This is the glue. It allows for complete decoupling. For example, we can add a new "Market Analytics" service that just listens to `JobPostingFound` and `PotentialMatchFound` events to generate real-time market insights, without any other service needing to know it exists.

## A Day in the Life of the System: New Job Match

1.  The **Job Sourcing Agent** finds a new "Senior AI Engineer" role and drops the data into S3. It publishes a `JobPostingFound` event to EventBridge with the S3 location.
2.  **EventBridge** routes this event to the **Matching Agent**.
3.  The **Matching Agent** wakes up, reads the job data, generates a vector embedding for it using **Bedrock**, and stores it in **OpenSearch**.
4.  It then queries OpenSearch: "Find me the top 10 candidate profiles most similar to this new job vector."
5.  For each match found, it publishes a `PotentialMatchFound` event containing the candidate ID and the job ID.
6.  The candidate's **WebApp** (listening for push notifications via another service) gets the event and displays: "We found a new high-match role for you: Senior AI Engineer."

This entire flow happens in seconds, with zero human intervention and zero servers to manage. This is the power of a serverless, agentic architecture. This is how we build a company that can scale to millions of users from day one.