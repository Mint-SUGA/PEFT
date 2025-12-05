import gradio as gr
from llama_cpp import Llama

llm = Llama.from_pretrained(
    repo_id="YT07/3B_Q8_0",
    filename="model-3b-Q8_0.gguf",
    n_ctx=2048,
    n_threads=2,
    verbose=False
)

RELATIONSHIP_OPTIONS = [
    "Classmate",
    "Friend",
    "Colleague",
    "Date",
    "Other (custom)"
]

SCENARIO_OPTIONS = {
    "Classmate": [
        "Study break",
        "Group project",
        "After class",
        "Other (custom)"
    ],
    "Friend": [
        "Catching up",
        "Weekend hangout",
        "Birthday / Party",
        "Other (custom)"
    ],
    "Colleague": [
        "Morning greeting",
        "Afternoon team fika",
        "Welcome fika for new employee",
        "Other (custom)"
    ],
    "Date": [
        "First date",
        "Coffee date follow-up",
        "Outdoor picnic fika",
        "Other (custom)"
    ],
    "Other (custom)": [
        "Other (custom)"
    ]
}

BACKGROUND_OPTIONS = [
    "I'm new to Sweden and nervous about cultural differences",
    "I want to make more Swedish friends",
    "I struggle with small talk in Swedish",
    "I want to improve my professional networking",
    "I'm preparing for an important meeting",
    "Other (custom)"
]

def generate_response(relationship, scenario, background):
    prompt = f"""<|begin_of_text|><|start_header_id|>system<|end_header_id|>

You are an expert in Swedish social culture and cross-cultural communication. You need to help foreigners in Sweden do fika (coffee break) conversations with confidence. You provide practical, culturally-sensitive advice in a friendly, encouraging tone.<|eot_id|>
<|start_header_id|>user<|end_header_id|>

I need help preparing for a fika in Sweden. Here are my details:

- Relationship with the Swedish person: {relationship}
- Scenario: {scenario}
- My background: {background}

Please provide a comprehensive fika conversation guide with these sections:

1. PERFECT OPENING: A natural, culturally-appropriate opening line
2. 3 SAFE TOPICS: Three conversation topics that work well in this situation, with example questions
3. 2 TOPICS TO AVOID: Topics to steer clear of and why
4. GRACEFUL EXIT: How to end the conversation naturally
5. SWEDISH CULTURAL TIP: One specific insight about Swedish culture relevant to this scenario

Format your response in clear English with emojis for each section. Keep it practical and encouraging.<|eot_id|>
<|start_header_id|>assistant<|end_header_id|>

"""
    response = llm(
        prompt,
        max_tokens=512,
        temperature=0.7,
        top_p=0.9,
        stop=["<|eot_id|>", "<|end_of_text|>"],
        echo=False
    )
    return response["choices"][0]["text"].strip()

def get_fika_guide(relationship, scenario, background):
    try:
        if relationship == "Other (custom)":
            relationship = "Custom relationship (user provided)"

        if scenario == "Other (custom)":
            scenario = "Custom scenario (user provided)"

        if background == "Other (custom)":
            background = "Custom background (user provided)"

        response = generate_response(relationship, scenario, background)

        header = f"""
# ☕️ FIKA Suggestions

**Relationship:** {relationship}
**Scenario:** {scenario}
**Background:** {background}

---

"""
        return header + response

    except Exception as e:
        return f"Error generating guide: {str(e)}"

