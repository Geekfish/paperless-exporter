import datetime
from pathlib import Path
from shutil import copy2 as copy

import mac_tag
import applescript
from peewee import *

DB = SqliteDatabase('DocumentWallet.documentwalletsql')
OUT_PATH = "doc_output"

class BaseModel(Model):
    class Meta:
        database = DB

class Category(BaseModel):
    pk = IntegerField(primary_key=True, column_name='Z_PK')
    name = CharField(column_name='ZNAME')

    class Meta:
        table_name = 'ZCATEGORY'

class SubCategory(BaseModel):
    pk = IntegerField(primary_key=True, column_name='Z_PK')
    name = CharField(column_name='ZNAME')

    class Meta:
        table_name = 'ZSUBCATEGORY'

class Receipt(BaseModel):
    pk = IntegerField(primary_key=True, column_name='Z_PK')
    merchant = CharField(column_name='ZMERCHANT')
    notes = TextField(column_name='ZNOTES')
    path = CharField(column_name='ZPATH')
    category = ForeignKeyField(Category, column_name="ZCATEGORY")
    subcategory = ForeignKeyField(SubCategory, column_name="ZSUBCATEGORY")

    class Meta:
        table_name = 'ZRECEIPT'

class Tag(BaseModel):
    pk = IntegerField(primary_key=True, column_name='Z_PK')
    name = CharField(column_name='ZNAME')

    class Meta:
        table_name = 'ZTAG'

class ReceiptTag(BaseModel):
    receipt = ForeignKeyField(Receipt, column_name="Z_14RECEIPTS1", backref="receipt_tags")
    tag = ForeignKeyField(Tag, column_name="Z_18TAGS", backref="receipt_tags")

    class Meta:
        table_name = 'Z_14TAGS'
        primary_key = False

def file_name(index, receipt):
    if receipt.merchant.strip():
        return f"{index}-{receipt.merchant.strip()}.pdf"
    try:
        return f"{index}-{receipt.category.name}.pdf"
    except Category.DoesNotExist:
        return f"{index}-no-name.pdf"


def create_out_dir(dir_path):
    Path(dir_path).mkdir(parents=True, exist_ok=True)

def collect_tags(receipt):
    tags = []
    try:
        tags.append(receipt.category.name.lower())
    except Category.DoesNotExist:
        pass
    try:
        tags.append(receipt.subcategory.name.lower())
    except SubCategory.DoesNotExist:
        pass

    for rtag in receipt.receipt_tags:
        tags.append(rtag.tag.name.strip().lower())

    return set(tags)

def set_comment(file_path, comment_text):
    applescript.tell.app("Finder", f'set comment of (POSIX file "{file_path}" as alias) to "{comment_text}" as Unicode text')


def run():
    create_out_dir(OUT_PATH)
    query = Receipt.select(Receipt)

    for index, receipt in enumerate(query):
        _file_name = file_name(index, receipt)
        print(f"#{index} " + _file_name)

        new_path = "/".join([OUT_PATH, _file_name])
        copy(receipt.path, new_path)

        if receipt.notes:
            notes = receipt.notes.strip()
            set_comment(new_path, notes)
            print(f"\tNotes:\n\t{notes}")

        tags = collect_tags(receipt)

        mac_tag.update(tags,[new_path])

        print("\tTags added:")
        for tag in tags:
            print(f"\t - {tag}")


if __name__ == "__main__":
    run()