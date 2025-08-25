import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QFileDialog,
    QVBoxLayout, QLabel, QPushButton, QTabWidget, QHBoxLayout, QListWidget, QSizePolicy, QListWidgetItem
)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # ----------------------------
        # Main Screen Settings
        # ----------------------------
        self.setWindowTitle("Media Converter for MacOS")
        self.setGeometry(200, 100, 700, 500)

        # ----------------------------
        # Initialize Data Source
        # ----------------------------
        self.image_items = []
        self.video_items = []

        # ----------------------------
        # App Home Settings
        # ----------------------------
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        tabs = QTabWidget()
        tabs.setTabPosition(QTabWidget.TabPosition.North)
        tabs.setTabShape(QTabWidget.TabShape.Rounded)
        tabs.setStyleSheet("QTabBar::tab { height: 30px; width: 100px; }")

        # ----------------------------
        # Image Tab Settings
        # ----------------------------
        image_tab = QWidget()
        image_layout = QVBoxLayout()
        top_layout = QHBoxLayout()

        # --- Process Item List & Buttons ---
        image_top_left_layout = QVBoxLayout()
        self.image_list_widget = QListWidget()
        self.image_list_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # Load datas
        self.load_image_items()

        # --- Top Left Items List ---
        image_top_left_layout.addWidget(QLabel("Files:"))
        image_top_left_layout.addWidget(self.image_list_widget)
        image_list_btns = QHBoxLayout()
        image_btn_add = QPushButton("Add")
        image_btn_delete = QPushButton("Delete")
        image_btn_clear = QPushButton("Clear")
        image_list_btns.addWidget(image_btn_add)
        image_list_btns.addWidget(image_btn_delete)
        image_list_btns.addWidget(image_btn_clear)
        image_top_left_layout.addLayout(image_list_btns)

        # --- Top Right Process Area ---
        image_top_right_layout = QLabel("Process btns here...")
        image_top_right_layout.setStyleSheet("border-radius: 10px; border: 1px solid gray;")
        image_top_right_layout.setMinimumWidth(200)

        # --- Combine Top Layout ---
        top_layout.addLayout(image_top_left_layout, stretch=1)
        top_layout.addWidget(image_top_right_layout, stretch=2)

        # --- Bottom Layout ---
        image_bottom_layout = QVBoxLayout()
        image_bottom_layout.addWidget(QLabel("Checkout the description & tutorial here -> "))

        # --- Assemble ---
        image_layout.addLayout(top_layout, stretch=2)
        image_layout.addLayout(image_bottom_layout, stretch=2)
        image_tab.setLayout(image_layout)
        tabs.addTab(image_tab, "Image")

        # ----------------------------
        # Video Tab Settings
        # ----------------------------
        video_tab = QWidget()
        video_layout = QVBoxLayout()
        video_layout.addWidget(QLabel("Checkout the description & tutorial here -> "))
        video_tab.setLayout(video_layout)
        tabs.addTab(video_tab, "Video")

        # ----------------------------
        # Follow Up Settings
        # ----------------------------
        main_layout.addWidget(tabs)
        central_widget.setLayout(main_layout)

        # ----------------------------
        # Button Connections
        # ----------------------------
        image_btn_clear.clicked.connect(self.clear_image_items)
        image_btn_add.clicked.connect(self.add_image_item)
        image_btn_delete.setEnabled(False)
        self.image_list_widget.itemSelectionChanged.connect(
            lambda: image_btn_delete.setEnabled(bool(self.image_list_widget.selectedItems()))
        )
        image_btn_delete.clicked.connect(self.delete_selected_image_item)


    # ----------------------------
    # Image Tab Helper Functions
    # ----------------------------
    def load_image_items(self):
        self.image_list_widget.clear()
        for item in self.image_items:
            QListWidgetItem(item, self.image_list_widget)
    
    def delete_selected_image_item(self):
      selected_items = self.image_list_widget.selectedItems()
      for item in selected_items:
          if item.text() in self.image_items:
              self.image_items.remove(item.text())
          self.image_list_widget.takeItem(self.image_list_widget.row(item))

    def clear_image_items(self):
        self.image_items.clear()
        self.image_list_widget.clear()

    def add_image_item(self):
      file_paths, _ = QFileDialog.getOpenFileNames(
          self,
          "Select Image Files",
          "",
          "Images (*.png *.jpg *.jpeg *.bmp *.gif);;All Files (*)"
      )
      for file_path in file_paths:
          if file_path and file_path not in self.image_items:
              self.image_items.append(file_path)
              QListWidgetItem(file_path, self.image_list_widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())