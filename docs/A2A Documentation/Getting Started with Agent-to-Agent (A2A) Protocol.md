---
title: "Getting Started with Agent-to-Agent (A2A) Protocol: A Purchasing Concierge and Remote Seller Agent Interactions with Gemini on Cloud Run  |  Google Codelabs"
description: "In this codelab we will deploy several agent services and inspect how we can implement A2A protocol to standardize communications between them. You will learn the core concepts and components of A2A and how to inspect the interactions by deploying the agents powered by different agentic framework with Gemini backend as different services on top of Cloud Run"
keywords: ""
source: "https://codelabs.developers.google.com/intro-a2a-purchasing-concierge?hl=en#1"
---

[Skip to main content](#main-content)

* On this page
* [Introduction](#0)
* [Before you begin](#1)
* [Deploying Remote Seller Agent - A2A Server to Cloud Run](#2)
* [Core Components of A2A Server](#3)
* [Deploying the Purchasing Concierge - A2A Client to Cloud Run](#4)
* [Core Components of A2A Client](#5)
* [Integration Testing and Payload Inspection](#6)
* [Clean up](#7)

About this codelab

_schedule_0 minutes

_subject_Last updated May 8, 2025

## 1. Introduction

![3356bc1e3134fab5.png](https://codelabs.developers.google.com/static/intro-a2a-purchasing-concierge/img/3356bc1e3134fab5.png)

Agent-to-agent (A2A) protocol is designed to standardize communication between AI agents, particularly for those which are deployed in external systems. Previously, such protocols were established for **Tools** called **Model Context Protocol (MCP)** which is an emerging standard to connect LLMs with data and resources. A2A tries to complement MCP where A2A is focused on a different problem, while MCP focuses on lowering complexity to connect agents with tools and data, A2A focuses on how to enable agents to collaborate in their natural modalities. It allows agents to communicate as **_agents_** (or as users) instead of as tools; for example, enable back-and-forth communication when you want to order something.

A2A is positioned to complement MCP, in the [official documentation](https://google.github.io/A2A/topics/a2a-and-mcp) it is recommended that applications model A2A agents as MCP resources - represented by **_AgentCard_** ( We will discuss this later on ). The frameworks can then use A2A to communicate with their user, the remote agents, and other agents.

![83b1a03588b90b68.png](https://codelabs.developers.google.com/static/intro-a2a-purchasing-concierge/img/83b1a03588b90b68.png)

In this demo, we will start with implementation of A2A only from scratch. Derived from these [sample repositories](https://github.com/google/A2A/tree/f8cff21a15667fd5223946574a9ed33ecccd6151/samples/python) , we will explore a use case when we have a personal purchasing concierge which can help us to communicate with burger and pizza seller agents to handle our order.

A2A utilizes client-server principle. Here is the typical A2A flow that we will expect in this demo

![73dae827aa9bddc3.png](https://codelabs.developers.google.com/static/intro-a2a-purchasing-concierge/img/73dae827aa9bddc3.png)

1. A2A Client will first doing discovery on all accessible A2A Server agent card and utilize its information to build a connection client
2. When necessary, A2A Client will send tasks to the A2A Server. If push notification receiver URL is configured on the A2A client, the A2A Server will also capable to publish the state of the task progression to the receiving endpoint
3. After task finished, the A2A server will send the response artifact to the A2A Client

Through the codelab, you will employ a step by step approach as follows:

1. Prepare your Google Cloud project and Enable all the required API on it
2. Setup workspace for your coding environment
3. Prepare env variables for burger and pizza agent services
4. Deploy burger and pizza agent to Cloud Run
5. Inspect the details on how A2A server established
6. Prepare env variables for purchasing concierge
7. Deploy purchasing concierge to Cloud Run
8. Inspect the details on how A2A client established and its data modelling
9. Inspect the payload and interaction between A2A client and server

## **Architecture Overview**

We will deploy the following service architecture

![bc8f96e071ae53ff.png](https://codelabs.developers.google.com/static/intro-a2a-purchasing-concierge/img/bc8f96e071ae53ff.png)

We will deploy 2 services which will act as A2A server, the Burger agent ( backed by CrewAI agent framework ) and Pizza agent ( backed by Langgraph agent framework ). The user will only directly interact with the Purchasing concierge which will be run using Agent Development Kit (ADK) framework which will act as A2A client.

Each of these agents will have their own environment and deployment on their own.

## **Prerequisites**

* Comfortable working with Python
* An understanding of basic full-stack architecture using HTTP service

## **What you'll learn**

* Core structure of A2A Server
* Core structure of A2A Client
* Deploying service to Cloud Run
* How A2A Client connect to A2A Server
* Request and Response structure on non-streaming connection

## **What you'll need**

* Chrome web browser
* A Gmail account
* A Cloud Project with billing enabled

This codelab, designed for developers of all levels (including beginners), uses Python in its sample application. However, Python knowledge isn't required for understanding the concepts presented.

## 2. Before you begin

## **Select Active Project in the Cloud Console**

This codelab assumes that you already have a Google Cloud project with billing enabled. If you do not have it yet, you can follow the instructions below to get started.

1. In the [Google Cloud Console](https://console.cloud.google.com/), on the project selector page, select or create a Google Cloud [project](https://cloud.google.com/resource-manager/docs/creating-managing-projects).
2. Make sure that billing is enabled for your Cloud project. Learn how to [check if billing is enabled on a project](https://cloud.google.com/billing/docs/how-to/verify-billing-enabled).

![bc8d176ea42fbb7.png](https://codelabs.developers.google.com/static/intro-a2a-purchasing-concierge/img/bc8d176ea42fbb7.png)

## **Setup Cloud Project in Cloud Shell Terminal**

1. You'll use [Cloud Shell](https://cloud.google.com/cloud-shell/), a command-line environment running in Google Cloud that comes preloaded with bq. Click Activate Cloud Shell at the top of the Google Cloud console. If it prompts you to authorize, click **Authorize**

![1829c3759227c19b.png](https://codelabs.developers.google.com/static/intro-a2a-purchasing-concierge/img/1829c3759227c19b.png)

2. Once connected to Cloud Shell, you check that you're already authenticated and that the project is set to your project ID using the following command:

```
gcloud auth list
```

3. Run the following command in Cloud Shell to confirm that the gcloud command knows about your project.

```
gcloud config list project
```

4. If your project is not set, use the following command to set it:

```
gcloud config set project <YOUR_PROJECT_ID>
```

Alternatively, you also can see the `PROJECT_ID` id in the console

![4032c45803813f30.jpeg](https://codelabs.developers.google.com/static/intro-a2a-purchasing-concierge/img/4032c45803813f30.jpeg)

Click it and you will all of your project and the project ID on the right side

![8dc17eb4271de6b5.jpeg](https://codelabs.developers.google.com/static/intro-a2a-purchasing-concierge/img/8dc17eb4271de6b5.jpeg)

5. Enable the required APIs via the command shown below. This could take a few minutes, so please be patient.

```
gcloud services enable aiplatform.googleapis.com \
                       run.googleapis.com \
                       cloudbuild.googleapis.com \
                       cloudresourcemanager.googleapis.com
```

On successful execution of the command, you should see a message similar to the one shown below:

Operation "operations/..." finished successfully.

The alternative to the gcloud command is through the console by searching for each product or using this [link](https://console.cloud.google.com/apis/enableflow?apiid=firestore.googleapis.com,compute.googleapis.com,cloudresourcemanager.googleapis.com,servicenetworking.googleapis.com,run.googleapis.com,cloudbuild.googleapis.com,cloudfunctions.googleapis.com,aiplatform.googleapis.com).

If any API is missed, you can always enable it during the course of the implementation.

Refer [documentation](https://cloud.google.com/sdk/gcloud/reference/config/list) for gcloud commands and usage.

## **Go to Cloud Shell Editor and Setup Application Working Directory**

Now, we can set up our code editor to do some coding stuff. We will use the Cloud Shell Editor for this

1. Click on the Open Editor button, this will open a Cloud Shell Editor, we can write our code here ![b16d56e4979ec951.png](https://codelabs.developers.google.com/static/intro-a2a-purchasing-concierge/img/b16d56e4979ec951.png)
2. Make sure the Cloud Code project is set in the bottom left corner (status bar) of the Cloud Shell editor, as highlighted in the image below and is set to the active Google Cloud project where you have billing enabled. **Authorize** if prompted. If you already follow previous command, the button may also point directly to your activated project instead of sign in button

![f5003b9c38b43262.png](https://codelabs.developers.google.com/static/intro-a2a-purchasing-concierge/img/f5003b9c38b43262.png)

3. Next, let's clone the template working directory for this codelab from Github, run the following command. It will create the working directory in the **purchasing-concierge-a2a** directory

```
git clone https://github.com/alphinside/purchasing-concierge-intro-a2a-codelab-starter.git purchasing-concierge-a2a
```

4. After that, go to the top section of the Cloud Shell Editor and click **File->Open Folder,** find your **username** directory and find the **purchasing-concierge-a2a** directory then click the OK button. This will make the chosen directory as the main working directory. In this example, the username is **alvinprayuda**, hence the directory path is shown below

![2c53696f81d805cc.png](https://codelabs.developers.google.com/static/intro-a2a-purchasing-concierge/img/2c53696f81d805cc.png)

![253b472fa1bd752e.png](https://codelabs.developers.google.com/static/intro-a2a-purchasing-concierge/img/253b472fa1bd752e.png)

Now, your Cloud Shell Editor should look like this

![6a2aa5fc278f5456.png](https://codelabs.developers.google.com/static/intro-a2a-purchasing-concierge/img/6a2aa5fc278f5456.png)

## **Environment Setup**

The next step is to prepare the development environment. Your current active terminal should be inside the **purchasing-concierge-a2a** working directory. We will utilize Python 3.12 in this codelab and we will use [uv python project manager](https://docs.astral.sh/uv/) to simplify the need of creating and managing python version and virtual environment

1. If you haven't opened the terminal yet, open it by clicking on **Terminal** -> **New Terminal** , or use **Ctrl + Shift + C** , it will open a terminal window on the bottom part of the browser

![f8457daf0bed059e.jpeg](https://codelabs.developers.google.com/static/intro-a2a-purchasing-concierge/img/f8457daf0bed059e.jpeg)

2. Download `uv` and install python 3.12 with the following command

```
curl -LsSf https://astral.sh/uv/0.7.2/install.sh | sh && \
source $HOME/.local/bin/env && \
uv python install 3.12
```

3. Now let's initialize the virtual environment of the purchasing concierge using `uv` , Run this command

```
uv sync --frozen
```

This will create the **.venv** directory and install the dependencies. Quick sneak peek on the **pyproject.toml** will give you information about the dependencies shown like this

dependencies = [
    "google-adk>=0.3.0",
    "gradio>=5.28.0",
    "httpx>=0.28.1",
    "jwcrypto>=1.5.6",
    "pydantic>=2.10.6",
    "pyjwt>=2.10.1",
    "sse-starlette>=2.3.3",
    "starlette>=0.46.2",
    "typing-extensions>=4.13.2",
    "uvicorn>=0.34.0",
]

4. To test the virtual env, create new file **main.py** and copy the following code

```
def main():
   print("Hello from purchasing-concierge-a2a!")

if __name__ == "__main__":
   main()
```

5. Then, run the following command

```
uv run main.py
```

You will get output like shown below

Using CPython 3.12
Creating virtual environment at: .venv
Hello from purchasing-concierge-a2a!

This shows that the python project is being set up properly.

Now we can move to the next step, configuring and deploying our remote seller agent

## 3. Deploying Remote Seller Agent - A2A Server to Cloud Run

In this step, we will deploy these two remote seller agents marked by the red box. The burger agent will be powered by CrewAI agent framework and the pizza agent will be powered by Langgraph agent, both of them are powered by Gemini Flash 2.0 model

![ba7eefb0c30f0c46.png](https://codelabs.developers.google.com/static/intro-a2a-purchasing-concierge/img/ba7eefb0c30f0c46.png)

## **Deploying the Remote Burger Agent**

The burger agent source code is under the **remote_seller_agents/burger_agent** directory. The agent initialization can be inspected on the **agent.py** script. Here is the code snippet of the initialized agent

```
from crewai import Agent, Crew, LLM, Task, Process
from crewai.tools import tool

...

model = LLM(
    model="vertex_ai/gemini-2.0-flash",  # Use base model name without provider prefix
)
burger_agent = Agent(
    role="Burger Seller Agent",
    goal=(
        "Help user to understand what is available on burger menu and price also handle order creation."
    ),
    backstory=("You are an expert and helpful burger seller agent."),
    verbose=False,
    allow_delegation=False,
    tools=[create_burger_order],
    llm=model,
)

agent_task = Task(
    description=self.TaskInstruction,
    output_pydantic=ResponseFormat,
    agent=burger_agent,
    expected_output=(
        "A JSON object with 'status' and 'message' fields."
        "Set response status to input_required if asking for user order confirmation."
        "Set response status to error if there is an error while processing the request."
        "Set response status to completed if the request is complete."
    ),
)

crew = Crew(
    tasks=[agent_task],
    agents=[burger_agent],
    verbose=False,
    process=Process.sequential,
)

inputs = {"user_prompt": query, "session_id": sessionId}
response = crew.kickoff(inputs)

...
```

Now, we need to prepare the **.env** variable first, let's copy the **.env.example** into **.env** file

```
cp remote_seller_agents/burger_agent/.env.example remote_seller_agents/burger_agent/.env
```

Now, open the **remote_seller_agents/burger_agent/.env** file and you will see the following content

AUTH_USERNAME=burgeruser123
AUTH_PASSWORD=burgerpass123
GCLOUD_LOCATION=us-central1
GCLOUD_PROJECT_ID={your-project-id}

The burger agent A2A Server runs using **Basic** HTTP Authentication ( using base64 encoded username and password ) and for the sake of this demo, we configure the allowed username and password here in the **.env** file. Now, please update the **GCLOUD_PROJECT_ID** variable to your current active project ID

Don't forget to save your changes, next we can directly deploy the services. We will inspect the code content later on. Run the following command to deploy it

```
gcloud run deploy burger-agent \
           --source remote_seller_agents/burger_agent \
           --port=8080 \
           --allow-unauthenticated \
           --min 1 \
           --region us-central1
```

When prompted that a container repository will be created for deploying from source, answer **Y**. After successful deployment it will show a log like this.

Service [burger-agent] revision [burger-agent-xxxxx-xxx] has been deployed and is serving 100 percent of traffic.
Service URL: https://burger-agent-xxxxxxxxx.us-central1.run.app

The `xxxx` part here will be a unique identifier when we deploy the service.

Now, let's try to go the `/.well-known/agent.json` route of those deployed burger agent services via browser and you should be see output like this

![7b4e9ffc00131552.png](https://codelabs.developers.google.com/static/intro-a2a-purchasing-concierge/img/7b4e9ffc00131552.png)

This is the burger agent card information that should be accessible for discovery purposes. We will discuss this later on. For now just remember the URL of our burger agent service, which we will utilize later on

## **Deploying the Remote Pizza Agent**

Similarly, pizza agent source code is under the **remote_seller_agents/pizza_agent** directory. The agent initialization can be inspected on the **agent.py** script. Here is the code snippet of the initialized agent

```
from langchain_google_vertexai import ChatVertexAI
from langgraph.prebuilt import create_react_agent

...

self.model = ChatVertexAI(
    model="gemini-2.0-flash",
    location=os.getenv("GCLOUD_LOCATION"),
    project=os.getenv("GCLOUD_PROJECT_ID"),
)
self.tools = [create_pizza_order]
self.graph = create_react_agent(
    self.model,
    tools=self.tools,
    checkpointer=memory,
    prompt=self.SYSTEM_INSTRUCTION,
    response_format=ResponseFormat,
)

...
```

Now, we need to prepare the **.env** variable first, let's copy the **.env.example** into **.env** file

```
cp remote_seller_agents/pizza_agent/.env.example remote_seller_agents/pizza_agent/.env
```

Now, open the **remote_seller_agents/pizza_agent/.env** file and you will see the following content

API_KEY=pizza123
GCLOUD_LOCATION=us-central1
GCLOUD_PROJECT_ID={your-project-id}

The pizza agent A2A Server runs using **Bearer** HTTP Authentication (using API Key) and for the sake of this demo, we configure the allowed API key here in the **.env** file. Now, please update the **GCLOUD_PROJECT_ID** variable to your current active project ID

Don't forget to save your changes, next we can directly deploy the services. We will inspect the code content later on. Run the following command to deploy it

```
gcloud run deploy pizza-agent \
           --source remote_seller_agents/pizza_agent \
           --port=8080 \
           --allow-unauthenticated \
           --min 1 \
           --region us-central1
```

After successful deployment it will show a log like this.

Service [pizza-agent] revision [pizza-agent-xxxxx-xxx] has been deployed and is serving 100 percent of traffic.
Service URL: https://pizza-agent-xxxxxxxxx.us-central1.run.app

The `xxxx` part here will be a unique identifier when we deploy the service.

Now, let's try to go the `/.well-known/agent.json` route of those deployed pizza agent services via browser and you should be see output like this

![88bd25001af5dcbc.png](https://codelabs.developers.google.com/static/intro-a2a-purchasing-concierge/img/88bd25001af5dcbc.png)

This is the pizza agent card information that should be accessible for discovery purposes. We will discuss this later on. For now just remember the URL of our pizza agent service.

At this point, we already successfully deploy both burger and pizza services to Cloud Run. Now let's discuss the core components of the A2A Server

## 4. Core Components of A2A Server

Now let's discuss the core concept and components of the A2A server

## **Agent Card**

Each of A2A Server must have an agent card that is accessible on the `/.well-known/agent.json` resource. This is to support the discovery phase on the A2A Client, which should give complete information and contexts on how to access the agent and know all of its capabilities. It's kinda similar with well documented API documentation using Swagger or Postman.

This is the content of our deployed burger agent agent card

```
{
  "name": "burger_seller_agent",
  "description": "Helps with creating burger orders",
  "url": "http://0.0.0.0:8080/",
  "version": "1.0.0",
  "capabilities": {
    "streaming": false,
    "pushNotifications": true,
    "stateTransitionHistory": false
  },
  "authentication": {
    "schemes": [
      "Basic"
    ]
  },
  "defaultInputModes": [
    "text",
    "text/plain"
  ],
  "defaultOutputModes": [
    "text",
    "text/plain"
  ],
  "skills": [
    {
      "id": "create_burger_order",
      "name": "Burger Order Creation Tool",
      "description": "Helps with creating burger orders",
      "tags": [
        "burger order creation"
      ],
      "examples": [
        "I want to order 2 classic cheeseburgers"
      ]
    }
  ]
}
```

These agent cards highlight many important components, such as agent skills, streaming capabilities, supported modalities, and authentication.

All of this information can be utilized to develop a proper communication mechanism so that the A2A client can communicate properly. The supported modality and authentication mechanism ensure the communication can be properly established, and the agent `skills` information can be embedded into A2A client system prompt to give the client's agent context about the remote agent capabilities and skills to be invoked. More detailed fields for this agent card can be found in [this documentation](https://google.github.io/A2A/specification/agent-card/#representation).

In our code, the implementation of agent card is established using [Pydantic](https://docs.pydantic.dev/latest/) on the **a2a_types.py** ( on the `remote_seller_agents/burger_agent` or `remote_seller_agents/pizza_agent` )

```
...

class AgentProvider(BaseModel):
    organization: str
    url: str | None = None


class AgentCapabilities(BaseModel):
    streaming: bool = False
    pushNotifications: bool = False
    stateTransitionHistory: bool = False


class AgentAuthentication(BaseModel):
    schemes: List[str]
    credentials: str | None = None


class AgentSkill(BaseModel):
    id: str
    name: str
    description: str | None = None
    tags: List[str] | None = None
    examples: List[str] | None = None
    inputModes: List[str] | None = None
    outputModes: List[str] | None = None


class AgentCard(BaseModel):
    name: str
    description: str | None = None
    url: str
    provider: AgentProvider | None = None
    version: str
    documentationUrl: str | None = None
    capabilities: AgentCapabilities
    authentication: AgentAuthentication | None = None
    defaultInputModes: List[str] = ["text"]
    defaultOutputModes: List[str] = ["text"]
    skills: List[AgentSkill]

...
```

And the object construction is on the `remote_seller_agents/burger_agent/__main__.py` reflected below

```
...

def main(host, port):
    """Starts the Burger Seller Agent server."""
    try:
        capabilities = AgentCapabilities(pushNotifications=True)
        skill = AgentSkill(
            id="create_burger_order",
            name="Burger Order Creation Tool",
            description="Helps with creating burger orders",
            tags=["burger order creation"],
            examples=["I want to order 2 classic cheeseburgers"],
        )
        agent_card = AgentCard(
            name="burger_seller_agent",
            description="Helps with creating burger orders",
            # The URL provided here is for the sake of demo,
            # in production you should use a proper domain name
            url=f"http://{host}:{port}/",
            version="1.0.0",
            authentication=AgentAuthentication(schemes=["Basic"]),
            defaultInputModes=BurgerSellerAgent.SUPPORTED_CONTENT_TYPES,
            defaultOutputModes=BurgerSellerAgent.SUPPORTED_CONTENT_TYPES,
            capabilities=capabilities,
            skills=[skill],
        )

        notification_sender_auth = PushNotificationSenderAuth()
        notification_sender_auth.generate_jwk()
        server = A2AServer(
            agent_card=agent_card,
            task_manager=AgentTaskManager(
                agent=BurgerSellerAgent(),
                notification_sender_auth=notification_sender_auth,
            ),
            host=host,
            port=port,
            auth_username=os.environ.get("AUTH_USERNAME"),
            auth_password=os.environ.get("AUTH_PASSWORD"),
        )

...
```

## **Task Definition and Task Manager**

One of the core components in A2A is the **_Task_** definition. It is adapting the payload format on top of the [JSON-RPC standard](https://www.jsonrpc.org/specification). In this demo, this is implemented using Pydantic on the **a2a_types.py** ( on the `remote_seller_agents/burger_agent` or `remote_seller_agents/pizza_agent` ) too in this section

```
...

## RPC Messages


class JSONRPCMessage(BaseModel):
    jsonrpc: Literal["2.0"] = "2.0"
    id: int | str | None = Field(default_factory=lambda: uuid4().hex)


class JSONRPCRequest(JSONRPCMessage):
    method: str
    params: dict[str, Any] | None = None

...

class SendTaskRequest(JSONRPCRequest):
    method: Literal["tasks/send"] = "tasks/send"
    params: TaskSendParams

class SendTaskStreamingRequest(JSONRPCRequest):
    method: Literal["tasks/sendSubscribe"] = "tasks/sendSubscribe"
    params: TaskSendParams

class GetTaskRequest(JSONRPCRequest):
    method: Literal["tasks/get"] = "tasks/get"
    params: TaskQueryParams

class CancelTaskRequest(JSONRPCRequest):
    method: Literal["tasks/cancel",] = "tasks/cancel"
    params: TaskIdParams

class SetTaskPushNotificationRequest(JSONRPCRequest):
    method: Literal["tasks/pushNotification/set",] = "tasks/pushNotification/set"
    params: TaskPushNotificationConfig

class GetTaskPushNotificationRequest(JSONRPCRequest):
    method: Literal["tasks/pushNotification/get",] = "tasks/pushNotification/get"
    params: TaskIdParams

class TaskResubscriptionRequest(JSONRPCRequest):
    method: Literal["tasks/resubscribe",] = "tasks/resubscribe"
    params: TaskIdParams

...
```

There are various task methods available to support different types of communication (e.g. sync, streaming, async ) and also configure notifications for the task status. A2A server can be flexibly configured to handle these task definition standards.

A2A server may be handling requests from different agents or users and be able to isolate each task perfectly. To better visualize the contexts of these, you can inspect the image below

![bf84e3517789fb9d.png](https://codelabs.developers.google.com/static/intro-a2a-purchasing-concierge/img/bf84e3517789fb9d.png)

Thus, each A2A server should be able to track incoming tasks and store proper information about it, usually each incoming request will have **task ID** and **session ID**. In our code, the implementation of this task manager is on the `remote_seller_agents/burger_agent/task_manager.py` (the pizza agent also share similar task manager)

```
...

class AgentTaskManager(InMemoryTaskManager):
    def __init__(
        self,
        agent: BurgerSellerAgent,
        notification_sender_auth: PushNotificationSenderAuth,
    ):
        super().__init__()
        self.agent = agent
        self.notification_sender_auth = notification_sender_auth

    ...

    async def on_send_task(self, request: SendTaskRequest) -> SendTaskResponse:
        """Handles the 'send task' request."""
        validation_error = self._validate_request(request)
        if validation_error:
            return SendTaskResponse(id=request.id, error=validation_error.error)

        await self.upsert_task(request.params)

        if request.params.pushNotification:
            if not await self.set_push_notification_info(
                request.params.id, request.params.pushNotification
            ):
                return SendTaskResponse(
                    id=request.id,
                    error=InvalidParamsError(
                        message="Push notification URL is invalid"
                    ),
                )

        task = await self.update_store(
            request.params.id, TaskStatus(state=TaskState.WORKING), None
        )
        await self.send_task_notification(task)

        task_send_params: TaskSendParams = request.params
        query = self._get_user_query(task_send_params)
        try:
            agent_response = self.agent.invoke(query, task_send_params.sessionId)
        except Exception as e:
            logger.error(f"Error invoking agent: {e}")
            raise ValueError(f"Error invoking agent: {e}")
        return await self._process_agent_response(request, agent_response)

    ...

    async def _process_agent_response(
        self, request: SendTaskRequest, agent_response: dict
    ) -> SendTaskResponse:
        """Processes the agent's response and updates the task store."""
        task_send_params: TaskSendParams = request.params
        task_id = task_send_params.id
        history_length = task_send_params.historyLength
        task_status = None

        parts = [{"type": "text", "text": agent_response["content"]}]
        artifact = None
        if agent_response["require_user_input"]:
            task_status = TaskStatus(
                state=TaskState.INPUT_REQUIRED,
                message=Message(role="agent", parts=parts),
            )
        else:
            task_status = TaskStatus(state=TaskState.COMPLETED)
            artifact = Artifact(parts=parts)
        task = await self.update_store(
            task_id, task_status, None if artifact is None else [artifact]
        )
        task_result = self.append_task_history(task, history_length)
        await self.send_task_notification(task)
        return SendTaskResponse(id=request.id, result=task_result)

   ...
```

From the above code, we can inspect that when processing incoming task ( the method `on_send_task` is executed when the incoming request method is `tasks/send` ) it will do several operations on updating task store ( `self.update_store` method call ) and sending notification ( `self.send_task_notification` method call ). This is one of the examples on how A2A server manages task status update and notification throughout the synchronous send task request.

## **Summary**

In short, so far our deployed A2A Server can support the 2 functionalities below:

1. Publishing the agent card on the `/.well-known/agent.json` route
2. Handle JSON-RPC request with method `tasks/send`

The entry point on starting these functionalities can be inspected on the **main.py** script ( on the `remote_seller_agents/burger_agent` or `remote_seller_agents/pizza_agent` ) . We can see that we need to configure the Agent Card first, then start the server in the code snippet below

```
...

capabilities = AgentCapabilities(pushNotifications=True)
skill = AgentSkill(
    id="create_pizza_order",
    name="Pizza Order Creation Tool",
    description="Helps with creating pizza orders",
    tags=["pizza order creation"],
    examples=["I want to order 2 pepperoni pizzas"],
)
agent_card = AgentCard(
    name="pizza_seller_agent",
    description="Helps with creating pizza orders",
    # The URL provided here is for the sake of demo,
    # in production you should use a proper domain name
    url=f"http://{host}:{port}/",
    version="1.0.0",
    authentication=AgentAuthentication(schemes=["Bearer"]),
    defaultInputModes=PizzaSellerAgent.SUPPORTED_CONTENT_TYPES,
    defaultOutputModes=PizzaSellerAgent.SUPPORTED_CONTENT_TYPES,
    capabilities=capabilities,
    skills=[skill],
)

...

server = A2AServer(
    agent_card=agent_card,
    task_manager=AgentTaskManager(
        agent=PizzaSellerAgent(),
        notification_sender_auth=notification_sender_auth,
    ),
    host=host,
    port=port,
    api_key=os.environ.get("API_KEY"),
)

...

logger.info(f"Starting server on {host}:{port}")
server.start()

...
```

## 5. Deploying the Purchasing Concierge - A2A Client to Cloud Run

In this step, we will deploy the purchasing concierge agent. This agent is the one that we will interact with.

![857aa91382185439.png](https://codelabs.developers.google.com/static/intro-a2a-purchasing-concierge/img/857aa91382185439.png)

The source code of our purchasing concierge agent is under the **purchasing_concierge** directory. The agent initialization can be inspected on the **purchasing_agent.py** script. Here is the code snippet of the initialized agent.

```
from google.adk import Agent

...

def create_agent(self) -> Agent:
    return Agent(
        model="gemini-2.0-flash-001",
        name="purchasing_agent",
        instruction=self.root_instruction,
        before_model_callback=self.before_model_callback,
        description=(
            "This purchasing agent orchestrates the decomposition of the user purchase request into"
            " tasks that can be performed by the seller agents."
        ),
        tools=[
            self.list_remote_agents,
            self.send_task,
        ],
    )

...
```

Now, we need to prepare the **.env** variable first, let's copy the **.env.example** into **.env** file

```
cp purchasing_concierge/.env.example purchasing_concierge/.env
```

Now, open the **purchasing_concierge/.env** file and you will see the following content

PIZZA_SELLER_AGENT_AUTH=pizza123
PIZZA_SELLER_AGENT_URL=http://localhost:10000
BURGER_SELLER_AGENT_AUTH=burgeruser123:burgerpass123
BURGER_SELLER_AGENT_URL=http://localhost:10001
GOOGLE_GENAI_USE_VERTEXAI=TRUE
GOOGLE_CLOUD_PROJECT={your-project-id}
GOOGLE_CLOUD_LOCATION=us-central1

This agent will be communicating with the burger and pizza agent, thus we need to provide the proper credentials for both of them. Now, please update the **GCLOUD_PROJECT_ID** variable to your current active project ID.

Now, we also need to update the **PIZZA_SELLER_AGENT_URL** and **BURGER_SELLER_AGENT_URL** with the Cloud Run URL from previous steps. If you forget about this, let's visit the Cloud Run console. Type "Cloud Run" on the search bar on top of your console and right click on the Cloud Run icon to open it in a new tab

![1adde569bb345b48.png](https://codelabs.developers.google.com/static/intro-a2a-purchasing-concierge/img/1adde569bb345b48.png)

You should see our previous deployed remote seller agent services like shown below

![179e55cc095723a8.png](https://codelabs.developers.google.com/static/intro-a2a-purchasing-concierge/img/179e55cc095723a8.png)

Now to see the public URL of those services, click on the one of the service and you'll be redirected to the Service details page. You can see the URL on the top area right beside the Region information

![64c01403a92b1107.png](https://codelabs.developers.google.com/static/intro-a2a-purchasing-concierge/img/64c01403a92b1107.png)

Copy and paste the value of this URL into the **PIZZA_SELLER_AGENT_URL** and **BURGER_SELLER_AGENT_URL** respectively.

The final environment variable should look similar to this one

PIZZA_SELLER_AGENT_AUTH=pizza123
PIZZA_SELLER_AGENT_URL=https://pizza-agent-xxxxx.us-central1.run.app
BURGER_SELLER_AGENT_AUTH=burgeruser123:burgerpass123
BURGER_SELLER_AGENT_URL=https://burger-agent-xxxxx.us-central1.run.app
GOOGLE_GENAI_USE_VERTEXAI=TRUE
GOOGLE_CLOUD_PROJECT={your-project-id}
GOOGLE_CLOUD_LOCATION=us-central1

Now, we are ready to deploy our purchasing concierge agent. To deploy this agent run the command below

```
gcloud run deploy purchasing-concierge \
           --source . \
           --port=8080 \
           --allow-unauthenticated \
           --min 1 \
           --region us-central1 \
           --memory 1024Mi
```

After successful deployment it will show a log like this.

Service [purchasing-concierge] revision [purchasing-concierge-xxxxx-xxx] has been deployed and is serving 100 percent of traffic.
Service URL: https://purchasing-concierge-xxxxxx.us-central1.run.app

The `xxxx` part here will be a unique identifier when we deploy the service.

Now, we can try to interact with the purchasing concierge agent via the UI. When you access the service URL, you should be able to see the [Gradio](https://www.gradio.app/) web interface like shown below

![3d705381f9219bf3.png](https://codelabs.developers.google.com/static/intro-a2a-purchasing-concierge/img/3d705381f9219bf3.png)

Now, let's discuss what are the core components and typical flow of A2A clients.

## 6. Core Components of A2A Client

![73dae827aa9bddc3.png](https://codelabs.developers.google.com/static/intro-a2a-purchasing-concierge/img/73dae827aa9bddc3.png)

The image shown above is the typical flow of A2A interactions:

1. Client will try to find any published agent card in the provided remote agent URL in the route `/.well-known/agent.json`
2. Then, when necessary it will send a Task to that agent with the message and necessary metadata parameters ( E.g. session ID, historical context, etc )
3. The A2A server will authenticate and process the request, if the server support push notifications, it will also try to publish some notifications throughout the task processing
4. After finished, the A2A server will send the response artifact back to the client

The core objects for above interactions is these items (details can be [read here](https://google.github.io/A2A/specification/agent-to-agent-communication/#agent-to-agent-communication)) :

* **Task**: stateful entity that allows Clients and Remote Agents to achieve a specific outcome and generate results
* **Artifact:** an end result of a **Task**
* **Message:** any content that is **not an Artifact**. For example - agent thoughts, user context, instructions, errors, status, or metadata
* **Part:** A fully formed piece of content exchanged between a client and a remote agent as **part of a Message or an Artifact**. Part can be a text, image, video, file, etc.
* **Push Notifications (Optional):** a secure notification mechanism whereby an agent can notify a client of an update outside of a connected session

## **Card Discovery**

When A2A Client service is being spun up, the typical process is to try to get the agent card information and store it to easily access it when needed. We can check it in the **purchasing_concierge/purchasing_agent.py** script here

```
...

class PurchasingAgent:
    """The purchasing agent.

    This is the agent responsible for choosing which remote seller agents to send
    tasks to and coordinate their work.
    """

    def __init__(
        self,
        remote_agent_addresses: List[str],
        task_callback: TaskUpdateCallback | None = None,
    ):
        self.task_callback = task_callback
        self.remote_agent_connections: dict[str, RemoteAgentConnections] = {}
        self.cards: dict[str, AgentCard] = {}
        for address in remote_agent_addresses:
            card_resolver = A2ACardResolver(address)
            try:
                card = card_resolver.get_agent_card()
                # The URL accessed here should be the same as the one provided in the agent card
                # However, in this demo we are using the URL provided in the key arguments
                remote_connection = RemoteAgentConnections(
                    agent_card=card, agent_url=address
                )
                self.remote_agent_connections[card.name] = remote_connection
                self.cards[card.name] = card
            except httpx.ConnectError:
                print(f"ERROR: Failed to get agent card from : {address}")
        agent_info = []
        for ra in self.list_remote_agents():
            agent_info.append(json.dumps(ra))
        self.agents = "\n".join(agent_info)

...
```

We will then provide the remote agents contexts in our purchasing concierge system prompt, and also provide tooling to send the task to the agent. This is the prompt and tool we provide to our ADK agent here

```
...

def root_instruction(self, context: ReadonlyContext) -> str:
    current_agent = self.check_active_agent(context)
    return f"""You are an expert purchasing delegator that can delegate the user product inquiry and purchase request to the
appropriate seller remote agents.

Execution:
- For actionable tasks, you can use `send_task` to assign tasks to remote agents to perform.
- When the remote agent is repeatedly asking for user confirmation, assume that the remote agent doesn't have access to user's conversation context. 
So improve the task description to include all the necessary information related to that agent
- Never ask user permission when you want to connect with remote agents. If you need to make connection with multiple remote agents, directly
connect with them without asking user permission or asking user preference
- Always show the detailed response information from the seller agent and propagate it properly to the user. 
- If the remote seller is asking for confirmation, rely the confirmation question to the user if the user haven't do so. 
- If the user already confirmed the related order in the past conversation history, you can confirm on behalf of the user
- Do not give irrelevant context to remote seller agent. For example, ordered pizza item is not relevant for the burger seller agent
- Never ask order confirmation to the remote seller agent 

Please rely on tools to address the request, and don't make up the response. If you are not sure, please ask the user for more details.
Focus on the most recent parts of the conversation primarily.

If there is an active agent, send the request to that agent with the update task tool.

Agents:
{self.agents}

Current active seller agent: {current_agent["active_agent"]}
"""

...

async def send_task(self, agent_name: str, task: str, tool_context: ToolContext):
    """Sends a task to remote seller agent

    This will send a message to the remote agent named agent_name.

    Args:
        agent_name: The name of the agent to send the task to.
        task: The comprehensive conversation context summary
            and goal to be achieved regarding user inquiry and purchase request.
        tool_context: The tool context this method runs in.

    Yields:
        A dictionary of JSON data.
    """
    if agent_name not in self.remote_agent_connections:
        raise ValueError(f"Agent {agent_name} not found")
    state = tool_context.state
    state["active_agent"] = agent_name
    client = self.remote_agent_connections[agent_name]
    if not client:
        raise ValueError(f"Client not available for {agent_name}")
    if "task_id" in state:
        taskId = state["task_id"]
    else:
        taskId = str(uuid.uuid4())
    sessionId = state["session_id"]
    task: Task
    messageId = ""
    metadata = {}
    if "input_message_metadata" in state:
        metadata.update(**state["input_message_metadata"])
        if "message_id" in state["input_message_metadata"]:
            messageId = state["input_message_metadata"]["message_id"]
    if not messageId:
        messageId = str(uuid.uuid4())
    metadata.update(**{"conversation_id": sessionId, "message_id": messageId})
    request: TaskSendParams = TaskSendParams(
        id=taskId,
        sessionId=sessionId,
        message=Message(
            role="user",
            parts=[TextPart(text=task)],
            metadata=metadata,
        ),
        acceptedOutputModes=["text", "text/plain"],
        # pushNotification=None,
        metadata={"conversation_id": sessionId},
    )
    task = await client.send_task(request, self.task_callback)
    # Assume completion unless a state returns that isn't complete
    state["session_active"] = task.status.state not in [
        TaskState.COMPLETED,
        TaskState.CANCELED,
        TaskState.FAILED,
        TaskState.UNKNOWN,
    ]
    if task.status.state == TaskState.INPUT_REQUIRED:
        # Force user input back
        tool_context.actions.escalate = True
    elif task.status.state == TaskState.COMPLETED:
        # Reset active agent is task is completed
        state["active_agent"] = "None"

    response = []
    if task.status.message:
        # Assume the information is in the task message.
        response.extend(convert_parts(task.status.message.parts, tool_context))
    if task.artifacts:
        for artifact in task.artifacts:
            response.extend(convert_parts(artifact.parts, tool_context))
    return response

...
```

In the prompt, we give our purchasing concierge agent all available remote agents name and description, and in the tool `self.send_task` we provide a mechanism to retrieve the appropriate client to connect to the agent and send the required metadata using the `TaskSendParams` object.

In the tool we also can specify how the agent will behave if somehow a task fails to be completed. And finally we need to handle the response artifact returned when the task is completed

## 7. Integration Testing and Payload Inspection

Now let's try the following conversation and inspect our purchasing concierge UI and service logs. Try to have a conversation like this :

* Show me burger and pizza menu
* I want to order 1 bbq chicken pizza and 1 spicy cajun burger

And continue the conversation until you finish the order. Inspect how the interaction is going and what is the tool call and response? The following image is an example of the interaction result.

![b06863bd746b4d1c.png](https://codelabs.developers.google.com/static/intro-a2a-purchasing-concierge/img/b06863bd746b4d1c.png)

![f550a0e65ac17fca.png](https://codelabs.developers.google.com/static/intro-a2a-purchasing-concierge/img/f550a0e65ac17fca.png)

![5dea2fba956548b1.png](https://codelabs.developers.google.com/static/intro-a2a-purchasing-concierge/img/5dea2fba956548b1.png)

![2da5d77fefc37cb9.png](https://codelabs.developers.google.com/static/intro-a2a-purchasing-concierge/img/2da5d77fefc37cb9.png)

We can see that communicating with 2 different agents yields 2 different behaviors and A2A can handle this well. The burger seller agent directly accepts our purchasing agent request, whereas the pizza agent needs our confirmation before proceeding with our request and after we confirm the agent can rely the confirmation to the pizza agent

Now, let's see the exchanged data on our **purchasing-agent** service log. First let's visit our cloud run console, **type "Cloud Run" on the search bar** on top of your console and **right click** on the Cloud Run icon to **open it in a new browser tab**

![1adde569bb345b48.png](https://codelabs.developers.google.com/static/intro-a2a-purchasing-concierge/img/1adde569bb345b48.png)

Now, you should see our previous deployed services like shown below. Click on the **purchasing-concierge**

![7d8a0b9a227e4372.png](https://codelabs.developers.google.com/static/intro-a2a-purchasing-concierge/img/7d8a0b9a227e4372.png)

Now you'll be in the Service details page, then click on the **Logs** tab

![7a45204e086ea264.png](https://codelabs.developers.google.com/static/intro-a2a-purchasing-concierge/img/7a45204e086ea264.png)

Now, we will see the logs of our deployed **purchasing-concierge** service. Try to scroll down and find the recent log about our interactions

![2f223615795c19e5.png](https://codelabs.developers.google.com/static/intro-a2a-purchasing-concierge/img/2f223615795c19e5.png)

![6226653668a0f83b.png](https://codelabs.developers.google.com/static/intro-a2a-purchasing-concierge/img/6226653668a0f83b.png)

You will see that the request and response between A2A Client and Server will be in the JSON-RPC format and conform to the A2A standard.

Now, we have finished the basic concepts of A2A and see how it implemented as client and server architecture

## 8. Clean up

To avoid incurring charges to your Google Cloud account for the resources used in this codelab, follow these steps:

1. In the Google Cloud console, go to the [Manage resources](https://console.cloud.google.com/iam-admin/projects?_ga=2.137741431.690084714.1674832835-1977883585.1670853686) page.
2. In the project list, select the project that you want to delete, and then click **Delete**.
3. In the dialog, type the project ID, and then click **Shut down** to delete the project.
4. Alternatively you can go to [Cloud Run](https://console.cloud.google.com/run) on the console, select the service you just deployed and delete.

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.