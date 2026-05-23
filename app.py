import gradio as gr
from graph import run_debate

def verify_claim(claim: str):
    if not claim.strip():
        return "Please enter a claim.", "", "", "", ""

    result = run_debate(claim)

    # Format verdict with emoji
    verdict_map = {
        "TRUE": "✅ TRUE",
        "FALSE": "❌ FALSE",
        "UNVERIFIABLE": "⚠️ UNVERIFIABLE"
    }
    verdict = verdict_map.get(result["verdict"], result["verdict"])
    confidence = f"{result['confidence']*100:.0f}%"
    reasoning = result["reasoning"]
    advocate = result["advocate_argument"]
    refuter = result["refuter_argument"]
    sources = "\n".join(f"• {s}" for s in result["sources"])

    return verdict, confidence, reasoning, advocate, refuter, sources


with gr.Blocks(theme=gr.themes.Soft(), title="Indian News Fact Verifier") as demo:
    gr.Markdown("# 🇮🇳 Indian News Fact Verifier\nMulti-agent AI debate system")

    claim_input = gr.Textbox(
        label="Enter a news claim to verify",
        placeholder="e.g. India's GDP grew 8.2% in Q3 2024",
        lines=2
    )
    verify_btn = gr.Button("⚖️ Verify Claim", variant="primary")

    with gr.Row():
        verdict_out = gr.Textbox(label="Verdict", interactive=False)
        confidence_out = gr.Textbox(label="Confidence", interactive=False)

    reasoning_out = gr.Textbox(label="Judge's Reasoning", lines=3, interactive=False)

    with gr.Accordion("View Full Debate", open=False):
        with gr.Row():
            advocate_out = gr.Textbox(label="✅ Advocate (TRUE case)", lines=8, interactive=False)
            refuter_out = gr.Textbox(label="❌ Refuter (FALSE case)", lines=8, interactive=False)

    sources_out = gr.Textbox(label="Key Evidence Used", lines=4, interactive=False)

    verify_btn.click(
        fn=verify_claim,
        inputs=[claim_input],
        outputs=[verdict_out, confidence_out, reasoning_out,
                 advocate_out, refuter_out, sources_out]
    )

    gr.Examples(
        examples=[
            ["India's unemployment rate fell below 7% in 2024"],
            ["The Indian government banned cryptocurrency trading in 2024"],
            ["India surpassed China as the world's most populous country"],
        ],
        inputs=claim_input
    )

demo.launch()