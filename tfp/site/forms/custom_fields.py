from datetime import datetime
from wtforms import DateTimeField


class NullableDateTimeField(DateTimeField):
    def process_formdata(self, valuelist):
        if not valuelist:
            return

        date_str = ' '.join(valuelist)

        if date_str == '':
            self.data = None
            return

        try:
            self.data = datetime.strptime(date_str, self.format)
        except ValueError:
            self.data = None
            raise ValueError(self.gettext('Not a valid datetime value.'))
