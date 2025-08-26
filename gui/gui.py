import sys
import os
from pathlib import Path
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QFileDialog, QCheckBox, QGridLayout, QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox,
    QVBoxLayout, QLabel, QPushButton, QTabWidget, QHBoxLayout, QListWidget, QSizePolicy, QListWidgetItem
)
from PyQt6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # ----------------------------
        # Main Screen Settings
        # ----------------------------
        self.setWindowTitle("Media Converter for MacOS")
        self.setGeometry(200, 100, 550, 500)

        # ============================
        # Initialize Data Source
        # ============================
        self.image_items = []
        self.video_items = []

        # ============================
        # App Home Settings
        # ============================
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        tabs = QTabWidget()
        tabs.setTabPosition(QTabWidget.TabPosition.North)
        tabs.setTabShape(QTabWidget.TabShape.Rounded)
        tabs.setStyleSheet("QTabBar::tab { height: 30px; width: 100px; }")

        # ============================
        # Image Tab Settings
        # ============================
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

        # --- Top Right Process Area (Image) ---
        image_top_right_widget = QWidget()
        image_top_right_layout = QVBoxLayout(image_top_right_widget)
        image_top_right_layout.setContentsMargins(0, 0, 0, 0)
        # Output Path row
        image_path_layout = QHBoxLayout()
        image_output_path_label = QLabel("Output Path:")
        image_output_path_label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        image_output_path_label.setStyleSheet("margin-right: 0px;")
        self.image_output_path_btn = QPushButton(str(Path.home() / "Downloads"))
        self.image_output_path_btn.setStyleSheet("")
        image_path_layout.addStretch(1)
        image_path_layout.addWidget(image_output_path_label, alignment=Qt.AlignmentFlag.AlignLeft)
        image_path_layout.addWidget(self.image_output_path_btn, alignment=Qt.AlignmentFlag.AlignLeft)
        image_top_right_layout.addLayout(image_path_layout, stretch=1)
        # Overwrite/Delete checkbox row
        image_checkbox_layout = QHBoxLayout()
        image_checkbox_layout.addStretch(1)
        self.image_delete_checkbox = QCheckBox("Delete original files after process")
        image_checkbox_layout.addWidget(self.image_delete_checkbox, alignment=Qt.AlignmentFlag.AlignLeft)
        image_top_right_layout.addLayout(image_checkbox_layout, stretch=1)
        # Process button row
        image_process_layout = QHBoxLayout()
        image_process_layout.addStretch(1)
        self.image_process_btn = QPushButton("Process")
        image_process_layout.addWidget(self.image_process_btn, alignment=Qt.AlignmentFlag.AlignLeft)
        image_top_right_layout.addLayout(image_process_layout, stretch=1)
        image_top_right_widget.setMinimumWidth(200)
        self.image_output_path_btn.clicked.connect(self.select_output_path)

        # --- Combine Top Layout ---
        top_layout.addLayout(image_top_left_layout, stretch=1)
        top_layout.addWidget(image_top_right_widget, stretch=2)

        # --- Bottom Layout ---
        image_bottom_layout = QVBoxLayout()
        # Create 2x3 Grid Layout
        image_ops_grid = QGridLayout()
        image_ops_grid.setHorizontalSpacing(15)
        image_ops_grid.setVerticalSpacing(15)
        image_ops_grid.setContentsMargins(0, 0, 0, 0)
        # Row 0, Column 0: Reformat
        self.image_reformat_cb = QCheckBox("Reformat")
        self.image_reformat_input = QComboBox()
        self.image_reformat_input.addItems(["png", "jpg", "bmp", "tiff", "webp"])
        self.image_reformat_input.setMaximumWidth(80)
        image_reformat_layout = QHBoxLayout()
        image_reformat_layout.addWidget(self.image_reformat_cb)
        image_reformat_layout.addWidget(self.image_reformat_input)
        image_reformat_layout.addStretch()
        image_reformat_widget = QWidget()
        image_reformat_widget.setLayout(image_reformat_layout)
        image_ops_grid.addWidget(image_reformat_widget, 0, 0)
        # Row 0, Column 1: Resize
        self.image_resize_cb = QCheckBox("Resize")
        self.image_resize_width = QSpinBox()
        self.image_resize_width.setRange(1, 10000)
        self.image_resize_width.setMaximumWidth(60)
        self.image_resize_height = QSpinBox()
        self.image_resize_height.setRange(1, 10000)
        self.image_resize_height.setMaximumWidth(60)
        image_resize_layout = QHBoxLayout()
        image_resize_layout.addWidget(self.image_resize_cb)
        image_resize_layout.addWidget(QLabel("W:"))
        image_resize_layout.addWidget(self.image_resize_width)
        image_resize_layout.addWidget(QLabel("H:"))
        image_resize_layout.addWidget(self.image_resize_height)
        image_resize_layout.addStretch()
        image_resize_widget = QWidget()
        image_resize_widget.setLayout(image_resize_layout)
        image_ops_grid.addWidget(image_resize_widget, 0, 1)
        # Row 1, Column 1: Rotate
        self.image_rotate_cb = QCheckBox("Rotate")
        self.image_rotate_combo = QComboBox()
        self.image_rotate_combo.addItems(["90", "180", "270"])
        self.image_rotate_combo.setMaximumWidth(80)
        image_rotate_layout = QVBoxLayout()
        image_rotate_row_layout = QHBoxLayout()
        image_rotate_row_layout.addWidget(self.image_rotate_cb)
        image_rotate_row_layout.addWidget(self.image_rotate_combo)
        image_rotate_row_layout.addStretch()
        image_rotate_layout.addLayout(image_rotate_row_layout)
        image_rotate_layout.addStretch()
        image_rotate_widget = QWidget()
        image_rotate_widget.setLayout(image_rotate_layout)
        image_ops_grid.addWidget(image_rotate_widget, 1, 0)
        # Row 2, Column 0: Rotate
        self.image_flip_cb = QCheckBox("Flip")
        self.image_flip_combo = QComboBox()
        self.image_flip_combo.addItems(["Horizontal", "Vertical"])
        self.image_flip_combo.setMaximumWidth(100)
        image_flip_layout = QHBoxLayout()
        image_flip_layout.addWidget(self.image_flip_cb)
        image_flip_layout.addWidget(self.image_flip_combo)
        image_flip_layout.addStretch()
        image_flip_widget = QWidget()
        image_flip_widget.setLayout(image_flip_layout)
        image_ops_grid.addWidget(image_flip_widget, 1, 1)
        # Row 1, Column 0: Crop
        self.image_crop_cb = QCheckBox("Crop")
        self.image_crop_start_x = QSpinBox()
        self.image_crop_start_x.setRange(0, 10000)
        self.image_crop_start_x.setMaximumWidth(60)
        self.image_crop_start_x.setValue(0)
        self.image_crop_start_y = QSpinBox()
        self.image_crop_start_y.setRange(0, 10000)
        self.image_crop_start_y.setMaximumWidth(60)
        self.image_crop_start_y.setValue(0)
        self.image_crop_width = QSpinBox()
        self.image_crop_width.setRange(1, 10000)
        self.image_crop_width.setMaximumWidth(60)
        self.image_crop_height = QSpinBox()
        self.image_crop_height.setRange(1, 10000)
        self.image_crop_height.setMaximumWidth(60)
        image_crop_layout = QVBoxLayout()
        image_crop_layout.addWidget(self.image_crop_cb)
        image_crop_xy_layout = QHBoxLayout()
        image_crop_xy_layout.addWidget(QLabel("X:"))
        image_crop_xy_layout.addWidget(self.image_crop_start_x)
        image_crop_xy_layout.addWidget(QLabel("Y:"))
        image_crop_xy_layout.addWidget(self.image_crop_start_y)
        image_crop_xy_layout.addStretch()
        image_crop_layout.addLayout(image_crop_xy_layout)
        image_crop_wh_layout = QHBoxLayout()
        image_crop_wh_layout.addWidget(QLabel("W:"))
        image_crop_wh_layout.addWidget(self.image_crop_width)
        image_crop_wh_layout.addWidget(QLabel("H:"))
        image_crop_wh_layout.addWidget(self.image_crop_height)
        image_crop_wh_layout.addStretch()
        image_crop_layout.addLayout(image_crop_wh_layout)
        image_crop_widget = QWidget()
        image_crop_widget.setLayout(image_crop_layout)
        image_ops_grid.addWidget(image_crop_widget, 2, 0)
        # Row 1, Column 2: Adjust Brightness/Contrast
        self.image_adjust_cb = QCheckBox("Adjust Brightness/Contrast")
        self.image_alpha_spin = QDoubleSpinBox()
        self.image_alpha_spin.setRange(0.1, 5.0)
        self.image_alpha_spin.setSingleStep(0.1)
        self.image_alpha_spin.setValue(1.0)
        self.image_alpha_spin.setMaximumWidth(60)
        self.image_beta_spin = QSpinBox()
        self.image_beta_spin.setRange(-255, 255)
        self.image_beta_spin.setValue(0)
        self.image_beta_spin.setMaximumWidth(60)
        image_adjust_layout = QVBoxLayout()
        image_adjust_cb_layout = QHBoxLayout()
        image_adjust_cb_layout.addWidget(self.image_adjust_cb)
        image_adjust_cb_layout.addStretch()
        image_adjust_layout.addLayout(image_adjust_cb_layout)
        image_adjust_params_layout = QHBoxLayout()
        image_adjust_params_layout.addWidget(QLabel("Alpha:"))
        image_adjust_params_layout.addWidget(self.image_alpha_spin)
        image_adjust_params_layout.addWidget(QLabel("Beta:"))
        image_adjust_params_layout.addWidget(self.image_beta_spin)
        image_adjust_params_layout.addStretch()
        image_adjust_layout.addLayout(image_adjust_params_layout)
        image_adjust_widget = QWidget()
        image_adjust_widget.setLayout(image_adjust_layout)
        image_ops_grid.addWidget(image_adjust_widget, 2, 1, alignment=Qt.AlignmentFlag.AlignTop)

        image_bottom_layout.addLayout(image_ops_grid)

        # --- Assemble ---
        image_layout.addLayout(top_layout, stretch=1)
        image_layout.addLayout(image_bottom_layout, stretch=1)
        image_tab.setLayout(image_layout)
        tabs.addTab(image_tab, "Image")

        # ============================
        # Video Tab Settings
        # ============================
        video_tab = QWidget()
        video_layout = QVBoxLayout()
        video_layout.addWidget(QLabel("Checkout the description & tutorial here -> "))
        video_tab.setLayout(video_layout)
        tabs.addTab(video_tab, "Video")

        # ============================
        # Follow Up Settings
        # ============================
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
            
    def select_output_path(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Output Folder", "")
        if folder:
            self.output_path_btn.setText(folder)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())