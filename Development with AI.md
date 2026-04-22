## Thinking Principles during Vibe Coding

I aim to define a clear vision for the app before building with AI. I first clarified the product logic, then used a PRD prompt template to direct AI in structuring, refining, and implementing the idea. This helped me keep the project realistic, cut unnecessary complexity, and stay focused on delivering a working MVP.
### Logical Thinking + AI: Defining what the app is

My first step was to define what the app actually is and what it is not. I used logical thinking to decide that this should not be a broad project management tool or a replacement for platforms like Slack, Wrike, or shared documents. Instead, it should be a focused internal request-tracking app where one person submits a request, another person responds to it, and both can track it clearly from start to finish.

Once I had that definition, I used AI to pressure-test the idea. I prompted it with the app concept and asked it to help build a PRD around that specific use case. The value of AI here was not that it invented the concept for me, but that it helped me organize and sharpen the concept after I had already decided on the core purpose.

### Analytical Thinking + AI: Clarifying the objective and user flow

After defining the app, I used analytical thinking to identify the main objective: reduce the messiness of file and response requests that often get buried in chat threads.

From there, I broke the product into a simple user flow:
1. submit a request
2. assign the request to someone
3. track the status
4. respond with a note or delivered item
5. mark the request complete

I then used AI to turn that flow into a more structured PRD. My prompts were specific about what I wanted back. I asked for sections such as product overview, problem statement, user workflow, MVP features, edge cases, and value proposition. That made the AI output more useful because it had a clear structure to follow instead of giving me a vague brainstorm.

This was also the stage where I used AI to compare feature ideas and decide which ones actually supported the main objective versus which ones were just nice-to-have.

### Computational Thinking + AI: Turning the idea into app logic

Once the workflow was clear, I moved into computational thinking by translating the idea into app logic and rules.

I identified the core fields each request needed:
- title
- request type
- description
- requester
- assignee
- priority
- status
- due date

I also defined some basic rules:
- certain fields should be required
- requests should move through a fixed set of status values
- users should be able to filter by sender, receiver, priority, and status
- the app should distinguish between sent and received requests

AI was useful here because I could give it these constraints directly. Rather than asking it to “build an app,” I gave it specific technical directions such as:
- use Python
- use Streamlit
- keep it to one page
- keep persistence lightweight
- avoid unnecessary features like authentication, integrations, and production infrastructure

The more specific I was, the better the output became. This was one of the biggest lessons of the project: AI performs much better when the problem is already framed clearly.

### Procedural Thinking + AI: Deciding how to succeed and what to cut

Procedural thinking helped me define what success looked like for the user and for the project.

For the user, success means following a simple repeatable process:
- create a clear request
- assign ownership
- use filters to stay organized
- update status consistently
- complete the request visibly

For the project, success meant delivering a working MVP by the deadline. This required reducing scope.

I originally explored more features, including additional delight or customization ideas, but I used AI as a tool to help think through tradeoffs and then intentionally reduced the feature set. I narrowed the project down to the two most important milestones:
- submit request and respond
- organize request lists

This helped me avoid building too much and gave the project a cleaner backbone. AI was useful in surfacing possibilities, but the important part was deciding what not to build.

### Context + AI: Improving output through better inputs

Throughout the project, I learned that the quality of AI output depends heavily on context.

The most useful prompts included:
- the core problem the app should solve
- the target users
- the one-page MVP constraint
- my technical stack
- the fact that it was an entry-level pre-work project
- specific feature priorities
- my environment details
- exact error messages when debugging

I also found that AI worked better when I asked for smaller, more specific outputs. For example, it was more effective to ask for:
- a PRD with defined sections
- a one-page MVP layout
- a minimal technical approach
- a simplified feature set
- targeted debugging help using the exact error

rather than asking it to generate the entire app in one large step.

### Overall Approach

The strongest results came from combining structured thinking with specific AI prompting. My process was not “let AI make the app.” It was:

1. define the product clearly
2. analyze the main workflow
3. translate that workflow into app logic
4. reduce the feature set to what could realistically be built
5. give AI specific product and technical prompts
6. use AI again for targeted debugging and refinement

This combined approach helped me keep the project focused, realistic, and aligned with the goal of producing a small but fully working MVP.
