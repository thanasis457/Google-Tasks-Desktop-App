import sys
from quickstart import ret_lists,ret_tasks,func,delete,complete
from functools import partial
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QWidget,\
    QPushButton, QHBoxLayout, QGridLayout, QComboBox, QVBoxLayout, QScrollArea,\
    QMessageBox
from PyQt5.QtGui import QFont


class MainGrid(QGridLayout):
    def __init__(self,window):
        super().__init__()
        self.window=window
        self.service=func()
        self.lists=ret_lists(self.service)
        self.list_idx=0
        self.tasks=ret_tasks(self.lists[0][1],self.service)
        self.drop_list=QComboBox()
        self.drop_list.adjustSize()
        self.reload=QPushButton("Reload")
        self.reload.clicked.connect(self.update_tasks)
        self.addWidget(self.drop_list,0,0)
        self.addWidget(self.reload,0,1)
        for i in self.lists:
            self.drop_list.addItem(i[0])
        self.drop_list.currentIndexChanged.connect(self.selectionchange)
        self.update_tasks()

    def selectionchange(self,i):
        self.reload_button(i)
        self.update_tasks()

    def update_tasks(self):
        # print(self.list_idx)
        self.tasks=ret_tasks(self.lists[self.list_idx][1],self.service)
        # print(all_tasks.itemAtPosition(0,1))
        for i in reversed(range(2,self.count())):
            self.itemAt(i).widget().setParent(None)

        for cnt,i in enumerate(self.tasks):
            label=QLabel(i[0])
            label.setWordWrap(True)
            label.setFont(QFont('Arial',14))
            self.addWidget(label,cnt+1,0)
            x=QPushButton("Delete")
            y=QPushButton("Complete")
            self.addWidget(x,cnt+1,1)
            self.addWidget(y,cnt+1,2)
            x.clicked.connect(partial(self.delete_button,cnt))
            y.clicked.connect(partial(self.complete_button,cnt))

    def reload_button(self,i):
        self.list_idx=i
        # print(self.list_idx)
        # self.reload.clicked.disconnect()
        # self.reload.clicked.connect(self.update_tasks)

    def delete_button(self,idx):
        reply = QMessageBox.question(self.window,'Quit', 'Are you sure you want to delete?',\
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if(reply==QMessageBox.Yes):
            delete(self.lists[self.list_idx][1],self.tasks[idx][1],self.service)
            self.update_tasks()

    def complete_button(self,idx):
        complete(self.lists[self.list_idx][1],self.tasks[idx][1],self.tasks[idx][2],self.service)
        self.update_tasks()

def main():
    app=QApplication(sys.argv)
    screen=app.primaryScreen()
    screen_size=screen.size()
    outer_window=QMainWindow()
    outer_window.setGeometry(screen_size.width()-380,0,380,screen_size.height())
    scroll = QScrollArea()
    scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
    scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    window=QWidget()
    window.setWindowTitle("My app")
    all_tasks=MainGrid(window)
    all_tasks.setVerticalSpacing(20)
    scroll.setWidgetResizable(True)
    window.setLayout(all_tasks)
    scroll.setWidget(window)
    outer_window.setCentralWidget(scroll)

    outer_window.show()
    sys.exit(app.exec_())


if __name__=='__main__':
    main()
