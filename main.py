import pysideoriginal as o

if __name__ == '__main__':
  app = o.Qw.QApplication(o.sys.argv)
  main_window = o.MainWindow()
  main_window.show()
  o.sys.exit(app.exec())