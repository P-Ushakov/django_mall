# Frontend actions

# Page button
class MlButton:
    def __init__(self, symbol_on, symbol_off, name_on, name_off, state, alert_on, alert_off, position,
                 btn_action_on, btn_action_off=None):
        self.symbol_on = symbol_on
        self.symbol_off = symbol_off
        self.name_on = name_on
        self.name_off = name_off
        self.state = state
        self.alert_on = alert_on
        self.alert_off = alert_off
        self.position = position
        self.submenu_items = []
        self.btn_action_on = btn_action_on
        self.btn_action_off = btn_action_off

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

    def set_state(self, state):
        self.state = state

    def change_state(self):
        self.state = not self.set_state
        return self.set_state

    def get_alert(self):
        if self.state:
            return self.alert_on
        else:
            return self.alert_off

    def get_position(self):
        return self.position

    def btn_action(self, obj):
        self.state = not self.state
        if not self.state:
            return self.btn_action_on(obj)
        else:
            return self.btn_action_off(obj)
