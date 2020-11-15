import sys
from quickstart import ret_lists,ret_tasks,func,delete,complete
from functools import partial
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QWidget,\
    QPushButton, QHBoxLayout, QGridLayout, QComboBox, QVBoxLayout, QScrollArea,\
    QMessageBox
from PyQt5.QtGui import QFont
def selectionchange(window,all_tasks,lists,reload,service,i):
    # print(type(all_tasks),type(lists),type(i))
    # print(i)
    update_tasks(window,all_tasks,lists[i][1],service)
    reload_button(reload,window,all_tasks,lists[i][1],service)
    # print(all_tasks.count())

def update_tasks(window,all_tasks,list_id,service):
    tasks=ret_tasks(list_id,service)
    # print(all_tasks.itemAtPosition(0,1))
    for i in reversed(range(2,all_tasks.count())):
        all_tasks.itemAt(i).widget().setParent(None)

    for cnt,i in enumerate(tasks):
        label=QLabel(i[0])
        label.setWordWrap(True)
        label.setFont(QFont('Arial',14))
        all_tasks.addWidget(label,cnt+1,0)
        x=QPushButton("Delete")
        y=QPushButton("Complete")
        all_tasks.addWidget(x,cnt+1,1)
        all_tasks.addWidget(y,cnt+1,2)
        x.clicked.connect(partial(delete_button,window,all_tasks,list_id,tasks[cnt][1],service))
        y.clicked.connect(partial(complete_button,window,all_tasks,list_id,tasks[cnt][1],tasks[cnt][2],service))

def complete_button(window,all_tasks,list_id,task_id,task,service):
    complete(all_tasks,list_id,task_id,task,service)
    update_tasks(window,all_tasks,list_id,service)


def delete_button(window,all_tasks,list_id,task_id,service):
    reply = QMessageBox.question(window,'Quit', 'Are you sure you want to delete?',\
        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
    if(reply==QMessageBox.Yes):
        delete(all_tasks,list_id,task_id,service)
        update_tasks(window,all_tasks,list_id,service)

def reload_button(self,window,all_tasks,list_id,service):
    self.clicked.connect(partial(update_tasks,window,all_tasks,list_id,service))


def main():
    app=QApplication(sys.argv)
    screen=app.primaryScreen()
    screen_size=screen.size()
    scroll = QScrollArea()
    all_tasks=QGridLayout()
    all_tasks.setVerticalSpacing(20)
    outer_window=QMainWindow()
    outer_window.setCentralWidget(scroll)
    outer_window.setGeometry(screen_size.width()-380,0,380,screen_size.height())
    window=QWidget()
    scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
    scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    scroll.setWidgetResizable(True)
    scroll.setWidget(window)

    service=func()
    lists=ret_lists(service)
    tasks=ret_tasks(lists[0][1],service)
    window.setWindowTitle("My app")
    # window.setGeometry(100,100,280,80)
    # window.move(0,0)
    drop_list=QComboBox()
    drop_list.adjustSize()
    # drop_list.resize(50,50)
    all_tasks.addWidget(drop_list,0,0)
    reload=QPushButton("Reload")
    # print(drop_list.currentIndex())
    reload.clicked.connect(partial(update_tasks,window,all_tasks,lists[0][1],service))
    all_tasks.addWidget(reload,0,1)
    # print(lists)
    for i in lists:
        drop_list.addItem(i[0])

    for cnt,i in enumerate(tasks):
        label=QLabel(i[0])
        label.setWordWrap(True)
        label.setFont(QFont('Arial',14))
        label.adjustSize()
        all_tasks.addWidget(label,cnt+1,0)
        x=QPushButton("Delete")
        y=QPushButton("Complete")
        all_tasks.addWidget(x,cnt+1,1)
        all_tasks.addWidget(y,cnt+1,2)
        x.clicked.connect(partial(delete_button,window,all_tasks,lists[0][1],tasks[cnt][1],service))
        y.clicked.connect(partial(complete_button,window,all_tasks,lists[0][1],tasks[cnt][1],tasks[cnt][2],service))
    # print(all_tasks.count())
    drop_list.currentIndexChanged.connect(partial(selectionchange,window,all_tasks,lists,reload,service))
    # all_tasks.change
    # helloMsg=QLabel('<h1>Hello world!</h1>',parent=window)
    # helloMsg.move(60,15)

    # layout=QGridLayout()
    # layout.addWidget(QPushButton('Button (0, 0)'), 0, 0)
    # layout.addWidget(QPushButton('Button (0, 1)'), 0, 1)
    # x=QPushButton('Button (0, 2)')
    # layout.addWidget(x, 0, 2)
    # x.clicked.connect(hey)

    # layout.move(80,40)

    window.setLayout(all_tasks)
    outer_window.show()
    sys.exit(app.exec_())


if __name__=='__main__':
    main()
