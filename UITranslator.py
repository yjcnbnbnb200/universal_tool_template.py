'''
based on Univeral Tool Template v008.1
by ying - https://github.com/shiningdesign/universal_tool_template.py

log:

v002: (2016.12) based on template v8.1
v001: (2016.07.22) based on template v6.1

'''
#------------------------------
# How to Use: 
# 1. global replace "UITranslator" to "YourToolName" in your editor
# 2. change file name "universal_tool_template.py" to "YourPreferedFileName.py"
# 3. load it up and run
#------------------------------
# loading template - Run in python panel
'''
import sys;myPath='/path_to_universal_tool_or_custom_name/';myPath in sys.path or sys.path.append(myPath);
import universal_tool_template
universal_tool_template.main()
'''
# loading template - Run in system command console
'''
python universal_tool_template.py
'''

tpl_ver = 8.0
hostMode = ""
qtMode = 0 # 0: PySide; 1 : PyQt, 2: PySide2, 3: PyQt5
qtModeList = ("PySide", "PyQt4", "PySide2", "PyQt5")

# python 2,3 support unicode function
try:
    UNICODE_EXISTS = bool(type(unicode))
except NameError:
    unicode = lambda s: str(s)

# ==== auto hostMode detect ====
# ref: https://github.com/fredrikaverpil/pyvfx-boilerplate/blob/master/boilerplate.py

try:
    # maya detection
    import maya.OpenMayaUI as mui
    import maya.cmds as cmds
    hostMode = "maya"
except ImportError:
    # houdini detection
    try:
        import hou 
        hostMode = "houdini"
    except ImportError:
        # nuke detection
        try:
            import nuke
            import nukescripts
            hostMode = "nuke"
        except ImportError:
            # blender detection
            try:
                import bpy 
                hostMode = "blender"
            except ImportError:
                hostMode = "desktop"
print("Host: {}".format(hostMode))
    
# ==== auto QtMode detection ====
# ref: https://github.com/mottosso/Qt.py
try:
    from PySide import QtGui, QtCore
    import PySide.QtGui as QtWidgets
    print("PySide Try")
    qtMode = 0
    if hostMode == "maya":
        import shiboken
except ImportError:
    try:
        from PySide2 import QtCore, QtGui, QtWidgets
        print("PySide2 Try")
        qtMode = 2
        if hostMode == "maya":
            import shiboken2 as shiboken
    except ImportError:
        try:
            from PyQt4 import QtGui,QtCore
            import PyQt4.QtGui as QtWidgets
            #if hostMode == "maya":
            import sip
            qtMode = 1
            print("PyQt4 Try")
        except ImportError:
            from PyQt5 import QtGui,QtCore,QtWidgets
            #if hostMode == "maya":
            import sip
            qtMode = 3
            print("PyQt5 Try")

# ==== auto PyMode detection ====
import sys
pyMode = '.'.join([ str(n) for n in sys.version_info[:3] ])
print("Python: {}".format(pyMode))

# ==== template module list ====
import os # for path and language code
from functools import partial # for partial function creation
import json # for file operation code
import os # for language code

# ================
#  user module list
# ================

import LNTextEdit # for text edit code

#------------------------------
# user UI class choice
#------------------------------
super_class = QtWidgets.QMainWindow # note: only one supports menu
#super_class = QtWidgets.QDialog
#super_class = QtWidgets.QWidget

