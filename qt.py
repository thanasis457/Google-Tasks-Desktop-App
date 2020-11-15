import sys
from quickstart import ret_lists,ret_tasks,func,delete,complete
from functools import partial
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QWidget,\
    QPushButton, QHBoxLayout, QGridLayout, QComboBox, QVBoxLayout, QScrollArea
def selectionchange(all_tasks,lists,service,i):
    # print(type(all_tasks),type(lists),type(i))
    update_tasks(all_tasks,lists[i][1],service)
    # print(all_tasks.count())

def update_tasks(all_tasks,list_id,service):
    tasks=ret_tasks(list_id,service)
    for i in reversed(range(1,all_tasks.count())):
        all_tasks.itemAt(i).widget().setParent(None)

    for cnt,i in enumerate(tasks):
        all_tasks.addWidget(QLabel(i[0]),cnt+1,0)
        x=QPushButton("Button2")
        y=QPushButton("Button2")
        all_tasks.addWidget(x,cnt+1,1)
        all_tasks.addWidget(y,cnt+1,2)
        x.clicked.connect(partial(delete_button,all_tasks,list_id,tasks[cnt][1],service))
        y.clicked.connect(partial(complete_button,all_tasks,list_id,tasks[cnt][1],tasks[cnt][2],service))

def complete_button(all_tasks,list_id,task_id,task,service):
    complete(all_tasks,list_id,task_id,task,service)
    update_tasks(all_tasks,list_id,service)


def delete_button(all_tasks,list_id,task_id,service):

    update_tasks(all_tasks,list_id,service)

def main():
    app=QApplication(sys.argv)
    scroll = QScrollArea()
    all_tasks=QGridLayout()
    outer_window=QMainWindow()
    outer_window.setCentralWidget(scroll)
    window=QWidget()
    scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
    scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    scroll.setWidgetResizable(True)
    scroll.setWidget(window)

    service=func()
    lists=ret_lists(service)
    tasks=ret_tasks(lists[0][1],service)
    window.setWindowTitle("My app")
    window.setGeometry(100,100,280,80)
    window.move(0,0)
    drop_list=QComboBox()
    # drop_list.resize(50,50)
    all_tasks.addWidget(drop_list,0,0)
    # print(lists)
    for i in lists:
        drop_list.addItem(i[0])

    for cnt,i in enumerate(tasks):
        all_tasks.addWidget(QLabel(i[0]),cnt+1,0)
        x=QPushButton("Button2")
        y=QPushButton("Button2")
        all_tasks.addWidget(x,cnt+1,1)
        all_tasks.addWidget(y,cnt+1,2)
        x.clicked.connect(partial(delete_button,all_tasks,lists[0][1],tasks[cnt][1],service))
        y.clicked.connect(partial(complete_button,all_tasks,lists[0][1],tasks[cnt][1],tasks[cnt][2],service))

    print(all_tasks.count())
    drop_list.currentIndexChanged.connect(partial(selectionchange,all_tasks,lists,service))
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
