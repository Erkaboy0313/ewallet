from . utils import format_money
class FormatMoneyMixin(object):

    def to_representation(self, instance):
        inst_rep = super().to_representation(instance)
        result = {}
        for field_name , fild in self.get_fields().items():
            if field_name == 'month':
                result.update({field_name:inst_rep[field_name]})
            else:
                result.update({field_name:format_money(inst_rep[field_name])})
        return result