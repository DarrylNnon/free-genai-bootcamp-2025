# Preweek - Livestream - Solution Architecting GenAI

In this preweek video, i develop my skills in genai and contribute to the architecture diagram of this bootcamp using lucichart.

I believe, practicing by doing the hard work is making me confident by building project-based learning with Andrew.

life is all about making choice and i choose to make myself valuable now and for the future by understanding, practicing and teaching all the skills that i learn cause i believe life is a teachin process.

# What are we building?

I have been hired as an AI Engineer for a Language learning school to augment the learning experience for student taking instructor-led classes.

I will be doing the following:
    - Augmenting the main web-app to include GenAI functionality
    - Creating a series of projects to act as learning activities for students.

    - Preparing the company to be production-ready with their GenAI Offerings

    - I can use any language i want.

    So because i live in romanian and i already speak french and english as a native i guess my choice is going to be to build this in "romanian language"

# Always remember that we're building the bridge as we cross it.

we will face challenges, struggles, etc.. but we will figure things out.

![alt text](image-1.png)


# Romanian alphabet language that i choose to utilise.

![alt text](image.png)

# local hardware

i have a dell "intel core i5 vpro  Dell Latitude 7480 13-Inch Laptop, Core i5-6300U, 8GB RAM, 256GB SSD, Windows 10"

# there is no wrong answer.

I will do my best to make sure i understand and be able to explain everything i learn in simple terms.

# what i will journal?

- hypotesis and technical uncertainty
- technical exploration
- final observations and outcomes

# Rola Dali explanation on the architecting GenAI System diagram

- the first question is 
Predictive ML vs GenAI ( chosing the right tool for the job)

![alt text](image-2.png)

#  GenAI Architecture:
Ground o: A model Call

<img width="571" height="272" alt="image" src="https://github.com/user-attachments/assets/0d29bf2c-796c-4799-b1bf-a953c25c7321" />

- Enhance Context/model input
  
  <img width="645" height="336" alt="image" src="https://github.com/user-attachments/assets/b7b8249c-22e0-4cb1-a788-523d2cde6332" />

  more parameters more brainsell

- put Gurdrails: input & output controls
  guardrails prevent and it is use for compliance , you choose what come in and out:

  <img width="571" height="343" alt="image" src="https://github.com/user-attachments/assets/d45b08ff-254d-4027-91b1-5baa86322b2a" />

  
- Abstract model interaction: add model router and gateway

<img width="634" height="344" alt="image" src="https://github.com/user-attachments/assets/392cabe5-e134-42e0-8921-8f97eb43ea8a" />

- Reduce latency with caches

  <img width="617" height="335" alt="image" src="https://github.com/user-attachments/assets/3ca7318d-0660-4cc4-8def-66be6d00d460" />

- add functionality with agents

  <img width="576" height="351" alt="image" src="https://github.com/user-attachments/assets/1bc03f59-729f-417d-b0a7-771a92dab60f" />

- other functionalities
  
add authentication & authorization; add state and session management; add monitoring & observability; add pipeline orchestration; add Human Feedback.


# Architecting GenAI

Architecting GenAI

Difficulty: Level 100

Architecting Link: Lucid Chart

Business Goal:
As a Solution Architect after consulting with real-world AI Engineers, you have been tasked to create architectural diagram(s) that serve as a teaching aid to help stakeholders understand their key components of GenAI workloads. The outcome is to help let stakeholders visualize possible technical paths, technical uncertainty when adopting GenAI.

We are guiding key stakeholders through the technical landscape without directly prescribing solutions, while fostering informed discussions about infrastructure choices, integration patterns, and system dependencies across the organization.

We can use all levels of technical diagramming to achieve our goal.

link for the full business goal homework:

```sh
https://docs.google.com/document/d/1KVDTDF4t8VtI69F5KMo67KoTBXgVhsd2O9hK-uPh2rA/edit?usp=sharing
```

link for the conceptual diagram architecture:

https://lucid.app/lucidchart/c7945e5c-a177-410c-8a24-2481a29563f1/edit?invitationId=inv_aef7b30b-bf51-4cc6-a320-4e5f30574496&page=wfKOB.kyPhrS#


<img width="420" height="305" alt="image" src="https://github.com/user-attachments/assets/e19b5bb6-0637-41ca-8ff0-2685c91c0817" />


# Asumptions

We are going to hook up a single serve fin our office to the internet and we should have enough bandwith to serve the 300 students.

# Data strategy

There is a concerned of copyrighted materials, so we must purchase and supply materials and store them for access in our database.

# Considerations

We are considering using IBM Granite because its a truley open-source model with training data that is traceable so we can avoid any copyright issues and we are able to know what is going on in the model.

https://huggingface.co/ibm-granite

