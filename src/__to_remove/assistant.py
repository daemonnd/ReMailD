from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM 
import torch

print("Starte GPT-Neo E-Mail-Assistent...")

# Modell und Tokenizer laden
model_name = "EleutherAI/gpt-neo-1.3B"


tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Textgenerator mit hoher Eingabelänge & korrektem Padding
generator = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    device=0 if torch.cuda.is_available() else -1,
)

print("Bereit. Gib eine E-Mail oder Nachricht ein (oder 'exit' zum Beenden).")

while True:
    user_input = input("\n>>> ")
    if user_input.lower() in ["exit", "quit"]:
        break

    print("\nAntwort wird generiert...\n")

    # Prompt vorbereiten
    prompt = f"\n\n{user_input}\n\n"

    # Generierung starten
    output = generator(
        prompt,
        max_new_tokens=250,  # Maximale Länge der Antwort
        truncation=True,
        do_sample=True,
        temperature=0.7,
        top_p=0.9,
        pad_token_id=tokenizer.eos_token_id
    )

    print(output[0]['generated_text'][len(prompt):].strip())















































