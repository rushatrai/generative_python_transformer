import os
from tokenizers import ByteLevelBPETokenizer
from transformers import GPT2Tokenizer
from transformers import GPT2Config, GPT2LMHeadModel
from transformers import DataCollatorForLanguageModeling, Trainer, TrainingArguments
from datasets import load_dataset

# tokenizing

paths = ["py_txt_file.txt"]  # can add more later to expand model

tokenizer = ByteLevelBPETokenizer()

# trains model
tokenizer.train(files=paths, vocab_size=52_000, min_frequency=2, special_tokens=[
    "<s>",  # beginning of a sentence token
    "<pad>",  # padding token
    "</s>",  # ending of a sentence token
    "<unk>",  # unknown word token
    "<mask>",  # mask token
])

# creates tokenizer directory if it doesn't already exist
save_folder = "tokenizer"

if not os.path.exists(save_folder):
  os.makedirs(save_folder)

# saves model to tokenizer directory
tokenizer.save_model(save_folder)

tokenizer = GPT2Tokenizer.from_pretrained(save_folder)

tokenizer.add_special_tokens({
    "eos_token": "</s>",
    "bos_token": "<s>",
    "unk_token": "<unk>",
    "pad_token": "<pad>",
    "mask_token": "<mask>",
})

# training

config = GPT2Config(
    vocab_size = tokenizer.vocab_size,
    bos_token = tokenizer.bos_token_id,
    eos_token = tokenizer.eos_token_id, 
)

model = GPT2LMHeadModel(config)

dataset = load_dataset("text", data_files=paths)

def encode(lines):
  return tokenizer(lines["text"], add_special_tokens=True, truncation=True, max_length=1024)

dataset.set_transform(encode)
dataset = dataset["train"]

data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=True, mlm_probability=0.15)

training_args = TrainingArguments(
    output_dir="GPT-python",
    overwrite_output_dir=True,
    num_train_epochs=1,
    per_device_train_batch_size=10,
    save_steps=100,
    save_total_limit=2,
    prediction_loss_only=True,
    remove_unused_columns=False,
)

trainer = Trainer(
    model=model,
    args=training_args,
    data_collator=data_collator,
    train_dataset=dataset,
)

trainer.train()

trainer.save_model("GPT-python")
