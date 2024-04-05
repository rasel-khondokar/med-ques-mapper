from field_extracting.ml import TagExtractor


class Extractor:

    def __init__(self):
        pass

    def gynhx(self):
        if 'gynHx' in self.medical_details:
            data = {"category":"Problem", "text":"OB\/GYN History"}
            gynHx = self.medical_details['gynHx']
            childrens = []
            if gynHx:
                if 'ObHx' in gynHx[0]:
                    ObHx = gynHx[0]['ObHx']
                    if ObHx:
                        tag_extractor = TagExtractor()
                        childrens.append({"category": "Problem","text": tag_extractor.get_pregstatus(ObHx)})

            if 'MAMMO' in self.medical_details:
                mammo = self.medical_details['MAMMO']
                if mammo:
                    childrens.append({"category": "Problem", "text": mammo})
            data['children'] = childrens
            self.bullets.append(data)

    def get_field_value_from_form_medical_history(self, key, category, prefix=None):
        try:
            data = {"category": category}
            value = self.medical_details['FORMS'][ "Medical History"][key]
            if prefix:
                value = prefix + ' ' + value
            data['text'] = value
            data['children'] = []
            self.bullets.append(data)
        except Exception as e:
            print(e)

    def get_field_value(self, field_name, category):
        if field_name in self.medical_details:
            data = {"category": category}
            text =  self.medical_details[field_name]
            if isinstance(text, list):
                text = ' '.join(text)
            data['text'] = text
            data['children'] = []
            self.bullets.append(data)

    def visit_reason(self):
        self.get_field_value('VISIT_REASON', 'Reason')

    def uri(self):
        self.get_field_value('CURRURI', 'Problem')

    def childhoodnfx(self):
        self.get_field_value('CHILDHOODINFX', 'Past')

    def dv(self):
        data = {"category": 'Data'}

        dvhome = ''
        if 'DVHOME' in self.medical_details:
            dvhome = self.medical_details['DVHOME']

        dvrel = ''
        if 'DVRELATION' in self.medical_details:
            dvrel = self.medical_details['DVRELATION']

        data["text"] = f'DV Screen: {dvhome}, {dvrel}'
        data['children'] = []
        self.bullets.append(data)

    def sh(self):
        try:
            if "SH"  in self.medical_details:
                sh_txt = self.medical_details['SH'][0]
                data = {"category": 'Habits'}

                etoh_cur = ''
                if 'CURRETOH' in sh_txt:
                    etoh_cur = sh_txt['CURRETOH']

                etoh_past = ''
                if 'PASTETOH' in sh_txt:
                    etoh_past = sh_txt['PASTETOH']


                data["text"] = f'ETOH: {etoh_past}, {etoh_cur}'
                data['children'] = []
                self.bullets.append(data)
        except Exception as e:
            print(e)
    def get_fields(self, cakephp_note):

        self.bullets = []
        self.medical_details = cakephp_note['medicalDetails']

        self.gynhx()
        self.visit_reason()
        self.uri()
        self.childhoodnfx()
        self.get_field_value_from_form_medical_history('How would you describe your Social Life?', "Social", "Social Life:" )
        self.get_field_value('FH', 'Family')
        self.get_field_value('PSH_', 'Surgical')
        self.dv()
        self.sh()

        return self.bullets


