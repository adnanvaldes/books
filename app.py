import loadscreen
import argparse
from library import Library
from typing import Dict
from repository import SQLRepository
from datetime import date
from tabulate import tabulate
repository = SQLRepository()
library = Library(repository)  
def add(data:Dict):
    data.pop('action', None)
    print("added book entry as :",library.add(data))
    #add -a camus -t Stranger -f book -p 123
    return

def edit(data:Dict):
    data.pop('action',None)
    data.pop('edit_action', None)
    identifiers={}
    updates={}
    for k,v in data.items():
        if k is not 'pairs':
            identifiers[k]=v
        else:
            if len(v) % 2 != 0:
                print(f"Incomplete command, please enter values for each field you want to update")
            else:
                updates=dict(zip(v[::2],v[1::2]))
    identifiers={key:value for key,value in identifiers.items() if value is not None }
    print(f"updated entry to {library.update(updates,**identifiers)}")
    return
    
        
def delete(data:dict):
    data.pop('action',None)
    data={key:value for key,value in data.items() if value is not None}
    library.delete(**data)
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
	edit_parser =subparsers.add_parser('edit', help='to edit existing book entries')
 
	edit_parser.add_argument('-a', '--author', type=str, help='name of author')
	edit_parser.add_argument('-t','--title',type=str,help='name of book')
	edit_parser.add_argument('-f','--format',type=str,help="eg: (pysical,e-book,audiobook)")
	edit_parser.add_argument('-i','--isbn',type=str,help='Code to help define genre')
	edit_parser.add_argument('-p','--pages',type=int,help="number of pages")
	edit_parser.add_argument('-r','--runtime',type=int,help="total runtime in case of audiobooks")
	edit_parser.add_argument('-sd','--start_date',type =date,help="date when the user started the book")
	edit_parser.add_argument('-fd','--finish_date',type=date,help="date the user finished the book ")
 
	edit_subparsers = edit_parser.add_subparsers(dest='edit_action', help='Edit actions')
	set_parser = edit_subparsers.add_parser('set', help='Set book properties')
	set_parser.add_argument('pairs',nargs='+',help='field value pairs (e.g., pages 123 author "John Doe")')#this lets me add multiple key value pairs after -set the '+' means one or more than one args x
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