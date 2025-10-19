import loadscreen
import argparse
from library import Library
from typing import Dict
from repository import SQLRepository
from datetime import date
from tabulate import tabulate
import shlex

repository = SQLRepository()
library = Library(repository)  
def add(data:Dict):
    data.pop('action', None)
    print("added book entry as :",library.add(data))
    return

def edit(data: Dict):
    data.pop('action', None)
    data.pop('edit_action', None)
    
    identifiers = {}
    updates = {}
    
    for k, v in data.items():
        if v is not None: 
            if k.startswith('set_'):
                field_name = k.replace('set_', '')
                updates[field_name] = v
            else:
                identifiers[k] = v
    if not updates:
        print("Error: Please specify at least one field to update using --set-* flags")
        return
    
    print(f"Updated entry to {library.update(updates, **identifiers)}")
    return
    
        
def delete(data:dict):
    data.pop('action',None)
    data={key:value for key,value in data.items() if value is not None}
    library.delete(**data)
    return
def finish():
	return
def import_():
	print("import function will be here ")
	return
def export_():
	print("Export function will be here ")
	return
def list_(data:Dict):
    data.pop('action', None)
    clean_data= {key:value for key,value in data.items() if value is not None}
    Books=library.list_(**clean_data)
    print(tabulate(Books))
    
def recap():
	print("recap function will be here")

def main():
	loadscreen.welcome()
	print("Welcome to Books ")
	print("For help enter : books -h")
	
	parser=argparse.ArgumentParser(prog="book",description="Book manager")

	subparsers=parser.add_subparsers(dest="action",required=True)
	clear_parser = subparsers.add_parser('clear', help='CLS')
	#EDIT SUBCOMMAND
	# EDIT SUBCOMMAND
	edit_parser = subparsers.add_parser('edit', help='to edit existing book entries')

	# Filter/search arguments (to identify which book to edit)
	edit_parser.add_argument('-a', '--author', type=str, help='name of author to search for')
	edit_parser.add_argument('-t', '--title', type=str, help='name of book to search for')
	edit_parser.add_argument('-f', '--format', type=str, help="format to search for (e.g., physical, e-book, audiobook)")
	edit_parser.add_argument('-i', '--isbn', type=str, help='ISBN to search for')
	edit_parser.add_argument('-p', '--pages', type=int, help="number of pages to search for")
	edit_parser.add_argument('-r', '--runtime', type=int, help="runtime to search for (audiobooks)")
	edit_parser.add_argument('-sd', '--start_date', type=date, help="start date to search for")
	edit_parser.add_argument('-fd', '--finish_date', type=date, help="finish date to search for")

	# Set arguments (new values to update)
	edit_parser.add_argument('--set-author', type=str, help='new author name')
	edit_parser.add_argument('--set-title', type=str, help='new book title')
	edit_parser.add_argument('--set-format', type=str, help="new format (e.g., physical, e-book, audiobook)")
	edit_parser.add_argument('--set-isbn', type=str, help='new ISBN')
	edit_parser.add_argument('--set-pages', type=int, help="new number of pages")
	edit_parser.add_argument('--set-runtime', type=int, help="new runtime (audiobooks)")
	edit_parser.add_argument('--set-start-date', type=date, help="new start date")
	edit_parser.add_argument('--set-finish-date', type=date, help="new finish date")

 	# LIST subcommand
	list_parser = subparsers.add_parser('list', help='List books')

	list_parser.add_argument('-a', '--author', type=str, help='name of author')
	list_parser.add_argument('-t','--title',type=str,help='name of book')
	list_parser.add_argument('-f','--format',type=str,help="eg: (pysical,e-book,audiobook)")
	list_parser.add_argument('-i','--isbn',type=str,help='Code to help define genre')
	list_parser.add_argument('-p','--pages',type=int,help="number of pages")
	list_parser.add_argument('-r','--runtime',type=int,help="total runtime in case of audiobooks")
	list_parser.add_argument('-sd','--start_date',type =date,help="date when the user started the book")
	list_parser.add_argument('-fd','--finish_date',type=date,help="date the user finished the book ")
 
    # ADD subcommand
	add_parser = subparsers.add_parser('add', help='Add a book')
	add_parser.add_argument('-a', '--author', type=str, help='name of author')
	add_parser.add_argument('-t','--title',type=str,help='name of book')
	add_parser.add_argument('-f','--format',type=str,help="eg: (pysical,e-book,audiobook)")
	add_parser.add_argument('-i','--isbn',type=str,help='Code to help define genre')
	add_parser.add_argument('-p','--pages',type=int,help="number of pages")
	add_parser.add_argument('-r','--runtime',type=int,help="total runtime in case of audiobooks")
	add_parser.add_argument('-sd','--start_date',type =date,help="date when the user started the book")
	add_parser.add_argument('-fd','--finish_date',type=date,help="date the user finished the book ")
	
    
    # DELETE subcommand
	delete_parser = subparsers.add_parser('delete', help='Delete a book')
	delete_parser.add_argument('-a', '--author', type=str, help='name of author')
	delete_parser.add_argument('-t','--title',type=str,help='name of book')
	delete_parser.add_argument('-f','--format',type=str,help="eg: (pysical,e-book,audiobook)")
	delete_parser.add_argument('-i','--isbn',type=str,help='Code to help define genre')
	delete_parser.add_argument('-p','--pages',type=int,help="number of pages")
	delete_parser.add_argument('-r','--runtime',type=int,help="total runtime in case of audiobooks")
	delete_parser.add_argument('-sd','--start_date',type =date,help="date when the user started the book")
	delete_parser.add_argument('-fd','--finish_date',type=date,help="date the user finished the book ")
	
    # FINISH subcommand
	finish_parser = subparsers.add_parser('finish', help='Mark book as finished')
	while True:
		try:
			user_input=input("> ").strip()
			if user_input in ['exit','quit']:
				print("\nThanks for using books")
				break
			if not user_input:
				continue
			args = parser.parse_args(shlex.split(user_input)) 
			command={
				"add":add,
				"list":list_,
				"edit":edit,
				"finish":finish,
				"delete":delete,
				"import":import_,
				"export":export_,
				"recap":recap,
				"clear":loadscreen.welcome()
			}
			func = command.get(args.action)
			# print(vars(args))
			if func:
				func(vars(args))
			
		except SystemExit:
			continue
		except KeyboardInterrupt:
			print("\nThanks for using books")
			break





if __name__ == "__main__":
	main()