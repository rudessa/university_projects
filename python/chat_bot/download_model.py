from transformers import AutoTokenizer, TFAutoModel

tokenizer = AutoTokenizer.from_pretrained("DeepPavlov/rubert-base-cased")
model = TFAutoModel.from_pretrained("DeepPavlov/rubert-base-cased", from_pt=True)
tokenizer.save_pretrained("rubert_tokenizer")
model.save_pretrained("rubert_model")
