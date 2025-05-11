import numpy as np
import pandas as pd
from PyQt5.QtWidgets import QFileDialog



class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view

        self.view.load_btn.clicked.connect(self.load_csv)
        self.view.clear_btn.clicked.connect(self.clear_data)
        self.view.calc_btn.clicked.connect(self.calculate_correlations)
        self.view.table.cellChanged.connect(self.table_data_changed)
        self.view.save_btn.clicked.connect(self.save_result)

    def load_csv(self):
        """Открывает диалог выбора файла для загрузки CSV и загружает данные в модель"""
        from pathlib import Path

        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self.view, "Загрузить файл", "", "CSV Files (*.csv)", options=options)

        if file_name:
            try:
                # Проверим, существует ли файл вообще
                if not Path(file_name).is_file():
                    raise FileNotFoundError("Файл не найден.")

                # Загружаем как строки
                raw_data = np.genfromtxt(file_name, delimiter=',', encoding='utf-8', skip_header=1, dtype=str)

                # Если одна строка данных
                if raw_data.ndim == 1:
                    raw_data = np.expand_dims(raw_data, axis=0)

                if raw_data.shape[1] != 2:
                    raise ValueError("Неверный формат данных. Ожидается 2 столбца.")

                # Очищаем пробелы и кавычки
                clean_data = np.char.strip(raw_data)
                clean_data = np.char.replace(clean_data, '"', '')
                clean_data = np.char.replace(clean_data, "'", '')
                clean_data = np.char.replace(clean_data, '«', '')
                clean_data = np.char.replace(clean_data, '»', '')

                # Убираем пустые строки
                mask = np.all(clean_data != '', axis=1)
                clean_data = clean_data[mask]

                if clean_data.size == 0:
                    raise ValueError("Файл не содержит допустимых данных.")

                # Преобразуем в float
                x_data = clean_data[:, 0].astype(float)
                y_data = clean_data[:, 1].astype(float)

                # Установка данных в модель
                self.model.set_data(x_data, y_data)
                self.update_view()

            except Exception as e:
                self.view.show_error(f"Ошибка загрузки файла! {str(e)}")
   
    def clear_data(self):
            self.model.set_data([], [])
            self.update_view()

    def table_data_changed(self, row, column):
            try: 
                x_data = []
                y_data = []    

                for i in range(self.view.table.rowCount()):
                     x_item = self.view.table.item(i, 0)
                     y_item = self.view.table.item(i, 1)

                     if x_item and y_item and x_item.text() and y_item.text():
                         x_data.append(float(x_item.text()))
                         y_data.append(float(y_item.text()))
 
                self.model.set_data(x_data, y_data)
                self.view.update_plot(*self.model.get_data()) 
                       
            except ValueError:
                self.view.show_error_message(f"Некоректные данные в таблице!")

    def save_result(self):
         options = QFileDialog.Options()
         file_name, _ = QFileDialog.getSaveFileName(
              self.view,
              "Сохранить результаты",
              "",
              "Excel Files (*.xlsx)",
              options=options
         )

         if not file_name:
              return
         
         try:
              writer = pd.ExcelWriter(file_name, engine='xlsxwriter')

              data_df = pd.DataFrame({
                   'X': self.model.x_data,
                   'Y': self.model.y_data
              })
              data_df.to_excel(writer, sheet_name="Данные", index=False)

              correlation = self.model.calculate_correlations()
              results = pd.DataFrame({
                   "Метод": ["Пирсон", "Спирмен", "Кендалл"],
                   "Корреляция" : [
                        correlation['pearson'][0],
                        correlation['spearman'][0],
                        correlation['kendall'][0]
                   ],
                   'p-value': [
                        correlation['pearson'][1],
                        correlation['spearman'][1],
                        correlation["kendall"][1]
                   ]
              })
              results.to_excel(writer, sheet_name="Результаты", index=False)

              workbook = writer.book
              worksheet = workbook.add_worksheet('График')

              buf = self.view.get_figure_image()
            #   self.figure.savefig(buf, format='png', dpi=300)
            #   buf.seek(0)

              worksheet.insert_image("B2", 'plot.png', {'image_data': buf})


              for sheet in writer.sheets:
                   writer.sheets[sheet].set_column('A:C', 15)

              writer.close()
              self.view.show_message("Файл успешно сохранен!")

         except Exception as e:
              self.view.show_error(f"Ошибка при сохранении файла: {str(e)}")
              
    def calculate_correlations(self):
         """Расчет корреляций"""
         try:
             results = self.model.calculate_correlations()
             x_range, y_range = self.model.calculate_regression_line()
             self.view.update_plot(*self.model.get_data(), (x_range, y_range))
             self.view.update_results(results)
         except ValueError as e:
            self.view.show_error(str(e))

    def update_view(self):
         x_data, y_data = self.model.get_data()
         self.view.update_table(x_data, y_data)
         self.view.update_plot(x_data, y_data)        