class UITranslator(super_class): 
    def __init__(self, parent=None, mode=0):
        super_class.__init__(self, parent)
        #------------------------------
        # class variables
        #------------------------------
        self.version="2.0"
        self.uiList={} # for ui obj storage
        self.memoData = {} # key based variable data storage
        
        self.fileType='.UITranslator_EXT'
        # mode: example for receive extra user input as parameter
        self.mode = 0
        if mode in [0,1]:
            self.mode = mode # mode validator
        
        self.location = ""
        if getattr(sys, 'frozen', False):
            # frozen - cx_freeze
            self.location = sys.executable
        else:
            # unfrozen
            self.location = os.path.realpath(__file__) # location: ref: sys.modules[__name__].__file__
        
        # Custom variable
        
        #------------------------------
        # initial data
        #------------------------------
        self.memoData['data']=[]
        
        self.setupStyle()
        if isinstance(self, QtWidgets.QMainWindow):
            self.setupMenu() # only if you use QMainWindows Class
        self.setupWin()
        self.setupUI()
        self.Establish_Connections()
        self.loadData()
        self.loadLang()
    
    def setupStyle(self):
        # global app style setting for desktop
        if hostMode == "desktop":
            QtWidgets.QApplication.setStyle(QtWidgets.QStyleFactory.create('Cleanlooks'))
        self.setStyleSheet("QLineEdit:disabled{background-color: gray;}")
    def setupMenu(self):
        self.quickMenu(['file_menu;&File','setting_menu;&Setting','help_menu;&Help'])
        cur_menu = self.uiList['setting_menu']
        self.quickMenuAction('setParaA_atn','Set Parameter &A','A example of tip notice.','setParaA.png', cur_menu)
        self.uiList['setParaA_atn'].setShortcut(QtGui.QKeySequence("Ctrl+R"))
        cur_menu.addSeparator()
        # for file menu
        cur_menu = self.uiList['file_menu']
        self.quickMenuAction('newLang_atn','&Add New Language','Add a new translation.','newLang.png', cur_menu)
        self.quickMenuAction('resetLang_atn','&Reset Languages','Reset All.','resetLang.png', cur_menu)
        # for info review
        cur_menu = self.uiList['help_menu']
        self.quickMenuAction('helpHostMode_atnNone','Host Mode - {}'.format(hostMode),'Host Running.','', cur_menu)
        self.quickMenuAction('helpPyMode_atnNone','Python Mode - {}'.format(pyMode),'Python Library Running.','', cur_menu)
        self.quickMenuAction('helpQtMode_atnNone','Qt Mode - {}'.format(qtModeList[qtMode]),'Qt Library Running.','', cur_menu)
        self.quickMenuAction('helpTemplate_atnNone','Universal Tool Teamplate - {}'.format(tpl_ver),'based on Univeral Tool Template v{} by Shining Ying - https://github.com/shiningdesign/universal_tool_template.py'.format(tpl_ver),'', cur_menu)
        cur_menu.addSeparator()
        self.uiList['helpGuide_msg'] = "How to Use:\n1. Put source info in\n2. Click Process button\n3. Check result output\n4. Save memory info into a file."
        self.quickMenuAction('helpGuide_atnMsg','Usage Guide','How to Usge Guide.','helpGuide.png', cur_menu)
        
    def setupWin(self):
        self.setWindowTitle("UITranslator" + " - v" + self.version + " - host: " + hostMode)
        self.setGeometry(300, 300, 300, 300)
        
        #------------------------------
        # auto window icon setup
        path = os.path.join(os.path.dirname(self.location),'icons','UITranslator.png')
        self.setWindowIcon(QtGui.QIcon(path))
        
        #------------------------------
        # initial win drag position
        self.drag_position=QtGui.QCursor.pos()
        
        #------------------------------
        # template list: for frameless or always on top option
        #------------------------------
        # - template : keep ui always on top of all;
        # While in Maya, dont set Maya as its parent
        '''
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint) 
        '''
        
        # - template: hide ui border frame; 
        # While in Maya, use QDialog instead, as QMainWindow will make it disappear
        '''
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        '''
        
        # - template: best solution for Maya QDialog without parent, for always on-Top frameless ui
        '''
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        '''
        
        # - template: for transparent and non-regular shape ui
        # note: use it if you set main ui to transparent, and want to use alpha png as irregular shape window
        # note: black color better than white for better look of semi trans edge, like pre-mutiply
        '''
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setStyleSheet("background-color: rgba(0, 0, 0,0);")
        '''
        
    #############################################
    # customized SUPER quick ui function for speed up programming
    #############################################
    def qui(self, ui_list_string, parentObject_string='', opt=''):
        # pre-defined user short name syntax
        type_dict = {
            'vbox': 'QVBoxLayout','hbox':'QHBoxLayout','grid':'QGridLayout', 'form':'QFormLayout',
            'split': 'QSplitter', 'grp':'QGroupBox', 'tab':'QTabWidget',
            'btn':'QPushButton', 'btnMsg':'QPushButton', 'label':'QLabel', 'input':'QLineEdit', 'check':'QCheckBox', 'choice':'QComboBox',
            'txtEdit': 'LNTextEdit', 'txt': 'QTextEdit',
            'tree': 'QTreeWidget', 'table': 'QTableWidget',
            'space': 'QSpacerItem', 
        }
        # get ui_list, creation or existing ui object
        ui_list = [x.strip() for x in ui_list_string.split('|')]
        for i in range(len(ui_list)):
            if ui_list[i] in self.uiList:
                # - exisiting object
                ui_list[i] = self.uiList[ui_list[i]]
            else:
                # - string creation: 
                # get part info
                partInfo = ui_list[i].split(';',1)
                uiName = partInfo[0].split('@')[0]
                uiType = uiName.rsplit('_',1)[-1]
                if uiType in type_dict:
                    uiType = type_dict[uiType]
                # set quickUI string format
                ui_list[i] = partInfo[0]+';'+uiType
                if len(partInfo)==1:
                    # give empty button and label a place holder name
                    if uiType in ('btn', 'btnMsg', 'QPushButton','label', 'QLabel'):
                        ui_list[i] = partInfo[0]+';'+uiType + ';'+uiName 
                elif len(partInfo)==2:
                    ui_list[i]=ui_list[i]+";"+partInfo[1]
        # get parentObject or exisiting object
        parentObject = parentObject_string
        if parentObject in self.uiList:
            parentObject = self.uiList[parentObject]
        # process quickUI
        self.quickUI(ui_list, parentObject, opt)
        
    def setupUI(self):
        #------------------------------
        # main_layout auto creation for holding all the UI elements
        #------------------------------
        main_layout = None
        if isinstance(self, QtWidgets.QMainWindow):
            main_widget = QtWidgets.QWidget()
            self.setCentralWidget(main_widget)        
            main_layout = self.quickLayout('vbox', 'main_layout') # grid for auto fill window size
            main_widget.setLayout(main_layout)
        else:
            # main_layout for QDialog
            main_layout = self.quickLayout('vbox', 'main_layout')
            self.setLayout(main_layout)

        #------------------------------
        # user ui creation part
        #------------------------------
        # + template: qui version since universal tool template v7
        #   - no extra variable name, all text based creation and reference
        
        self.qui('dict_table | source_txtEdit | result_txtEdit','info_split;v')
        self.qui('filePath_input | fileLoad_btn;Load | fileLang_choice | fileExport_btn;Export', 'fileBtn_layout;hbox')
        
        self.qui('info_split | process_btn;Process and Update Memory From UI | fileBtn_layout', 'main_layout')
        self.uiList["source_txtEdit"].setWrap(0)
        self.uiList["result_txtEdit"].setWrap(0)
        
        #------------- end ui creation --------------------
        for name,each in self.uiList.items():
            if isinstance(each, QtWidgets.QLayout) and name!='main_layout' and not name.endswith('_grp_layout'):
                each.setContentsMargins(0,0,0,0) # clear extra margin some nested layout
        #self.quickInfo('Ready')
        
    def Establish_Connections(self):
        for ui_name in self.uiList.keys():
            if ui_name.endswith('_btn'):
                self.uiList[ui_name].clicked.connect(getattr(self, ui_name[:-4]+"_action", partial(self.default_action,ui_name)))
            elif ui_name.endswith('_atn'):
                self.uiList[ui_name].triggered.connect(getattr(self, ui_name[:-4]+"_action", partial(self.default_action,ui_name)))
            elif ui_name.endswith('_btnMsg'):
                self.uiList[ui_name].clicked.connect(getattr(self, ui_name[:-7]+"_message", partial(self.default_message,ui_name)))
            elif ui_name.endswith('_atnMsg'):
                self.uiList[ui_name].triggered.connect(getattr(self, ui_name[:-4]+"_action", partial(self.default_message,ui_name)))
        # custom ui response
        self.uiList['dict_table'].horizontalHeader().sectionDoubleClicked[int].connect(self.changeTableHeader)
        
    #=======================================
    # UI Response functions (custom + prebuilt functions)
    #=======================================
    # ==== user response list ====
    def loadData(self):
        print("Load data")
        self.memoData['fileList']={}
        
    def newLang_action(self):
        if len(self.memoData['fileList'].keys()) == 0:
            print("You need have UI name structure loaded in order to create a new language.")
        else:
            text, ok = QtWidgets.QInputDialog.getText(self, 'New Translation Creation', 'Enter language file name (eg. lang_cn):')
            if ok:
                if text in self.memoData['fileList'].keys():
                    print("This Language already in the table.")
                else:
                    self.uiList['dict_table'].insertColumn(self.uiList['dict_table'].columnCount())
                    index = self.uiList['dict_table'].columnCount() - 1
                    self.uiList['dict_table'].setHorizontalHeaderItem(index, QtWidgets.QTableWidgetItem(text) )
    def changeTableHeader(self, index):
        table = self.uiList["dict_table"]
        oldHeader = str(table.horizontalHeaderItem(index).text())
        text, ok = QtWidgets.QInputDialog.getText(self, 'Change header label for column %d' % index,'Header:',QtWidgets.QLineEdit.Normal, oldHeader)
        if ok:
            if text in self.memoData['fileList'].keys():
                print("This Language already in the table.")
            else:
                table.setHorizontalHeaderItem(index, QtWidgets.QTableWidgetItem(text) )
    
    def resetLang_action(self):
        self.loadData()
        self.uiList['fileLang_choice'].clear()
        self.uiList['dict_table'].setRowCount(0)
        self.uiList['dict_table'].setColumnCount(0)
        self.uiList['source_txtEdit'].setText("")
        self.uiList['result_txtEdit'].setText("Reset Done")
    
    def process_action(self): # (optional)
        print("Process ....")
        self.source_ui_to_memory()
        print("Update Result")
        self.memory_to_result_ui()
        
    # ==== template response list ====
    def default_action(self, ui_name):
        print("No action defined for this button: "+ui_name)
    def default_message(self, ui_name):
        msgName = ui_name[:-7]+"_msg"
        msg_txt = msgName + " is not defined in uiList."
        if msgName in self.uiList:
            msg_txt = self.uiList[msgName]
        tmpMsg = QtWidgets.QMessageBox()
        tmpMsg.setWindowTitle("Info")
        tmpMsg.setText(msg_txt)
        tmpMsg.addButton("OK",QtWidgets.QMessageBox.YesRole)
        tmpMsg.exec_()
    '''
    # maya related custom default button input function
    def default_action(self, ui_name):
        if ui_name.endswith('_input_set_btn'):
            input_ui = ui_name.replace('_input_set_btn', '_input')
            selected = cmds.ls(sl=1)
            if len(selected)>0 and input_ui in self.uiList.keys():
                self.uiList[input_ui].setText(selected[0])
        else:
            print("No action defined for this button: "+ui_name)    
    '''
    #=======================================
    #- UI and RAM content update functions (optional)
    #=======================================
    def memory_to_source_ui(self):
        # update ui once memory gets update
        txt='\n'.join([row for row in self.memoData['fileList']])
        self.uiList['source_txtEdit'].setText(txt)
        # table
        table = self.uiList['dict_table']
        table.clear()
        table.setRowCount(0)
        table.setColumnCount(0)
        
        headers = ["UI Name"]
        table.insertColumn(table.columnCount())
        for key in self.memoData['fileList']:
            headers.append(key)
            table.insertColumn(table.columnCount())
        table.setHorizontalHeaderLabels(headers)
        
        ui_name_ok = 0
        translate = 1
        for file in self.memoData['fileList']:
            for row, ui_name in enumerate(self.memoData['fileList'][file]):
                #create ui list
                if ui_name_ok == 0:
                    ui_item = QtWidgets.QTableWidgetItem(ui_name)
                    table.insertRow(table.rowCount())
                    table.setItem(row, 0, ui_item)
                translate_item = QtWidgets.QTableWidgetItem(self.memoData['fileList'][file][ui_name])
                table.setItem(row, translate, translate_item)
            ui_name_ok = 1
            translate +=1
    
    def memory_to_result_ui(self):
        # update result ui based on memory data
        txt='\n'.join([('Updated: '+row) for row in self.memoData['fileList']])
        self.uiList['result_txtEdit'].setText(txt)
    
    def source_ui_to_memory(self):
        # 1: get source content
        # 2: update memory
        table = self.uiList['dict_table']
        rowCnt = table.rowCount()
        colCnt = table.columnCount()
        
        if colCnt < 2:
            print("You need at least 2 column to make the valid ui-to-language data.")
        else:
            headers = [ str(table.horizontalHeaderItem(i).text()) for i in range(1,colCnt) ]
            for index, each_file in enumerate(headers):
                self.memoData['fileList'][each_file]={}
                col = index + 1
                for row in range(rowCnt):
                    ui_name = str(table.item(row,0).text())
                    if not table.item(row,col):
                        ui_txt = ""
                    else:
                        ui_txt = unicode(table.item(row,col).text())
                    self.memoData['fileList'][each_file][ui_name] = ui_txt
            print("Memory: update finished.")
            # update export combo box
            self.uiList['fileLang_choice'].clear()
            self.uiList['fileLang_choice'].addItems(self.memoData['fileList'].keys())
        # 3. process memory data and update result ui
        self.memory_to_result_ui()
        print("Process: process memory finished.")
    
    #=======================================
    #- File Operation functions (optional and custom functions)
    #=======================================
    def fileExport_action(self):
        filePath_input = self.uiList['filePath_input']
        file=str(filePath_input.text()).strip()
        # open file dialog if no text input for file path
        if file == "":
            file = QtWidgets.QFileDialog.getSaveFileName(self, "Save File","","RAW data (*.json);;Format Txt(*{});;AllFiles(*.*)".format(self.fileType))
            if isinstance(file, (list, tuple)): # for deal with pyside case
                file = file[0]
            else:
                file = str(file) # for deal with pyqt case
        # read file if open file dialog not cancelled
        if not file == "":
            filePath_input.setText(file)
            if file.endswith(self.fileType): # formated txt file
                lang = str( self.uiList['fileLang_choice'].currentText() )
                self.writeFormatFile(self.process_rawData_to_formatData(self.memoData['fileList'][lang]), file) 
            else:
                lang = str( self.uiList['fileLang_choice'].currentText() )
                self.writeRawFile(self.memoData['fileList'][lang], file) # raw json file
            self.uiList['result_txtEdit'].setText("File: '"+file+"' creation finished.")
    
    def fileLoad_action(self):
        filePath_input = self.uiList['filePath_input']
        file=str(filePath_input.text()).strip()
        # open file dialog if no text input for file path
        if file == "":
            file = QtWidgets.QFileDialog.getOpenFileName(self, "Open File","","RAW data (*.json);;Format Txt(*{});;AllFiles(*.*)".format(self.fileType))
            if isinstance(file, (list, tuple)): # for deal with pyside case
                file = file[0]
            else:
                file = str(file) # for deal with pyqt case
        # read file if open file dialog not cancelled
        if not file == "":
            fileName=os.path.splitext( os.path.basename(file) )[0]
            filePath_input.setText(file)
            if file.endswith(self.fileType): # formated txt file loading
                self.memoData['fileList'][fileName] = self.process_formatData_to_rawData( self.readFormatFile(file) )
            else: 
                self.memoData['fileList'][fileName] = self.readRawFile(file) # raw json file loading
            self.memory_to_source_ui()
            self.uiList['result_txtEdit'].setText("File: '"+file+"' loading finished.")
        # update export combo box
        self.uiList['fileLang_choice'].clear()
        self.uiList['fileLang_choice'].addItems(self.memoData['fileList'].keys())
    
    def process_formatData_to_rawData(self, file_txt):
        # 1: prepare clean data from file Data
        file_data=[] # to implement here
        return file_data
    def process_rawData_to_formatData(self, memo_data):
        # 1: prepare memory data from file Data
        file_txt = '' # to implement here
        return file_txt
        
    #############################################################
    #############################################################
    # ----------------- CORE TEMPLATE FUNCTIONS -----------------
    #                 note: dont touch code below               #
    #############################################################
    
    #############################################
    # ui data fetch functions
    #############################################
    # valid input functions
    # maya obj related
    '''
    def valid_input_newObj(self, input_name, name_format, msg=None):
        name = self.valid_input_str(input_name, msg=msg)
        if name == None:
            return None
        elif cmds.objExists(name_format.format(name)):
            print("{0} object already exists in the scene".format(name_format.format(name)))
            return None
        return name
    def valid_input_obj(self, input_name, msg=None):
        obj = str(self.uiList[input_name].text())
        if not cmds.objExists(obj):
            print("Please define the existing object. {0}".format(msg))
            return None
        return obj
    '''
    def valid_input_str(self, input_name, msg=None):
        name = str(self.uiList[input_name].text())
        if name == '':
            print("Please define the name. {0}".format(msg))
            return None
        return name
    def valid_input_int(self, input_name, min=None, max=None, msg=None):
        input_txt = str(self.uiList[input_name].text())
        result = None
        # int valid
        if not input_txt.isdigit():
            print("Please enter a valid int. {0}".format(msg))
            return None
        result = int(input_txt)
        # min
        if min != None:
            if result < min:
                print("Please enter a valid int number >= {0}. {1}".format(min, msg))
                return None
        # max
        if max != None:
            if result > max:
                print("Please enter a valid int number <= {0}. {1}".format(max, msg))
                return None
        return result
    def valid_input_float(self, input_name, min=None, max=None, msg=None):
        input_txt = str(self.uiList[input_name].text())
        result = None
        try:
            result = float(input_txt)
        except (ValueError, TypeError):
            return None
        # min
        if min != None:
            if result < min:
                print("Please enter a valid int number >= {0}. {1}".format(min, msg))
                return None
        # max
        if max != None:
            if result > max:
                print("Please enter a valid int number <= {0}. {1}".format(max, msg))
                return None
        return result
    def input_choice(self, ui_name):
        if ui_name in self.uiList.keys():
            return self.uiList[ui_name].currentIndex()
        else:
            return None 
    def output_text(self, ui_name, text):
        if ui_name in self.uiList.keys():
            self.uiList[ui_name].setText(text)
    #############################################
    # json and text data functions
    #############################################
    def readRawFile(self,file):
        with open(file) as f:
            data = json.load(f)
        return data
    def writeRawFile(self, data, file):
        with open(file, 'w') as f:
            json.dump(data, f)
            
    # format data functions
    def readFormatFile(self, file):
        with open(file) as f:
            txt = f.read()
        return txt
    def writeFormatFile(self, txt, file):    
        with open(file, 'w') as f:
            f.write(txt)
    #############################################
    # UI and Mouse Interaction functions
    #############################################
    def contextMenuEvent(self, event):
        menu = QtWidgets.QMenu(self)
        quitAction = menu.addAction("Quit")
        action = menu.exec_(self.mapToGlobal(event.pos()))
        if action == quitAction:
            self.close()
    '''
    def mouseMoveEvent(self, event):
        if (event.buttons() == QtCore.Qt.LeftButton):
            self.move(event.globalPos().x() - self.drag_position.x(),
                event.globalPos().y() - self.drag_position.y())
        event.accept()
    def mousePressEvent(self, event):
        if (event.button() == QtCore.Qt.LeftButton):
            self.drag_position = event.globalPos() - self.pos()
        event.accept()
    '''
    #############################################
    # UI language functions
    #############################################
    def loadLang(self):
        self.quickMenu(['language_menu;&Language'])
        cur_menu = self.uiList['language_menu']
        self.quickMenuAction('langDefault_atnLang', 'Default','','langDefault.png', cur_menu)
        cur_menu.addSeparator()
        self.uiList['langDefault_atnLang'].triggered.connect(partial(self.setLang,'default'))
        # store default language
        self.memoData['lang']={}
        self.memoData['lang']['default']={}
        for ui_name in self.uiList:
            ui_element = self.uiList[ui_name]
            if type(ui_element) in [ QtWidgets.QLabel, QtWidgets.QPushButton, QtWidgets.QAction, QtWidgets.QCheckBox ]:
                # uiType: QLabel, QPushButton, QAction(menuItem), QCheckBox
                self.memoData['lang']['default'][ui_name] = str(ui_element.text())
            elif type(ui_element) in [ QtWidgets.QGroupBox, QtWidgets.QMenu ]:
                # uiType: QMenu, QGroupBox
                self.memoData['lang']['default'][ui_name] = str(ui_element.title())
            elif type(ui_element) in [ QtWidgets.QTabWidget]:
                # uiType: QTabWidget
                tabCnt = ui_element.count()
                tabNameList = []
                for i in range(tabCnt):
                    tabNameList.append(str(ui_element.tabText(i)))
                self.memoData['lang']['default'][ui_name]=';'.join(tabNameList)
            elif type(ui_element) == str:
                # uiType: string for msg
                self.memoData['lang']['default'][ui_name] = self.uiList[ui_name]
        
        # try load other language
        lang_path = os.path.dirname(self.location) # better in packed than(os.path.abspath(__file__))
        baseName = os.path.splitext( os.path.basename(self.location) )[0]
        for fileName in os.listdir(lang_path):
            if fileName.startswith(baseName+"_lang_"):
                langName = fileName.replace(baseName+"_lang_","").split('.')[0].replace(" ","")
                self.memoData['lang'][ langName ] = self.readRawFile( os.path.join(lang_path,fileName) )
                self.quickMenuAction(langName+'_atnLang', langName.upper(),'',langName + '.png', cur_menu)
                self.uiList[langName+'_atnLang'].triggered.connect(partial(self.setLang,langName))
        # if no language file detected, add export default language option
        if len(self.memoData['lang']) == 1:
            self.quickMenuAction('langExport_atnLang', 'Export Default Language','','langExport.png', cur_menu)
            self.uiList['langExport_atnLang'].triggered.connect(self.exportLang)
    def setLang(self, langName):
        uiList_lang_read = self.memoData['lang'][langName]
        for ui_name in uiList_lang_read:
            ui_element = self.uiList[ui_name]
            if type(ui_element) in [ QtWidgets.QLabel, QtWidgets.QPushButton, QtWidgets.QAction, QtWidgets.QCheckBox ]:
                # uiType: QLabel, QPushButton, QAction(menuItem), QCheckBox
                if uiList_lang_read[ui_name] != "":
                    ui_element.setText(uiList_lang_read[ui_name])
            elif type(ui_element) in [ QtWidgets.QGroupBox, QtWidgets.QMenu ]:
                # uiType: QMenu, QGroupBox
                if uiList_lang_read[ui_name] != "":
                    ui_element.setTitle(uiList_lang_read[ui_name])
            elif type(ui_element) in [ QtWidgets.QTabWidget]:
                # uiType: QTabWidget
                tabCnt = ui_element.count()
                if uiList_lang_read[ui_name] != "":
                    tabNameList = uiList_lang_read[ui_name].split(';')
                    if len(tabNameList) == tabCnt:
                        for i in range(tabCnt):
                            if tabNameList[i] != "":
                                ui_element.setTabText(i,tabNameList[i])
            elif type(ui_element) == str:
                # uiType: string for msg
                if uiList_lang_read[ui_name] != "":
                    self.uiList[ui_name] = uiList_lang_read[ui_name]
    def exportLang(self):
        file = QtWidgets.QFileDialog.getSaveFileName(self, "Export Default UI Language File","","RAW data (*.json);;AllFiles(*.*)")
        if isinstance(file, (list, tuple)): # for deal with pyside case
            file = file[0]
        else:
            file = str(file) # for deal with pyqt case
        # read file if open file dialog not cancelled
        if not file == "":
            self.writeRawFile( self.memoData['lang']['default'], file )
            self.quickMsg("Languge File created: '"+file)
    #############################################
    # quick ui function for speed up programming
    #############################################
    def quickMenu(self, ui_names):
        if isinstance(self, QtWidgets.QMainWindow):
            menubar = self.menuBar()
            for each_ui in ui_names:
                createOpt = each_ui.split(';')
                if len(createOpt) > 1:
                    uiName = createOpt[0]
                    uiLabel = createOpt[1]
                    self.uiList[uiName] = QtWidgets.QMenu(uiLabel)
                    menubar.addMenu(self.uiList[uiName])
        else:
            print("Warning (QuickMenu): Only QMainWindow can have menu bar.")
        
    def quickMenuAction(self, objName, title, tip, icon, menuObj):
        self.uiList[objName] = QtWidgets.QAction(QtGui.QIcon(icon), title, self)        
        self.uiList[objName].setStatusTip(tip)
        menuObj.addAction(self.uiList[objName])
    
    def quickLayout(self, type, ui_name=""):
        the_layout = ''
        if type in ("form", "QFormLayout"):
            the_layout = QtWidgets.QFormLayout()
            the_layout.setLabelAlignment(QtCore.Qt.AlignLeft)
            the_layout.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)    
        elif type in ("grid", "QGridLayout"):
            the_layout = QtWidgets.QGridLayout()
        elif type in ("hbox", "QHBoxLayout"):
            the_layout = QtWidgets.QHBoxLayout()
            the_layout.setAlignment(QtCore.Qt.AlignTop)
        else:        
            the_layout = QtWidgets.QVBoxLayout()
            the_layout.setAlignment(QtCore.Qt.AlignTop)
        if ui_name != "":
            self.uiList[ui_name] = the_layout
        return the_layout
    
    def quickUI(self, part_list, parentObject="", insert_opt=""):
        # part_list contains: 
        # -- 1. string (strings for widget/space, layout, container[group, tab, splitter])
        # -- 2. object (widget/space, layout, container[group, tab, splitter])
        # -- 3. object list 
        # -- 4. [object list, label_object list]
        # parentObject contains:
        # -- 1. string (strings for layout, container[group, tab, splitter])
        # -- 2. object (layout, container[group, tab, splitter])
        # insert_opt:
        # -- insert into grid layout, h, v
        # -- insert into tab, titles
        if not isinstance(part_list, (list, tuple)):
            part_list = [part_list]
        # func variable
        ui_list = []
        ui_label_list = []
        form_type = 0 # flag for store whether ui_list need a label widget list for form layout creation
        
        # 1. convert string to object and flatten part_list
        for each_part in part_list:
            # 1.1 string
            if isinstance(each_part, str):
                # - string : get part info
                partInfo = each_part.split(';')
                uiNameLabel = partInfo[0].split('@')
                uiName = uiNameLabel[0]
                uiLabel = ''
                if len(uiNameLabel) > 1:
                    uiLabel = uiNameLabel[1]
                    form_type = 1
                uiType = partInfo[1] if len(partInfo) > 1 else ""
                uiArgs = partInfo[2] if len(partInfo) > 2 else ""
                # - string : valid info
                if uiType == "":
                    print(uiType)
                    print("Warning (QuickUI): uiType is empty for "+each_part)
                else:
                    # - string : to object creation
                    ui_create_state = 0 # flag to track creation success
                    if not uiType[0] == 'Q':
                        # -- 3rd ui type, create like UI_Class.UI_Class()
                        self.uiList[uiName] = getattr(eval(uiType), uiType)()
                        ui_list.append(self.uiList[uiName])
                        ui_create_state = 1
                    else:
                        # -- Qt ui
                        if uiType in ('QVBoxLayout', 'QHBoxLayout', 'QFormLayout', 'QGridLayout'):
                            # --- Qt Layout creation preset func
                            ui_list.append(self.quickLayout(uiType, uiName))
                            ui_create_state = 1
                        elif uiType in ('QSplitter', 'QTabWidget', 'QGroupBox'):
                            # --- Qt container creation
                            if uiType == 'QSplitter':
                                # ---- QSplitter as element
                                split_type = QtCore.Qt.Horizontal
                                if uiArgs == 'v':
                                    split_type = QtCore.Qt.Vertical
                                self.uiList[uiName]=QtWidgets.QSplitter(split_type)
                                ui_list.append(self.uiList[uiName])
                                ui_create_state = 1
                            elif uiType == 'QTabWidget':
                                # ---- QTabWidget as element, no tab label need for input
                                self.uiList[uiName]=QtWidgets.QTabWidget()
                                self.uiList[uiName].setStyleSheet("QTabWidget::tab-bar{alignment:center;}QTabBar::tab { min-width: 100px; }")
                                ui_list.append(self.uiList[uiName])
                                ui_create_state = 1
                            elif uiType == 'QGroupBox':
                                # ---- QGroupBox as element, with layout type and optional title
                                arg_list = [x.strip() for x in uiArgs.split(',')]
                                grp_layout = arg_list[0] if arg_list[0]!='' else 'vbox'
                                grp_title = arg_list[1] if len(arg_list)>1 else uiName
                                # create layout and set grp layout
                                grp_layout = self.quickLayout(grp_layout, uiName+"_layout" )
                                self.uiList[uiName] = QtWidgets.QGroupBox(grp_title)
                                self.uiList[uiName].setLayout(grp_layout)
                                ui_list.append(self.uiList[uiName])
                                ui_create_state = 1
                        else:
                            # --- Qt widget creation
                            if uiArgs == "":
                                # ---- widget with no uiArgs
                                self.uiList[uiName] = getattr(QtWidgets, uiType)()
                                ui_list.append(self.uiList[uiName])
                                ui_create_state = 1
                            else:
                                # ---- widget with uiArgs
                                if not ( uiArgs.startswith("(") and uiArgs.endswith(")") ):
                                    # ----- with string arg
                                    self.uiList[uiName] = getattr(QtWidgets, uiType)(uiArgs)
                                    ui_list.append(self.uiList[uiName])
                                    ui_create_state = 1
                                else:
                                    # ----- with array arg
                                    arg_list = uiArgs.replace('(','').replace(')','').split(',')
                                    if uiType == 'QComboBox':
                                        self.uiList[uiName] = QtWidgets.QComboBox()
                                        self.uiList[uiName].addItems(arg_list)
                                        ui_list.append(self.uiList[uiName])
                                        ui_create_state = 1
                                    elif uiType == 'QSpacerItem':
                                        policyList = ( QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Ignored)
                                        # 0 = fixed; 1 > min; 2 < max; 3 = prefered; 4 = <expanding>; 5 = expanding> Aggresive; 6=4 ignored size input
                                        # factors in fighting for space: horizontalStretch
                                        # extra space: setContentsMargins and setSpacing
                                        # ref: http://www.cnblogs.com/alleyonline/p/4903337.html
                                        arg_list = [ int(x) for x in arg_list ]
                                        self.uiList[uiName] = QtWidgets.QSpacerItem(arg_list[0],arg_list[1], policyList[arg_list[2]], policyList[arg_list[3]] )
                                        ui_list.append(self.uiList[uiName])
                                        ui_create_state = 1
                                    else:
                                        print("Warning (QuickUI): uiType don't support array arg for "+each_part)
                    # - string : Qt widget label for form element creation
                    if ui_create_state == 1:
                        if uiLabel != '':
                            ui_label_list.append((uiName,uiLabel))
                        else:
                            ui_label_list.append('')
                    ui_create_state = 0
            else:
                # 1.2 other part like: object, object list, [object, label object]
                if isinstance(each_part, (QtWidgets.QWidget, QtWidgets.QLayout, QtWidgets.QSpacerItem)):
                    # - object
                    ui_list.append(each_part)
                    ui_label_list.append('')
                elif isinstance(each_part, (tuple, list)):
                    # - object list, [object, label object]
                    if len(each_part) != 0:
                        if isinstance(each_part[0], (tuple, list)) and len(each_part)==2:
                            # -- [object, label object]
                            ui_list.extend(each_part[0])
                            ui_label_list.extend(each_part[1])
                        else:
                            # -- object list
                            ui_list.extend(each_part)
                            ui_label_list.extend(['']*len(each_part))
                
        # 2 parentObject part
        if parentObject == '':
            # - if no parentObject, return object list or [object list, label_object list] 
            if form_type == 1:
                return [ui_list, ui_label_list]
            else:
                return ui_list
        else:
            if isinstance(parentObject, str):
                # - if parentObject, convert string to parentObject
                parentName = ''
                parentType = ''
                parentArgs = ''
                layout_type_list = (
                    'QVBoxLayout', 'QHBoxLayout', 'QFormLayout', 'QGridLayout', 'vbox', 'hbox', 'grid', 'form',
                    'QSplitter', 'QTabWidget', 'QGroupBox', 'split', 'tab', 'grp',
                )
                # get options
                parentOpt = parentObject.split(';')
                if len(parentOpt) == 1:
                    # -- only 1 arg case: strict name format, eg. conf_QHBoxLayout, config_hbox
                        parentName = parentOpt[0] # 1 para case: strict name endfix format
                        parentType = parentName.rsplit('_',1)[-1]
                elif len(parentOpt)==2:
                    # -- only 2 arg case: 
                    # a. flexible name format + type eg. conf_layout;QGridLayout, conf_layout;hbox
                    # b. strict name format, + setting eg. conf_QGridLayout;h, config_grid;h
                    parentName = parentOpt[0]
                    if parentOpt[1] in layout_type_list:
                        parentType = parentOpt[1] # a
                    else:
                        parentType = parentName.rsplit('_',1)[-1]
                        parentArgs = parentOpt[1] # b
                elif len(parentOpt)>=3: 
                    # -- 3 arg case: 
                    # flexible name format + type + settings eg. conf_layout;QGridLayout;h
                    parentName = parentOpt[0]
                    parentType = parentOpt[1]
                    parentArgs = parentOpt[2]
                # - validate layout options
                if parentName=='' or (parentType not in layout_type_list):
                    print("Warning (QuickUI): quickUI not support parent layout as "+parentObject)
                    return
                else:
                    # - create layout
                    if parentType in ('QVBoxLayout', 'QHBoxLayout', 'QFormLayout', 'QGridLayout', 'vbox', 'hbox', 'grid', 'form'):
                        # -- layout object case
                        parentObject = self.quickLayout(parentType, parentName)
                    elif parentType in ('QSplitter', 'QTabWidget', 'QGroupBox', 'split', 'tab', 'grp'):
                        # --- Qt container creation
                        if parentType in ('QSplitter', 'split'):
                            # ---- QSplitter as element
                            split_type = QtCore.Qt.Horizontal
                            if parentArgs == 'v':
                                split_type = QtCore.Qt.Vertical
                            self.uiList[parentName]=QtWidgets.QSplitter(split_type)
                            parentObject = self.uiList[parentName]
                        elif parentType in ('QTabWidget', 'tab'):
                            # ---- QTabWidget as element, no tab label need for input
                            self.uiList[parentName]=QtWidgets.QTabWidget()
                            self.uiList[parentName].setStyleSheet("QTabWidget::tab-bar{alignment:center;}QTabBar::tab { min-width: 100px; }")
                            parentObject = self.uiList[parentName]
                        elif parentType in ('QGroupBox', 'grp'):
                            # ---- QGroupBox as element, with layout type and optional title
                            arg_list = [x.strip() for x in parentArgs.split(',')]
                            grp_layout = arg_list[0] if arg_list[0]!='' else 'vbox'
                            grp_title = arg_list[1] if len(arg_list)>1 else parentName
                            # create layout and set grp layout
                            grp_layout = self.quickLayout(grp_layout, parentName+"_layout" )
                            self.uiList[parentName] = QtWidgets.QGroupBox(grp_title)
                            self.uiList[parentName].setLayout(grp_layout)
                            parentObject = self.uiList[parentName]
            
            # 3. get parentLayout inside parentObject
            parentLayout = ''
            if isinstance(parentObject, QtWidgets.QLayout):
                parentLayout = parentObject
            elif isinstance(parentObject, QtWidgets.QGroupBox):
                parentLayout = parentObject.layout()
            # 3.1 insert part_list into parentLayout for layout and groupbox
            if isinstance(parentLayout, QtWidgets.QBoxLayout):
                for each_ui in ui_list:
                    if isinstance(each_ui, QtWidgets.QWidget):
                        parentLayout.addWidget(each_ui)
                    elif isinstance(each_ui, QtWidgets.QSpacerItem):
                        parentLayout.addItem(each_ui)
                    elif isinstance(each_ui, QtWidgets.QLayout):
                        parentLayout.addLayout(each_ui)
            elif isinstance(parentLayout, QtWidgets.QGridLayout):
                # one row/colume operation only
                insertRow = parentLayout.rowCount()
                insertCol = parentLayout.columnCount()
                for i in range(len(ui_list)):
                    each_ui = ui_list[i]
                    x = insertRow if insert_opt=="h" else i
                    y = i if insert_opt=="h" else insertCol
                    if isinstance(each_ui, QtWidgets.QWidget):
                        parentLayout.addWidget(each_ui,x,y)
                    elif isinstance(each_ui, QtWidgets.QSpacerItem):
                        parentLayout.addItem(each_ui,x,y)
                    elif isinstance(each_ui, QtWidgets.QLayout):
                        parentLayout.addLayout(each_ui,x,y)
            elif isinstance(parentLayout, QtWidgets.QFormLayout):
                for i in range(len(ui_list)):
                    each_ui = ui_list[i]
                    if isinstance(each_ui, QtWidgets.QWidget) or isinstance(each_ui, QtWidgets.QLayout):
                        # create and add label: (uiName, uiLabel)
                        if ui_label_list[i] != '':
                            uiLabelName = ui_label_list[i][0] + "_label"
                            uiLabelText = ui_label_list[i][1]
                            self.uiList[uiLabelName] = QtWidgets.QLabel(uiLabelText)
                            parentLayout.addRow(self.uiList[uiLabelName], each_ui)
                        else:
                            parentLayout.addRow(each_ui)
            else:
                # 3.2 insert for empty parentLayout for split, and tab
                if isinstance(parentObject, QtWidgets.QSplitter):
                    for each_ui in ui_list:
                        if isinstance(each_ui, QtWidgets.QWidget):
                            parentObject.addWidget(each_ui)
                        else:
                            tmp_holder = QtWidgets.QWidget()
                            tmp_holder.setLayout(each_ui)
                            parentObject.addWidget(tmp_holder)
                elif isinstance(parentObject, QtWidgets.QTabWidget):
                    tab_names = insert_opt.replace('(','').replace(')','').split(',')
                    for i in range( len(ui_list) ):
                        each_tab = ui_list[i]
                        each_name = 'tab_'+str(i) 
                        if i < len(tab_names):
                            if tab_names[i] != '':
                                each_name = tab_names[i]
                        if isinstance(each_tab, QtWidgets.QWidget):
                            parentObject.addTab(each_tab, each_name)
                        else:
                            tmp_holder = QtWidgets.QWidget()
                            tmp_holder.setLayout(each_tab)
                            parentObject.addTab(tmp_holder, each_name)
            return parentObject
    def quickSplitUI(self, name, part_list, type):
        split_type = QtCore.Qt.Horizontal
        if type == 'v':
            split_type = QtCore.Qt.Vertical
        self.uiList[name]=QtWidgets.QSplitter(split_type)
        
        for each_part in part_list:
            if isinstance(each_part, QtWidgets.QWidget):
                self.uiList[name].addWidget(each_part)
            else:
                tmp_holder = QtWidgets.QWidget()
                tmp_holder.setLayout(each_part)
                self.uiList[name].addWidget(tmp_holder)
        return self.uiList[name]
        
    def quickTabUI(self, name, tab_list, tab_names):
        self.uiList[name]=QtWidgets.QTabWidget()
        self.uiList[name].setStyleSheet("QTabWidget::tab-bar{alignment:center;}QTabBar::tab { min-width: 100px; }")
        for i in range( len(tab_list) ):
            each_tab = tab_list[i]
            each_name = tab_names[i]
            if isinstance(each_tab, QtWidgets.QWidget):
                self.uiList[name].addTab(each_tab, each_name)
            else:
                tmp_holder = QtWidgets.QWidget()
                tmp_holder.setLayout(each_tab)
                self.uiList[name].addTab(tmp_holder, each_name)
        return self.uiList[name]
        
    def quickGrpUI(self, ui_name, ui_label, ui_layout):
        self.uiList[ui_name] = QtWidgets.QGroupBox(ui_label)
        if isinstance(ui_layout, QtWidgets.QLayout):
            self.uiList[ui_name].setLayout(ui_layout)
        elif isinstance(ui_layout, str):
            ui_layout = self.quickLayout(ui_name+"_layout", ui_layout)
            self.uiList[ui_name].setLayout(ui_layout)
        return [self.uiList[ui_name], ui_layout]
    
    def quickPolicy(self, ui_list, w, h):
        if not isinstance(ui_list, (list, tuple)):
            ui_list = [ui_list]
        # 0 = fixed; 1 > min; 2 < max; 3 = prefered; 4 = <expanding>; 5 = expanding> Aggresive; 6=4 ignored size input
        policyList = ( QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Ignored)
        for each_ui in ui_list:
            if isinstance(each_ui, str):
                each_ui = self.uiList[each_ui]
            each_ui.setSizePolicy(policyList[w],policyList[h])
    
    def quickInfo(self, info):
        self.statusBar().showMessage(info)            
    def quickMsg(self, msg):
        tmpMsg = QtWidgets.QMessageBox() # for simple msg that no need for translation
        tmpMsg.setWindowTitle("Info")
        tmpMsg.setText(msg)
        tmpMsg.addButton("OK",QtWidgets.QMessageBox.YesRole)
        tmpMsg.exec_()
    def quickMsgAsk(self, msg):
        txt, ok = QtWidgets.QInputDialog.getText(self, "Input", msg)
        return (str(txt), ok)

    def mui_to_qt(self, mui_name):
        if hostMode != "maya":
            return
        ptr = mui.MQtUtil.findControl(mui_name)
        if ptr is None:
            ptr = mui.MQtUtil.findLayout(mui_name)
        if ptr is None:
            ptr = mui.MQtUtil.findMenuItem(mui_name)
        if ptr is not None:
            if qtMode in (0,2):
                # ==== for pyside ====
                return shiboken.wrapInstance(long(ptr), QtWidgets.QWidget)
            elif qtMode in (1,3):
                # ==== for PyQt====
                return sip.wrapinstance(long(ptr), QtCore.QObject)
    def qt_to_mui(self, qt_obj):
        if hostMode != "maya":
            return
        ref = None
        if qtMode in (0,2):
            # ==== for pyside ====
            ref = long(shiboken.getCppPointer(qt_obj)[0])
        elif qtMode in (1,3):
            # ==== for PyQt====
            ref = long(sip.unwrapinstance(qt_obj))
        if ref is not None:
            return mui.MQtUtil.fullName(ref)

