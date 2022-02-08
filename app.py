from transformers import AutoTokenizer, AutoModelWithLMHead
import gradio as gr

# inference function
def inference(inp):
    tokenizer = AutoTokenizer.from_pretrained("GPT-python")
    model = AutoModelWithLMHead.from_pretrained("GPT-python")

    input_ids = tokenizer.encode(inp, return_tensors="pt")
    beam_output = model.generate(input_ids, 
                               max_length=512,
                               num_beams=10,
                               temperature=0.7,
                               no_repeat_ngram_size=5,
                               num_return_sequences=1,
                               )
  
    output = []
    for beam in beam_output:
        out = tokenizer.decode(beam)
        fout = out.replace("<N>", "\n")
        output.append(fout)

    return '\n'.join(output)

desc = """
        Enter some Python code and click submit to see the model's autocompletion.\n
        
        Best results have been observed with the prompt of \"import\".\n

        Please note that outputs are reflective of a model trained on a measly 40 MBs of text data for 
        a single epoch of ~16 GPU hours. Given more data and training time, the autocompletion should be much stronger.\n
        
        Computation will take some time.
        """

# Creates and launches gradio interface
gr.Interface(fn=inference,
            inputs=gr.inputs.Textbox(lines=5, label="Input Text"),
            outputs=gr.outputs.Textbox(),
            title="Generative Python Transformer",
            description=desc,
            ).launch()
