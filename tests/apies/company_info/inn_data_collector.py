import unittest
from src.apies.company_info.inn_data_collector import InnDataCollector


class InnDataCollectorTest(unittest.TestCase):
    '''Тесты для класса InnDataCollector'''

    def setUp(self):
        """Создание экземляра класса"""
        self.inn_collector = InnDataCollector()

    def test_collect_inn_data(self):
        """Проверка на совпадение ИНН"""

        dict_values = {'Тинькофф': '7710140679',
                       'HeadHunter': '7718620740',
                       'Сбербанк': '7707083893'}

        for key, value in dict_values.items():
            self.assertEqual(value, self.inn_collector.collect_inn(key))


if __name__ == '__main__':
    unittest.main()
