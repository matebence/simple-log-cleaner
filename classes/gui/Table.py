import pandasgui


class Table:

    __input_data_frame = None

    def set_data_frame(self, input_data_frame):
        self.__input_data_frame = input_data_frame
        return self

    def get_data_frame(self):
        return self.__input_data_frame

    def start_gui(self):
        pandasgui.show(self.get_data_frame())
