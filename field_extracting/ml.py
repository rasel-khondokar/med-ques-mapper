from transformers import pipeline


class ZeroshotExtractor:

    def __init__(self, model,  multi_label=False):
        self.model = model
        self.multi_label = multi_label

    def get_prediction(self, text, candidate_labels):
        pipe = pipeline("zero-shot-classification", model=self.model)
        predicted = pipe(text,
                         candidate_labels=candidate_labels,
                         multi_label=self.multi_label)
        return predicted

class TagExtractor:

    def __init__(self):
        pass

    def get_pregstatus(self, text):
        model = "facebook/bart-large-mnli"
        candidate_labels = ["Denies pregnancy", "Accept pregnancy"]
        zeroshot = ZeroshotExtractor(model)
        pred = zeroshot.get_prediction(text, candidate_labels)
        max_index = max(range(len(pred['scores'])), key=pred['scores'].__getitem__)
        pred_cls = pred['labels'][max_index]
        return pred_cls

