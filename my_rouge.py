from rouge import Rouge
import re
import string
from nltk.translate.bleu_score import sentence_bleu

def preprocess_text(text):
    # Küçük harflere dönüştürme
    text = text.lower()

    # Gereksiz karakterlerin ve özel karakterlerin temizlenmesi
    text = re.sub(r"\d+", "", text)  # Sayıları kaldırma
    text = re.sub(r"[" + string.punctuation + "]", "", text)  # Noktalama işaretlerini kaldırma
    text = re.sub(r"\s+", " ", text)  # Birden fazla boşluğu tek bir boşlukla değiştirme
    text = text.strip()  # Baştaki ve sondaki boşlukları kaldırma

    return text

# def get_rouge_scores():
#     rouge = Rouge()

#     with open('reference.txt', 'r', encoding='utf-8') as reference_file:
#         reference = reference_file.read()
#         reference = preprocess_text(reference)
#     with open('summary.txt', 'r', encoding='utf-8') as summary_file:
#         summary = summary_file.read()
#         summary = preprocess_text(summary)  # Özet metin için ön işleme
    
#     print(reference)
#     print()
#     print(summary)

#     scores = rouge.get_scores(summary, reference)

#     if scores:
#         for metric, results in scores[0].items():
#             print(f"{metric}: {results['f']}")
#     else:
#         print("Rouge scores could not be calculated.")
def get_rouge_scores2():
    with open('reference.txt', 'r', encoding='utf-8') as reference_file:
        reference = reference_file.read()
        reference = preprocess_text(reference)  # Referans metin için ön işleme

    with open('summary.txt', 'r', encoding='utf-8') as summary_file:
        summary = summary_file.read()
        summary = preprocess_text(summary)  # Özet metin için ön işleme
    
    # print(reference)
    # print()
    # print(summary)

    score = sentence_bleu([reference.split()], summary.split())

    # print(f"Rouge score: {score}")
    return score

#get_rouge_scores()
#get_rouge_scores2()
