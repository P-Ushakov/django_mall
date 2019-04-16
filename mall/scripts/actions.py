from wagtail.core.models import Page

# Frontend actions

# Page button
class MlButton:
    def __init__(self, symbol_on, symbol_off, name_on, name_off, state_field, alert_on, alert_off, position,
                 btn_action_on=None, btn_action_off=None):
        self.symbol_on = symbol_on
        self.symbol_off = symbol_off
        self.name_on = name_on
        self.name_off = name_off
        self.state_field = state_field
        self.alert_on = alert_on
        self.alert_off = alert_off
        self.position = position
        self.submenu_items = []
        self.btn_action_on = btn_action_on
        self.btn_action_off = btn_action_off
        self.state = True
        self.state_field_name = None

    def add_submenu_item(self, item):
        self.submenu_items.append(item)

    def get_submenu(self):
        return self.submenu_items

    def get_symbol(self):
        if self.state:
            return self.symbol_on
        else:
            return self.symbol_off

    def get_name(self):
        if self.state:
            return self.name_on
        else:
            return self.name_off

    def get_state(self):
        return self.state

    def get_orm_state(self, obj):
        self.state_field_name = str(self.state_field).split(".").pop()
        self.state = getattr(obj, self.state_field_name)

    def set_state(self, state):
        self.state = state

    def change_state(self):
        self.state = not self.state
        return self.state

    def get_alert(self):
        if self.state:
            return self.alert_on
        else:
            return self.alert_off

    def get_position(self):
        return self.position

    def btn_action(self, obj):
        self.state = not self.state
        setattr(obj, self.state_field_name, self.state)
        obj.save()
        if not self.state:
            return self.btn_action_on(self, obj=obj)
        else:
            return self.btn_action_off(self, obj=obj)

    def btn_custom_action(self, obj):
        if self.state:
            return self.btn_action_on(self, obj=obj)
        else:
            return self.btn_action_off(self, obj=obj)


def execute_func(obj, func_name):
    # Execute function by name. If name have '.', execute last part
    if func_name:
        if '.' in func_name:
            func_name_list = func_name.split('.')
            if len(func_name_list) == 2:
                func = getattr(getattr(obj, func_name_list[0]), func_name_list[1])
                func(obj)
        else:
            func = getattr(obj, func_name)
            func()
