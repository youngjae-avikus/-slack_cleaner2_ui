import sys
from slack_cleaner2 import *
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt

class SlackCleanerWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Slack Cleaner")
        
        # 위젯 초기화
        self.token_label = QLabel("Slack API Token:")
        self.token_input = QLineEdit()
        self.token_input.setMinimumWidth(500) 
        
        self.pattern_label = QLabel("Pattern (e.g., youngjae\.you):")
        self.pattern_input = QLineEdit()
        
        self.run_button = QPushButton("Run")
        
        self.remove_button = QPushButton("Remove")
        self.remove_button.setEnabled(False)  # 초기에 비활성화 상태로 설정
        
        self.skip_button = QPushButton("Skip")
        self.skip_button.setEnabled(False)  # 초기에 비활성화 상태로 설정
        
        self.output_label = QLabel()
        
        # 레이아웃 생성 및 위젯 추가
        layout = QVBoxLayout()
        
        layout.addWidget(self.token_label)
        layout.addWidget(self.token_input)
        
        layout.addWidget(self.pattern_label)
        layout.addWidget(self.pattern_input)
        
        layout.addWidget(self.run_button)
        
        layout.addWidget(self.remove_button)
        
        layout.addWidget(self.skip_button)
        
        layout.addWidget(self.output_label)
        
        self.setLayout(layout)
        
        # 버튼 클릭 이벤트 연결
        self.run_button.clicked.connect(self.run_cleanup)
        self.remove_button.clicked.connect(self.remove_message)
        self.skip_button.clicked.connect(self.skip_message)
        
        # 메시지 리스트 초기화
        self.messages = []
        self.current_message_index = 0
        
    def run_cleanup(self):
        token = self.token_input.text()
        pattern = self.pattern_input.text()

        s = SlackCleaner(token, show_progress=False)
        
        self.messages = list(s.msgs(filter(match(pattern=pattern), s.conversations)))
        self.messages = [msg for msg in self.messages if s.myself == msg.user]

        self.current_message_index = 0
        
        self.output_label.setText(f"{len(self.messages)} messages found.")
        
        if len(self.messages) > 0:
            self.remove_button.setEnabled(True)
            self.skip_button.setEnabled(True)
            self.show_current_message()
    
    def show_current_message(self):
        msg = self.messages[self.current_message_index]
        self.output_label.setText(f"Message {self.current_message_index + 1}/{len(self.messages)}:\n{msg}")
    
    def remove_message(self):
        if self.current_message_index < len(self.messages):
            msg = self.messages[self.current_message_index]
            msg.delete(replies=True, files=True)
            
        self.current_message_index += 1
        if self.current_message_index < len(self.messages):
            self.show_current_message()
        else:
            self.output_label.setText("All messages removed.")
            self.remove_button.setEnabled(False)
            self.skip_button.setEnabled(False)
    
    def skip_message(self):
        self.current_message_index += 1
        if self.current_message_index < len(self.messages):
            self.show_current_message()
        else:
            self.output_label.setText("No more messages to skip.")
            self.skip_button.setEnabled(False)
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SlackCleanerWindow()
    window.show()
    sys.exit(app.exec_())