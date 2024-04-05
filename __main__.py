import json

from field_extracting.extracting import Extractor


def main():
    with open("DATASET/input/cakephp_Note_Request.json") as f:
        cakephp_note = json.load(f)

    extractor = Extractor()
    bullets = extractor.get_fields(cakephp_note)

    with open('DATASET/output/out.json', 'w') as f:
        json.dump({"bullets": bullets}, f, indent=4)



if __name__ == '__main__':
    main()