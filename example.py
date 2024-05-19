from swarms import Agent
from swarms.models.llama3_hosted import llama3Hosted


# Initialize the agent
agent = Agent(
    agent_name="Transcript Generator",
    agent_description=(
        "Generate a transcript for a youtube video on what swarms" " are!"
    ),
    llm=llama3Hosted(),
    max_loops="auto",
    autosave=True,
    dashboard=False,
    streaming_on=True,
    verbose=True,
    stopping_token="<DONE>",
    interactive=True,
    state_save_file_type="json",
    saved_state_path="transcript_generator.json",
)

# Run the Agent on a task
out = agent.run(
    "Generate a transcript for a youtube video on what swarms are!"
)
print(out)
