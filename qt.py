import sys
from quickstart import *
from functools import partial
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QWidget,\
    QPushButton, QHBoxLayout, QGridLayout, QComboBox, QVBoxLayout, QScrollArea,\
    QMessageBox,QLineEdit
from PyQt5.QtGui import QFont


class MainGrid(QGridLayout):
    def __init__(self,window):
        super().__init__()
        self.window=window
        self.service=func()
        self.lists=ret_lists(self.service)
        self.list_idx=0
        self.completed=QPushButton("Show completed")
        self.deleted=QPushButton("Show deleted")
        self.tasks=[]
        self.completed_tasks=[]
        self.drop_list=QComboBox()
        self.text_box=QLineEdit()
        self.reload=QPushButton("Reload")
        self.add_button=QPushButton("Add")
        self.drop_list.adjustSize()
        self.text_box.returnPressed.connect(self.add_task)
        self.add_button.clicked.connect(self.add_task)
        self.reload.clicked.connect(self.update_tasks)
        self.addWidget(self.drop_list,0,0)
        self.addWidget(self.reload,0,1)
        self.addWidget(self.text_box,1,0)
        self.addWidget(self.add_button,1,1)
        for i in self.lists:
            self.drop_list.addItem(i[0])
        self.drop_list.currentIndexChanged.connect(self.selectionchange)
        self.completed.clicked.connect(self.show_completed)
        self.deleted.clicked.connect(self.show_deleted)
        self.update_tasks()
        # self.resizeColumnsToContents()

    def selectionchange(self,i):
        self.reload_button(i)
        self.update_tasks()

    def add_task(self):
        new_task={
            "status": "needsAction",
            "kind": "tasks#task",
            # "updated": "A String", # Last modification time of the task (as a RFC 3339 timestamp).
            "title": self.text_box.text(),
            # "etag": "A String", # ETag of the resource.
            # "position": "A String",
        }
        add(self.lists[self.list_idx][1],new_task,self.service)
        self.text_box.clear()
        self.update_tasks()

    def update_tasks(self):
        self.tasks=ret_tasks(self.lists[self.list_idx][1],self.service)
        for i in reversed(range(4,self.count())):
            self.itemAt(i).widget().setParent(None)

        for cnt,i in enumerate(self.tasks):
            label=QLabel(i[0])
            label.setWordWrap(True)
            label.setFont(QFont('Arial',14))
            self.addWidget(label,cnt+2,0)
            x=QPushButton("Delete")
            y=QPushButton("Complete")
            self.addWidget(x,cnt+2,1)
            self.addWidget(y,cnt+2,2)
            x.clicked.connect(partial(self.delete_button,cnt))
            y.clicked.connect(partial(self.complete_button,cnt))
        self.addWidget(self.completed,2+len(self.tasks),0)
        self.addWidget(self.deleted,2+len(self.tasks),1)
    
    def show_completed(self):
        self.completed_tasks=ret_tasks(self.lists[self.list_idx][1],self.service,True)
        height=2+len(self.tasks)+1
        for i in reversed(range(4+(len(self.tasks))*3+2,self.count())):
            self.itemAt(i).widget().setParent(None)
        for cnt,i in enumerate(self.completed_tasks):
            label=QLabel(i[0])
            label.setWordWrap(True)
            label.setFont(QFont('Arial',14))
            self.addWidget(label,height+cnt,0)
            x=QPushButton("Restore")
            self.addWidget(x,height+cnt,1)
            x.clicked.connect(partial(self.restore_button,cnt,'completed'))
    
    def show_deleted(self):
        self.deleted_tasks=ret_tasks(self.lists[self.list_idx][1],self.service,False,True)
        height=2+len(self.tasks)+1
        for i in reversed(range(4+(len(self.tasks))*3+2,self.count())):
            self.itemAt(i).widget().setParent(None)
        for cnt,i in enumerate(self.deleted_tasks):
            label=QLabel(i[0])
            label.setWordWrap(True)
            label.setFont(QFont('Arial',14))
            self.addWidget(label,height+cnt,0)
            x=QPushButton("Restore")
            self.addWidget(x,height+cnt,1)
            x.clicked.connect(partial(self.restore_button,cnt,'deleted'))

    def reload_button(self,i):
        self.list_idx=i

    def restore_button(self,idx,task_type):
        if(task_type=='completed'):
            restore(self.lists[self.list_idx][1],self.completed_tasks[idx][1],self.completed_tasks[idx][2],self.service)
        elif(task_type=='deleted'):
            restore(self.lists[self.list_idx][1],self.deleted_tasks[idx][1],self.deleted_tasks[idx][2],self.service)
        self.update_tasks()

    def delete_button(self,idx):
        reply = QMessageBox.question(self.window,'Quit', 'Are you sure you want to delete?',\
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if(reply==QMessageBox.Yes):
            delete(self.lists[self.list_idx][1],self.tasks[idx][1],self.service)
            self.update_tasks()

    def complete_button(self,idx):
        complete(self.lists[self.list_idx][1],self.tasks[idx][1],self.tasks[idx][2],self.service)
        self.update_tasks()
        # self.update_tasks()

def main():
    app=QApplication(sys.argv)
    screen=app.primaryScreen()
    screen_size=screen.size()
    outer_window=QMainWindow()
    outer_window.setGeometry(screen_size.width()-410,0,410,screen_size.height())
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
