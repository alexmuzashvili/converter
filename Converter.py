import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QApplication
from design import Ui_Converter


class Converter(QMainWindow):
    parameters = {"Weight":{"American":["Ounce","Pound","Stone","Short ton","Long ton","Grain"],
                            "European":["Grams", "Kilograms","Milligrams", "Tonnes","Decagrams",
                                        "Centigrams","Carats","Micrograms"]},
                  "Length":{"American":["Inch", "Foot","Yard", "Mile","Nautical mile", "Thou"],
                            "European":["Centimeters","Kilometers","Meters", "Millimeters","Decimeters",
                                        "Nanometers", "Micrometers"]},

                  "Area":{"American":["Square inch","Square foot","Square yard","Square mile",
                                      "Acre","Square rod","Square chain"],
                          "European":["Square centimeters","Square meters","Square kilometers",
                                      "Hectares","Square decimeters", "Square millimeters","Ares","Decares"]},

                  "Volume":{"American":["Cup","Pint","Quart","Gallon","Fluid ounce","Barrel","Cubic inch",
                                        "Cubic foot","Cubic yard"],
                            "European":["Milliliters","Liters","Cubic meters","Cubic centimeters",
                                        "Deciliters","Hectoliters"]},

                  "Temperature":{"American":["Fahrenheit"], "European":["Celsius","Kelvin"]},

                  "Speed":{"American":["mph","knot","fps","ft/min"],"European":["km/h","m/s","cs/s","mach",
                                                                                "Speed of light"]}
                  }


    def __init__(self):
        super().__init__()
        self.ui = Ui_Converter()
        self.ui.setupUi(self)

        self.ui.lineEdit_2.setReadOnly(True)


        self.ui.comboBox_3.addItem("")
        self.ui.comboBox_3.addItems(self.parameters.keys())




        self.ui.comboBox_3.currentTextChanged.connect(self.determine_category)

        self.ui.comboBox.currentTextChanged.connect(self.set_proper_category)

        self.ui.pushButton.clicked.connect(self.convert)
        self.ui.pushButton.clicked.connect(self.history_add)
        self.ui.pushButton_2.clicked.connect(self.reset_btn)
        self.ui.pushButton_3.clicked.connect(self.exit)
        self.ui.checkBox.stateChanged.connect(lambda: (self.ui.comboBox.setCurrentIndex(0),
                                                       self.ui.comboBox_2.clear(), self.ui.lineEdit.clear(),
                                                       self.ui.lineEdit_2.clear()))


        self.history = []

    def determine_category(self):
        self.ui.comboBox.clear()
        self.ui.comboBox_2.clear()
        self.ui.lineEdit.clear()
        self.ui.lineEdit_2.clear()

        cat = self.ui.comboBox_3.currentText()
        if cat in self.parameters.keys():
            text_to_add = self.parameters[cat]["American"] + self.parameters[cat]["European"]
            self.ui.comboBox.addItem("")
            self.ui.comboBox.addItems(text_to_add)

        else:
            self.ui.lineEdit.clear()
            self.ui.lineEdit_2.clear()
            self.ui.comboBox.clear()
            self.ui.comboBox_2.clear()






    def set_proper_category(self):

        unit = self.ui.comboBox.currentText()
        cat = self.ui.comboBox_3.currentText()
        self.ui.lineEdit.clear()
        self.ui.lineEdit_2.clear()

        if cat == "":
            return
        if not self.ui.checkBox.isChecked():
            if unit in self.parameters[cat]["American"]:
                units = self.parameters[cat]["European"]
                self.ui.comboBox_2.clear()
                self.ui.comboBox_2.addItem("")
                self.ui.comboBox_2.addItems(units)
                self.ui.comboBox_2.setCurrentIndex(1)
            elif unit in self.parameters[cat]["European"]:
                units = self.parameters[cat]["American"]
                self.ui.comboBox_2.clear()
                self.ui.comboBox_2.addItem("")
                self.ui.comboBox_2.addItems(units)
                self.ui.comboBox_2.setCurrentIndex(1)
        else:
            self.ui.comboBox_2.clear()

            units = self.parameters[cat]["European"] + self.parameters[cat]["American"]
            if unit in units:
                units.remove(unit)
            self.ui.comboBox_2.addItem("")
            self.ui.comboBox_2.addItems(units)
            self.ui.comboBox_2.setCurrentIndex(1) if self.ui.comboBox.currentText() != "" \
                else self.ui.comboBox_2.setCurrentIndex(0)



    def convert(self):
        if not self.ui.comboBox_3.currentText():
            return
        try:
            val = float(self.ui.lineEdit.text())

        except:
            self.ui.lineEdit.setText("Error")
            self.ui.lineEdit_2.setText("Error")
            return

        cat = self.ui.comboBox_3.currentText()
        from_unit = self.ui.comboBox.currentText()
        to_unit = self.ui.comboBox_2.currentText()
        precision = self.ui.spinBox.value()

        if cat == "Weight":
            result = self.convert_weight(val,cat, from_unit, to_unit, precision)
            if result != "Error":
                rounded = f"{result:.{precision}f}" if float(f"{result:.{precision}f}") > 1 else (
                    f"{result:.10f}".rstrip("0").rstrip("."))
                self.ui.lineEdit_2.setText(rounded)
                self.history.append(f"{val} {from_unit} = {rounded} {to_unit} ")
            else:
                self.ui.lineEdit.clear()
                self.ui.lineEdit_2.clear()
                self.ui.lineEdit.setText("Error")
                self.ui.lineEdit_2.setText("Error")

        elif cat == "Length":
            result = self.convert_length(val,cat, from_unit, to_unit, precision)
            if result != "Error":
                rounded = f"{result:.{precision}f}" if float(f"{result:.{precision}f}") > 1 else (
                    f"{result:.10f}".rstrip("0").rstrip("."))
                self.ui.lineEdit_2.setText(rounded)
                self.history.append(f"{val} {from_unit} = {rounded} {to_unit} ")

        elif cat == "Area":
            result = self.convert_area(val,cat, from_unit, to_unit, precision)
            if result != "Error":
                rounded = f"{result:.{precision}f}" if float(f"{result:.{precision}f}") > 1 \
                    else f"{result:.10f}".rstrip("0").rstrip(".")
                self.ui.lineEdit_2.setText(rounded)
                self.history.append(f"{val} {from_unit} = {rounded} {to_unit} ")
            else:
                self.ui.comboBox_2.clear()
                self.ui.comboBox.clear()
                self.ui.lineEdit.clear()
                self.ui.lineEdit_2.clear()
                self.ui.lineEdit.setText("Error")
                self.ui.lineEdit_2.setText("Error")

        elif cat == "Volume":
            result = self.convert_volume(val,cat, from_unit, to_unit, precision)
            if result != "Error":
                rounded = f"{result:.{precision}f}" if float(f"{result:.{precision}f}") > 1 \
                    else f"{result:.10f}".rstrip("0").rstrip(".")
                self.ui.lineEdit_2.setText(rounded)
                self.history.append(f"{val} {from_unit} = {rounded} {to_unit} ")
            else:
                self.ui.comboBox_2.clear()
                self.ui.comboBox.clear()
                self.ui.lineEdit.clear()
                self.ui.lineEdit_2.clear()
                self.ui.lineEdit.setText("Error")
                self.ui.lineEdit_2.setText("Error")

        elif cat == "Temperature":
            result = self.convert_temperature(val,cat, from_unit, to_unit, precision)
            if result != "Error":
                rounded = f"{result:.{precision}f}" if float(f"{result:.{precision}f}") > 1 \
                    else f"{result:.10f}".rstrip("0").rstrip(".")
                self.ui.lineEdit_2.setText(rounded)
                self.history.append(f"{val} {from_unit} = {rounded} {to_unit} ")

        elif cat == "Speed":
            result = self.convert_speed(val,cat, from_unit, to_unit, precision)
            if result != "Error":
                rounded = f"{result:.{precision}f}" if float(f"{result:.{precision}f}") > 1 \
                    else f"{result:.10f}".rstrip("0").rstrip(".")
                self.ui.lineEdit_2.setText(rounded)
                self.history.append(f"{val} {from_unit} = {rounded} {to_unit} ")


    def reset_btn(self):
        self.ui.lineEdit.clear()
        self.ui.lineEdit_2.clear()

    def exit(self):
        sys.exit()

    def convert_weight(self,value,category,f_unit,t_unit,prec):
        to_grams = {"Grams":1,"Kilograms":1000,"Milligrams":0.001,
                    "Tonnes":1000000,"Pound":453.592,"Stone":6350.29,
                    "Short ton":907184.74,"Long ton":1016047,"Ounce":28.3495,"Grain":0.0647989,
                    "Decagrams":10,"Centigrams":0.01,"Carats":0.2,"Micrograms":0.000001}

        if f_unit not in to_grams or t_unit not in to_grams or value < 0:
            return "Error"

        grams = value * to_grams[f_unit]
        res = grams / to_grams[t_unit]
        return res

    def convert_length(self,value,category,f_unit,t_unit,prec):
        to_meters = {"Meters":1, "Kilometers":1000,"Centimeters":0.01,
                     "Millimeters":0.001, "Inch":0.0254, "Foot": 0.3048,
                     "Yard":0.9144, "Mile": 1609.34, "Nautical mile": 1852,"Thou":0.0000254,
                     "Decimeters":0.1, "Nanometers":0.0000000001,"Micrometers":0.0000001}
        if f_unit not in to_meters or t_unit not in to_meters:
            return "Error"
        meters = value * to_meters[f_unit]
        res = meters / to_meters[t_unit]
        return res

    def convert_area(self,value,category,f_unit,t_unit,prec):
        to_square_meters = {"Square meters":1, "Square centimeters":0.0001,
                            "Square kilometers":1000000,"Hectares":10000,"Square inch":0.00064516,
                            "Square foot":0.092903,"Square yard":0.836127,"Square mile":2589988.11,"Acre":4046.86,
                            "Square rod":25.2929,"Square chain":404.686,"Square decimeters":0.01,
                            "Square millimeters":0.000001,"Ares":100,"Decares":1000}

        if f_unit not in to_square_meters or t_unit not in to_square_meters or value < 0:
            return "Error"
        meters = value * to_square_meters[f_unit]
        res = meters / to_square_meters[t_unit]
        return res

    def convert_volume(self,value,category,f_unit,t_unit,prec):
        to_milliliters = {"Milliliters":1,"Liters":1000,"Cubic meters":1000000,
                          "Cup":236.588,"Pint":473.176,"Quart":946.353,"Gallon":3785.41,"Fluid ounce":29.5735,
                          "Barrel":158987.3,"Cubic inch":16.3871,"Cubic foot":28316.8,"Cubic yard":764555,
                          "Cubic centimeters":1, "Deciliters":100,"Hectoliters":100000}
        if f_unit not in to_milliliters or t_unit not in to_milliliters or value < 0:
            return "Error"
        milliliters = value * to_milliliters[f_unit]
        res = milliliters / to_milliliters[t_unit]
        return res

    def convert_temperature(self, value, category, f_unit, t_unit, prec):
        if f_unit == t_unit:
            return value

        if f_unit == "Celsius":
            celsius = value
        elif f_unit == "Fahrenheit":
            celsius = (value - 32) * 5/9
        elif f_unit == "Kelvin":
            celsius = value - 273.15
        else:
            return "Error"

        if t_unit == "Celsius":
            return celsius
        elif t_unit == "Fahrenheit":
            return (celsius * 9/5) + 32
        elif t_unit == "Kelvin":
            return celsius + 273.15
        else:
            return "Error"

    def convert_speed(self, value, category, f_unit, t_unit, prec):
        to_mps = {"mph":0.44704,"km/h":1000/3600, "knot":0.514444,"fps":0.3048,"ft/min":0.00508,
                  "m/s":1, "cs/s":0.01,"mach":340.29,"Speed of light":299792458}
        if f_unit not in to_mps or t_unit not in to_mps:
            return "Error"
        mps = value * to_mps[f_unit]
        res = mps / to_mps[t_unit]
        return res

    def history_add(self):
        if self.history:
            if (self.ui.lineEdit.text() != "Error" and self.ui.comboBox.currentText() != "" and
                    self.ui.comboBox_2.currentText() != ""):
                self.ui.listWidget.addItem(self.history[-1])

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.exit()
        elif event.key() == Qt.Key_Return:
            self.convert()
            self.history_add()
        elif event.key() == Qt.Key_C:
            self.reset_btn()




app = QApplication(sys.argv)
main = Converter()
main.show()
sys.exit(app.exec_())