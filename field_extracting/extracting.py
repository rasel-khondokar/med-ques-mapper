from itertools import chain

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
            self.bullets.append(data)
        except Exception as e:
            print(e)

    def get_field_value(self, field_name, category, prefix=None):
        if field_name in self.medical_details:
            data = {"category": category}
            text =  self.medical_details[field_name]
            if isinstance(text, list):
                text = ' '.join(text)
            if prefix:
                data['text'] = prefix + ' ' + text
            else:
                data['text'] = text
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
                self.bullets.append(data)
        except Exception as e:
            print(e)

    def get_from_bullets(self, childrens, key, category, prefix):
        self.get_field_value_from_form_medical_history(key, category,
                                                       prefix)
        c_weight = self.bullets.pop()
        childrens.append(c_weight)

    def weight_history(self):
        data = {"category": "Problem","text": "Weight History"}
        childrens = []
        self.get_from_bullets(childrens, 'About how much to you currently weigh? (pounds)',
                              'Problem', "Current weight:")
        self.get_from_bullets(childrens, 'About how much did you weigh 1 YEAR ago? (pounds)',
                              'Problem', " Weight 1 yr ago:")
        self.get_from_bullets(childrens, 'What was the highest weight you have EVER been? (pounds)',
                              'Problem', "Maximum weight:")

        data['children'] = childrens
        self.bullets.append(data)

    def work(self):
        self.get_field_value_from_form_medical_history('What do you currently do for work?', "Social")
        occup = self.bullets.pop()['text']
        self.get_field_value_from_form_medical_history('Who is your current employer?', "Social")
        employer = self.bullets.pop()['text']
        self.get_field_value_from_form_medical_history('About how many hours do you work each week? (hours)', "Social")
        work_hour = self.bullets.pop()['text']
        val = f'Occupation: {occup} at {employer}; works {work_hour} hours/wk'
        self.bullets.append({"category": "Social","text": val})

    def pre_and_post(self, field_name, category, prefix):
        self.get_field_value(field_name, category, prefix)
        hobby_hour = self.bullets.pop()['text'] + " hours\/wk"
        self.bullets.append({"category": "Habits", "text": hobby_hour})

    def combine_multiple_key(self,keys, category, prefix='',parent_key=None, list_index=None):
        data = {"category": category}
        text = f'{prefix}'

        if parent_key:
            if list_index is None:
                raw_data = self.medical_details[parent_key]
            else:
                raw_data = self.medical_details[parent_key][list_index]
        else:
            raw_data = self.medical_details

        for key in keys:
            if key in raw_data:
                text += f' {raw_data[key]},'

        data["text"] = text[:-1]
        self.bullets.append(data)


    def assesment(self):
        if "ASSESMENTS" in self.medical_details:

            keys = list(chain(*[list(i.keys()) for i in self.medical_details['ASSESMENTS']]))
            data = {"category": "Data"}
            text = f''
            for k in keys:
                k_text = k.replace('_', ' ').title()
                text += f' {k_text} and'
            text = f'{text[:-3]}assessments completed and filed under reports'
            data["text"] = text.strip()
            self.bullets.append(data)

    def get_fields(self, cakephp_note):

        self.bullets = []
        self.medical_details = cakephp_note['medicalDetails']

        self.uri()
        self.weight_history()
        self.childhoodnfx()
        self.get_field_value_from_form_medical_history('Which of the follow best describes your living situation?', "Social",
                                                       "Living situation:")
        self.get_field_value('PETS', 'Social', "Pets:")
        self.work()
        self.get_field_value_from_form_medical_history('What is your marital status?', "Social", "Marital Status:" )
        self.get_field_value('RELIGION', 'Social', "Religion:")
        self.get_field_value_from_form_medical_history('How would you describe your Social Life?', "Social", "Social Life:" )
        self.get_field_value('FH', 'Family')
        self.get_field_value_from_form_medical_history('Which of the following best describe your parents living status?', "Family")
        self.get_field_value('PSH_', 'Surgical')
        self.gynhx()
        self.dv()
        self.assesment()
        self.sh()
        self.combine_multiple_key(['CURRTOBAC', 'PASTTOBAC'], 'Habits', "Tobacco:", "SH", 0)
        self.combine_multiple_key(['CURRIDU', 'PASTIDU'], 'Habits', "Rec Drugs:", "SH", 0)
        self.get_field_value('CURRVAPE', 'Habits', "Vape:")
        self.pre_and_post("TV", "Habits", "TV:")
        self.pre_and_post("READ", "Habits", "Reading:")
        self.get_field_value_from_form_medical_history(
            'What are some of your main interests and hobbies?', "Habits", "Hobbies:")

        # self.visit_reason()

        return self.bullets