with gr.Blocks() as demo:

    gr.Markdown("# 🇸🇪 FIKA Helper")
    gr.Markdown("*A step-to-step guide to great FIKA conversations*")

    with gr.Column() as step1:
        gr.Markdown("### Step 1: Choose Relationship")
        relationship_radio = gr.Radio(
            choices=RELATIONSHIP_OPTIONS,
            label="Who are you meeting for fika?",
            interactive=True,
            value=None
        )
        relationship_custom = gr.Textbox(
            label="Custom Relationship (if you selected 'Other')",
            placeholder="e.g., teacher, neighbor, etc.",
            visible=False
        )

    with gr.Column(visible=False) as step2:
        gr.Markdown("### Step 2: Choose Scenario")
        scenario_radio = gr.Radio(
            choices=[],
            label="What type of fika situation is this?",
            interactive=True,
            value=None
        )
        scenario_custom = gr.Textbox(
            label="Custom Scenario (if you selected 'Other')",
            placeholder="e.g., After-work, Holiday, etc.",
            visible=False
        )

    with gr.Column(visible=False) as step3:
        gr.Markdown("### Step 3: Choose Background")
        background_radio = gr.Radio(
            choices=BACKGROUND_OPTIONS,
            label="What's your main situation?",
            interactive=True,
            value=None
        )
        background_custom = gr.Textbox(
            label="Custom Background (if you selected 'Other')",
            placeholder="e.g., I want to practice Swedish, I'm preparing for a job interview, etc.",
            visible=False
        )

        with gr.Row(visible=False) as generate_row:
            generate_btn = gr.Button(
                "✨ Generate Fika Guide",
                variant="primary",
                size="lg"
            )

    with gr.Column(visible=False) as result_box:
        gr.Markdown("### Your Fika Guide")
        output = gr.Markdown()
        restart_btn = gr.Button("🔄 Start Over", variant="secondary")

    def update_scenario_options(relationship):
        if relationship == "Other (custom)":
            return (
                gr.update(choices=["Other (custom)"], value=None, visible=True),
                gr.update(visible=True),
                gr.update(visible=True),
                gr.update(visible=False),
                gr.update(visible=False),
                gr.update(visible=False),
                gr.update(visible=False),
            )
        else:
            rel_key = relationship.split("(")[0].strip() if "(" in relationship else relationship

            if rel_key in SCENARIO_OPTIONS:
                return (
                    gr.update(choices=SCENARIO_OPTIONS[rel_key], value=None, visible=True),
                    gr.update(visible=False),
                    gr.update(visible=True),
                    gr.update(visible=False),
                    gr.update(visible=False),
                    gr.update(visible=False),
                    gr.update(visible=False),
                )
            else:
                return (
                    gr.update(choices=SCENARIO_OPTIONS["Colleague"], value=None, visible=True),
                    gr.update(visible=False),
                    gr.update(visible=True),
                    gr.update(visible=False),
                    gr.update(visible=False),
                    gr.update(visible=False),
                    gr.update(visible=False),
                )

    def update_background_options(scenario):
        if scenario == "Other (custom)":
            return (
                gr.update(visible=True),
                gr.update(visible=True),
                gr.update(visible=False),
                gr.update(visible=False)
            )
        else:
            return (
                gr.update(visible=False),
                gr.update(visible=True),
                gr.update(visible=False),
                gr.update(visible=False)
            )

    def update_generate_button(background):
        if background == "Other (custom)":
            return (
                gr.update(visible=True),
                gr.update(visible=True),
                gr.update(visible=False)
            )
        else:
            return (
                gr.update(visible=False),
                gr.update(visible=True),
                gr.update(visible=False)
            )

    def generate_guide(relationship, scenario, background, rel_custom, scen_custom, bg_custom):
        yield "⏳ **Generating your personalized Fika guide...**\n\nThis will just take a moment!", gr.update(visible=True)
        final_relationship = rel_custom if relationship == "Other (custom)" and rel_custom else relationship
        final_scenario = scen_custom if scenario == "Other (custom)" and scen_custom else scenario
        final_background = bg_custom if background == "Other (custom)" and bg_custom else background
        guide = get_fika_guide(final_relationship, final_scenario, final_background)
        yield guide, gr.update(visible=True)

    def reset_all():
      return (
          gr.update(value=None),
          gr.update(value="", visible=False),
          gr.update(visible=False),
          gr.update(choices=[], value=None),
          gr.update(value="", visible=False),
          gr.update(visible=False),
          gr.update(value=None),
          gr.update(value="", visible=False),
          gr.update(visible=False),
          gr.update(visible=False),
          gr.update(value="")
      )

    relationship_radio.change(
        fn=update_scenario_options,
        inputs=relationship_radio,
        outputs=[
            scenario_radio,
            relationship_custom,
            step2,
            step3,
            scenario_custom,
            generate_row,
            result_box
        ]
    )

    scenario_radio.change(
        fn=update_background_options,
        inputs=scenario_radio,
        outputs=[
            scenario_custom,
            step3,
            generate_row,
            result_box
        ]
    )

    background_radio.change(
        fn=update_generate_button,
        inputs=background_radio,
        outputs=[
            background_custom,
            generate_row,
            result_box
        ]
    )

    generate_btn.click(
        fn=generate_guide,
        inputs=[
            relationship_radio, scenario_radio, background_radio,
            relationship_custom, scenario_custom, background_custom
        ],
        outputs=[output, result_box]
    )

    restart_btn.click(
        fn=reset_all,
        outputs=[
            relationship_radio,
            relationship_custom,
            step2,
            scenario_radio,
            scenario_custom,
            step3,
            background_radio,
            background_custom,
            generate_row,
            result_box,
            output
        ]
    )

if __name__ == "__main__":
    demo.launch()