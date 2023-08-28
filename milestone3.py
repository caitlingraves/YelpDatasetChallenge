import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget,QTableWidgetItem,QVBoxLayout
from PyQt5 import uic, QtCore
from PyQt5.QtGui import QIcon, QPixmap
import psycopg2

qtCreatorFile = "milestone3App.ui" # Enter file here.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class milestone3(QMainWindow):
    def __init__(self):
        super(milestone3, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.loadStateList()
        self.ui.stateList.currentTextChanged.connect(self.stateChanged)
        self.ui.cityList.itemSelectionChanged.connect(self.cityChanged)
        self.ui.zipcodeList.itemSelectionChanged.connect(self.zipChanged)
        self.ui.filterCategories.itemSelectionChanged.connect(self.categoryChanged)
        self.ui.business_name.textChanged.connect(self.searchBusiness)
        #self.ui.bname.textChanged.connect(self.getBusinessNames)
        #self.ui.businesses.itemSelectionChanged.connect(self.displayBusinessCity)
        self.ui.resetButton.clicked.connect(self.reset)
        


    def executeQuery(self,sql_str) :
        try:
            conn = psycopg2.connect("dbname='milestone1db' user='postgres' host='localhost' password='Duke2023!'")
        except:
            print('Unable to connect to the database!')
        cur = conn.cursor()
        cur.execute(sql_str)
        conn.commit()
        result = cur.fetchall()
        conn.close()
        return result

    #Loads all states:
    def loadStateList(self) :
        self.ui.stateList.clear()
        sql_str = "SELECT distinct state FROM businesstable ORDER BY state"
        try:
            results = self.executeQuery(sql_str)
            for row in results:
                self.ui.stateList.addItem(row[0])
        except:
            print("Query failed!")
        self.ui.stateList.setCurrentIndex(-1)
        self.ui.stateList.clearEditText()

    #When a state is selected or changed:
    def stateChanged(self):
        self.ui.categoryTable.clear()
        self.ui.categoryTable.setRowCount(0)
        self.ui.zipcodeList.clearSelection()
        self.ui.zipcodeList.clear()
        self.ui.filterCategories.clearSelection()
        self.ui.filterCategories.clear()
        self.ui.population.clear()
        self.ui.income.clear()
        self.ui.businessNumber.clear()
        self.ui.cityList.clearSelection()
        self.ui.cityList.clear()
        self.ui.popular.clear()
        self.ui.popular.setRowCount(0)
        self.ui.popular.setColumnCount(0)
        self.ui.successful.clear()
        self.ui.successful.setRowCount(0)
        self.ui.successful.setColumnCount(0)
        state = self.ui.stateList.currentText()
        
        if (self.ui.stateList.currentIndex() >= 0) :
            sql_str = "SELECT distinct city FROM businesstable WHERE state ='" + state + "'ORDER BY city;"
            print(sql_str)
            index = self.ui.cityList.count()-1
            if index >= 0:
                self.ui.cityList.clear()
            try:
                results = self.executeQuery(sql_str)
                for row in results:
                    self.ui.cityList.addItem(row[0])
            except:
                print("Query failed!")
            
            sql_str = "SELECT name, address, city, state, stars, review_count, checkins, zipcode FROM businesstable WHERE state ='" + state + "'ORDER BY name;"
            print(sql_str)
            try:
                results = self.executeQuery(sql_str)
                style = "::section {""background-color: #f3f3f3; }"
                self.ui.businessTable.horizontalHeader().setStyleSheet(style)
                self.ui.businessTable.setColumnCount(len(results[0]))
                self.ui.businessTable.setRowCount(len(results))
                self.ui.businessTable.setHorizontalHeaderLabels(['Business Name', 'Address', 'City', 'State', 'Stars', 'Review\nCount', 'Number of\nCheckins', 'Zipcode'])
                self.ui.businessTable.setColumnWidth(0, 300)
                self.ui.businessTable.setColumnWidth(1, 300)
                self.ui.businessTable.setColumnWidth(2, 140)
                self.ui.businessTable.setColumnWidth(3, 75)
                self.ui.businessTable.setColumnWidth(4, 75)
                self.ui.businessTable.setColumnWidth(5, 100)
                self.ui.businessTable.setColumnWidth(5, 130)
                self.ui.businessTable.setColumnWidth(6, 130)
                self.ui.businessTable.setColumnWidth(7, 90)


                currentRowCount = 0
                for row in results:
                    for colCount in range (0,len(results[0])) :
                        if isinstance(row[colCount], float):
                            self.ui.businessTable.setItem(currentRowCount,colCount,QTableWidgetItem(str(round(float(row[colCount]), 2))))
                        else:
                            self.ui.businessTable.setItem(currentRowCount,colCount,QTableWidgetItem(str(row[colCount])))
                    currentRowCount += 1
            except:
                print("Query failed!")
            
            

    #When a city is selected or changed, it gets all zip codes and displays cities:
    def cityChanged(self) :
        self.ui.categoryTable.clear()
        self.ui.categoryTable.setRowCount(0)
        self.ui.zipcodeList.clearSelection()
        self.ui.zipcodeList.clear()
        self.ui.filterCategories.clearSelection()
        self.ui.filterCategories.clear()
        self.ui.population.clear()
        self.ui.income.clear()
        self.ui.businessNumber.clear()
        self.ui.popular.clear()
        self.ui.popular.setRowCount(0)
        self.ui.popular.setColumnCount(0)
        self.ui.successful.clear()
        self.ui.successful.setRowCount(0)
        self.ui.successful.setColumnCount(0)
        #Get city selected:
        if (self.ui.stateList.currentIndex() >= 0) and (len(self.ui.cityList.selectedItems()) > 0):
            city_list = self.ui.cityList.selectedItems()
            if city_list:
                city = city_list[0].text()
            
            #Zipcodes displayed:
            sql_str = "SELECT distinct zipcode FROM businesstable WHERE city ='" + city + "' ORDER BY zipcode;"
            print(sql_str)
            
            index = self.ui.zipcodeList.count()-1
            if index >= 0:
                self.ui.zipcodeList.clear()
            try:
                results = self.executeQuery(sql_str)
                for row in results:
                    self.ui.zipcodeList.addItem(row[0])
            except:
                print("Query failed!")
            #Businesses displayed:
            state = self.ui.stateList.currentText()
            city = self.ui.cityList.selectedItems()[0].text()
            sql_str = "SELECT name, address, city, state, stars, review_count, checkins, zipcode FROM businesstable WHERE state = '" + state + "' AND city='" + city + "' ORDER BY name;"
            try:
                results = self.executeQuery(sql_str)
                style = "::section {""background-color: #f3f3f3; }"
                self.ui.businessTable.horizontalHeader().setStyleSheet(style)
                self.ui.businessTable.setColumnCount(len(results[0]))
                self.ui.businessTable.setRowCount(len(results))
                self.ui.businessTable.setHorizontalHeaderLabels(['Business Name', 'Address', 'City', 'State', 'Stars', 'Review\nCount', 'Number of\nCheckins', 'Zipcode'])
                self.ui.businessTable.setColumnWidth(0, 300)
                self.ui.businessTable.setColumnWidth(1, 300)
                self.ui.businessTable.setColumnWidth(2, 140)
                self.ui.businessTable.setColumnWidth(3, 75)
                self.ui.businessTable.setColumnWidth(4, 75)
                self.ui.businessTable.setColumnWidth(5, 100)
                self.ui.businessTable.setColumnWidth(5, 130)
                self.ui.businessTable.setColumnWidth(6, 130)
                self.ui.businessTable.setColumnWidth(7, 90)


                currentRowCount = 0
                for row in results:
                    for colCount in range (0,len(results[0])) :
                        if isinstance(row[colCount], float):
                            self.ui.businessTable.setItem(currentRowCount,colCount,QTableWidgetItem(str(round(float(row[colCount]), 2))))
                        else:
                            self.ui.businessTable.setItem(currentRowCount,colCount,QTableWidgetItem(str(row[colCount])))
                    currentRowCount += 1
            except:
                print("Query failed!")

    #TODO:
    #When a zip code is selected, it displays all businesses
    def zipChanged(self):
        self.ui.categoryTable.clear()
        self.ui.categoryTable.setRowCount(0)
        self.ui.filterCategories.clearSelection()
        self.ui.filterCategories.clear()
        self.ui.population.clear()
        self.ui.income.clear()
        self.ui.businessNumber.clear()
        self.ui.popular.clear()
        self.ui.popular.setRowCount(0)
        self.ui.popular.setColumnCount(0)
        self.ui.successful.clear()
        self.ui.successful.setRowCount(0)
        self.ui.successful.setColumnCount(0)
        #Get zip selected:
        if (self.ui.stateList.currentIndex() >= 0) and (len(self.ui.cityList.selectedItems()) > 0) and (len(self.ui.zipcodeList.selectedItems()) > 0):
            zipcode_list = self.ui.zipcodeList.selectedItems()
            if zipcode_list:
                zipcode = zipcode_list[0].text()
            #Businesses displayed:
                state = self.ui.stateList.currentText()
                city = self.ui.cityList.selectedItems()[0].text()
                zipcode = self.ui.zipcodeList.selectedItems()[0].text()
                sql_str = "SELECT name, address, city, state, stars, review_count, checkins, zipcode FROM businesstable WHERE state = '" + state + "' AND city='" + city + "' AND zipcode='" + zipcode + "' ORDER BY name ;"
                results = self.executeQuery(sql_str)
                try:
                    results = self.executeQuery(sql_str)
                    style = "::section {""background-color: #f3f3f3; }"
                    self.ui.businessTable.horizontalHeader().setStyleSheet(style)
                    self.ui.businessTable.setColumnCount(len(results[0]))
                    self.ui.businessTable.setRowCount(len(results))
                    self.ui.businessTable.setHorizontalHeaderLabels(['Business Name', 'Address', 'City', 'State', 'Stars', 'Review\nCount', 'Number of\nCheckins', 'Zipcode'])
                    self.ui.businessTable.setColumnWidth(0, 300)
                    self.ui.businessTable.setColumnWidth(1, 300)
                    self.ui.businessTable.setColumnWidth(2, 140)
                    self.ui.businessTable.setColumnWidth(3, 75)
                    self.ui.businessTable.setColumnWidth(4, 75)
                    self.ui.businessTable.setColumnWidth(5, 100)
                    self.ui.businessTable.setColumnWidth(5, 130)
                    self.ui.businessTable.setColumnWidth(6, 130)
                    self.ui.businessTable.setColumnWidth(7, 90)


                    currentRowCount = 0
                    for row in results:
                        for colCount in range (0,len(results[0])) :
                            if isinstance(row[colCount], float):
                                self.ui.businessTable.setItem(currentRowCount,colCount,QTableWidgetItem(str(round(float(row[colCount]), 2))))
                            else:
                                self.ui.businessTable.setItem(currentRowCount,colCount,QTableWidgetItem(str(row[colCount])))
                        currentRowCount += 1
                except:
                    print("Query failed!")

                sql_str = "SELECT distinct category_name, COUNT(category_name) FROM categoriestable WHERE business_id IN (SELECT business_id FROM businesstable WHERE zipcode = '" + zipcode + "') GROUP BY category_name;"
                results = self.executeQuery(sql_str)
                try:
                    style = "::section {""background-color: #f3f3f3; }"
                    self.ui.categoryTable.horizontalHeader().setStyleSheet(style)
                    self.ui.categoryTable.setColumnCount(2)
                    self.ui.categoryTable.setRowCount(len(results))
                    self.ui.categoryTable.setHorizontalHeaderLabels(['Category', 'Amount'])
                    self.ui.categoryTable.setColumnWidth(0, 150)
                    self.ui.categoryTable.setColumnWidth(1, 50)
                    currentRowCount = 0
                    print(results)

                    for row in results:
                        self.ui.categoryTable.setItem(currentRowCount,0,QTableWidgetItem(str(row[0])))
                        self.ui.categoryTable.setItem(currentRowCount,1,QTableWidgetItem(str(row[1])))
                        currentRowCount += 1
                except:
                    print(results)
                    print("categoriesTable query failed!")
                #Query to get amount of businesses:
                sql_str = "SELECT COUNT(business_id) FROM businesstable WHERE zipcode = '" + zipcode + "';"
                results = self.executeQuery(sql_str)
                try:
                    self.ui.businessNumber.insertPlainText(str(results[0][0]))
                except:
                    print(results)
                    print("businessNumber query failed!")
                #Query to get zipcode data:
                sql_str = "SELECT population, meanincome FROM zipcodetable WHERE zipcode = '" + zipcode + "';"
                results = self.executeQuery(sql_str)
                try:
                    self.ui.population.insertPlainText(str(results[0][0]))#str(results[0][0]))
                    self.ui.income.insertPlainText(str(results[0][1]))
                except:
                    print(results[0][0])
                    print("Zipcodetable query failed!")

                sql_str = "SELECT distinct category_name FROM categoriestable WHERE business_id IN (SELECT business_id FROM businesstable WHERE zipcode = '" + zipcode + "') GROUP BY category_name;"
                
                try:
                    results = self.executeQuery(sql_str)
                    print(results)
                    for row in results:
                        self.ui.filterCategories.addItem(row[0])
                except:
                    print(results)
                    print("filterCategories query failed!")

                #display popular businesses:
    # (SELECT AVG(checkins - average) as popular, name FROM 
    #  (SELECT * FROM businesstable
    #  FULL OUTER JOIN categoriestable 
    #   ON categoriestable.business_id=businesstable.business_id) as F
    #  FULL OUTER JOIN
    #  (SELECT AVG(checkins) as average, category_name
    #  FROM businessTable FULL OUTER JOIN 
    #   categoriestable ON businesstable.business_id = categoriestable.business_id
    #  GROUP BY category_name) as E
    #  ON E.category_name = F.category_name
    #  WHERE checkins - average > 0
    #  AND zipcode = zipcode
    # GROUP BY name, zipcode
    # ORDER BY popular DESC)

                sql_str = "(SELECT AVG(checkins - average) as popular, name, stars, checkins FROM \
                            (SELECT * FROM businesstable \
                            FULL OUTER JOIN categoriestable \
                            ON categoriestable.business_id=businesstable.business_id) as F \
                            FULL OUTER JOIN \
                            (SELECT AVG(checkins) as average, category_name \
                            FROM businessTable FULL OUTER JOIN \
                            categoriestable ON businesstable.business_id = categoriestable.business_id \
                            GROUP BY category_name) as E \
                            ON E.category_name = F.category_name \
                            WHERE checkins - average > 0 \
                            AND zipcode = '" + zipcode + "' \
                            AND city = '" + city + "' \
                            GROUP BY name, zipcode, stars, review_count, checkins \
                            ORDER BY popular DESC)"
                try:
                    results = self.executeQuery(sql_str)
                    style = "::section {""background-color: #f3f3f3; }"
                    self.ui.popular.horizontalHeader().setStyleSheet(style)
                    self.ui.popular.setColumnCount(3)
                    self.ui.popular.setRowCount(len(results))
                    self.ui.popular.setHorizontalHeaderLabels(['Name', 'Stars', 'Checkins'])
                    self.ui.popular.setColumnWidth(0, 350)
                    self.ui.popular.setColumnWidth(1, 75)
                    self.ui.popular.setColumnWidth(2, 75)
                    currentRowCount = 0
                    print(results)

                    for row in results:
                        for colCount in (range(0,len(results[0]) - 1)):
                            if isinstance(row[colCount + 1], float):
                                self.ui.popular.setItem(currentRowCount,colCount,QTableWidgetItem(str(round(float(row[colCount + 1]), 2))))
                            else:
                                self.ui.popular.setItem(currentRowCount,colCount,QTableWidgetItem(str(row[colCount + 1])))
                        currentRowCount += 1
                    print(results)

                except:
                    print(results)
                    print("filterCategories query failed!")

                #display successful businesses:
    #             (SELECT review_count, stars, business_id,
    #  businessTable.zipcode
    #  FROM  businessTable
    # WHERE businessTable.stars >=4)
    #OR 
    # review > average and above 3
    # AND review count > average

    # SELECT review_count, stars, business_id, checkins
    #   FROM  businessTable
    #  WHERE businessTable.stars >=4 
    #  AND zipcode = '28027' ORDER BY review_count DESC

                #sql_str = "(SELECT name FROM  businessTable WHERE businessTable.stars >=4 AND zipcode = '" + zipcode + "' AND city = '" + city + "' ORDER BY review_count);"
                sql_str = "SELECT name, stars, review_count FROM businessTable FULL OUTER JOIN \
                            (SELECT AVG(review_count) avgReviews, AVG(stars) as avgStars, zipcode FROM businessTable \
                            GROUP BY zipcode) as E ON E.zipcode = businessTable.zipcode \
                            WHERE businessTable.zipcode = '" + zipcode + "' \
                            AND city = '" + city + "' \
                            AND businessTable.stars >= avgStars \
                            AND businessTable.stars >= 3 \
                            AND businessTable.review_count >= avgReviews"
                try:
                    results = self.executeQuery(sql_str)
                    style = "::section {""background-color: #f3f3f3; }"
                    self.ui.successful.horizontalHeader().setStyleSheet(style)
                    self.ui.successful.setColumnCount(3)
                    self.ui.successful.setRowCount(len(results))
                    self.ui.successful.setHorizontalHeaderLabels(['Name', 'Stars', 'Review Count'])
                    self.ui.successful.setColumnWidth(0, 350)
                    self.ui.successful.setColumnWidth(1, 75)
                    self.ui.successful.setColumnWidth(2, 75)

                    currentRowCount = 0
                    print(results)

                    for row in results:
                        for colCount in range (0,len(results[0])) :
                            if isinstance(row[colCount], float):
                                self.ui.successful.setItem(currentRowCount,colCount,QTableWidgetItem(str(round(float(row[colCount]), 2))))
                            else:
                                self.ui.successful.setItem(currentRowCount,colCount,QTableWidgetItem(str(row[colCount])))
                        currentRowCount += 1
                    print(results)

                except:
                    print(results)
                    print("filterCategories query failed!")

    def categoryChanged(self):
        print("TEST")
        #print(category)
        if (self.ui.stateList.currentIndex() >= 0) and (len(self.ui.cityList.selectedItems()) > 0) and (len(self.ui.zipcodeList.selectedItems()) >= 0) and (len(self.ui.filterCategories.selectedItems()) > 0):
            category_items = self.ui.filterCategories.selectedItems()
            if category_items:
                category = category_items[0].text()

                state = self.ui.stateList.currentText()
                city = self.ui.cityList.selectedItems()[0].text()
                zipcode = self.ui.zipcodeList.selectedItems()[0].text()
                sql_str = "SELECT name, address, city, state, stars, review_count, checkins, zipcode FROM businesstable WHERE state = '" + state + "' AND city='" + city + "' AND zipcode='" + zipcode + "' AND business_id IN (SELECT business_id FROM categoriestable WHERE category_name = '" + category + "') ORDER BY name ;"
                results = self.executeQuery(sql_str)
                try:
                    style = "::section {""background-color: #f3f3f3; }"
                    self.ui.businessTable.horizontalHeader().setStyleSheet(style)
                    self.ui.businessTable.setColumnCount(len(results[0]))
                    self.ui.businessTable.setRowCount(len(results))
                    self.ui.businessTable.setHorizontalHeaderLabels(['Business Name', 'Address', 'City', 'State', 'Stars', 'Review\nCount', 'Number of\nCheckins', 'Zipcode'])
                    self.ui.businessTable.setColumnWidth(0, 300)
                    self.ui.businessTable.setColumnWidth(1, 300)
                    self.ui.businessTable.setColumnWidth(2, 140)
                    self.ui.businessTable.setColumnWidth(3, 75)
                    self.ui.businessTable.setColumnWidth(4, 75)
                    self.ui.businessTable.setColumnWidth(5, 100)
                    self.ui.businessTable.setColumnWidth(5, 130)
                    self.ui.businessTable.setColumnWidth(6, 130)
                    self.ui.businessTable.setColumnWidth(7, 90)


                    currentRowCount = 0
                    for row in results:
                        for colCount in range (0,len(results[0])) :
                            if isinstance(row[colCount], float):
                                self.ui.businessTable.setItem(currentRowCount,colCount,QTableWidgetItem(str(round(float(row[colCount]), 2))))
                            else:
                                self.ui.businessTable.setItem(currentRowCount,colCount,QTableWidgetItem(str(row[colCount])))
                        currentRowCount += 1
                except:
                    print("categoryChanged query failed!")
                    print(results)




#Milestone 2 business search:
    def searchBusiness(self):
        #state = self.ui.stateList.currentText()
        #city = self.ui.cityList.selectedItems()[0].text()
        #zipcode = self.ui.zipcodeList.selectedItems()[0].text()

        businessname = self.ui.business_name.text()
        if (self.ui.stateList.currentIndex() >= 0):
            state = self.ui.stateList.currentText()
            sql_str = "SELECT name, address, city, state, stars, review_count, checkins, zipcode FROM businesstable WHERE name LIKE '%" + businessname + "%' AND state = '" + state + "'"# AND city='" + city + "' zipcode='" + zipcode + "'ORDER BY name;"
        else:
            sql_str = "SELECT name, address, city, state, stars, review_count, checkins, zipcode FROM businesstable WHERE name LIKE '%" + businessname + "%'"# AND state = '" + state + "' AND city='" + city + "' zipcode='" + zipcode + "'ORDER BY name;"
        if (self.ui.stateList.currentIndex() >= 0) and (len(self.ui.cityList.selectedItems()) > 0):
                city_items = self.ui.cityList.selectedItems()
                if city_items:
                    city = city_items[0].text()
                    sql_str = "SELECT name, address, city, state, stars, review_count, checkins, zipcode FROM businesstable WHERE name LIKE '%" + businessname + "%' AND state = '" + state + "' AND city='" + city + "' "# zipcode='" + zipcode + "'ORDER BY name;"
        if (self.ui.stateList.currentIndex() >= 0) and (len(self.ui.cityList.selectedItems()) > 0) and (len(self.ui.zipcodeList.selectedItems()) > 0):
                zipcode_items = self.ui.zipcodeList.selectedItems()
                if zipcode_items:
                    zipcode = zipcode_items[0].text()
                    sql_str = "SELECT name, address, city, state, stars, review_count, checkins, zipcode FROM businesstable WHERE name LIKE '%" + businessname + "%' AND state = '" + state + "' AND city='" + city + "' AND zipcode='" + zipcode + "' "#ORDER BY name;"
        print(sql_str)
        # if self.ui.stateList.currentIndex() >= 0:
        #     sql_str += " AND state = '" + state + "'"
        # if self.ui.cityList.currentIndex() >= 0:
        #     sql_str += " AND city = '" + city + "'"
        # if self.ui.zipcodeList.currentIndex() >= 0:
        #     sql_str += " AND zipcode = '" + zipcode + "'"
        sql_str += " ORDER BY name;"
        try:
            results = self.executeQuery(sql_str)
            style = "::section {""background-color: #f3f3f3; }"
            self.ui.businessTable.horizontalHeader().setStyleSheet(style)
            self.ui.businessTable.setColumnCount(len(results[0]))
            self.ui.businessTable.setRowCount(len(results))
            self.ui.businessTable.setHorizontalHeaderLabels(['Business Name', 'Address', 'City', 'State', 'Stars', 'Review\nCount', 'Number of\nCheckins', 'Zipcode'])
            self.ui.businessTable.setColumnWidth(0, 300)
            self.ui.businessTable.setColumnWidth(1, 300)
            self.ui.businessTable.setColumnWidth(2, 140)
            self.ui.businessTable.setColumnWidth(3, 75)
            self.ui.businessTable.setColumnWidth(4, 75)
            self.ui.businessTable.setColumnWidth(5, 100)
            self.ui.businessTable.setColumnWidth(5, 130)
            self.ui.businessTable.setColumnWidth(6, 130)
            self.ui.businessTable.setColumnWidth(7, 90)


            currentRowCount = 0
            for row in results:
                for colCount in range (0,len(results[0])) :
                    if isinstance(row[colCount], float):
                        self.ui.businessTable.setItem(currentRowCount,colCount,QTableWidgetItem(str(round(float(row[colCount]), 2))))
                    else:
                        self.ui.businessTable.setItem(currentRowCount,colCount,QTableWidgetItem(str(row[colCount])))
                currentRowCount += 1
        except:
            self.ui.businessTable.clear()
            self.ui.businessTable.setRowCount(0)
            self.ui.businessTable.setColumnCount(0)
            print("Query failed!")

    # def getBusinessNames(self):
    #     self.ui.businesses.clear()
    #     businessname = self.ui.bname.text()
    #     sql_str = "SELECT name FROM businesstable WHERE name LIKE '%" + businessname + "%' ORDER BY name;"
    #     try:
    #         results = self.executeQuery(sql_str)
    #         for row in results:
    #             self.ui.businesses.addItem(row[0])
    #     except:
    #         print("Query failed!")

    # def displayBusinessCity(self):
    #     businessname = self.ui.businesses.selectedItems()[0].text()
    #     sql_str = "SELECT city FROM businesstable WHERE name = '" + businessname + "';"
    #     try:
    #         results = self.executeQuery(sql_str)
    #         self.ui.bcity.setText(results[0][0])
    #     except:
    #         print("Query failed!")

    def reset(self):
        self.ui.categoryTable.clear()
        self.ui.categoryTable.setRowCount(0)
        self.ui.categoryTable.setColumnCount(0)
        self.ui.businessTable.clear()
        self.ui.businessTable.setRowCount(0)
        self.ui.businessTable.setColumnCount(0)
        self.ui.popular.clear()
        self.ui.popular.setRowCount(0)
        self.ui.popular.setColumnCount(0)
        self.ui.successful.clear()
        self.ui.successful.setRowCount(0)
        self.ui.successful.setColumnCount(0)
        self.ui.population.clear()
        self.ui.income.clear()
        self.ui.businessNumber.clear()

        self.ui.filterCategories.clearSelection()
        self.ui.filterCategories.clear()

        self.ui.zipcodeList.clearSelection()
        self.ui.zipcodeList.clear()

        self.ui.cityList.clearSelection()
        self.ui.cityList.clear()

        self.ui.stateList.setCurrentIndex(-1)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = milestone3()
    window.show()
    sys.exit(app.exec_())