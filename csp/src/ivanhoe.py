from transformers import T5ForConditionalGeneration, T5Tokenizer

tokenizer = T5Tokenizer.from_pretrained("Ivanhoe9/finetune_T5_small_title_generation_NLP_cours")
model = T5ForConditionalGeneration.from_pretrained("Ivanhoe9/finetune_T5_small_title_generation_NLP_cours")

article = "This is an article about the latest technological innovations in the field of AI and how they are impacting industries."
input_text = "Generate a title: " + article
input_ids = tokenizer.encode(input_text, return_tensors="pt")

# Generate title
generated_ids = model.generate(input_ids, max_length=30, num_beams=4, early_stopping=True)
title = tokenizer.decode(generated_ids[0], skip_special_tokens=True)
print(title)
