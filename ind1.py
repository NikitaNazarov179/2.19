#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

import json
import argparse
import os.path
import os
import sys

def get_product(products, product, shop, cost):
    """""
    Запросить данные о товаре.
    """""
    products.append(
        {
            'product': product,
            'shop': shop,
            'cost': cost,
        }
    )
    return products

def display_products(products):
    """""
    Отобразить список товаров
    """""
    # Проверить что список товаров не пуст
    if products:
        # Заголовок таблицы
        line = '+-{}-+-{}-+-{}-+-{}-+'.format(
            '-' * 4,
            '-' * 30,
            '-' * 20,
            '-' * 15
        )
        print(line)
        print(
            '| {:^4} | {:^30} | {:^20} | {:^15} |'.format(
                "№",
                "Товар",
                "Магазин",
                "Стоимость товара"
            )
        )
        print(line)

        #Вывести данные о всех товарах
        for idx, products in enumerate(products, 1):
            print(
                '| {:^4} | {:<30} | {:<20} | {:<15} |'.format(
                    idx,
                    products.get('product', ''),
                    products.get('shop', ''),
                    products.get('cost', ''),
                    ' ' * 5
                )
            )

        print(line)

    else:
        print("Список товаров пуст.")


def select_products(products, addedtovar):
    """""
    Выбрать необходимый товар
    """""
    # Сформировать список товаров
    result = []
    for asd in products:
        if asd.get('product') == addedtovar:
            result.append(asd)
        else:
            print("Выбран неправильный товар")

    # Вернуть список товаров
    return result

def help():
    print("Список команд:\n")
    print("add - добавить студента;")
    print("display - вывести список продуктов;")
    print("select - запросить продукты")
    print("save - сохранить список продуктов;")
    print("load - загрузить список продуктов;")
    print("exit - завершить работу с программой.")

def save_products(file_name, products):
    """
    Сохранить все товары в файл JSON
    """
    # Открыть файл с заданным именем для записи
    with open(file_name, "w", encoding="utf-8") as fout:
        # Выполнить сериализацию данных в формат JSON
        json.dump(products, fout, ensure_ascii=False, indent=4)
    directory = pathlib.Path.cwd().joinpath(file_name)
    directory.replace(pathlib.Path.home().joinpath(file_name))

def load_products(file_name):
    """
    Загрузить всех работников из файла JSON
    """
    # Открыть файл с заданным именем для чтения
    with open(file_name, "r", encoding="utf-8") as fin:
        return json.load(fin)


def main(command_line=None):
    # Создать родительский парсер для определения имени файла.
    file_parser = argparse.ArgumentParser(add_help=False)
    file_parser.add_argument(
        "filename",
        action="store",
        help="The data file name"
    )

    # Создать основной парсер командной строки.
    parser = argparse.ArgumentParser("products")
    parser.add_argument(
        "--version",
        action="version",
        help="The main parser",
        version="%(prog)s 0.1.0"
    )

    subparsers = parser.add_subparsers(dest="command")

    # Создать субпарсер для добавления товара.
    add = subparsers.add_parser(
        "add",
        parents=[file_parser],
        help="Add a new product"
    )
    add.add_argument(
        "-n",
        "--product",
        action="store",
        required=True,
        help="The product's name"
    )
    add.add_argument(
        "-g",
        "--cost",
        type=int,
        action="store",
        help="The product's cost"
    )
    add.add_argument(
        "-gr",
        "--shop",
        action="store",
        required=True,
        help="The product's shop"
    )

    # Создать субпарсер для отображения всех продуктов.
    _ = subparsers.add_parser(
        "display",
        parents=[file_parser],
        help="Display all products"
    )

    # Создать субпарсер для выбора продуктов.
    select = subparsers.add_parser(
        "select",
        parents=[file_parser],
        help="Select the products"
    )
    select.add_argument(
        "-s",
        "--select",
        action="store",
        required=True,
        help="The required select"
    )

    # Выполнить разбор аргументов командной строки.
    args = parser.parse_args(command_line)

    # Загрузить всех продуктов из файла, если файл существует.
    is_dirty = False
    if os.path.exists(args.filename):
        products = load_products(args.filename)
    else:
        products = []

    # Добавить продукт.
    if args.command == "add":
        products = get_product(
            products,
            args.product,
            args.shop,
            args.cost
        )
        is_dirty = True

    # Отобразить все продукты.
    elif args.command == "display":
        display_products(products)

    # Выбрать требуемые продукты.
    elif args.command == "select":
        selected = select_products(products, addedtovar)
        display_products(selected)

    # Сохранить данные в файл, если список продуктов был изменен.
    if is_dirty:
        save_products(args.filename, products)


if __name__ == '__main__':
    main()