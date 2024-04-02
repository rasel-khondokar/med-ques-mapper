import json

def get_pregstatus(text):
    if "not" in text.lower():
        return "Denies pregnancy"

with open("DATASET/input/cakephp_Note_Request.json") as f:
    cakephp_note  = json.load(f)

bullets = []
medicalDetails = cakephp_note['medicalDetails']

if 'gynHx' in medicalDetails:
    data = {"category":"Problem", "text":"OB\/GYN History"}
    gynHx = medicalDetails['gynHx']
    childrens = []
    if gynHx:
        if 'ObHx' in gynHx[0]:
            ObHx = gynHx[0]['ObHx']
            if ObHx:
                childrens.append({"category": "Problem","text": get_pregstatus(ObHx)})

    if 'MAMMO' in medicalDetails:
        mammo = medicalDetails['MAMMO']
        if mammo:
            childrens.append({"category": "Problem", "text": mammo})
    data['children'] = childrens
    bullets.append(data)

with open('DATASET/output/out.json', 'w') as f:
    json.dump({"bullets": bullets}, f, indent=4)

    print(0)
print(0)


