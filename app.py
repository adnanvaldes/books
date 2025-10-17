import loadscreen
import argparse
from library import Library
from typing import Dict
from repository import SQLRepository
from datetime import date
repository = SQLRepository()
library = Library(repository)  
def add(data:Dict):
    data.pop('action', None)
    print("added book entry as :",library.add(data))
    #add -a camus -t Stranger -f book -p 123
    
    return
def edit():
	print("edit function will be here ")
	return
def delete():
	print("delete function will be here ")
	return
def finish():
	print("finish function will be here ")
	return
def import_():
	print("import function will be here ")
	return
def export_():
	print("Export function will be here ")
	return
def list_():
	print("list function will be here ")
def recap():
	print("recap function will be here")

    
    

def main():
	loadscreen.welcome()
	print("Welcome to Books ")
	print("For help enter : books -h")
	
	parser=argparse.ArgumentParser(prog="book",description="Book manager")

	subparsers=parser.add_subparsers(dest="action",required=True)
	clear_parser = subparsers.add_parser('clear', help='CLS')
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
	delete_parser.add_argument('title', type=str, help='Book title')
    
    # EDIT subcommand
	edit_parser = subparsers.add_parser('edit', help='Edit a book')
	
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
			"""
   				this is how args looks like for eg 
				args = Namespace(
				action='list',
				author='John Doe',
				genre=None,
				format=None,
				sort='title',
				page_count=False,
				date=False,
				start_date=False)
       		"""
			args = parser.parse_args(user_input.split()) 
			command={
				"add":add,
				"list":list_,
				"edit":edit,
				"finish":finish,
				"delete":delete,
				"import":import_,
				"export":export_,
				"recap":recap,
				"clear":loadscreen.welcome
			}
			func = command.get(args.action)
			if func:
				func(vars(args))
			
		except SystemExit:
			continue
		except KeyboardInterrupt:
			print("\nThanks for using books")
			break





if __name__ == "__main__":
	main()