import sys
import os
from UI.test import Ui_MainWindow
from PyQt5 import QtGui, QtWidgets
from ACSAPICall.acsancestrycall import ACSAncestryCall, ancestry
from ACSAPICall.acstraveltimecall import ACSTravelTimeCall
from ACSAPICall.acehouseholdtypecall import ACSHouseHoldTypeCall, households
from Choropleth.choropleth import Choropleth


# to convert ui to python:
# pyuic5 test.ui -o test.py

class UIFunctions:
    def __init__(self, geojson_list: []):
        self.geojson_list = geojson_list
        self.is_county = None
        self.data_index = 0

        # setting up UI
        self.app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(MainWindow)
        MainWindow.show()

        # hide particular combo-boxes
        self.ui.combo2_travel.hide()
        self.ui.combo2_household.hide()

        # actions
        self.ui.updateButton.clicked.connect(self.update_button)
        self.ui.combo1.currentIndexChanged.connect(self.update_combo1)

        sys.exit(self.app.exec_())

    def update_button(self):
        if self.ui.combo0.currentIndex() == 0:
            self.is_county = False
        elif self.ui.combo0.currentIndex() == 1:
            self.is_county = True

        if self.ui.combo1.currentIndex() == 0:
            data = self.ancestry()
        elif self.ui.combo1.currentIndex() == 1:
            data = self.households()
        elif self.ui.combo1.currentIndex() == 2:
            data = self.travel_time()

        choropleth = Choropleth(dataset=data.dataset, geojson_list=self.geojson_list, is_county=self.is_county,
                                data_index=self.data_index)

        # set image
        choropleth.fig.write_image("/Users/ninjacats/Documents/Programming/Python/CensusApp/Images/fig1.jpeg")
        self.ui.label_image.setPixmap(QtGui.QPixmap("/Users/ninjacats/Documents/Programming/Python/CensusApp/Images/fig1.jpeg"))
        # os.remove("/Users/ninjacats/Documents/Programming/Python/CensusApp/Images/fig1.jpeg")

    def update_combo1(self):
        if self.ui.combo1.currentIndex() == 0:
            # ancestry
            self.ui.combo2_travel.hide()
            self.ui.combo2_household.hide()
            self.ui.combo2_ancest.show()
            self.ui.combo3_ancest.show()
        elif self.ui.combo1.currentIndex() == 1:
            # households
            self.ui.combo2_ancest.hide()
            self.ui.combo3_ancest.hide()
            self.ui.combo2_travel.hide()
            self.ui.combo2_household.show()
        elif self.ui.combo1.currentIndex() == 2:
            # travel time
            self.ui.combo2_ancest.hide()
            self.ui.combo3_ancest.hide()
            self.ui.combo2_household.hide()
            self.ui.combo2_travel.show()

    def ancestry(self):
        ancestry_str = self.find_ancestry_str()
        self.data_index = self.ui.combo3_ancest.currentIndex()
        data = ACSAncestryCall(ancestry_var=ancestry[ancestry_str], is_county=self.is_county)
        return data

    def find_ancestry_str(self):
        ancestry_string = self.ui.combo2_ancest.currentText().lower()
        ancestry_string = ancestry_string.replace("-", "_")
        ancestry_string = ancestry_string.replace(" ", "_")
        if ancestry_string == "arab":
            ancestry_string = "arab_total"
        if ancestry_string == "assyrian":
            ancestry_string = "assyrian/chaldean/syriac"
        if ancestry_string == "french":
            ancestry_string = "french_except_basque"
        if ancestry_string == "subsaharan_african":
            ancestry_string = "subsaharan_african_total"
        if ancestry_string == "subsaharan_african":
            ancestry_string = "subsaharan_african_total"
        if ancestry_string == "west_indian":
            ancestry_string = "west_indian_except_hispanic_groups_total"
        return ancestry_string

    def travel_time(self):
        self.data_index = self.ui.combo2_travel.currentIndex()
        data = ACSTravelTimeCall(is_county=self.is_county)
        return data

    def households(self):
        household_str = self.find_household_str()
        data = ACSHouseHoldTypeCall(household_type_var=households[household_str],
                                    is_county=self.is_county)
        return data

    def find_household_str(self):
        household_string = self.ui.combo2_household.currentText().lower()
        household_string = household_string.replace(" ", "_")
        return household_string
