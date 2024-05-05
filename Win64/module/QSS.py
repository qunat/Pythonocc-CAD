butstyle='''
            QPushButton{color:rgb(0,0,0)}s
            QPushButton{background-color:rgb(238, 238, 238)}
            QPushButton:hover{background-color:rgb(85, 170, 255)} 
            #QPushButton{border-radius:6px}
            QPushButton:pressed{background-color:rgb(180,180,180);border: None;}
            '''

butstyle_1="""
            #QPushButton{background-image: url('./pic/001.08.30.30GW.png')}'
            QPushButton:hover{background-color:rgb(0, 170, 255)} 
            """
butstyle_2= '''
            QPushButton:pressed{background-color:rgb(180,180,180);border: None;}
            '''
labstyle = '''
            QLabel{color:rgb(0,0,0)}s
            QLabel{background-color:rgb(0, 170, 255)}
            QLabel:hover{color:rgb(85, 170, 255)} 
            QLabel:pressed{background-color:rgb(180,180,180);border: None;}
                   '''
#qss定义
tabwidget="""
            QTabWidget{"
                "background-color:transparent;"
                "}"
                "QTabWidget.pane{"
                "    border:2px;"
                "}"
                "QTabWidget.tab-bar{"
                "        alignment:left;"
                "}"
                "QTabBar.tab{"
                "    background:rgb(14, 106, 175);"
                "    color:white;"
                "    min-width:35ex;"
                "    min-height:10ex;"
                "}"
                "QTabBar.tab:hover{"
                "    background:rgb(255, 255, 255, 100);"
                "color:black;"
                "}"
                "QTabBar.tab:selected{"
                "    border-color: black;"
                "    background:red;"
                "    color:white;"
                "}
            """