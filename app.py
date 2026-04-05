import gradio as gr
from grna_generator import find_grnas


def run(sequence, mutation_pos, mutant_nt):
    try:
        mutation_pos = int(mutation_pos)
        result = find_grnas(sequence, mutation_pos, mutant_nt)

        out = []
        out.append(f"Sequence length: {result['sequence_length']}")
        out.append(f"Wild-type base at mutation site: {result['wildtype_base']}")
        out.append("")
        out.append("Mutant sequence:")
        out.append(result["mutant_sequence"])
        out.append("")
        out.append("Candidate guide RNAs:")

        if not result["candidates"]:
            out.append("No candidate guides found.")
        else:
            for i, c in enumerate(result["candidates"], 1):
                out.append(f"Candidate {i}")
                out.append(f"Guide: {c['guide']}")
                out.append(f"PAM: {c['pam']}")
                out.append(f"Full target: {c['full_target']}")
                out.append(f"Mutation position in guide: {c['mutation_pos_in_guide']}")
                out.append(f"Classification: {c['classification']}")
                out.append(f"PAM location: {c['pam_location']}")
                out.append("")

        return "\n".join(out)

    except Exception as e:
        return f"Error: {str(e)}"


iface = gr.Interface(
    fn=run,
    inputs=[
        gr.Textbox(label="DNA String (100–120 letters)", lines=4),
        gr.Textbox(label="Mutation Position (1-based)"),
        gr.Textbox(label="Mutant Nucleotide")
    ],
    outputs="text",
    title="CRISPR gRNA Finder"
)

iface.launch()