#############################################
# window instance creation
#############################################

single_UITranslator = None
def main(mode=0):
    # get parent window in Maya
    parentWin = None
    if hostMode == "maya":
        if qtMode in (0,2): # pyside
            parentWin = shiboken.wrapInstance(long(mui.MQtUtil.mainWindow()), QtWidgets.QWidget)
        elif qtMode in (1,3): # PyQt
            parentWin = sip.wrapinstance(long(mui.MQtUtil.mainWindow()), QtCore.QObject)
    # create app object for certain host
    app = None
    if hostMode in ("desktop", "blender"):
        app = QtWidgets.QApplication(sys.argv)
    
    #--------------------------
    # ui instance
    #--------------------------
    # template 1 - Keep only one copy of windows ui in Maya
    global single_UITranslator
    if single_UITranslator is None:
        if hostMode == "maya":
            single_UITranslator = UITranslator(parentWin, mode)
        else:
            single_UITranslator = UITranslator()
        # extra note: in Maya () for no parent; (parentWin,0) for extra mode input
    single_UITranslator.show()
    ui = single_UITranslator
    
    # template 2 - allow loading multiple windows of same UI in Maya
    '''
    if hostMode == "maya":
        ui = UITranslator(parentWin)
        ui.show()
    else:
        
    # extra note: in Maya () for no parent; (parentWin,0) for extra mode input
    
    '''
    
    # loop app object for certain host
    if hostMode in ("desktop"):
        sys.exit(app.exec_())
    
    return ui

if __name__ == "__main__":
    main()

if hostMode == "blender":
    app = QtWidgets.QApplication(sys.argv)
    ui = UITranslator()
    ui.show()
