import sys
import os
import ctypes
from pathlib import Path
from ctypes import cdll, c_char_p, c_int, c_double
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QFileDialog, QCheckBox, QGridLayout, QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox,
    QVBoxLayout, QLabel, QPushButton, QTabWidget, QHBoxLayout, QListWidget, QSizePolicy, QListWidgetItem, QButtonGroup, QRadioButton
)
from PyQt6.QtCore import Qt

def get_lib_path(libname):
    if getattr(sys, "frozen", False):
        base_path = Path(sys._MEIPASS) / "core" / "build"
    else:
        base_path = Path(__file__).parent.parent / "core" / "build"
    return str(base_path / libname)

image_lib = ctypes.CDLL(get_lib_path("libimage_converter.dylib"))
video_lib = ctypes.CDLL(get_lib_path("libvideo_converter.dylib"))

image_lib.reformat_image.restype = int
image_lib.resize_image.restype = int
image_lib.crop_image.restype = int
image_lib.rotate_image.restype = int
image_lib.flip_image.restype = int
image_lib.adjust_brightness_image.restype = int
video_lib.reformat_video.restype = int
video_lib.resize_video.restype = int
video_lib.crop_video.restype = int
video_lib.rotate_video.restype = int
video_lib.flip_video.restype = int
video_lib.adjust_brightness_video.restype = int
if getattr(sys, "frozen", False):
    ffmpeg_path = str(Path(sys._MEIPASS) / "bin" / "ffmpeg")
