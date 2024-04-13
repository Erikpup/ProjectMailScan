#include <iostream>
#include <regex>
#include <string>
#include <sstream>

using namespace std;


bool findPattern(const string& text, const string& pattern); // Функция поиска паттерна
bool leakDetection(string checkText, string inputLeak); // Функция обнаружения угрозы утечки информации

bool leakDetection(string checkText, string input) {

    // Вектор для хранения разделенных значений
    vector<string> patterns;

    // Создание строкового потока
    stringstream str_s(input);

    // Разделение строки по запятой и добавление в вектор
    string pattern;
    while (getline(str_s, pattern, ',')) {
        patterns.push_back(pattern);
    }

    // Перебор вектора для поиска паттерна
    for (const auto& pattern : patterns) {
        if (findPattern(checkText, pattern)) {
            return true;
        }
    }

    return false;
}


bool findPattern(const string& text, const string& pattern) {
    regex regex_pattern(pattern);
    return regex_search(text, regex_pattern);
}