else:
    ffmpeg_path = str(Path(__file__).parent.parent / "bin" / "ffmpeg")

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
        self.image_tab = QWidget()
        image_layout = QVBoxLayout()
        top_layout = QHBoxLayout()

        # --- Process Item List & Buttons ---
        image_top_left_layout = QVBoxLayout()
        self.image_list_widget = QListWidget()
        self.image_list_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # Load datas
        self.load_image_items()

        # --- Top Left Items List ---
        image_top_left_layout.addWidget(QLabel("Image Files:"))
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
        # image_path_layout = QHBoxLayout()
        # image_output_path_label = QLabel("Output Path:")
        # image_output_path_label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        # image_output_path_label.setStyleSheet("margin-right: 0px;")
        # self.image_output_path_btn = QPushButton(str(Path.home() / "Downloads"))
        # self.image_output_path_btn.setStyleSheet("")
        # image_path_layout.addStretch(1)
        # image_path_layout.addWidget(image_output_path_label, alignment=Qt.AlignmentFlag.AlignLeft)
        # image_path_layout.addWidget(self.image_output_path_btn, alignment=Qt.AlignmentFlag.AlignLeft)
        # image_top_right_layout.addLayout(image_path_layout, stretch=1)
        # Overwrite/Delete checkbox row
        image_checkbox_layout = QHBoxLayout()
        image_checkbox_layout.addStretch(1)
        self.image_delete_checkbox = QCheckBox("Delete original files after process")
        image_checkbox_layout.addWidget(self.image_delete_checkbox, alignment=Qt.AlignmentFlag.AlignLeft)
        image_top_right_layout.addLayout(image_checkbox_layout, stretch=1)
        # Process button row
        self.image_process_layout = QHBoxLayout()
        self.image_process_layout.addStretch(1)
        self.image_process_btn = QPushButton("Process")
        self.image_process_layout.addWidget(self.image_process_btn, alignment=Qt.AlignmentFlag.AlignLeft)
        image_top_right_layout.addLayout(self.image_process_layout, stretch=1)
        image_top_right_widget.setMinimumWidth(200)
        # self.image_output_path_btn.clicked.connect(self.select_output_path)

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
        self.image_ops_group = QButtonGroup()
        self.image_ops_group.setExclusive(True)
        # Row 0, Column 0: Reformat
        self.image_reformat_rb = QRadioButton("Reformat")
        self.image_reformat_input = QComboBox()
        self.image_reformat_input.addItems(["png", "jpg", "bmp", "tiff", "webp"])
        self.image_reformat_input.setMaximumWidth(80)
        image_reformat_layout = QHBoxLayout()
        image_reformat_layout.addWidget(self.image_reformat_rb)
        image_reformat_layout.addWidget(self.image_reformat_input)
        image_reformat_layout.addStretch()
        image_reformat_widget = QWidget()
        image_reformat_widget.setLayout(image_reformat_layout)
        image_ops_grid.addWidget(image_reformat_widget, 0, 0)
        self.image_ops_group.addButton(self.image_reformat_rb, 1)
        # Row 0, Column 1: Resize
        self.image_resize_rb = QRadioButton("Resize")
        self.image_resize_width = QSpinBox()
        self.image_resize_width.setRange(1, 10000)
        self.image_resize_width.setMaximumWidth(60)
        self.image_resize_height = QSpinBox()
        self.image_resize_height.setRange(1, 10000)
        self.image_resize_height.setMaximumWidth(60)
        image_resize_layout = QHBoxLayout()
        image_resize_layout.addWidget(self.image_resize_rb)
        image_resize_layout.addWidget(QLabel("W:"))
        image_resize_layout.addWidget(self.image_resize_width)
        image_resize_layout.addWidget(QLabel("H:"))
        image_resize_layout.addWidget(self.image_resize_height)
        image_resize_layout.addStretch()
        image_resize_widget = QWidget()
        image_resize_widget.setLayout(image_resize_layout)
        image_ops_grid.addWidget(image_resize_widget, 0, 1)
        self.image_ops_group.addButton(self.image_resize_rb, 2)
        # Row 1, Column 1: Rotate
        self.image_rotate_rb = QRadioButton("Rotate")
        self.image_rotate_combo = QComboBox()
        self.image_rotate_combo.addItems(["90", "180", "270"])
        self.image_rotate_combo.setMaximumWidth(80)
        image_rotate_layout = QVBoxLayout()
        image_rotate_row_layout = QHBoxLayout()
        image_rotate_row_layout.addWidget(self.image_rotate_rb)
        image_rotate_row_layout.addWidget(self.image_rotate_combo)
        image_rotate_row_layout.addStretch()
        image_rotate_layout.addLayout(image_rotate_row_layout)
        image_rotate_layout.addStretch()
        image_rotate_widget = QWidget()
        image_rotate_widget.setLayout(image_rotate_layout)
        image_ops_grid.addWidget(image_rotate_widget, 1, 0)
        self.image_ops_group.addButton(self.image_rotate_rb, 3)
        # Row 2, Column 0: Flip
        self.image_flip_rb = QRadioButton("Flip")
        self.image_flip_combo = QComboBox()
        self.image_flip_combo.addItems(["Horizontal", "Vertical"])
        self.image_flip_combo.setMaximumWidth(100)
        image_flip_layout = QHBoxLayout()
        image_flip_layout.addWidget(self.image_flip_rb)
        image_flip_layout.addWidget(self.image_flip_combo)
        image_flip_layout.addStretch()
        image_flip_widget = QWidget()
        image_flip_widget.setLayout(image_flip_layout)
        image_ops_grid.addWidget(image_flip_widget, 1, 1)
        self.image_ops_group.addButton(self.image_flip_rb, 4)
        # Row 1, Column 0: Crop
        self.image_crop_rb = QRadioButton("Crop")
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
        image_crop_layout.addWidget(self.image_crop_rb)
        image_crop_xy_layout    = QHBoxLayout()
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
        self.image_ops_group.addButton(self.image_crop_rb, 5)
        # Row 1, Column 2: Adjust Brightness/Contrast
        self.image_adjust_rb = QRadioButton("Adjust Brightness/Contrast")
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
        image_adjust_rb_layout = QHBoxLayout()
        image_adjust_rb_layout.addWidget(self.image_adjust_rb)
        image_adjust_rb_layout.addStretch()
        image_adjust_layout.addLayout(image_adjust_rb_layout)
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
        self.image_ops_group.addButton(self.image_adjust_rb, 6)

        image_bottom_layout.addLayout(image_ops_grid)

        # --- Assemble ---
        image_layout.addLayout(top_layout, stretch=1)
        image_layout.addLayout(image_bottom_layout, stretch=1)
        self.image_tab.setLayout(image_layout)
        tabs.addTab(self.image_tab, "Image")

        # ============================
        # Video Tab Settings
        # ============================
        self.video_tab = QWidget()
        video_layout = QVBoxLayout()
        video_top_layout = QHBoxLayout()

        # --- Process Item List & Buttons (Left side) ---
        video_top_left_layout = QVBoxLayout()
        self.video_list_widget = QListWidget()
        self.video_list_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # Load video items
        self.load_video_items()

        # --- Top Left Items List ---
        video_top_left_layout.addWidget(QLabel("Video Files:"))
        video_top_left_layout.addWidget(self.video_list_widget)
        video_list_btns = QHBoxLayout()
        video_btn_add = QPushButton("Add")
        video_btn_delete = QPushButton("Delete")
        video_btn_clear = QPushButton("Clear")
        video_list_btns.addWidget(video_btn_add)
        video_list_btns.addWidget(video_btn_delete)
        video_list_btns.addWidget(video_btn_clear)
        video_top_left_layout.addLayout(video_list_btns)

        # --- Top Right Process Area (Video) ---
        video_top_right_widget = QWidget()
        video_top_right_layout = QVBoxLayout(video_top_right_widget)
        video_top_right_layout.setContentsMargins(0, 0, 0, 0)
        # Overwrite/Delete checkbox row
        video_checkbox_layout = QHBoxLayout()
        video_checkbox_layout.addStretch(1)
        self.video_delete_checkbox = QCheckBox("Delete original files after process")
        video_checkbox_layout.addWidget(self.video_delete_checkbox, alignment=Qt.AlignmentFlag.AlignLeft)
        video_top_right_layout.addLayout(video_checkbox_layout, stretch=1)
        # Process button row
        self.video_process_layout = QHBoxLayout()
        self.video_process_layout.addStretch(1)
        self.video_process_btn = QPushButton("Process")
        self.video_process_layout.addWidget(self.video_process_btn, alignment=Qt.AlignmentFlag.AlignLeft)
        video_top_right_layout.addLayout(self.video_process_layout, stretch=1)
        video_top_right_widget.setMinimumWidth(200)

        # --- Combine Top Layout ---
        video_top_layout.addLayout(video_top_left_layout, stretch=1)
        video_top_layout.addWidget(video_top_right_widget, stretch=2)

        # --- Bottom Layout (operations) ---
        video_bottom_layout = QVBoxLayout()
        video_ops_grid = QGridLayout()
        video_ops_grid.setHorizontalSpacing(15)
        video_ops_grid.setVerticalSpacing(15)
        video_ops_grid.setContentsMargins(0, 0, 0, 0)
        self.video_ops_group = QButtonGroup()
        self.video_ops_group.setExclusive(True)

        # Row 0, Column 0: Reformat
        self.video_reformat_rb = QRadioButton("Reformat")
        self.video_reformat_input = QComboBox()
        self.video_reformat_input.addItems(["mp4", "mkv", "avi", "mov", "webm"])
        self.video_reformat_input.setMaximumWidth(80)
        video_reformat_layout = QHBoxLayout()
        video_reformat_layout.addWidget(self.video_reformat_rb)
        video_reformat_layout.addWidget(self.video_reformat_input)
        video_reformat_layout.addStretch()
        video_reformat_widget = QWidget()
        video_reformat_widget.setLayout(video_reformat_layout)
        video_ops_grid.addWidget(video_reformat_widget, 0, 0)
        self.video_ops_group.addButton(self.video_reformat_rb, 1)
        # Row 0, Column 1: Resize
        self.video_resize_rb = QRadioButton("Resize")
        self.video_resize_width = QSpinBox()
        self.video_resize_width.setRange(1, 10000)
        self.video_resize_width.setMaximumWidth(60)
        self.video_resize_height = QSpinBox()
        self.video_resize_height.setRange(1, 10000)
        self.video_resize_height.setMaximumWidth(60)
        video_resize_layout = QHBoxLayout()
        video_resize_layout.addWidget(self.video_resize_rb)
        video_resize_layout.addWidget(QLabel("W:"))
        video_resize_layout.addWidget(self.video_resize_width)
        video_resize_layout.addWidget(QLabel("H:"))
        video_resize_layout.addWidget(self.video_resize_height)
        video_resize_layout.addStretch()
        video_resize_widget = QWidget()
        video_resize_widget.setLayout(video_resize_layout)
        video_ops_grid.addWidget(video_resize_widget, 0, 1)
        self.video_ops_group.addButton(self.video_resize_rb, 2)
        # Row 1, Column 1: Rotate
        self.video_rotate_rb = QRadioButton("Rotate")
        self.video_rotate_combo = QComboBox()
        self.video_rotate_combo.addItems(["90", "180", "270"])
        self.video_rotate_combo.setMaximumWidth(80)
        video_rotate_layout = QVBoxLayout()
        video_rotate_row_layout = QHBoxLayout()
        video_rotate_row_layout.addWidget(self.video_rotate_rb)
        video_rotate_row_layout.addWidget(self.video_rotate_combo)
        video_rotate_row_layout.addStretch()
        video_rotate_layout.addLayout(video_rotate_row_layout)
        video_rotate_layout.addStretch()
        video_rotate_widget = QWidget()
        video_rotate_widget.setLayout(video_rotate_layout)
        video_ops_grid.addWidget(video_rotate_widget, 1, 0)
        self.video_ops_group.addButton(self.video_rotate_rb, 3)
        # Row 2, Column 0: Flip
        self.video_flip_rb = QRadioButton("Flip")
        self.video_flip_combo = QComboBox()
        self.video_flip_combo.addItems(["Horizontal", "Vertical"])
        self.video_flip_combo.setMaximumWidth(100)
        video_flip_layout = QHBoxLayout()
        video_flip_layout.addWidget(self.video_flip_rb)
        video_flip_layout.addWidget(self.video_flip_combo)
        video_flip_layout.addStretch()
        video_flip_widget = QWidget()
        video_flip_widget.setLayout(video_flip_layout)
        video_ops_grid.addWidget(video_flip_widget, 1, 1)
        self.video_ops_group.addButton(self.video_flip_rb, 4)
        # Row 1, Column 0: Crop
        self.video_crop_rb = QRadioButton("Crop")
        self.video_crop_start_x = QSpinBox()
        self.video_crop_start_x.setRange(0, 10000)
        self.video_crop_start_x.setMaximumWidth(60)
        self.video_crop_start_x.setValue(0)
        self.video_crop_start_y = QSpinBox()
        self.video_crop_start_y.setRange(0, 10000)
        self.video_crop_start_y.setMaximumWidth(60)
        self.video_crop_start_y.setValue(0)
        self.video_crop_width = QSpinBox()
        self.video_crop_width.setRange(1, 10000)
        self.video_crop_width.setMaximumWidth(60)
        self.video_crop_height = QSpinBox()
        self.video_crop_height.setRange(1, 10000)
        self.video_crop_height.setMaximumWidth(60)
        video_crop_layout = QVBoxLayout()
        video_crop_layout.addWidget(self.video_crop_rb)
        video_crop_xy_layout    = QHBoxLayout()
        video_crop_xy_layout.addWidget(QLabel("X:"))
        video_crop_xy_layout.addWidget(self.video_crop_start_x)
        video_crop_xy_layout.addWidget(QLabel("Y:"))
        video_crop_xy_layout.addWidget(self.video_crop_start_y)
        video_crop_xy_layout.addStretch()
        video_crop_layout.addLayout(video_crop_xy_layout)
        video_crop_wh_layout = QHBoxLayout()
        video_crop_wh_layout.addWidget(QLabel("W:"))
        video_crop_wh_layout.addWidget(self.video_crop_width)
        video_crop_wh_layout.addWidget(QLabel("H:"))
        video_crop_wh_layout.addWidget(self.video_crop_height)
        video_crop_wh_layout.addStretch()
        video_crop_layout.addLayout(video_crop_wh_layout)
        video_crop_widget = QWidget()
        video_crop_widget.setLayout(video_crop_layout)
        video_ops_grid.addWidget(video_crop_widget, 2, 0)
        self.video_ops_group.addButton(self.video_crop_rb, 5)
        # Row 1, Column 2: Adjust Brightness/Contrast
        self.video_adjust_rb = QRadioButton("Adjust Brightness/Contrast")
        self.video_alpha_spin = QDoubleSpinBox()
        self.video_alpha_spin.setRange(0.1, 5.0)
        self.video_alpha_spin.setSingleStep(0.1)
        self.video_alpha_spin.setValue(1.0)
        self.video_alpha_spin.setMaximumWidth(60)
        self.video_beta_spin = QSpinBox()
        self.video_beta_spin.setRange(-255, 255)
        self.video_beta_spin.setValue(0)
        self.video_beta_spin.setMaximumWidth(60)
        video_adjust_layout = QVBoxLayout()
        video_adjust_rb_layout = QHBoxLayout()
        video_adjust_rb_layout.addWidget(self.video_adjust_rb)
        video_adjust_rb_layout.addStretch()
        video_adjust_layout.addLayout(video_adjust_rb_layout)
        video_adjust_params_layout = QHBoxLayout()
        video_adjust_params_layout.addWidget(QLabel("Alpha:"))
        video_adjust_params_layout.addWidget(self.video_alpha_spin)
        video_adjust_params_layout.addWidget(QLabel("Beta:"))
        video_adjust_params_layout.addWidget(self.video_beta_spin)
        video_adjust_params_layout.addStretch()
        video_adjust_layout.addLayout(video_adjust_params_layout)
        video_adjust_widget = QWidget()
        video_adjust_widget.setLayout(video_adjust_layout)
        video_ops_grid.addWidget(video_adjust_widget, 2, 1, alignment=Qt.AlignmentFlag.AlignTop)
        self.video_ops_group.addButton(self.video_adjust_rb, 6)

        video_bottom_layout.addLayout(video_ops_grid)

        # --- Assemble ---
        video_layout.addLayout(video_top_layout, stretch=1)
        video_layout.addLayout(video_bottom_layout, stretch=1)
        self.video_tab.setLayout(video_layout)
        tabs.addTab(self.video_tab, "Video")

        # --- Button Connections ---
        video_btn_clear.clicked.connect(self.clear_video_items)
        video_btn_add.clicked.connect(self.add_video_item)
        video_btn_delete.setEnabled(False)
        self.video_list_widget.itemSelectionChanged.connect(
            lambda: video_btn_delete.setEnabled(bool(self.video_list_widget.selectedItems()))
        )
        video_btn_delete.clicked.connect(self.delete_selected_video_item)
        self.video_process_btn.clicked.connect(self.process_video_items)

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
        self.image_process_btn.clicked.connect(self.process_image_items)


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
            
    # def select_output_path(self):
    #     folder = QFileDialog.getExistingDirectory(self, "Select Output Folder", "")
    #     if folder:
    #         self.output_path_btn.setText(folder)

    def process_image_items(self):
        if not hasattr(self, 'image_processing_label'):
            self.image_processing_label = QLabel("Processing...")
            self.image_process_layout.insertWidget(0, self.image_processing_label)
        self.image_processing_label.show()
        self.image_process_btn.setEnabled(False)
        process_failed = []
        
        QApplication.processEvents()
        selected_id = self.image_ops_group.checkedId()
        overwrite_flag = 1 if self.image_delete_checkbox.isChecked() else 0
        if not self.image_items:
            print("⚠ No input files to process!")
            self.image_processing_label.hide()
            self.image_process_btn.setEnabled(True)
            return

        for img_path in self.image_items:
            if selected_id == 1:
                output_ext = self.image_reformat_input.currentText().strip()
                ret = image_lib.reformat_image(c_char_p(img_path.encode("utf-8")), c_char_p(output_ext.encode("utf-8")), overwrite_flag)
            elif selected_id == 2:
                width = self.image_resize_width.value()
                height = self.image_resize_height.value()
                ret = image_lib.resize_image(c_char_p(img_path.encode("utf-8")), width, height, overwrite_flag)
            elif selected_id == 3:
                angle = int(self.image_rotate_combo.currentText())
                ret = image_lib.rotate_image(c_char_p(img_path.encode("utf-8")), angle, overwrite_flag)
            elif selected_id == 4:
                direction = 0 if self.image_flip_combo.currentText() == "Vertical" else 1
                ret = image_lib.flip_image(c_char_p(img_path.encode("utf-8")), direction, overwrite_flag)
            elif selected_id == 5:
                start_x = self.image_crop_start_x.value()
                start_y = self.image_crop_start_y.value()
                width = self.image_crop_width.value()
                height = self.image_crop_height.value()
                ret = image_lib.crop_image(c_char_p(img_path.encode("utf-8")), start_x, start_y, width, height, overwrite_flag)
            elif selected_id == 6:
                alpha = c_double(self.image_alpha_spin.value())
                beta = c_int(self.image_beta_spin.value())
                ret = image_lib.adjust_brightness_image(c_char_p(img_path.encode("utf-8")), alpha, beta, overwrite_flag)
            else:
                ret = 0

            if ret:
                process_failed.append(f"⚠ Processing failed for {img_path}")
            QApplication.processEvents()

        self.image_processing_label.hide()
        self.image_process_btn.setEnabled(True)
        for i in process_failed:
            print(i)

    # ----------------------------
    # Video Tab Helper Functions
    # ----------------------------
    def load_video_items(self):
        self.video_list_widget.clear()
        for item in self.video_items:
            QListWidgetItem(item, self.video_list_widget)

    def delete_selected_video_item(self):
        selected_items = self.video_list_widget.selectedItems()
        for item in selected_items:
            if item.text() in self.video_items:
                self.video_items.remove(item.text())
            self.video_list_widget.takeItem(self.video_list_widget.row(item))

    def clear_video_items(self):
        self.video_items.clear()
        self.video_list_widget.clear()

    def add_video_item(self):
        file_paths, _ = QFileDialog.getOpenFileNames(
            self,
            "Select Video Files",
            "",
            "Videos (*.mp4 *.avi *.mov *.mkv *.webm);;All Files (*)"
        )
        for file_path in file_paths:
            if file_path and file_path not in self.video_items:
                self.video_items.append(file_path)
                QListWidgetItem(file_path, self.video_list_widget)

    def process_video_items(self):
        if not hasattr(self, 'video_processing_label'):
            self.video_processing_label = QLabel("Processing...")
            self.video_process_layout.insertWidget(0, self.video_processing_label)
        self.video_processing_label.show()
        self.video_process_btn.setEnabled(False)
        process_failed = []

        QApplication.processEvents()
        selected_id = self.video_ops_group.checkedId()
        overwrite_flag = 1 if self.video_delete_checkbox.isChecked() else 0
        if not self.video_items:
            print("⚠ No input files to process!")
            self.video_processing_label.hide()
            self.video_process_btn.setEnabled(True)
            return

        for vid_path in self.video_items:
            if selected_id == 1:
                output_ext = self.video_reformat_input.currentText().strip()
                ret = video_lib.reformat_video(c_char_p(vid_path.encode("utf-8")), c_char_p(output_ext.encode("utf-8")), c_char_p(ffmpeg_path.encode("utf-8")), overwrite_flag)
            elif selected_id == 2:
                width = self.video_resize_width.value()
                height = self.video_resize_height.value()
                ret = video_lib.resize_video(c_char_p(vid_path.encode("utf-8")), width, height, c_char_p(ffmpeg_path.encode("utf-8")), overwrite_flag)
            elif selected_id == 3:
                angle = int(self.video_rotate_combo.currentText())
                ret = video_lib.rotate_video(c_char_p(vid_path.encode("utf-8")), angle, c_char_p(ffmpeg_path.encode("utf-8")), overwrite_flag)
            elif selected_id == 4:
                direction = 0 if self.video_flip_combo.currentText() == "Vertical" else 1
                ret = video_lib.flip_video(c_char_p(vid_path.encode("utf-8")), direction, c_char_p(ffmpeg_path.encode("utf-8")), overwrite_flag)
            elif selected_id == 5:
                start_x = self.video_crop_start_x.value()
                start_y = self.video_crop_start_y.value()
                width = self.video_crop_width.value()
                height = self.video_crop_height.value()
                ret = video_lib.crop_video(c_char_p(vid_path.encode("utf-8")), start_x, start_y, c_int(width), c_int(height), c_char_p(ffmpeg_path.encode("utf-8")), overwrite_flag)
            elif selected_id == 6:
                alpha = c_double(self.video_alpha_spin.value())
                beta = c_int(self.video_beta_spin.value())
                ret = video_lib.adjust_brightness_video(c_char_p(vid_path.encode("utf-8")), alpha, beta, c_char_p(ffmpeg_path.encode("utf-8")), overwrite_flag)
            else:
                ret = 0

            if ret:
                process_failed.append(f"⚠ Processing failed for {vid_path}")
            QApplication.processEvents()

        self.video_processing_label.hide()
        self.video_process_btn.setEnabled(True)
        for i in process_failed:
            print(i)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())